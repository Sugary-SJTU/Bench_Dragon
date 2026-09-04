"""问题 3：搜索转弯空间内无碰撞的最小螺距。"""

import matplotlib.pyplot as plt

from project.utils import spiral
from project.visualisation.plotting import visualize_turning_state

if __package__:
    from .config import (
        ANGLE_STEP,
        ITERATIONS,
        P_HIGH,
        P_LOW,
        PICTURES_DIR,
        RESULT_PATH,
        TOLERANCE,
        VISUALIZATION_PITCHES,
    )
else:
    from config import (
        ANGLE_STEP,
        ITERATIONS,
        P_HIGH,
        P_LOW,
        PICTURES_DIR,
        RESULT_PATH,
        TOLERANCE,
        VISUALIZATION_PITCHES,
    )


def run(visualize=False):
    """功能：求问题 3 最小可行螺距；输入：是否绘图；返回：最小螺距。"""
    minimum_pitch = spiral.find_minimum_pitch(
        P_LOW, P_HIGH, iterations=ITERATIONS, dtheta=ANGLE_STEP, tol=TOLERANCE
    )
    minimum_spacing = minimum_pitch * 2 * np.pi
    print(f"最小可行的 p = {minimum_pitch:.6f}")
    print(f"最小可行的 PITCH = {minimum_spacing:.6f}")

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(
        f"p_min = {minimum_pitch:.10f}\nPITCH_MIN = {minimum_spacing:.10f}\n",
        encoding="utf-8",
    )
    if visualize:
        PICTURES_DIR.mkdir(parents=True, exist_ok=True)
        for pitch in VISUALIZATION_PITCHES:
            label = "minimum" if pitch == "minimum" else f"{pitch:.2f}"
            figure = visualize_turning_state(minimum_pitch if pitch == "minimum" else pitch)
            output_path = PICTURES_DIR / f"problem3_turning_state_{label}.png"
            figure.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close(figure)
            print(f"可视化结果已保存到 {output_path}")
    return minimum_pitch


if __name__ == "__main__":
    run()
