# lean-distributed-build

**Summary (English).** How to build a large Lean 4 repository on several machines, and how fast that can be. This repository collects a working tool (`lakeshard/`: a coordinator plus pull workers that call `lean` per module, byte-identical to `lake build`), a trace-driven scheduling simulator with tests (`study/`), reproducible benchmarks with predicted and measured results (`bench/`), and the reports behind them (`docs/`), with every external claim tied to a numbered source in `REFERENCES.md`. Main findings: dispatching ready modules by *remaining longest path* is within about 1% of the true optimum (proved with CP-SAT on 89 sub-graphs; Lake's ready-order dispatch is up to 44% slower); adding machines helps only up to about W/CP cores (Mathlib v4.34.0: 12.0 core-hours of work, a 1,184 s critical path, W/CP = 36.6); pre-partitioning the graph never beat dynamic dispatch in our simulations; on three 16-core machines a 4,333-module synthetic build went from 564 s to 249 s, and the simulator, given each machine's measured speed, start time and per-task overhead, predicts such runs within about 8%. The Riemann-hypothesis Lean archive (175,187 modules) is predicted at about 1 hour on 512 to 2,048 cores. The documents are in Chinese.

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
| 用时 | 约 max(最长链, 总工作量 ÷ 总核数) 的 1.0–1.1 倍，外加 worker 启动与每任务开销（见下表） |

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
| 预先切块（按目录、沿导入链、线性聚类） | 一直到传输比模块慢 10 倍都没赢过动态派发 | 模拟 | 3.2 |
| 重文件多线程 | 2 线程 1.44 倍，8 线程 1.47 倍；核紧张时 16 线程比 1 线程多用 25% CPU | 实测 | 3.5 |
| 合成中图（3,156 模块，W/CP 31.7），3 × 16 核 | 单机原版 Lake 733 秒 → 三机 419 秒 | 实测 | `bench/results/` |
| 合成宽图（4,333 模块，W/CP 60），3 × 16 核 | 本工具单机 564 秒 → 三机 249 秒（2.27 倍），产物与 `lake build` 逐字节一致 | 实测 | 同上 |
| 模拟器对三机运行的预测误差（给定机器速度、开工时刻、每任务开销） | −7.0% 到 +7.7%（7 次运行，含单机与三机） | 实测 vs 模拟 | `bench/expected.md` |
| Mathlib 在 8 + 8 + 16 核上 | 21–24 分钟；核再多也约 20 分钟（每文件 2 线程约 14 分钟） | 预测 | `bench/expected.md` E2 |
| 黎曼猜想归档（175,187 模块） | 约 475 核·时，最长链约 0.93 小时；128 核 3.9 小时，512 核 69 分钟，2,048 核 56 分钟 | 预测 | 3.7 |

（“3.x”指 `docs/study-report.md` 的节号。）理论框架与文献核对见 `docs/scheduling-theory.md`；问题定义、业界做法、目标架构与路线图见 `docs/problem-and-roadmap.md`；一页结论见 `docs/study-summary.md`。

## 怎么复现

- **模拟与分析**（只要 Python 3.12 与 uv）：

  ```bash
  cd study
  uv run --with numpy --with pytest --with ortools python -m pytest tests     # 34 个单元测试
  uv run --with numpy python experiments.py q4 data/mathlib.trace.json.gz      # 例：调度规则比较
  uv run --with numpy --with ortools python t1_optimality.py quick             # 例：离最优多远
  uv run --with numpy python t6_calibrate.py                                   # 例：三机运行的回测
  ```

- **合成基准与三机运行**：`bench/README.md`（生成实例、准备机器、运行队列、分析）。
- **Mathlib 全量从源码构建与逐模块计时**：`bench/README.md` 第 4 节。

## 目录

| 位置 | 内容 |
|---|---|
| `docs/problem-and-roadmap.md` | 问题定义、业界的标准解法、Lean 的技术事实、证据、目标架构、集群上怎么做、分阶段验收、待办 |
| `docs/scheduling-theory.md` | 调度理论：标准形式、Graham 界与拐点、最优性与难度、带通信的粒度、可塑任务、真实系统，附文献核对记录 |
| `docs/study-summary.md`、`docs/study-report.md` | 研究结论（一页）与完整报告（七个问题、最优性、校准） |
| `docs/research/` | 别人的做法：黎曼猜想归档的各次构建、Omega Institute 的分片构建、Isabelle 与 Mathlib 的基础设施 |
| `REFERENCES.md` | 完整书目：调度理论 [T…]、系统文档与源码 [S…]、公开的构建数据 [D…]，每条标明读了全文、只读了摘要或未重新核对 |
| `lakeshard/` | 工具快照 |
| `study/` | 模拟器、测试、trace、实验脚本与结果 |
| `bench/` | 基准实例、运行脚本、预期效果、运行记录 |

## 说明

- 机器只用角色名（worker-1、worker-2、worker-3）；运行记录里的主机名与地址已替换。一个 230 模块的私有工程只以编号形式出现（`study/data/p230.trace.json.gz`）。
- 黎曼猜想归档的模块名里有一个四字母词被遮成 `S··d`。
- 第三方内容只引用和链接，不转载。
- 许可：Apache-2.0（`LICENSE`）。
