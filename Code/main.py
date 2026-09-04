"""板凳龙（阿基米德螺线）数学建模 —— 统一入口。

各题的运行逻辑位于 ``problems/problemN``，公共算法位于 ``src/project``；
本文件只负责命令行路由。

用法
----
    python main.py problem1        # 计算 0~420 s 各时刻全部把手位置/速度 → results/result1.xlsx
    python main.py problem2        # 二分求首次碰撞时间与碰撞板凳对
    python main.py problem2-viz    # 绘制碰撞时刻可视化图 → pictures/
    python main.py problem3        # 二分求最小可行螺距 p / PITCH（计算量较大）
    python main.py problem3 --viz  # 求最小螺距后，对样本螺距绘制转弯状态图
    python main.py problem4        # 展示问题 4 参数（notebook 中未实现求解）
    python main.py all             # 依次运行 problem1 / problem2 / problem3
"""

import argparse
from problems.problem1 import run as run_problem1
from problems.problem2 import run as run_problem2
from problems.problem2 import run_visualization as run_problem2_viz
from problems.problem3 import run as run_problem3
from problems.problem4 import run as run_problem4


def main():
    """功能：解析命令行并运行指定问题；输入：命令行参数；返回：无。"""
    parser = argparse.ArgumentParser(description="板凳龙（阿基米德螺线）数学建模统一入口")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("problem1", help="计算位置/速度并保存 result1.xlsx")
    sub.add_parser("problem2", help="求首次碰撞时间与碰撞板凳对")
    sub.add_parser("problem2-viz", help="绘制碰撞时刻可视化图")
    problem3 = sub.add_parser("problem3", help="求最小可行螺距")
    problem3.add_argument("--viz", action="store_true", help="绘制转弯状态图")
    sub.add_parser("problem4", help="展示问题 4 参数")
    sub.add_parser("all", help="依次运行问题 1、2、3")

    args = parser.parse_args()
    if args.command == "problem1":
        run_problem1()
    elif args.command == "problem2":
        run_problem2()
    elif args.command == "problem2-viz":
        run_problem2_viz()
    elif args.command == "problem3":
        run_problem3(visualize=args.viz)
    elif args.command == "problem4":
        run_problem4()
    elif args.command == "all":
        run_problem1()
        run_problem2()
        print("\n[提示] problem3 计算量较大，建议单独运行：python main.py problem3")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
