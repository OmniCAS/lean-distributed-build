# 文档

这个目录是独立的文档模块：只读这里和根目录的 `REFERENCES.md`，就能知道问题是什么、业界和别人怎么做、理论上的最优是什么、我们测到了什么、下一步怎么做。代码、数据、基准在仓库的其他目录，文档里的路径都标明了位置。

## 先读哪份

1. **[study-summary.md](study-summary.md)**（一页）：结论和数字——最优算法是什么、离最优多远、什么时候该加机器、什么时候加机器没用、该不该切、线程怎么给、每个仓库的可并行度与预计时长。每条标明实测、精确求解、模拟还是预测。
2. **[problem-and-roadmap.md](problem-and-roadmap.md)**：问题定义（黑箱的输入、输出、目标与约束）、业界的标准解法（远程缓存 + 远程执行）与 Lean 的不同、Lake 的技术事实、证据、目标架构、有了集群以后怎么做、分阶段验收、完整待办与风险。
3. **[scheduling-theory.md](scheduling-theory.md)**：调度理论——标准形式 P | prec | C_max、Graham 界与拐点参数 x、最优性与难度、带通信延迟的粒度、可塑任务、真实系统怎么调度、思想实验与预测；文末是文献核对与修改记录。
4. **[lessons.md](lessons.md)**：实践经验——在真实的三台共用服务器上做多机构建时遇到的现象、原因与对策（路径依赖、无外网时工具链怎么分发、机器快慢、线程开销、启动与每任务开销、预测的对错、一次机器故障的经过）。
5. **[study-report.md](study-report.md)**：研究的完整报告——Mathlib 全量的实测 trace、七个问题（时间、空间、结构上的切，调度规则，线程，估计误差，外推）、离最优多远、三机运行的校准、对调度器实现的建议、局限。

## 别人的做法

| 文档 | 内容 |
|---|---|
| [research/precedents-rh.md](research/precedents-rh.md) | 黎曼猜想 Lean 归档（175,187 个模块）的各次构建：Omega Institute 的分片、MIT 的核验与沙箱重建、几次独立复现 |
| [research/precedents-omega-shards.md](research/precedents-omega-shards.md) | Omega Institute 分片构建脚本的机制（读原文件）：导入图、两轮切片、片键、每片怎么建、调度 |
| [research/precedents-infra.md](research/precedents-infra.md) | Isabelle 的集群构建、Mathlib 的 CI 与缓存、Lake 的产物缓存、Nix 与 Bazel 的 Lean 规则、并行内核重放 |

## 出处

**[../REFERENCES.md](../REFERENCES.md)**：完整书目。正文里的 [T…] 是调度理论的论文，[S…] 是各系统的文档与源码，[D…] 是公开的构建数据；每条标明读了全文、读了相关段落、只读了摘要或未重新核对，文末列出还没找到出处的说法。

## 与其他目录的关系

| 想看 | 去哪 |
|---|---|
| 预期效果（每个实验每一格的预测、容差与实测） | `bench/expected.md` |
| 运行记录 | `bench/results/` |
| 模拟器、实验脚本与结果 | `study/`（`study-report.md` 里的 `sim/…`、`results/…` 等路径都相对于这里） |
| 工具 | `lakeshard/` |
