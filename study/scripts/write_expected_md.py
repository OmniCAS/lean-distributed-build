"""Write bench/expected.md of the public repository from results/e1-expected.json (E1 table and
measured-vs-predicted ratios) plus the fixed E2-E4 sections. Re-run after every new batch:
  uv run --with numpy python e1_expected.py && python scripts/write_expected_md.py DEST_REPO
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
DEST = sys.argv[1]
d = json.load(open(os.path.join(STUDY, "results", "e1-expected.json")))
cells = {c["run"]: c for c in d["cells"]}
DESC = {"A0": "单机原版 `lake build`", "A1": "本工具单机", "B1": "本工具三机，剩余最长链优先", "B1s": "三机，只按图结构排优先级",
        "B4": "三机，先就绪先派（FIFO）", "B2": "三机，按目录预先固定放置", "B3": "三机，沿导入链预先固定放置"}

rows = []
for c in d["cells"]:
    code = c["run"].split("-")[1]
    extra = f"，每次取产物人为加 {c['run'].split('-d')[1]} 秒" if "-d" in c["run"] else ""
    meas = f"{c['measured_s']:.0f}" if c.get("measured_s") else "待测"
    err = f"{c['error_pct']:+.1f}%" if c.get("error_pct") is not None else ""
    rows.append(f"| `{c['run']}` | {c['inst']} | {DESC.get(code, code)}{extra} | {c['c']} | {c['predicted_s']:.0f} | "
                f"{c['band_s'][0]:.0f}–{c['band_s'][1]:.0f} | {meas} | {err} |")
measured = [c for c in d["cells"] if c.get("measured_s")]
errs = [c["error_pct"] for c in measured]
inside = sum(1 for c in measured if c.get("within_band"))


def ratio(a, b):
    ca, cb = cells.get(a), cells.get(b)
    if not ca or not cb:
        return None
    pr = ca["predicted_s"] / cb["predicted_s"]
    me = ca["measured_s"] / cb["measured_s"] if ca.get("measured_s") and cb.get("measured_s") else None
    return pr, me


RATIOS = [("单机 ÷ 三机（宽图 16 核，加速比）", "wide-A1-c16-r1", "wide-B1-c16-r1"),
          ("单机 ÷ 三机（中图 16 核）", "mid-A1-c16-r1", "mid-B1-c16-r1"),
          ("先就绪先派 ÷ 剩余最长链（宽图三机 16 核）", "wide-B4-c16-r1", "wide-B1-c16-r1"),
          ("只按图结构 ÷ 按耗时（宽图三机 16 核）", "wide-B1s-c16-r1", "wide-B1-c16-r1"),
          ("按目录固定放置 ÷ 动态派发（宽图三机 16 核）", "wide-B2-c16-r1", "wide-B1-c16-r1"),
          ("沿导入链固定放置 ÷ 动态派发（宽图三机 16 核）", "wide-B3-c16-r1", "wide-B1-c16-r1"),
          ("单机 ÷ 三机（宽图 8 核）", "wide-A1-c8-r1", "wide-B1-c8-r1"),
          ("单机 ÷ 三机（宽图 4 核）", "wide-A1-c4-r1", "wide-B1-c4-r1"),
          ("单机 ÷ 三机（窄图 16 核）", "narrow-A1-c16-r1", "narrow-B1-c16-r1"),
          ("单机 ÷ 三机（窄图 4 核）", "narrow-A1-c4-r1", "narrow-B1-c4-r1")]
rrows = []
for name, a, b in RATIOS:
    r = ratio(a, b)
    if r:
        rrows.append(f"| {name} | {r[0]:.2f} | {'%.2f' % r[1] if r[1] else '待测'} |")

inst = d["instances"]
two_path = os.path.join(STUDY, "results", "e1-two-machines.json")
TWO = ""
if os.path.exists(two_path):
    two = json.load(open(two_path))
    D2 = {"A0": "单机原版 `lake build`（worker-2）", "A1": "本工具单机（worker-2）", "B1": "本工具两机，剩余最长链优先",
          "B4": "两机，先就绪先派", "B1s": "两机，只按图结构", "B2": "两机，按目录固定放置", "B3": "两机，沿导入链固定放置"}
    lines_ = ["| 运行 | 实例 | 做法 | 每台核数 | 预测 | 容差带 | 实测 | 误差 |", "|---|---|---|---:|---:|---:|---:|---:|"]
    for r in two:
        code = r["run"].split("-")[1]
        extra = f"，每次取产物人为加 {r['run'].split('-d')[1]} 秒" if "-d" in r["run"] else ""
        u, unit = (60.0, "分钟") if r["inst"] == "mathlib" else (1.0, "秒")
        meas = f"{r['measured_s'] / u:.0f} {unit}" if r.get("measured_s") else "待测"
        err = f"{r['error_pct']:+.1f}%" if r.get("error_pct") is not None else ""
        lines_.append(f"| `{r['run']}` | {r['inst']} | {D2.get(code, code)}{extra} | {r['c']} | {r['predicted_s'] / u:.0f} {unit} | "
                      f"{r['band_s'][0] / u:.0f}–{r['band_s'][1] / u:.0f} {unit} | {meas} | {err} |")
    pr = {r["run"]: r["predicted_s"] for r in two}
    me = {r["run"]: r["measured_s"] for r in two if r.get("measured_s")}
    done = [r for r in two if r.get("measured_s")]
    n_in = sum(1 for r in done if r.get("within_band"))

    def q(a, b, src):
        return f"{src[a] / src[b]:.2f}" if a in src and b in src else "待测"
    R2 = [("单机 ÷ 两机（宽图 16 核，加速比）", "wide2-A1-c16-r1", "wide2-B1-c16-r1"),
          ("单机 ÷ 两机（宽图 8 核）", "wide2-A1-c8-r1", "wide2-B1-c8-r1"),
          ("单机 ÷ 两机（宽图 4 核）", "wide2-A1-c4-r1", "wide2-B1-c4-r1"),
          ("单机 ÷ 两机（窄图 16 核）", "narrow2-A1-c16-r1", "narrow2-B1-c16-r1"),
          ("单机 ÷ 两机（窄图 4 核）", "narrow2-A1-c4-r1", "narrow2-B1-c4-r1"),
          ("先就绪先派 ÷ 剩余最长链（宽图两机 16 核）", "wide2-B4-c16-r1", "wide2-B1-c16-r1"),
          ("先就绪先派 ÷ 剩余最长链（宽图两机 4 核）", "wide2-B4-c4-r1", "wide2-B1-c4-r1"),
          ("只按图结构 ÷ 按耗时（宽图两机 16 核）", "wide2-B1s-c16-r1", "wide2-B1-c16-r1"),
          ("按目录固定放置 ÷ 动态派发（宽图两机 16 核）", "wide2-B2-c16-r1", "wide2-B1-c16-r1"),
          ("沿导入链固定放置 ÷ 动态派发（宽图两机 16 核）", "wide2-B3-c16-r1", "wide2-B1-c16-r1"),
          ("每次取产物加 0.1 秒 ÷ 不加（宽图两机 16 核）", "wide2-B1-c16-d0.1", "wide2-B1-c16-r1"),
          ("每次取产物加 1 秒 ÷ 不加（宽图两机 16 核）", "wide2-B1-c16-d1", "wide2-B1-c16-r1"),
          ("每次取产物加 10 秒 ÷ 不加（宽图两机 16 核）", "wide2-B1-c16-d10", "wide2-B1-c16-r1"),
          ("单机 ÷ 两机（Mathlib 16 + 16 核）", "mathlib2-A1-c16-r1", "mathlib2-B1-c1616-r1")]
    rtab = ["| 比较 | 预测 | 实测 |", "|---|---:|---:|"] + [f"| {n} | {q(a, b, pr)} | {q(a, b, me)} |" for n, a, b in R2]
    bt_path = os.path.join(STUDY, "results", "e1-delay-backtest.json")
    BT = ""
    if os.path.exists(bt_path):
        bt = json.load(open(bt_path))["backtest"]
        dl = [x for x in bt if x["delay_s"] > 0]
        BT = ("加延迟的格：同样按当场速度重算，但仍用“产物建完即推送、派发看数据所在”的模型，误差 " +
              "、".join(f"{x['dispatch']} {x['delay_s']:g} 秒 {x['push-est']['error_pct']:+.1f}%" for x in dl) +
              "。工具其实是派发不看数据所在、每个任务开工时才取件；按这个做法回测（`python e1_delay_backtest.py`）误差 " +
              "、".join(f"{x['pull-blind']['error_pct']:+.1f}%" for x in dl) +
              "，要取件的任务数也对得上（模拟 " + "、".join(f"{x['pull-blind']['fetch_tasks']:,}" for x in dl) +
              "，实测 " + "、".join(f"{x['measured_fetch_tasks']:,}" for x in dl) + "）。B1 是动态派发，B2 是按目录固定切分。细节与对策见 `docs/study-report.md` 4.4 节。")
    rec_path = os.path.join(STUDY, "results", "e1-two-machines-recalibrated-wide.json")
    REC = ""
    if os.path.exists(rec_path):
        rec = json.load(open(rec_path))
        e = [x["error_pct"] for x in rec if "-d" not in x["run"]]
        ed = [(x["run"].split("-d")[1], x["error_pct"]) for x in rec if "-d" in x["run"]]
        s2 = [x["speed_vs_reference"][0] for x in rec]
        s3 = [x["speed_vs_reference"][1] for x in rec if x["run"].split("-")[1].startswith("B")]
        REC = (f"\n\n**校准**：这批运行里 worker-2 只比参考机慢 {min(s2):.2f}–{max(s2):.2f} 倍（校准时是 1.438；两批记录的系统负载相近，变快的原因不明），"
               f"worker-3 {min(s3):.2f}–{max(s3):.2f} 倍（原 1.122）。按每次运行自身记录里量出的速度重算（`python e1_two_machines.py --recalibrate`），"
               f"宽图不加延迟的 {len(e)} 格误差是 {min(e):+.1f}% 到 {max(e):+.1f}%：模型本身没问题，偏差来自机器速度变了。"
               + BT +
               "所以每次运行前都要当场量一次每台机器的速度。窄图的逐模块耗时来自 macOS，不能这样校准，只看比值。")
    mb_path = os.path.join(STUDY, "results", "e1-mathlib-backtest.json")
    MB = ""
    if os.path.exists(mb_path):
        mb = json.load(open(mb_path))
        me_, tw = mb["measured"], mb["two_machines"]
        tool = tw["on demand, one request per file (the tool)"]
        fix = tw["on demand, one batched request per task (33 ms + bytes at 1.1 GB/s)"]
        MB = (f"\n\n**Mathlib**：本工具单机 {me_['one_machine_s'] / 60:.1f} 分钟，两机 {me_['two_machines_s'] / 60:.1f} 分钟（{me_['one_machine_s'] / me_['two_machines_s']:.2f} 倍），"
              f"比预测慢 {100 * (me_['two_machines_s'] / pr['mathlib2-B1-c1616-r1'] - 1):.0f}%。除根模块 `Mathlib` 外 {me_['two_machines_all_but_root_s']:,.0f} 秒建完；"
              f"根模块逐个文件取了 {me_['root_fetched_files']:,} 个文件，用了 {me_['root_fetch_s']:.0f} 秒。"
              f"另外 1 线程 `lean` 只省 7%（0.93 倍，预测用 0.86），每任务开销 {mb['params']['task_overhead_s']:.2f} 秒（预测用 0.21）。"
              f"把这些建进模型（`python e1_mathlib_backtest.py`）：两机 {tool['makespan_if_root_on_hub_s']:,.0f} 秒，"
              f"除根模块外 {tool['all_but_root_s']:,.0f} 秒；单机 {mb['one_machine']['simulated_s']:,.0f} 秒。"
              f"改成每任务一次成批取，预计 {fix['makespan_s']:,.0f} 秒（{fix['makespan_s'] / 60:.1f} 分钟，{me_['one_machine_s'] / fix['makespan_s']:.2f} 倍），修好后重测。"
              "细节见 `docs/study-report.md` 4.5 节。")
    TWO = ("\n".join(lines_) + f"\n\n已测 {len(done)} 格，{n_in} 格在容差带内。\n\n" + "\n".join(rtab) + REC + MB +
           "\n\n说明：单机运行放在 worker-2 上（协调器也在那里）。`wide2-B5`（原版 Lake 调度、只把 `lean` 转发出去）没有模型，没给预测；实测 909 秒，比本工具两机慢 2.5 倍、比本工具单机还慢 35%，原因见 `docs/lessons.md` 第 12 节。"
           "Mathlib 的单机原版 Lake 就在本研究量 trace 的那台机器上，预测即那次实测的复现（47.7 分钟）；本工具每个 `lean` 1 线程，按 Mathlib 文件实测的 0.86 倍计。")
doc = f"""# 预期效果：实验 E1–E4 每一格的预期值、容差与当前实测

标记：**预测**（模拟器 + 校准参数，在运行之前给出）、**实测**（`bench/results/` 里的运行记录）。预测怎么算的见 `study/e1_expected.py`、`study/q7_extrapolate.py`、`study/rh_import_sensitivity.py`；校准见 `docs/study-report.md` 第 4.2 节。本文件由 `study/scripts/write_expected_md.py` 生成，每来一批新结果重新生成一次。

## 预测用到的参数（都在运行之前就能量）

| 参数 | 值 | 来源 |
|---|---|---|
| 每个实例的逐模块耗时 | 该实例单机原版 `lake build`（A0）的逐模块秒数 | 实测 |
| 三台机器相对 A0 所在机器的速度 | worker-1 1.022，worker-2 1.438，worker-3 1.122 倍耗时 | 实测（中图三机运行；宽图上为 1.033 / 1.383 / 1.134，一致） |
| 各 worker 开始干活的时刻 | 13.0、22.4、29.3 秒（单机运行 14.6 秒） | 实测 |
| 每任务在编译之外的开销 | 三机 0.21 秒，单机 0.044 秒 | 实测 |
| 同一机器上两次运行之间每模块耗时的随机差异 | 对数标准差 0.12 | 实测（0.11–0.14） |

每一格跑 10 次带随机差异的模拟，**预测 = 中位数，容差带 = 5%–95% 分位，且至少 ±15%**（一次受最长链限制的运行本身就有这么大的起伏）。

## E1 合成仓库（机制）

三个实例，生成好的工程在 `bench/instances/`，规格与生成命令见 `bench/README.md`：

| 实例 | 模块 | 总工作量 W（A0 实测） | 最长链 CP（A0 实测） | 可并行度 W/CP |
|---|---:|---:|---:|---:|
| mid（中图） | {inst['mid']['modules']:,} | {inst['mid']['W_s']:,.0f} 秒 | {inst['mid']['CP_s']:.0f} 秒 | {inst['mid']['W_s'] / inst['mid']['CP_s']:.1f} |
| wide（宽图） | {inst['wide']['modules']:,} | {inst['wide']['W_s']:,.0f} 秒 | {inst['wide']['CP_s']:.0f} 秒 | {inst['wide']['W_s'] / inst['wide']['CP_s']:.1f} |
| narrow（窄图，反例） | {inst['narrow']['modules']:,} | {inst['narrow']['W_s']:,.0f} 秒（macOS 上的数，仅作相对比较） | {inst['narrow']['CP_s']:.0f} 秒 | {inst['narrow']['W_s'] / inst['narrow']['CP_s']:.1f} |

| 运行 | 实例 | 做法 | 每台核数 | 预测（秒） | 容差带（秒） | 实测（秒） | 误差 |
|---|---|---|---:|---:|---:|---:|---:|
""" + "\n".join(rows) + f"""

已测 {len(measured)} 格，{inside} 格在容差带内，误差 {min(errs):+.1f}% 到 {max(errs):+.1f}%。三机运行的预测一贯偏慢 4%–8%，单机运行的误差在 ±7% 以内。

**比值**（比值比绝对时长更能检验结论；预测与实测都按上表的中位数 / 实测值相除）：

| 比较 | 预测 | 实测 |
|---|---:|---:|
""" + "\n".join(rrows) + """

说明：
- 宽图三机的产物与单机原版 `lake build` 逐字节一致（12,999 / 12,999 个文件，实测）。
- 窄图（反例）预测**三机比单机还慢**，因为模块平均只有 0.44 秒，而三机时每任务多 0.21 秒开销、两台机器更慢、开工更晚。这是一个可以被实测否定的预测；窄图的逐模块耗时来自 macOS，绝对值仅供参考。
- B2、B3（预先固定放置）的预测用的是 `study/sim/partition.py` 里的划分近似（按目录第 3 层 / 沿导入链贪心），与工具实际生成的划分文件不完全相同。
- 加延迟的几格：每次跨机取产物多等 0.1 / 1 / 10 秒。预测 0.1 秒、1 秒几乎无影响；10 秒时动态派发变慢，沿链固定放置反而占优（只有在这么慢的网络上预先聚类才划算）。这些预测用的是“产物建完即推送、派发看数据所在”的模型；两机实测表明它低估了工具按需取件的代价（下一节）。

## 两台机器（进行中）

worker-1 的根盘掉线后（经过见 `docs/lessons.md` 第 10 节），实验改在 worker-2、worker-3 两台上继续，队列共 27 个运行（宽图 16、8、4 核，窄图，两种预先切块，加延迟，原版 Lake 加转发，Mathlib 16 + 16 核）。协调器、产物库和所有单机运行都在 worker-2 上（worker-3 不接受连入）。预测参数同上（worker-2 1.438、worker-3 1.122 倍耗时；Mathlib 的 trace 本来就在 worker-2 上量，worker-3 比它快 1.28 倍），由 `study/e1_two_machines.py` 按队列逐个运行算出，都在运行之前给出。

""" + TWO + """

## E2 Mathlib 全量（真实仓库）

| 配置 | 预测 | 容差 | 实测 |
|---|---:|---:|---:|
| 单机 16 核原版 `lake build`（Mathlib v4.34.0） | — | — | **47.7 分钟**（2,863 秒） |
| 三机 8 + 8 + 16 核，剩余最长链优先，每个 `lean` 1 线程 | 21–22 分钟（另两台按 E1 实测快 1.28、1.41 倍）；24 分钟（若只按主频快 1.06 倍） | ±15% | 待测 |
| 同上，先就绪先派（FIFO） | 25–29 分钟 | ±15% | 待测 |
| 32 核以上任意多核（单线程） | 约 20 分钟（最长链 1,184 秒） | ±15% | — |
| 核富余时每个文件 2 线程 | 约 14 分钟 | ±20% | — |

## E3 缓存（复用）

| 检查 | 预期 | 实测 |
|---|---|---|
| 三机产物与单机原版 Lake 逐字节一致 | 一致 | 宽图：12,999 / 12,999 个文件一致 |
| 把缓存恢复进全新检出后，原版 `lake build` | 不重新编译任何模块 | 待测 |
| 改一个文件后增量构建 | 只重建它的下游；时长与下游的最长链和工作量成正比 | 待测 |

## E4 大集群（黎曼猜想归档，之后 CFSG）

预测（模型用 Mathlib 校准，每个文件的固定导入开销 F 取单核实测 6.1 秒；容差 ±30%，即路线图第四步的验收标准）：

| 核数 | 预测时长 | F = 2 秒 | F = 8 秒 |
|---:|---:|---:|---:|
| 128 | 3.9 小时 | 2.4 小时 | 4.7 小时 |
| 512 | 69 分钟 | 47 分钟 | 80 分钟 |
| 2,048 | 56 分钟 | 47 分钟 | 61 分钟 |

总工作量 476 核·时（F = 2 / 4 / 8 秒时 276 / 373 / 568 核·时），最长链 0.93 小时，可并行度约 510。CFSG 没有模型，需先做分析（W、CP）。
"""
open(os.path.join(DEST, "bench", "expected.md"), "w").write(doc)
print("wrote", os.path.join(DEST, "bench", "expected.md"), len(measured), "measured cells")
