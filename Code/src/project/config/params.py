"""参数：项目全部只读常量。

本文件集中存放“板凳龙”问题的所有几何 / 运动学参数，供
``spiral.py``（曲线工具）、``collision.py``（碰撞工具）、
``plotting.py``（作图工具）只读复用。

可变状态说明
------------
螺线参数 ``p = PITCH / (2π)`` 是问题 3 中会被 ``global p`` 反复改写的
**可变状态**。为保证所有读取方立即看到改写值，它不放在本文件，而作为
唯一可变全局量保留在 ``spiral.py`` 中（由 ``PITCH`` 计算得出）。
"""

import numpy as np

# 1. 基本参数
PITCH = 0.55                 # 螺距，m

HEAD_LENGTH = 3.41           # 龙头长度，m
BODY_LENGTH = 2.20           # 龙身/龙尾长度，m
HOLE_OFFSET = 0.275          # 把手孔中心距板头，m
BOARD_WIDTH = 0.30           # 板凳宽度，m
HEAD_SPEED = 1.0             # 龙头前把手速度，m/s

N_HANDLES = 224              # 把手总数
BODY_HANDLE_DISTANCE = BODY_LENGTH - 2 * HOLE_OFFSET  # 相邻龙身把手中心距
HEAD_HANDLE_DISTANCE = HEAD_LENGTH - 2 * HOLE_OFFSET  # 龙头前后把手中心距

# 龙头初始角度（题设 16 圈）
THETA0 = 16 * 2 * np.pi      # theta0(0) = 32pi

# 问题 3 新增：转弯半径（9 m 转向空间 → 半径 4.5 m）
TURNING_RADIUS = 4.5
