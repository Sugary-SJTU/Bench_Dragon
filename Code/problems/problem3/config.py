"""问题 3 的最小螺距搜索配置。"""

from pathlib import Path

P_LOW = 0.05
P_HIGH = 0.10
ITERATIONS = 25
ANGLE_STEP = 0.15
TOLERANCE = 1e-6
PICTURES_DIR = Path("pictures")
RESULT_PATH = Path("results/problem3_min_pitch.txt")
VISUALIZATION_PITCHES = (0.05, "minimum", 0.08)
