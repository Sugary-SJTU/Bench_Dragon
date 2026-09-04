"""曲线工具：阿基米德螺线几何量与位置/速度求解。

模块职责
--------
集中存放“板凳龙”沿阿基米德螺线运动所需的曲线工具函数：

* 螺线几何量（半径、坐标、切向、弧长、把手递推等）；
* 单时刻 / 多时刻的位置与速度求解；
* 问题 3 的最小螺距二分搜索与转弯状态判断。

可变状态说明
------------
螺线参数 ``p = PITCH / (2π)`` 是本模块的**唯一可变全局状态**：
问题 3 通过 ``global p`` 反复改写它。为保证改写对所有读取方立即生效，
``p`` 与所有读写它的函数保持在同一个模块中；其余只读参数见
``params.py``。
"""

import numpy as np
from scipy.optimize import brentq

from ..config.params import (
    PITCH,
    HEAD_SPEED,
    N_HANDLES,
    BODY_HANDLE_DISTANCE,
    HEAD_HANDLE_DISTANCE,
    THETA0,
    TURNING_RADIUS,
)

# 阿基米德螺线参数 p（可变状态，问题 3 会通过 global p 改写）
p = PITCH / (2 * np.pi)


# ---------------------------------------------------------------------------
# 1. 螺线几何量
# ---------------------------------------------------------------------------

# 螺线半径
def radius(theta) -> float:
    """功能：计算螺线半径；输入：极角 theta；返回：半径。"""
    return p * theta


# 由theta返回坐标
def position(theta):
    """功能：计算螺线坐标；输入：极角 theta；返回：二维坐标数组。"""
    r = radius(theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return np.array([x, y])


# 由theta求速度
def dr_dtheta(theta):
    """功能：计算位置对极角的导数；输入：极角 theta；返回：导数向量。"""
    dx = p * (np.cos(theta) - theta * np.sin(theta))
    dy = p * (np.sin(theta) + theta * np.cos(theta))
    return np.array([dx, dy])


# 弧长公式
def ds_dtheta(theta):
    """功能：计算弧长对极角的导数；输入：极角 theta；返回：弧长导数。"""
    r = radius(theta)
    return np.sqrt(r * r + p * p)


# 弧长积分
def arc_length(theta1, theta2):
    """功能：计算两极角间弧长；输入：theta1、theta2；返回：非负弧长。"""
    def S(theta):
        return (p / 2 * (theta * np.sqrt(theta**2 + 1) + np.arcsinh(theta)))

    return abs(S(theta2) - S(theta1))


# 龙头 theta0(t)函数
def head_theta(t) -> float:
    """功能：求龙头在时刻 t 的极角；输入：时间 t；返回：极角。"""
    target_length = HEAD_SPEED * t

    def equation(theta):
        return arc_length(theta, THETA0) - target_length  # 注意theta0 > theta , theta 随时间减小

    lower = THETA0 - 2 * np.pi

    while equation(lower) < 0:
        lower -= 2 * np.pi

    return brentq(
        equation,
        lower,
        THETA0,
        xtol=1e-12,
        rtol=1e-12  # type: ignore
    )


# 计算相邻螺线点之间距离
def point_distance(theta1, theta2):
    """功能：计算两螺线点的直线距离；输入：两个极角；返回：距离。"""
    p1 = position(theta1)
    p2 = position(theta2)
    return np.linalg.norm(p2 - p1)


# 通过迭代求下一个把手 theta
def next_theta(theta_current, distance) -> float:
    """功能：按给定间距求下一个把手角度；输入：当前角度与间距；返回：下一角度。"""

    def equation(theta):
        return point_distance(theta_current, theta) - distance

    # 从非常接近 theta_current 的位置开始搜索，
    # 找到第一个物理上合理的根。
    left = theta_current + 1e-10

    step = 0.05

    right = left + step

    f_right = equation(right)
    f_left = equation(left)

    # 不断扩大搜索范围
    while f_left * f_right > 0:
        right += step
        f_right = equation(right)
        step *= 1.2

        # 防止出现异常死循环
        # if right - theta_current  > 32 * np.pi:
        #     raise RuntimeError(
        #         "无法找到下一个把手，请检查螺线方向或初始 theta。"
        #     )

    theta_next = brentq(
        equation,
        left,
        right,
        xtol=np.float64(1e-12),
        rtol=np.float64(1e-12),
        maxiter=1000,
    )

    return theta_next  # type: ignore


# ---------------------------------------------------------------------------
# 2. 位置与速度求解
# ---------------------------------------------------------------------------

# 计算一个时刻的所有把手位置
def solve_positions(t):
    """功能：求指定时刻全部把手位置；输入：时间 t；返回：theta、x、y 数组。"""
    theta = np.zeros(N_HANDLES)

    # 龙头前把手
    theta[0] = head_theta(t)

    # 龙头后把手
    theta[1] = next_theta(theta[0], HEAD_HANDLE_DISTANCE)

    # 后续龙身
    for i in range(2, N_HANDLES):
        theta[i] = next_theta(theta[i - 1], BODY_HANDLE_DISTANCE)

    # 转换成 x,y
    xy = np.array([position(th) for th in theta])
    x = xy[:, 0]
    y = xy[:, 1]

    return theta, x, y


# 速度计算
def solve_velocity(theta):
    """功能：按刚性约束求全部把手速度；输入：把手角度数组；返回：速度数组。"""
    N = len(theta)

    # 计算所有把手的位置
    pos = np.array([position(th) for th in theta])

    # 计算 dr/dtheta
    tangent = np.array([dr_dtheta(th) for th in theta])

    # 计算 theta_dot
    theta_dot = np.zeros(N)

    # 龙头前把手速度 = 1 m/s
    tangent_norm = np.linalg.norm(tangent[0])

    theta_dot[0] = -HEAD_SPEED / tangent_norm

    # 逐节递推
    for i in range(N - 1):
        delta = pos[i + 1] - pos[i]
        numerator = np.dot(delta, tangent[i])
        denominator = np.dot(delta, tangent[i + 1])
        theta_dot[i + 1] = numerator / denominator * theta_dot[i]

    # 转换成速度大小
    speed = np.linalg.norm(tangent, axis=1) * np.abs(theta_dot)

    return speed


# 单时刻求解api
def solve_one_time(t):
    """功能：汇总单时刻位置与速度；输入：时间 t；返回：包含 theta、x、y、speed 的字典。"""
    theta, x, y = solve_positions(t)
    speed = solve_velocity(theta)
    return {
        "theta": theta,
        "x": x,
        "y": y,
        "speed": speed
    }


# 由龙头 theta 直接求整支队伍（问题 2/3 复用）
def solve_positions_from_theta(theta_head):
    """功能：由龙头角度求全队位置；输入：龙头角度；返回：theta、x、y 数组。"""
    theta = np.zeros(N_HANDLES)

    # 龙头前把手
    theta[0] = theta_head

    # 龙头后把手
    theta[1] = next_theta(theta[0], HEAD_HANDLE_DISTANCE)

    # 龙身
    for i in range(2, N_HANDLES):
        theta[i] = next_theta(theta[i - 1], BODY_HANDLE_DISTANCE)

    xy = np.array([position(th) for th in theta])
    return theta, xy[:, 0], xy[:, 1]


# ---------------------------------------------------------------------------
# 3. 问题 3：转弯可行性 / 最小螺距
# ---------------------------------------------------------------------------

def head_turning_state():
    """功能：计算当前螺距下龙头转弯状态；输入：无；返回：转弯角度与时间。"""
    theta_turn = TURNING_RADIUS / p
    if theta_turn >= THETA0:
        return None, None
    t_turn = arc_length(theta_turn, THETA0)
    return theta_turn, t_turn


def check_pitch(pitch_new, dtheta=0.1, tol=1e-5):
    """功能：检查螺距是否全程无碰撞；输入：螺距、角度步长与容差；返回：状态字典。"""
    global p
    p = pitch_new
    theta_turn = TURNING_RADIUS / p
    if theta_turn >= THETA0:
        return {
            "feasible": False,
            "pitch": p,
            "theta_turn": None,
            "t_turn": None,
            "collision_time": None,
            "collision_pair": None
        }
    # --------------------------------------------
    # 搜索首次碰撞
    # --------------------------------------------
    from .collision import find_first_collision_theta
    collision_theta, collision_pair = find_first_collision_theta(
        THETA0, theta_turn, dtheta=dtheta, tol=tol
    )
    # --------------------------------------------
    # 发生碰撞
    # --------------------------------------------
    if collision_theta is not None:
        collision_time = arc_length(collision_theta, THETA0)
        t_turn = arc_length(theta_turn, THETA0)
        return {
            "feasible": False,
            "pitch": p,
            "theta_turn": theta_turn,
            "t_turn": t_turn,
            "collision_time": collision_time,
            "collision_pair": collision_pair
        }
    # --------------------------------------------
    # 全程没有碰撞
    # --------------------------------------------
    t_turn = arc_length(theta_turn, THETA0)
    return {
        "feasible": True,
        "pitch": p,
        "theta_turn": theta_turn,
        "t_turn": t_turn,
        "collision_time": None,
        "collision_pair": None
    }


def find_minimum_pitch(p_low, p_high, iterations=15, dtheta=0.15, tol=1e-6):
    """功能：二分搜索最小可行螺距；输入：螺距区间及迭代参数；返回：最小可行螺距。"""
    result_low = check_pitch(p_low, dtheta=dtheta, tol=tol)
    result_high = check_pitch(p_high, dtheta=dtheta, tol=tol)

    print(
        f"p_low  = {p_low:.6f}, "
        f"feasible = {result_low['feasible']}"
    )
    print(
        f"p_high = {p_high:.6f}, "
        f"feasible = {result_high['feasible']}"
    )

    if result_low["feasible"]:
        raise ValueError("p_low 已经可行，请减小 p_low。")
    if not result_high["feasible"]:
        raise ValueError("p_high 仍不可行，请增大 p_high。")

    for i in range(iterations):
        p_mid = (p_low + p_high) / 2
        result = check_pitch(p_mid, dtheta=dtheta, tol=tol)
        print(
            f"[{i + 1:02d}/{iterations}] "
            f"p = {p_mid:.10f} "
            f"-> {result['feasible']}"
        )
        if result["feasible"]:
            p_high = p_mid
        else:
            p_low = p_mid

    return p_high
