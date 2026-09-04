"""原始 notebook 中被注释掉的实验性代码（仅作存档，不参与运行）。

本文件完整保留了 ``main.ipynb`` 中所有被注释掉的代码块
（problem1 主程序里的多时刻绘图、problem3 的临界碰撞可视化等），
与原始源码逐字一致，便于日后需要时参考或恢复。

注意：本模块不会被执行，也不应被任何业务模块 import。
"""

# =============================================================================
# 以下内容来自 notebook cell[06]（Problem1 主程序）中被注释掉的多时刻绘图代码
# =============================================================================

#     # 绘制几个时刻
#     plot_times = [
#         0,
#         60,
#         120,
#         180,
#         240,
#         300,
#         360,
#         420,
#     ]
#
#     # theta_sample = np.linspace(0 , 32 * np.pi , 2000)
#     # x_sample = p * theta_sample * np.cos(theta_sample)
#     # y_sample = p * theta_sample * np.sin(theta_sample)
#
#     # fig , axes = plt.subplots(4 , 2 , figsize = (25 , 25))
#     # axes = axes.flatten()
#     # for t , ax in zip(plot_times , axes):
#     #     result = df[df["time"] == t]
#     #     ax.plot(x_sample , y_sample , linestyle = "--" , linewidth = 0.7 , marker = 'None' , color  = 'black' , alpha = 0.5)
#     #     ax.plot()
#     #     ax.plot(result["x"] , result["y"] , "o-" , markersize=1)
#     #     ax.scatter(result["x"] , result["y"] , s=30 , label="Handle" , c = '#665bdc' , edgecolor='#690005' , alpha = 0.8)
#     #     ax.set_xlim(-10 , 10)
#     #     ax.set_ylim(-10 , 10)
#     #     ax.axis("equal")
#     #     ax.set_xlabel("x / m")
#     #     ax.set_ylabel("y / m")
#     #     # 在 -10,-8,-6 …… 8,10 这些位置放刻度
#     #     ax.set_xticks(np.arange(-10, 11, 2.5))
#     #     ax.set_yticks(np.arange(-10, 11, 2.5))
#
#     #     ax.set_title(f"Dragon position at t = {t} s")
#     #     ax.legend()
#     #     ax.grid(True)
#     #     ax.set_aspect("equal" , 'box', anchor="C")
#     # axes[0].axvline(x = p * 32 * np.pi , label = 'init' , color = 'red' , linestyle = '--' , linewidth = 1)
#     # plt.tight_layout()
#     # plt.savefig(
#     #     "pictures/figure_p_1_spiral.png",
#     #     dpi=300,                # 分辨率，论文建议300dpi
#     #     bbox_inches="tight",    # 裁掉多余白边，必加！
#     #     pad_inches=0.05,        # tight模式下保留少量边距
#     #     facecolor="white",      # 背景白色，避免透明背景
#     #     format="png"            # 可选：png / pdf / svg / jpg)
#     #     )
#
#     # plt.show()
#
#     # plot_times_2 = [
#     #     0 , 120 , 240 , 360
#     # ]
#
#     # fig , axes = plt.subplots(2 , 2 , figsize = (16 , 16))
#     # axes = axes.flatten()
#     # for t , ax in zip(plot_times_2 , axes):
#     #     result = df[df["time"] == t]
#     #     ax.plot(x_sample , y_sample , linestyle = "--" , linewidth = 0.7 , marker = 'None' , color  = 'black' , alpha = 0.5)
#     #     ax.plot()
#     #     ax.plot(result["x"] , result["y"] , "o-" , markersize=1)
#     #     ax.scatter(result["x"] , result["y"] , s=40 , label="Handle" , c = '#665bdc' , edgecolor='#690005' , alpha = 0.9)
#     #     ax.set_xlim(-10 , 10)
#     #     ax.set_ylim(-10 , 10)
#     #     ax.axis("equal")
#     #     ax.set_xlabel("x / m")
#     #     ax.set_ylabel("y / m")
#     #     # 在 -10,-8,-6 …… 8,10 这些位置放刻度
#     #     ax.set_xticks(np.arange(-10, 11, 2.5))
#     #     ax.set_yticks(np.arange(-10, 11, 2.5))
#
#     #     ax.set_title(f"Dragon position at t = {t} s")
#     #     ax.legend()
#     #     ax.grid(True)
#     #     ax.set_aspect("equal" , 'box', anchor="C")
#     # axes[0].axvline(x = p * 32 * np.pi , label = 'init' , color = 'red' , linestyle = '--' , linewidth = 1)
#     # plt.tight_layout()
#     # plt.savefig(
#     #     "pictures/figure_p_1_spiral_2.png",
#     #     dpi=300,                # 分辨率，论文建议300dpi
#     #     bbox_inches="tight",    # 裁掉多余白边，必加！
#     #     pad_inches=0.05,        # tight模式下保留少量边距
#     #     facecolor="white",      # 背景白色，避免透明背景
#     #     format="png"            # 可选：png / pdf / svg / jpg)
#     #     )
#
#     # plt.show()


# =============================================================================
# 以下内容来自 notebook cell[15]（Problem3）中被整体注释掉的可视化函数
# =============================================================================

# from matplotlib.patches import Circle as Circle_plt
# def visualize_critical_collision(pitch, dtheta=0.02, tol=1e-6):
#     global p
#     p = pitch
#     theta_turn = TURNING_RADIUS / p
#     collision_theta, collision_pair = find_first_collision_theta(
#         THETA0,
#         theta_turn,
#         dtheta=dtheta,
#         tol=tol
#     )
#     if collision_theta is None:
#         print(f"p = {p:.10f} 在当前精度下未检测到碰撞")
#         return  {
#         "pitch": p,
#         "collision_theta": collision_theta,
#         "collision_time": collision_time,
#         "collision_pair": collision_pair,
#         "rectangles": rectangles,
#         "theta": theta,
#         "x": x,
#         "y": y
#     }
#     collision_time = arc_length(collision_theta, THETA0)
#     theta, x, y = solve_positions_from_theta(collision_theta)
#     rectangles = build_rectangles(x, y)
#     fig, ax = plt.subplots(figsize=(12, 12))
#     # -----------------------------
#     # 螺线
#     # -----------------------------
#     plot_spiral(
#         ax,
#         theta_start=0,
#         theta_end=THETA0,
#         linestyle="--",
#         linewidth=0.8,
#         alpha=0.4
#     )
#     # -----------------------------
#     # 9 m 转向空间
#     # -----------------------------
#     turning_circle = Circle_plt(
#         (0, 0),
#         TURNING_RADIUS,
#         fill=False,
#         linewidth=2,
#         linestyle="--"
#     )
#     ax.add_patch(turning_circle)
#     # -----------------------------
#     # 绘制所有木凳
#     # -----------------------------
#     for i, rect in enumerate(rectangles):
#         plot_obb(
#             ax,
#             rect,
#             alpha=0.25,
#             linewidth=0.7
#         )
#     # -----------------------------
#     # 高亮碰撞木凳
#     # -----------------------------
#     i, j = collision_pair
#     plot_obb(
#         ax,
#         rectangles[i],
#         alpha=1.0,
#         linewidth=3.0
#     )
#     plot_obb(
#         ax,
#         rectangles[j],
#         alpha=1.0,
#         linewidth=3.0
#     )
#     # -----------------------------
#     # 标出木凳中心
#     # -----------------------------
#     for index in [i, j]:
#         center = rectangles[index].center
#         ax.scatter(
#             center[0],
#             center[1],
#             s=80,
#             zorder=10
#         )
#         ax.text(
#             center[0],
#             center[1],
#             f"  Bench {index}",
#             fontsize=12,
#             fontweight="bold",
#             zorder=11
#         )
#     # -----------------------------
#     # 碰撞点附近连线
#     # -----------------------------
#     center_i = rectangles[i].center
#     center_j = rectangles[j].center
#     ax.plot(
#         [center_i[0], center_j[0]],
#         [center_i[1], center_j[1]],
#         linestyle=":",
#         linewidth=2
#     )
#     # -----------------------------
#     # 图形设置
#     # -----------------------------
#     ax.set_aspect("equal", "box")
#     ax.set_xlabel("x / m")
#     ax.set_ylabel("y / m")
#     ax.set_title(
#         f"Critical Collision\n"
#         f"p = {p:.10f}, "
#         f"t = {collision_time:.6f} s, "
#         f"Bench {i} ↔ Bench {j}"
#     )
#     ax.grid(True, alpha=0.3)
#     plt.tight_layout()
#     plt.show()
#     print("=" * 60)
#     print(f"pitch           = {p:.10f}")
#     print(f"collision time  = {collision_time:.8f} s")
#     print(f"collision theta = {collision_theta:.8f}")
#     print(f"collision pair  = ({i}, {j})")
#     print("=" * 60)
#     return {
#         "pitch": p,
#         "collision_theta": collision_theta,
#         "collision_time": collision_time,
#         "collision_pair": collision_pair,
#         "rectangles": rectangles,
#         "theta": theta,
#         "x": x,
#         "y": y
#     }
# def visualize_collision_detail(result, padding=0.5):
#     rectangles = result["rectangles"]
#     i, j = result["collision_pair"]
#     rect_i = rectangles[i]
#     rect_j = rectangles[j]
#     centers = np.array([
#         rect_i.center,
#         rect_j.center
#     ])
#     xmin = centers[:, 0].min() - padding
#     xmax = centers[:, 0].max() + padding
#     ymin = centers[:, 1].min() - padding
#     ymax = centers[:, 1].max() + padding
#     fig, ax = plt.subplots(figsize=(8, 8))
#     # 两个碰撞木凳
#     plot_obb(
#         ax,
#         rect_i,
#         alpha=1.0,
#         linewidth=3.0
#     )
#     plot_obb(
#         ax,
#         rect_j,
#         alpha=1.0,
#         linewidth=3.0
#     )
#     # 中心点
#     ax.scatter(
#         rect_i.center[0],
#         rect_i.center[1],
#         s=100,
#         zorder=10
#     )
#     ax.scatter(
#         rect_j.center[0],
#         rect_j.center[1],
#         s=100,
#         zorder=10
#     )
#     # 中心连线
#     ax.plot(
#         [rect_i.center[0], rect_j.center[0]],
#         [rect_i.center[1], rect_j.center[1]],
#         linestyle="--",
#         linewidth=1.5
#     )
#     # 标签
#     ax.text(
#         rect_i.center[0],
#         rect_i.center[1],
#         f"Bench {i}",
#         fontsize=12,
#         fontweight="bold"
#     )
#     ax.text(
#         rect_j.center[0],
#         rect_j.center[1],
#         f"Bench {j}",
#         fontsize=12,
#         fontweight="bold"
#     )
#     ax.set_xlim(xmin, xmax)
#     ax.set_ylim(ymin, ymax)
#     ax.set_aspect("equal", "box")
#     ax.grid(True, alpha=0.3)
#     ax.set_xlabel("x / m")
#     ax.set_ylabel("y / m")
#     ax.set_title(
#         f"Collision Detail: Bench {i} ↔ Bench {j}"
#     )
#     plt.tight_layout()
#     plt.show()
