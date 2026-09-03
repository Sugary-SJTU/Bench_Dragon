```python
def solve_problem2():
    print("\n开始计算问题二（SAT 碰撞检测，确定盘入终止时刻）……")

    t_star, t_safe, ts, gaps, pair_coarse = find_termination_time()
    print("    终止时刻 t* = %.4f s" % t_star)
    print("    最后一次无碰撞时刻 = %.4f s" % t_safe)

    theta, x, y = solve_positions(t_star)
    speed = solve_velocity(t_star)
    H = np.column_stack([x, y])
    corners, u, n = board_rectangles(H)
    pair = sat_collision_pair(corners, u, n)
    if pair is None:
        pair = pair_coarse
    print("    终止时刻碰撞板凳对：第 %d 节与第 %d 节（SAT 检测）" % (pair[0] + 1, pair[1] + 1))
    pair_full = sat_collision_pair(corners, u, n, window=len(u))
    print("    全窗口复核碰撞对：", pair_full)
    _, xb, yb = solve_positions(t_star - 1.0)
    pc_before = sat_collision_pair(*board_rectangles(np.column_stack([xb, yb])))
    print("    t* - 1 s 是否碰撞：", pc_before)

    # ---------- 填写 result2.xlsx ----------
    wb = openpyxl.load_workbook(TEMPLATE_PATH2)
    ws = wb["Sheet1"]
    for r in range(2, 2 + N_HANDLES):        # Excel 行 2..225
        m = r - 1                            # 把手编号 1..224
        i = m - 1
        c = ws.cell(row=r, column=2)
        c.value = r6(x[i])
        c.number_format = "0.000000"
        c = ws.cell(row=r, column=3)
        c.value = r6(y[i])
        c.number_format = "0.000000"
        c = ws.cell(row=r, column=4)
        c.value = r6(speed[i])
        c.number_format = "0.000000"
    ws.column_dimensions["A"].width = 16
    for col in (2, 3, 4):
        ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 14

    result2_path = os.path.join(OUTPUT_DIR, "result2.xlsx")
    try:
        wb.save(result2_path)
        print("    已保存：%s" % result2_path)
    except PermissionError:
        alt2 = os.path.join(OUTPUT_DIR, "result2_备用.xlsx")
        wb.save(alt2)
        print("    result2.xlsx 正被占用（可能已在 Excel 中打开），已另存为：%s" % alt2)

    # ---------- 论文需要的 7 个把手 ----------
    paper_idx = [1, 2, 52, 102, 152, 202, 224]
    paper_labels = ["龙头前把手", "第1节龙身前把手", "第51节龙身前把手",
                    "第101节龙身前把手", "第151节龙身前把手",
                    "第201节龙身前把手", "龙尾后把手"]
    print("\n======== 问题 2：t* 时刻论文表 ========")
    print("终止时刻 t* = %.4f s" % t_star)
    print("点".ljust(18) + "x (m)".rjust(14) + "y (m)".rjust(14) + "速度 (m/s)".rjust(14))
    for idx, lab in zip(paper_idx, paper_labels):
        i = idx - 1
        print(lab.ljust(18) + ("%14.6f" % r6(x[i])) + ("%14.6f" % r6(y[i])) + ("%14.6f" % r6(speed[i])))

    # ---------- 可视化 1：终止时刻整体图 ----------
    fig, ax = plt.subplots(figsize=(9, 9))
    draw_dragon(ax, H, highlight=pair,
                title="t* = %.3f s 时的舞龙队（红色为碰撞板凳：第 %d 节与第 %d 节）" % (t_star, pair[0] + 1, pair[1] + 1))
    ax.legend(loc="upper right")
    fig.tight_layout()
    p_fig = os.path.join(OUTPUT_DIR, "fig2_termination.png")
    fig.savefig(p_fig, dpi=150)
    plt.close(fig)
    print("    已保存：%s" % p_fig)

    # ---------- 可视化 2：最小间距曲线 ----------
    gaps = list(gaps)
    g_last, _ = min_segment_gap(H)
    gaps.append(g_last)
    ts = list(ts)
    ts.append(t_star)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(ts, gaps, lw=1.5)
    ax.axhline(BOARD_WIDTH, color="red", ls="--", lw=1, label="板凳宽度 0.30 m")
    ax.axvline(t_star, color="orange", ls="-.", lw=1, label="t* = %.3f s" % t_star)
    ax.set_xlabel("t / s")
    ax.set_ylabel("相邻非相邻板凳最小中心线间距 / m")
    ax.set_title("问题 2：板凳间最小间距随时间的变化")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    p_gap = os.path.join(OUTPUT_DIR, "fig2_gap_curve.png")
    fig.savefig(p_gap, dpi=150)
    plt.close(fig)
    print("    已保存：%s" % p_gap)

    # ---------- 可视化 3：最后 20 s 盘入动画 GIF ----------
    try:
        import matplotlib.animation as animation
        frames = np.arange(max(0.0, t_star - 20.0), t_star + 1e-9, 0.5)
        fig, ax = plt.subplots(figsize=(8, 8))

        def anim_frame(k):
            t = float(frames[k])
            _, xa, ya = solve_positions(t)
            Ha = np.column_stack([xa, ya])
            ax.clear()
            draw_dragon(ax, Ha, title="t = %.1f s" % t)
            return ax

        anim = animation.FuncAnimation(fig, anim_frame, frames=len(frames), interval=200)
        gif_path = os.path.join(OUTPUT_DIR, "fig2_approach.gif")
        anim.save(gif_path, writer="pillow", fps=5)
        plt.close(fig)
        print("    已保存：%s" % gif_path)
    except Exception as exc:
        print("    GIF 动画生成失败（跳过）：", exc)
```