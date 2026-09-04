"""问题 1：计算板凳龙各指定时刻的位置与速度。"""

from pathlib import Path

import pandas as pd

from project.utils import spiral

if __package__:
    from .config import RESULT_PATH, TIME_SERIES
else:
    from config import RESULT_PATH, TIME_SERIES


def run():
    """功能：计算问题 1 并导出 Excel；输入：无；返回：结果文件路径。"""
    records = []
    for time_value in TIME_SERIES:
        print(f"\r正在计算 t = {time_value:3d} s", end="")
        result = spiral.solve_one_time(time_value)
        for handle_index in range(spiral.N_HANDLES):
            records.append({
                "time": time_value,
                "handle": handle_index + 1,
                "x": result["x"][handle_index],
                "y": result["y"][handle_index],
                "speed": result["speed"][handle_index],
            })

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_excel(RESULT_PATH, index=False)
    print(f"\n结果保存到 {RESULT_PATH}")
    return RESULT_PATH


if __name__ == "__main__":
    run()
