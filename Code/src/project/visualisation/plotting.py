"""作图工具函数：螺线 / 板凳 / 碰撞与转弯状态可视化。

模块职责
--------
集中存放所有 matplotlib 绘图辅助函数：

* 基础绘图（``plot_spiral`` / ``plot_obb`` / ``radius_to_turn``）；
* 问题 2 碰撞过程可视化（``visualize_filter_process`` /
  ``visualize_filter_process_subax``）；
* 问题 3 转弯状态总览图（``visualize_turning_state``）。

可变状态说明
------------
``plot_spiral`` / ``radius_to_turn`` / ``visualize_turning_state`` 需要
读取 / 改写可变螺线参数 ``p``（其唯一状态源在 ``spiral.py``），因此这里
统一通过 ``spiral.p`` 访问，保证总能读到最新值。
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle as Circle_plt

from ..utils import spiral
from ..config.params import THETA0, TURNING_RADIUS
from ..utils.collision import build_rectangles, detect_collision
from ..utils.spiral import arc_length, solve_positions_from_theta


# ---------------------------------------------------------------------------
# 1. 基础绘图工具
# ---------------------------------------------------------------------------

def plot_spiral(ax, theta_start=0, theta_end=THETA0, num_points=2000, **kwargs):
    """功能：绘制阿基米德螺线；输入：坐标轴、角度范围及绘图参数；返回：无。"""
    theta = np.linspace(theta_start, theta_end, num_points)
    r = spiral.p * theta
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    ax.plot(x, y, **kwargs)


def radius_to_turn(r):
    """功能：将半径换算为螺线圈数；输入：半径 r；返回：圈数。"""
    theta = r / spiral.p
    return theta / (2 * np.pi)


def plot_obb(ax, rect, color="red", alpha=0.6, linewidth=1.2):
    """功能：绘制有向包围盒；输入：坐标轴、Rectangle 与样式参数；返回：无。"""
    p0 = rect.center + rect.half_length * rect.axis_x + rect.half_width * rect.axis_y
    p1 = rect.center - rect.half_length * rect.axis_x + rect.half_width * rect.axis_y
    p2 = rect.center - rect.half_length * rect.axis_x - rect.half_width * rect.axis_y
    p3 = rect.center + rect.half_length * rect.axis_x - rect.half_width * rect.axis_y
    verts = np.array([p0, p1, p2, p3, p0])
    ax.plot(verts[:, 0], verts[:, 1], color=color, alpha=alpha, linewidth=linewidth)


# ---------------------------------------------------------------------------
# 2. 问题 2：碰撞过程可视化
# ---------------------------------------------------------------------------

def visualize_filter_process(x_handle, y_handle, time):
    """功能：绘制指定时刻的碰撞筛选图；输入：把手坐标与时间；返回：Figure。"""
    rects = build_rectangles(x_handle, y_handle)

    fig, ax = plt.subplots(figsize=(12, 12))

    plot_spiral(ax, theta_start=0, theta_end=THETA0,
                linestyle="--", linewidth=0.8, color="gray", alpha=0.5)

    for idx, rect in enumerate(rects):
        r_center = np.hypot(rect.center[0], rect.center[1])
        turn = radius_to_turn(r_center)

        if idx == 0 or idx == 8:
            plot_obb(ax, rect, color="#d20700", alpha=1.0, linewidth=0.5)
        else:
            plot_obb(ax, rect, color="#2ca02c", alpha=0.4, linewidth=0.95)

        # 每 5 个标记一次圈号
        if idx % 5 == 0:
            ax.text(rect.center[0], rect.center[1], f"{turn:.1f}", fontsize=7, ha="center")

    # 坐标轴设置
    ax.set_aspect("equal", "box")
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("x / m")
    ax.set_ylabel("y / m")
    ax.set_title(f"Visualisation of Collision  Time:{time}s")

    legend_elements = [
        Line2D([0], [0], color="#d62728", lw=2, label="Dragon head / Chair 8"),
        Line2D([0], [0], color="#2ca02c", lw=2, label="filtered"),
    ]
    ax.legend(handles=legend_elements, loc="upper right")

    plt.tight_layout()
    plt.savefig(f"pictures/collision_filter_vis_{time}.png", dpi=300, bbox_inches="tight")

    return fig


def visualize_filter_process_subax(x_handle, y_handle, time, ax):
    """功能：在指定子图绘制碰撞筛选图；输入：把手坐标、时间与坐标轴；返回：无。"""
    rects = build_rectangles(x_handle, y_handle)

    plot_spiral(ax, theta_start=0, theta_end=THETA0,
                linestyle="--", linewidth=0.8, color="gray", alpha=0.5)

    for idx, rect in enumerate(rects):
        r_center = np.hypot(rect.center[0], rect.center[1])
        turn = radius_to_turn(r_center)

        if idx == 0 or idx == 8:
            plot_obb(ax, rect, color="#d20700", alpha=1.0, linewidth=0.4)
        else:
            plot_obb(ax, rect, color="#2ca02c", alpha=0.4, linewidth=0.95)

        # 每 5 个标记一次圈号
        if idx % 5 == 0:
            ax.text(rect.center[0], rect.center[1], f"{turn:.1f}", fontsize=7, ha="center")

    # 坐标轴设置
    ax.set_aspect("equal", "box")
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("x / m")
    ax.set_ylabel("y / m")
    ax.set_title(f"Visualisation of Collision  Time:{time}s")

    legend_elements = [
        Line2D([0], [0], color="#d62728", lw=2, label="Dragon head / Chair 8"),
        Line2D([0], [0], color="#2ca02c", lw=2, label="filtered"),
    ]
    ax.legend(handles=legend_elements, loc="upper right")


# ---------------------------------------------------------------------------
# 3. 问题 3：转弯状态可视化
# ---------------------------------------------------------------------------

def visualize_turning_state(pitch):
    """
    功能：可视化龙头到达转弯边界时的队伍状态。
    输入：螺线参数 pitch；返回：Figure 或 None。

    可视化内容：
    龙头到达 r = 4.5 m 转弯边界时的队伍状态。
    总览图：
        - 所有普通木凳：绿色
        - 龙头 Bench 0：红色突出
        - Bench 16：蓝色突出
        - 显示 9 m 转弯圆
        - 左上角显示 Bench 0 与 Bench 16 的特写
    特写图：
        - 只显示 Bench 0（龙头）
        - 只显示 Bench 16
    """
    spiral.p = pitch

    # =========================================================
    # 1. 计算龙头到达转弯边界时的 theta 和时间
    # =========================================================
    theta_turn = TURNING_RADIUS / spiral.p
    if theta_turn >= THETA0:
        print("错误：当前 pitch 太小，龙头初始位置已经位于转弯区域内。")
        return
    t_turn = arc_length(theta_turn, THETA0)

    # =========================================================
    # 2. 计算此时所有把手的位置
    # =========================================================
    theta, x, y = solve_positions_from_theta(theta_turn)

    # =========================================================
    # 3. 创建木凳 OBB
    # =========================================================
    rectangles = build_rectangles(x, y)

    # =========================================================
    # 4. 检查碰撞
    # =========================================================
    collision, collision_pair = detect_collision(x, y, theta)

    # =========================================================
    # 5. 创建画布
    # =========================================================
    fig, ax = plt.subplots(figsize=(12, 10))

    # 绘制阿基米德螺线
    plot_spiral(
        ax,
        theta_start=0,
        theta_end=THETA0,
        linestyle="--",
        linewidth=0.8,
        color="gray",
        alpha=0.5
    )

    # =========================================================
    # 7. 绘制 9 m 转弯区域
    # =========================================================
    turning_circle = Circle_plt(
        (0, 0),
        TURNING_RADIUS,
        fill=False,
        linestyle="--",
        linewidth=1.5,
        alpha=0.7
    )
    ax.add_patch(turning_circle)

    # 转弯圆中心
    ax.scatter(0, 0, s=40, zorder=5)

    # =========================================================
    # 8. 绘制所有木凳
    #
    # 普通木凳：绿色
    # 龙头 Bench 0：红色
    # Bench 16：蓝色
    # =========================================================
    for i, rect in enumerate(rectangles):
        # -----------------------------------------------------
        # 龙头 Bench 0
        # -----------------------------------------------------
        if i == 0:
            plot_obb(
                ax,
                rect,
                color="red",
                alpha=0.8,
                linewidth=1
            )
            ax.scatter(
                rect.center[0],
                rect.center[1],
                s=30,
                color="red",
                zorder=10,
                alpha=0.6
            )
            ax.text(
                rect.center[0],
                rect.center[1],
                " Dragon Head \n  Bench 0",
                fontsize=11,
                fontweight="bold",
                color="red",
                zorder=11,
                alpha=0.6
            )
        # -----------------------------------------------------
        # Bench 16
        # -----------------------------------------------------
        elif i == 16:
            plot_obb(
                ax,
                rect,
                color="blue",
                alpha=0.8,
                linewidth=1
            )
            ax.scatter(
                rect.center[0],
                rect.center[1],
                s=30,
                color="blue",
                zorder=10
            )
            ax.text(
                rect.center[0],
                rect.center[1],
                "  Bench 16",
                fontsize=11,
                color="blue",
                zorder=11
            )
        # -----------------------------------------------------
        # 普通木凳
        # -----------------------------------------------------
        else:
            plot_obb(
                ax,
                rect,
                color="green",
                alpha=0.4,
                linewidth=1.0
            )

    # =========================================================
    # 9. 标记龙头当前位置
    # =========================================================
    head_position = np.array([x[0], y[0]])
    ax.scatter(
        head_position[0],
        head_position[1],
        s=100,
        facecolors="none",
        edgecolors="red",
        linewidths=1,
        zorder=12
    )

    # =========================================================
    # 10. 固定特写区域：
    #     龙头 Bench 0 + Bench 16
    # =========================================================
    i = 0
    j = 16
    rect_i = rectangles[i]
    rect_j = rectangles[j]
    centers = np.array([rect_i.center, rect_j.center])

    # ---------------------------------------------------------
    # 特写区域范围
    # ---------------------------------------------------------
    xmin = centers[:, 0].min() - 0.8
    xmax = centers[:, 0].max() + 0.8
    ymin = centers[:, 1].min() - 0.8
    ymax = centers[:, 1].max() + 0.8

    # =========================================================
    # 11. 在总览图中画出特写框
    # =========================================================
    from matplotlib.patches import Rectangle as MplRectangle
    zoom_box = MplRectangle(
        (xmin, ymin),
        xmax - xmin,
        ymax - ymin,
        fill=False,
        linewidth=2.5,
        linestyle=":"
    )
    ax.add_patch(zoom_box)

    # =========================================================
    # 12. 创建左上角特写
    # =========================================================
    inset = ax.inset_axes([0.04, 0.58, 0.38, 0.38])

    # =========================================================
    # 13. 特写中绘制 Bench 0
    # =========================================================
    plot_obb(
        inset,
        rect_i,
        color="red",
        alpha=1.0,
        linewidth=3.5
    )

    # =========================================================
    # 14. 特写中绘制 Bench 16
    # =========================================================
    plot_obb(
        inset,
        rect_j,
        color="blue",
        alpha=1.0,
        linewidth=2
    )

    # =========================================================
    # 15. 特写中的中心点
    # =========================================================
    inset.scatter(
        rect_i.center[0],
        rect_i.center[1],
        s=90,
        color="red",
        zorder=10
    )
    inset.scatter(
        rect_j.center[0],
        rect_j.center[1],
        s=90,
        color="blue",
        zorder=10
    )

    # =========================================================
    # 16. 特写中的文字标签
    # =========================================================
    inset.text(
        rect_i.center[0],
        rect_i.center[1],
        "  Dragon head\n  Bench 0",
        fontsize=10,
        fontweight="bold",
        color="red",
        zorder=11
    )
    inset.text(
        rect_j.center[0],
        rect_j.center[1],
        "  Bench 16",
        fontsize=10,
        fontweight="bold",
        color="blue",
        zorder=11
    )

    # =========================================================
    # 17. 特写中画两木凳中心连线
    # =========================================================
    inset.plot(
        [rect_i.center[0], rect_j.center[0]],
        [rect_i.center[1], rect_j.center[1]],
        linestyle="--",
        linewidth=1.5,
        alpha=0.8
    )

    # =========================================================
    # 18. 特写范围
    # =========================================================
    inset.set_xlim(xmin, xmax)
    inset.set_ylim(ymin, ymax)
    inset.set_aspect("equal", adjustable="box")
    inset.grid(True, alpha=0.3)

    # 19. 特写标题
    inset.set_title(
        "Specification of Bench 0 / Bench 16 ",
        fontsize=11,
        fontweight="bold"
    )

    # 20. 总览图标题
    if collision:
        title = (
            f"State at turning point\n"
            f"p = {pitch:.6f} m    "
            f"t = {t_turn:.3f} s    "
            f"Collision:Bench {collision_pair[0]} ↔ "
            f"Bench {collision_pair[1]}"
        )
    else:
        title = (
            f"State at turning point\n"
            f"p = {pitch:.6f} m    "
            f"t = {t_turn:.3f} s    "
            f"No collision"
        )
    ax.set_title(title, fontsize=15, fontweight="bold", pad=15)

    # =========================================================
    # 21. 坐标轴
    # =========================================================
    ax.set_xlabel("x / m", fontsize=12)
    ax.set_ylabel("y / m", fontsize=12)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.25)

    # =========================================================
    # 22. 坐标范围
    # =========================================================
    margin = 2.0
    all_x = np.asarray(x)
    all_y = np.asarray(y)
    ax.set_xlim(all_x.min() - margin, all_x.max() + margin)
    ax.set_ylim(all_y.min() - margin, all_y.max() + margin)

    # =========================================================
    # 23. 图例
    # =========================================================
    legend_elements = [
        Line2D([0], [0], color="green", linewidth=2, label="Bench"),
        Line2D([0], [0], color="red", linewidth=3, label="Dragon head Bench 0"),
        Line2D([0], [0], color="blue", linewidth=3, label="Bench 16"),
        Line2D([0], [0], linestyle="--", color="black", linewidth=2, label="9 m Turning Verge")
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=10)

    # =========================================================
    # 24. 调整布局并显示
    # =========================================================
    plt.tight_layout()
    return fig
