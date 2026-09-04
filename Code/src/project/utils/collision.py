"""板凳碰撞检测（OBB 有向包围盒 + SAT 分离轴）。

模块职责
--------
把每块板凳建模为有向包围盒（OBB），先后用“外接圆粗筛”与
“SAT 分离轴定理精判”判断两块板凳是否相碰，并在时间 / 角度
上二分搜索首次碰撞时刻 / 角度。

本模块不持有可变全局量 ``p``，仅以只读方式复用
``src.spiral`` 中的常量与求解函数，函数体与原始 notebook 一致。
"""

import numpy as np
from dataclasses import dataclass

from ..config.params import (
    HEAD_LENGTH,
    BODY_LENGTH,
    BOARD_WIDTH,
)
from .spiral import (
    solve_positions,
    solve_positions_from_theta,
)


# 矩形数据结构
@dataclass
class Rectangle:
    """
    用有向包围盒（OBB）表示一块板凳。

    center      : 矩形中心
    axis_x      : 矩形长度方向单位向量
    axis_y      : 矩形宽度方向单位向量
    half_length : 矩形半长
    half_width  : 矩形半宽
    """
    center: np.ndarray
    axis_x: np.ndarray
    axis_y: np.ndarray
    half_length: float
    half_width: float

def build_rectangles(x, y):
    """功能：根据相邻把手坐标构建板凳 OBB；输入：x、y 坐标序列；返回：矩形列表。"""
    N = len(x)
    rectangles = []

    for i in range(N - 1):
        # 两个把手的位置
        p1 = np.array([x[i], y[i]])
        p2 = np.array([x[i + 1], y[i + 1]])

        delta = p2 - p1
        distance = np.linalg.norm(delta)
        axis_x = delta / distance

        # 与 axis_x 垂直
        axis_y = np.array([-axis_x[1], axis_x[0]])
        center = (p1 + p2) / 2

        if i == 0:
            board_length = HEAD_LENGTH
        else:
            board_length = BODY_LENGTH

        # 构造矩形
        rectangles.append(
            Rectangle(
                center=center,
                axis_x=axis_x,
                axis_y=axis_y,
                half_length=board_length / 2,
                half_width=BOARD_WIDTH / 2
            )
        )

    return rectangles



def bounding_radius(rect):
    """功能：计算矩形外接圆半径；输入：Rectangle；返回：半径。"""
    return np.sqrt(rect.half_length ** 2 + rect.half_width ** 2)


def coarse_collision(rect_a, rect_b):
    """功能：用外接圆快速筛查碰撞；输入：两个 Rectangle；返回：是否可能相碰。"""
    delta = rect_a.center - rect_b.center
    center_distance_sq = np.dot(delta, delta)

    radius_sum = bounding_radius(rect_a) + bounding_radius(rect_b)
    return center_distance_sq <= radius_sum ** 2


def project_rectangle(rect, axis):
    """功能：将矩形投影到指定轴；输入：Rectangle 与单位轴；返回：投影区间。"""
    # 矩形中心在 axis 上的投影
    center_projection = np.dot(rect.center, axis)
    projection_radius = rect.half_length * abs(np.dot(rect.axis_x, axis)) + \
        rect.half_width * abs(np.dot(rect.axis_y, axis))

    return (center_projection - projection_radius, center_projection + projection_radius)


def projections_overlap(proj_a, proj_b):
    """功能：判断两个投影区间是否重叠；输入：两个区间；返回：是否重叠。"""
    min_a, max_a = proj_a
    min_b, max_b = proj_b

    return not (
        max_a < min_b
        or
        max_b < min_a
    )


def sat_collision(rect_a, rect_b):
    """功能：用 SAT 精确判断两个 OBB 是否碰撞；输入：两个 Rectangle；返回：是否碰撞。"""
    axes = [
        rect_a.axis_x,
        rect_a.axis_y,
        rect_b.axis_x,
        rect_b.axis_y
    ]

    for axis in axes:
        proj_a = project_rectangle(rect_a, axis)
        proj_b = project_rectangle(rect_b, axis)

        if not projections_overlap(proj_a, proj_b):
            return False

    return True


def rectangles_collision(rect_a, rect_b):
    """功能：组合粗筛与 SAT 检测碰撞；输入：两个 Rectangle；返回：是否碰撞。"""
    if not coarse_collision(rect_a, rect_b):
        return False

    return sat_collision(rect_a, rect_b)


def detect_collision(x, y, theta: np.ndarray):
    """功能：检测整支队伍的碰撞；输入：把手 x、y、theta；返回：碰撞标志及板凳索引对。"""
    rectangles = build_rectangles(x, y)
    N = len(rectangles)

    # 两两检测
    for i in range(N):
        for j in range(i + 2, N):
            if abs(theta[i] - theta[j]) >= 3 * np.pi:
                continue

            # 粗筛 + SAT
            if rectangles_collision(rectangles[i], rectangles[j]):
                return True, (i, j)

    return False, None


def has_collision(t):
    """功能：检测指定时刻的队伍碰撞；输入：时间 t；返回：碰撞标志及板凳索引对。"""
    theta, x, y = solve_positions(t)
    collision, pair = detect_collision(x, y, theta)

    return collision, pair


def find_first_collision(t_start=0.0, t_end=420.0, dt=1.0, tol=1e-6):
    """功能：搜索首次碰撞时刻；输入：时间范围、步长与容差；返回：时刻及板凳索引对。"""
    t_prev = t_start
    collision, pair = has_collision(t_prev)

    if collision:
        print(f"在{t_prev}时刻前发生碰撞，碰撞对为{pair}")
        return t_prev, pair

    t = t_start + dt
    while t <= t_end:
        collision, pair = has_collision(t)

        # 第一次发现碰撞
        if collision:
            left = t_prev
            right = t

            while right - left > tol:
                mid = (left + right) / 2
                collision_mid, pair_mid = has_collision(mid)

                if collision_mid:
                    right = mid
                    if pair_mid is not None:
                        pair = pair_mid
                else:
                    left = mid

            return right, pair

        t_prev = t
        t += dt

    return None, None


def has_collision_theta(theta_head):
    """功能：检测指定龙头角度的队伍碰撞；输入：龙头角度；返回：碰撞标志及板凳索引对。"""
    theta, x, y = solve_positions_from_theta(theta_head)
    return detect_collision(x, y, theta)


def find_first_collision_theta(theta_start, theta_end, dtheta=0.2, tol=1e-5):
    """功能：按递减龙头角度搜索首次碰撞；输入：角度范围、步长与容差；返回：角度及板凳索引对。"""
    theta_prev = theta_start
    collision, pair = has_collision_theta(theta_prev)
    if collision:
        return theta_prev, pair

    while theta_prev > theta_end:
        theta_next = max(theta_prev - dtheta, theta_end)
        collision, pair = has_collision_theta(theta_next)

        if collision:
            left = theta_next
            right = theta_prev
            collision_pair = pair

            while right - left > tol:
                mid = (left + right) / 2
                collision_mid, pair_mid = has_collision_theta(mid)

                if collision_mid:
                    left = mid
                    if pair_mid is not None:
                        collision_pair = pair_mid
                else:
                    right = mid

            return left, collision_pair

        theta_prev = theta_next

    return None, None
