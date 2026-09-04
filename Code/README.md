# 板凳龙（阿基米德螺线）数学建模项目

由原始 Jupyter Notebook `main.ipynb` 重组而来的结构化 Python 项目。
**核心算法代码保持与原 notebook 一致**，仅做了模块拆分、目录整理与入口封装。

## 背景

一条 223 节板凳拼接而成的“板凳龙”，其龙头前把手沿阿基米德螺线匀速
（1 m/s）运动，龙身/龙尾通过刚性板凳连接跟随盘入。本项目完成：

| 问题 | 内容 | 关键结果（原 notebook） |
| ---- | ---- | ----------------------- |
| Problem 1 | 0~420 s 各整分钟时刻全部 224 个把手的位置与速度 | `results/result1.xlsx` |
| Problem 2 | 板凳碰撞检测（OBB + SAT），求首次碰撞 | 首次碰撞 412.473838 s，板凳 1 与 9 |
| Problem 3 | 求最小可行螺距，使整支龙在 9 m 转弯空间内不碰撞 | `find_minimum_pitch` 二分 |
| Problem 4 | 仅定义了参数（`PITCH=1.70`, `TURNING_RADIUS=0.451`），notebook 中未实现求解 | — |

## 目录结构

```
bench-dragon/
├── main.py                 # 统一入口（problem1 / problem2 / problem2-viz / problem3 / problem4 / all）
├── requirements.txt
├── README.md
├── problems/
│   ├── problem1/            # 问题 1：位置与速度计算
│   │   ├── config.py        # 本题时间序列与结果路径
│   │   ├── main.py          # 本题执行入口
│   │   └── __init__.py
│   ├── problem2/            # 问题 2：首次碰撞及可视化
│   │   ├── config.py
│   │   ├── main.py
│   │   └── __init__.py
│   ├── problem3/            # 问题 3：最小可行螺距
│   │   ├── config.py
│   │   ├── main.py
│   │   └── __init__.py
│   └── problem4/            # 问题 4：题设参数展示
│       ├── config.py
│       ├── main.py
│       └── __init__.py
├── src/
│   └── project/
│       ├── config/params.py             # 参数：全部只读常量
│       ├── utils/spiral.py              # 曲线、位置/速度与问题 3 工具
│       ├── utils/collision.py           # OBB、SAT 与首次碰撞工具
│       ├── visualisation/plotting.py    # 螺线/板凳/碰撞可视化工具
│       └── _archive/_archive.py         # 原 notebook 实验代码（仅存档）
├── results/                # 数值结果输出（result1.xlsx 等）
└── pictures/               # 绘图输出
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

在项目根目录下运行：

```bash
python main.py problem1      # → results/result1.xlsx
python main.py problem2      # → 打印首次碰撞时间与板凳对
python main.py problem2-viz  # → pictures/ 下生成碰撞可视化图
python main.py problem3      # 二分求最小可行螺距（计算量较大，可加 --viz 绘图）
python main.py problem3 --viz
python main.py problem4      # 展示问题 4 参数
python main.py all           # 依次运行 problem1 / problem2 / problem3
```

## 源码组织说明（相对 notebook 的改动）

1. **按题目与工具拆分模块**：
   - `problems/problemN`：每题独立保留 `config.py`、`main.py`、`__init__.py`，分别维护题目参数与执行编排；
   - `project.config.params`：参数 —— 全部只读常量；
   - `project.utils.spiral`：曲线工具 —— 螺线几何量、位置/速度求解、问题 3 二分；
   - `project.utils.collision`：碰撞工具 —— OBB 建模、SAT 检测、首次碰撞二分；
   - `project.visualisation.plotting`：作图工具 —— 螺线/OBB/碰撞/转弯状态可视化；
   - 入口统一收敛到 `main.py`。
2. **可变全局状态 `p`**：原始代码通过 `global p` 在问题 3 中反复改写螺线参数
   `p`。为保证所有读取方立即看到改写值，`p` 作为唯一可变状态保留在
   `src/spiral.py`（由 `params.py` 的 `PITCH` 计算得出）；作图工具通过
   `spiral.p` 读取/改写。其余只读参数集中在 `params.py`。算法函数体本身
   未做改动。
3. **被注释代码归档**：notebook 中被注释掉的实验性绘图代码完整保留在
   `src/_archive.py`。
4. **输出路径**：`result1.xlsx` 输出到 `results/`，绘图输出到 `pictures/`
   （原 notebook 输出到当前目录与 `pictures/`）。
5. **问题 4**：notebook 中只有参数定义、无求解代码，本项目如实保留为占位说明，
   未虚构实现。

## 与原 notebook 结果一致性验证

- Problem 2 输出与 notebook 一致：`首次碰撞时间：412.473838 s`，
  `发生碰撞的板凳：1 和 9`。
- Problem 1 的 `results/result1.xlsx` 结构（time / handle / x / y / speed）
  与原 notebook 一致。
