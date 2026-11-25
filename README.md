# lean-distributed-build

**Summary (English).** How to build a large Lean 4 repository on several machines, and how fast that can be. This repository collects a working tool (`lakeshard/`: a coordinator plus pull workers that call `lean` per module, byte-identical to `lake build`), a trace-driven scheduling simulator with tests (`study/`), reproducible benchmarks with predicted and measured results (`bench/`), and the reports behind them (`docs/`), with every external claim tied to a numbered source in `REFERENCES.md`. Main findings: dispatching ready modules by *remaining longest path* is within about 1% of the true optimum (proved with CP-SAT on 89 sub-graphs; Lake's ready-order dispatch is up to 44% slower); adding machines helps only up to about W/CP cores (Mathlib v4.34.0: 12.0 core-hours of work, a 1,184 s critical path, W/CP = 36.6); pre-partitioning the graph never beat dynamic dispatch in our simulations; on three 16-core machines a 4,333-module synthetic build went from 564 s to 249 s, and the simulator, given each machine's measured speed, start time and per-task overhead, predicts such runs within about 8%. The Riemann-hypothesis Lean archive (175,187 modules) is predicted at about 1 hour on 512 to 2,048 cores. The documents are in Chinese.

> **要在自己的机器上验证？** 按 [`TODO.md`](TODO.md) 的分阶段清单走：每个阶段写明做什么、通过标准和预期数值。

## 这是什么

给一个 Lean 仓库和一组机器，尽快产出它的**构建缓存**（每个模块的编译产物），使别人拿到缓存后不必再编译。这里放三样东西：

1. **工具** `lakeshard/`：协调器 + 常驻 worker。worker 主动领任务，照 Lake 的参数直接调 `lean`，产物与原版 `lake build` 逐字节一致，按内容哈希存进产物库。这是工具仓库某一提交的快照（见 `lakeshard/README.md`）。
2. **研究** `study/`：事件驱动的调度模拟器（机器快慢、开工时刻、每任务开销、跨机传输、线程、估计误差）、下界与精确求解、实测 trace（Mathlib 全量、合成工程、黎曼猜想归档的导入图），以及回答“怎么切、怎么派”的全部实验脚本与结果。
3. **基准** `bench/`：可重新生成的合成实例、真实仓库的钉住版本、运行脚本、每一格的**预期值与容差**（`bench/expected.md`）和已完成运行的逐模块记录。

## 黑箱：输入、输出、用时

| | 内容 |
|---|---|
| 输入 | 一个 Lean 仓库（Git 地址 + 提交号）及其锁定的依赖；一组机器（核数、内存、网络） |
| 输出 | 构建缓存（产物按内容哈希存放 + 清单）与运行报告（每个模块在哪台机器、起止、CPU、内存） |
| 用时 | 约 max(最长链, 总工作量 ÷ 总核数) 的 1.05–1.25 倍（拐点附近取上端），外加 worker 启动与每任务开销（见下表） |

## 结果

标记：**实测**（机器上量的）、**精确**（求解器证明的最优）、**模拟**（实测 trace 驱动的模拟器）、**预测**（模型外推，待验证）。

| 结论 | 数字 | 标记 | 出处 |
|---|---|---|---|
| Mathlib v4.34.0 全量的工作量、最长链、可并行度 | 12.0 核·时，1,184 秒，W/CP = 36.6 | 实测 | `docs/study-report.md` 2.1 |
| Mathlib 单机 16 核原版 `lake build` | 47.7 分钟，是下界的 1.058 倍 | 实测 | 同上 |
| “剩余最长链优先”离真正的最优 | 平均 0.5%–1.1%，最坏 3.9%（89 个证明了最优的子图） | 精确 | 3.8 |
| 整个合成工程 4 核：最优与剩余最长链优先 | 383.1 秒对 383.3 秒 | 精确 | 3.8 |
| Lake 那样“先就绪先派” | 拐点处慢 18%–24%，最坏 44% | 模拟、精确 | 3.4、3.8 |
| 预先算好的静态计划，耗时估计误差 σ = 0.3 时 | 慢 24%–35% | 模拟 | 3.6 |
| 预先切块（按目录、沿导入链、线性聚类） | 对看数据所在、产物建完即推送的动态派发：一直到传输比模块慢 10 倍都没赢过（模拟）。工具现在的派发不看数据所在、开工时才取件：两机宽图每次取件多等 10 秒时，动态派发 894 秒、按目录切块 580 秒，切块快 35%；多等 1 秒时动态仍快 8%（406 对 440 秒） | 模拟；实测 | 3.2、4.4 |
| 模拟器补上“按需拉取”后回测上面的取件延迟 | 动态派发 −5.1% 到 −0.4%，按目录切块 −9.9% 到 −3.9%；原模型在 10 秒那格低估 41% | 实测 vs 模拟 | 4.4 |
| 补上看数据所在的派发（预取 + 延迟调度），两机宽图 | 每次取件多等 1 秒：359 秒（现在 409）；10 秒：467 秒（现在 861，按目录切块 518） | 预测 | 4.4 |
| 重文件多线程 | 2 线程 1.44 倍，8 线程 1.47 倍；核紧张时 16 线程比 1 线程多用 25% CPU | 实测 | 3.5 |
| 合成中图（3,156 模块，W/CP 31.7），3 × 16 核 | 单机原版 Lake 733 秒 → 三机 419 秒 | 实测 | `bench/results/` |
| 合成宽图（4,333 模块，W/CP 60），3 × 16 核 | 原版 Lake 570 秒、本工具单机 564 秒 → 三机 249 秒（对 Lake 2.29 倍），12,999 个产物文件与 `lake build` 逐字节一致 | 实测 | 同上 |
| 同上，三机换派发方式 | 先就绪先派 290 秒（慢 17%），只按图结构排优先级 273 秒（慢 10%），按目录预先固定放置 327 秒（慢 31%） | 实测 | 同上 |
| 模拟器对实测运行的预测误差（给定机器速度、开工时刻、每任务开销） | −7.0% 到 +7.7%（9 次运行，含单机与三机）；派发方式之间的比值，预测与实测相差 0.04–0.05 | 实测 vs 模拟 | `bench/expected.md` |
| Mathlib 在 8 + 8 + 16 核上 | 21–24 分钟；核再多也约 20 分钟（每文件 2 线程约 14 分钟） | 预测 | `bench/expected.md` E2 |
| 黎曼猜想归档（175,187 模块） | 约 475 核·时，最长链约 0.93 小时；128 核 3.9 小时，512 核 69 分钟，2,048 核 56 分钟 | 预测 | 3.7 |
| Tau Ceti（34,760 模块，中间台阶） | 约 57 核·时，最长链 8–17 分钟，可并行度约 200–450；32 核 1.8 小时，128 核 27 分钟，512 核 8–17 分钟 | 预测 | 3.7 |
| 合成宽图、窄图，2 × 4 / 8 / 16 核（一台机器的根盘掉线后改用两台） | 两机对单机：宽图 1.87–1.95 倍（预测 2.04–2.11），窄图 1.00–1.28 倍（预测 1.03–1.26）；16 核时先就绪先派慢 23%，只按图结构慢 7%，按目录预先固定放置慢 18%，沿导入链预先固定放置持平；每次跨机取产物多等 1 秒慢 13%（预测 1%） | 实测 | `bench/expected.md` |
| 同上，模拟器的绝对时长误差 | 沿用上一批的机器速度：18 格中 8 格出容差（一台机器变快了）；按每次运行当场量的速度重算：宽图不加延迟的 11 格 −8.4% 到 +4.1% | 实测 vs 模拟 | 同上 |
| 原版 Lake 调度、只把 `lean` 转发到两台（构建目录在共享盘上），宽图 2 × 16 核 | 909 秒：比本工具两机 359 秒慢 2.5 倍，比本工具单机 671 秒还慢 35%；每个 `lean` 经共享盘读导入多约 1 秒，总工作量多 54%；32 个槽平均只有 17 个在跑 | 实测 | `docs/lessons.md` 第 12 节 |
| 整个 Mathlib，本工具，2 × 16 核对单机 16 核 | 两机 26.8 分钟、单机 45.2 分钟，1.69 倍；比预测（约 19、40 分钟）慢 41%、13%。根模块 `Mathlib` 开工前逐个文件取 7,525 个文件用了 250 秒，其余模块 22.5 分钟建完。根因：HTTP 服务没关 Nagle，每次请求约 40 毫秒（已修，0.8 毫秒），重测在跑 | 实测 | `bench/expected.md`、`docs/lessons.md` 第 13、14 节 |
| 同一台机器上的原版 `lake build`（16 线程） | Mathlib 46.3 分钟、宽图 697 秒：本工具两机对它 1.73 倍、1.94 倍；本工具单机与它基本持平（2,713 对 2,775 秒；671 对 697 秒），预测的“单机快 15%–20%”没有出现，因为整个构建上 1 线程只省 5%，又被上传开销抵掉 | 实测 | 4.6 |
| Mathlib 两机先就绪先派 | 1,766 秒，比剩余最长链优先慢 10%（除根模块外慢 12.6%，预测 15%） | 实测 | 4.6 |
| 产物逐字节核对（两机） | 宽图 12,999 / 12,999，窄图 7,839 / 7,839，Mathlib 59,707 / 59,710；不同的 3 个文件属于一个原版 Lean 自己编两次就不同的模块 | 实测 | `docs/lessons.md` 第 15 节 |
| 同上，把逐个取件、1 线程只省 7%、每任务上传 0.37 秒建进模型 | 两机 1,610 秒（实测 1,606），单机 2,704 秒（实测 2,713）；修 Nagle 后预计两机 20.5 分钟、单机 42.3 分钟 | 实测 vs 模拟；预测 | 4.5、4.6 |
| 黎曼猜想归档的顶端模块（各导入 15 万个以上的模块），512 核 | 修 Nagle 之前每个文件一次请求，每个多等 0.7–10 小时（整个构建预计 69 分钟）；修后逐个请求 3.5–15 分钟；成批取 11 秒到 4.6 分钟；建完即推送接近 0 | 推断 | 4.5 |
| 阶段 1“仓库进、缓存出”，公开仓库 PFR（76 个模块，单机） | 516/516 个产物文件与原版 `lake build` 逐字节一致；在另一路径的全新检出上恢复 1,108 个文件后原版 Lake 编译 0 个；中途杀掉后同一条命令复用 41 个、新建 35 个；改一个文件只重建 4 个（21.0 秒） | 实测 | `bench/README.md` 第 5 节、`bench/results/step1-pfr/` |

（“3.x”指 `docs/study-report.md` 的节号。）**文档是独立的模块，从 [`docs/README.md`](docs/README.md) 开始读**：一页结论、问题定义与路线图、调度理论、完整报告、别人的做法，以及出处 [`REFERENCES.md`](REFERENCES.md)。

## 关联的实验仓库

OmniCAS 下的 fork，版本钉死在下表的提交上（细节与用途见 `bench/README.md` 第 4 节）：

| 仓库 | 钉住的版本 | 用途 |
|---|---|---|
| [`OmniCAS/mathlib4`](https://github.com/OmniCAS/mathlib4) | `v4.34.0`（`5ed29652…`） | E2：真实仓库的三机构建；本仓库 Mathlib trace 的版本 |
| [`OmniCAS/carleson`](https://github.com/OmniCAS/carleson) | `f7487cc9…`（工具链 v4.36.0-rc1） | 小仓库一档：125 个模块，只验正确性 |
| [`OmniCAS/pfr`](https://github.com/OmniCAS/pfr) | `1ef23c3c…`（工具链 v4.36.0-rc2；验证过的修订，fork 上更新的提交没验证） | 小仓库一档：76 个模块，阶段 1 已通过 |
| [`OmniCAS/riemann-hypothesis`](https://github.com/OmniCAS/riemann-hypothesis) | 原始提交 `40e56bab…` | E4：大集群；导入图与合成实例的结构来源 |
| [`OmniCAS/riemann-hypothesis-omega`](https://github.com/OmniCAS/riemann-hypothesis-omega) | `c7d25b3b…` | 参考实现：Omega Institute 按内容哈希分片构建的脚本 |
| [`OmniCAS/CFSG`](https://github.com/OmniCAS/CFSG) | `965a0775…` | E4 之后 |
| [`OmniCAS/TauCeti`](https://github.com/OmniCAS/TauCeti) | `5d7b2806…` | RH 之前的中间台阶：模型预测 W ≈ 57 核·时、可并行度约 200–450、128 核约 27 分钟（预测） |
| [`OmniCAS/Weil`](https://github.com/OmniCAS/Weil) | `27cdb204…` | 候选，按行数估的可并行度约 25 |

除 Mathlib 外都是第三方代码（多为 AI 生成的形式化），**只在隔离环境里构建**。

## 怎么复现

- **模拟与分析**（只要 Python 3.12 与 uv）：

  ```bash
  cd study
  uv run --with numpy --with pytest --with ortools python -m pytest tests     # 34 个单元测试
  uv run --with numpy python experiments.py q4 data/mathlib.trace.json.gz      # 例：调度规则比较
  uv run --with numpy --with ortools python t1_optimality.py quick             # 例：离最优多远
  uv run --with numpy python t6_calibrate.py                                   # 例：三机运行的回测
  ```

- **合成基准与三机运行**：`bench/README.md`（准备机器、运行队列、分析）；三个实例的工程已生成好，在 `bench/instances/`。
- **Mathlib 全量从源码构建与逐模块计时**：`bench/README.md` 第 4 节。

## 目录

| 位置 | 内容 |
|---|---|
| `docs/README.md` | 文档索引：每份讲什么、先读哪份 |
| `docs/lessons.md` | 实践经验：在真实机器上做多机构建遇到的现象、原因与对策 |
| `docs/problem-and-roadmap.md` | 问题定义、业界的标准解法、Lean 的技术事实、证据、目标架构、集群上怎么做、分阶段验收、待办 |
| `docs/scheduling-theory.md` | 调度理论：标准形式、Graham 界与拐点、最优性与难度、带通信的粒度、可塑任务、真实系统，附文献核对记录 |
| `docs/study-summary.md`、`docs/study-report.md` | 研究结论（一页）与完整报告（七个问题、最优性、校准） |
| `docs/research/` | 别人的做法：黎曼猜想归档的各次构建、Omega Institute 的分片构建、Isabelle 与 Mathlib 的基础设施 |
| `REFERENCES.md` | 完整书目：调度理论 [T…]、系统文档与源码 [S…]、公开的构建数据 [D…]，每条标明读了全文、只读了摘要或未重新核对 |
| `lakeshard/` | 工具快照（工具仓库提交 `e408d78`，阶段 1 验收用的版本） |
| `study/` | 模拟器、测试、trace、实验脚本与结果 |
| `bench/` | 基准实例（规格、生成脚本、生成好的工程）、运行脚本、预期效果、运行记录 |

## 说明

- 机器只用角色名（worker-1、worker-2、worker-3）；运行记录里的主机名与地址已替换。一个 230 模块的私有工程只以编号形式出现（`study/data/p230.trace.json.gz`）。
- 黎曼猜想归档的模块名里有一个四字母词被遮成 `S··d`。
- 第三方内容只引用和链接，不转载。
- 许可：Apache-2.0（`LICENSE`）。
