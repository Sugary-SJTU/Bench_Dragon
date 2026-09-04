"""问题 2：搜索板凳龙首次碰撞并绘制碰撞过程。"""

import matplotlib.pyplot as plt

from project.utils import spiral
from project.utils.collision import find_first_collision
from project.visualisation.plotting import (
    visualize_filter_process,
    visualize_filter_process_subax,
)

if __package__:
    from .config import (
        GROUP_VISUALIZATION_TIMES,
        PICTURES_DIR,
        SINGLE_VISUALIZATION_TIME,
        TIME_END,
        TIME_START,
        TIME_STEP,
        TIME_TOLERANCE,
    )
else:
    from config import (
        GROUP_VISUALIZATION_TIMES,
        PICTURES_DIR,
        SINGLE_VISUALIZATION_TIME,
        TIME_END,
        TIME_START,
        TIME_STEP,
        TIME_TOLERANCE,
    )


def run():
    """功能：计算问题 2 的首次碰撞；输入：无；返回：碰撞时间及板凳索引对。"""
    collision_time, pair = find_first_collision(
        t_start=TIME_START,
        t_end=TIME_END,
        dt=TIME_STEP,
        tol=TIME_TOLERANCE,
    )
    if collision_time is None or pair is None:
        print("420 s 内没有发生碰撞。")
    else:
        print(f"首次碰撞时间：{collision_time:.6f} s")
        print(f"发生碰撞的板凳：{pair[0] + 1} 和 {pair[1] + 1}")
    return collision_time, pair


def run_visualization():
    """功能：绘制问题 2 的碰撞过程；输入：无；返回：组图文件路径。"""
    PICTURES_DIR.mkdir(parents=True, exist_ok=True)
    _, x_values, y_values = spiral.solve_positions(SINGLE_VISUALIZATION_TIME)
    figure = visualize_filter_process(x_values, y_values, SINGLE_VISUALIZATION_TIME)
    plt.close(figure)

    figure, axes = plt.subplots(2, 2, figsize=(20, 20))
    for time_value, axis in zip(GROUP_VISUALIZATION_TIMES, axes.flat):
        _, x_values, y_values = spiral.solve_positions(time_value)
        visualize_filter_process_subax(x_values, y_values, time_value, axis)
    output_path = PICTURES_DIR / "collision_visualization_group.png"
    figure.savefig(output_path)
    plt.close(figure)
    print(f"可视化结果已保存到 {PICTURES_DIR}/")
    return output_path


if __name__ == "__main__":
    run()
