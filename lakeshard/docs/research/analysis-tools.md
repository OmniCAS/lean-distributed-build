# 多机构建前的仓库分析：工具与数据源（Lean 4 / Lake）

调研日期：搜索结果显示的“当前”日期约为 2026-10。标注规则：
- 【已核】：本次打开过原页面，并核对了相关段落。
- 【仅见摘要】：只看到搜索引擎摘要，没打开原页面。
- 【未找到】：查过，但没找到出处。
- 【推断】：没有出处，是我的推断。
- 所有英文引文都不超过 15 个词。

---

## 1. 导入图

**import-graph 包（`lake exe graph`）**
- 用法：`lake exe graph --to MyModule my_graph.pdf`。还可以写成 `--from A,B --to C,D`，只看一段上下游子图。【已核】https://github.com/leanprover-community/import-graph
- 输出格式由文件扩展名决定：
  - 默认输出 `.dot`。
  - 其他格式（如 `.pdf`）需要装 graphviz。
  - 要 JSON 就用 `.xdot_json`，原文是 "you can use `.xdot_json` as output type"。
  - `.html` 会生成单文件的交互式可视化页面。【已核】同上
- 使用前要先 `lake build`（或至少构建 `--to` 指定的模块），因为它读的是已构建的环境。【已核】同上
- 提供不需要先构建的版本：`ImportGraph.Imports.FromSource` 直接解析源文件头，有两个函数：
  - `findImportsFromSource`：取直接导入；
  - `findTransitiveImportsFromSource`：取传递闭包。

  原文称这是 "without requiring a built environment"。【已核】同上
- 其他工具：
  - `#redundant_imports`、`#min_imports`、`#import_diff`；
  - `lake exe unused_transitive_imports`。【已核】同上
- 早期 Mathlib 版本的示例里有 `--reduce`（传递约简）。【仅见摘要】见一个镜像仓库：https://plmlab.math.cnrs.fr/nuccio/mathlib4/-/blob/fb3066b37f41be9cdc794eb435bc2d2d36b9e853/Mathlib/Util/Imports.lean 。当前版本的完整参数表（`--help`）本次没能打开 `MainGraph.lean` 核对（请求被限流）。
- 对大仓库的性能：【未找到】没有公开的基准。

**Lake 自身**
- `lake query [targets...]`：
  - Lean 4.17.0 加入（#6323），会构建目标并输出结果，`--json`/`-J` 输出 JSON。【已核】https://lean-lang.org/doc/reference/latest/releases/v4.17.0/
  - 参考手册说明：没有配置输出的目标会打印空串或 `null`。【已核】https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/
- 模块 facet（可以写成 `Mod:facet` 的形式交给 query/build）包括：
  - `deps`、`imports`（只含直接导入）、`transImports`、`allImports`；
  - `header`、`depHash`、`depTrace`、`olean`、`c`、`o` 等。【已核】同上手册

  每个 facet 在 `lake query --json` 下具体输出什么，本次没有核对。【推断】可能需要实测，看 `imports` 会不会输出模块名数组。
- `lake build --json` 实际上不生效。lean4 issue #15139 的原文："only `lake query` honors it"。这个 RFC 提议让 `lake build --json` 每条日志输出一个 JSON 对象，目前还只是提议。【已核】https://github.com/leanprover/lean4/issues/15139
- `lake build -v`：手册的说明是 "Shows trace logs (typically command invocations) and built targets"。`--log-level=trace` 的效果相同。【已核】Lake 手册
- trace 文件：
  - 每个产物有一个 trace 文件，记录输入哈希的 Merkle 混合值；
  - 同时保存该任务的日志，增量构建时会回放。【已核】Lake 手册
- Lean 命令行：4.17.0 新增 `--src-deps`，与 `--deps` 对应，解析文件头后输出传递导入的源文件路径。不经过 Lake 也能拿到依赖。【已核】v4.17.0 发布说明

## 2. 构建耗时

**Lake 输出里的逐模块耗时**
- Lean 4.23.0（#9677）开始，构建监视器在每个构建步骤后显示耗时，只在 `-v` 或 CI 环境下显示。【仅见摘要】https://lean-lang.org/doc/reference/latest/releases/v4.23.0/
- 输出格式示例：`✔ [1/6] Built A (264ms)`，较长的会显示为秒，如 `(12s)`。【仅见摘要】https://github.com/leanprover/lean4/issues/15435
- Lake API 中 Job 有一个 `buildTime` 字段，原文是 "How long the job spent building (in milliseconds)"。【仅见摘要】https://lean-lang.org/doc/api/Lake/Build/Job/Basic.html
- 注意：增量构建时会出现 `Replayed` 行，这些行不代表真实编译耗时。这一点来自第三方 issue。【仅见摘要】

**Lean 自带的 profiler**
- `trace.profiler` 的作用是激活执行时间超过 `trace.profiler.threshold` 的嵌套 trace。【仅见摘要】https://github.com/leanprover/lean4/blob/master/src/Lean/Util/Trace.lean
- Lean 4.8.0 新增 `trace.profiler.output`，可以导出成 Firefox Profiler 能打开的格式。【仅见摘要】https://lean-lang.org/blog/2024-6-1-lean-480/
- 局限：issue #8038 报告 `#time`/`trace.profiler` 在某些文件里漏掉了绝大部分时间，原文是 "only about 200ms of about 30s--60s is accounted for"。【仅见摘要】https://github.com/leanprover/lean4/issues/8038
- `set_option profiler true` 和 `lean --profile` 的确切输出格式，本次没有找到官方页面。【未找到】
- profiler 适合找文件内的热点，不适合做逐模块的总时长统计。【推断】

**Mathlib 的公开基准**
- speedcenter（VelCom）：
  - 2023 年 3 月起按文件统计指令数（instructions），没有按文件的墙钟时间。原文："only reports per-file instruction counts, rather than wall-clock"。【已核】https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Lake.20parallel.20builds.html
  - 当年可通过 `speed.lean-fro.org/mathlib4/api/run/<id>?all_values=true` 拿到全部值，但要先把 commit sha 映射成 velcom id。【已核】同上
- radar：
  - 2025-11 起替代 speedcenter：https://radar.lean-lang.org/repos/mathlib4 。
  - 维护者在 2025-11-28 表示计划“下周”关闭旧 speedcenter；历史数据已导入 radar。【已核】https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/mathlib4.20speedcenter.html
- radar 的逐模块数据：
  - 指标名形如 `build/module/<模块名>//instructions`；
  - 在单个 commit 页面底部的表格里，可以用正则 `^build/module/.*//instructions$` 过滤，再按 Value 排序。【已核】同上
  - radar 有没有公开的 JSON API：【未找到】。
- 论文《Growing Mathlib》提到，基准包含 "per-file compilation timings"。【仅见摘要】https://arxiv.org/html/2508.21593v1

## 3. CI 日志分析

- 下载整个 run 的日志：`GET /repos/{owner}/{repo}/actions/runs/{run_id}/logs`。
  - 返回 302 和归档包的下载地址，原文是 "This link expires after 1 minute"；
  - 公开仓库读取时可以不认证；
  - 单次尝试的日志用 `.../runs/{run_id}/attempts/{n}/logs`。【已核】https://docs.github.com/en/rest/actions/workflow-runs
- 单个 job 的日志接口（`/actions/jobs/{job_id}/logs`）和日志保留期限，本次没有核对。【未找到】
- 能否从日志里解析出逐模块耗时：
  - 工具链 ≥4.23 且 CI 环境下，日志里应该有 `Built <Mod> (<t>)` 行，可以用正则抽取。【推断，基于第 2 节】
  - 旧工具链的日志里没有耗时。
- Mathlib 是否有现成脚本，从 CI 日志统计最慢文件或关键路径：【未找到】。Mathlib 和 CSLib 的周报目前是把 `lake build` 的文本输出交给 grep/sed 处理，处理对象是告警，不是耗时。【已核】见 issue #15139
- 第三方做法【仅见摘要，仓库可信度未核】：
  - ArkLib PR #1212：用 `scripts/module_times.py` 把每个模块最近一次的 `Built` 耗时存成 JSON，随缓存一起传递。https://github.com/Verified-zkEVM/ArkLib/pull/1212
  - dtumad/sp1-lean PR #44：提供按导入加权的关键路径报告。https://github.com/dtumad/sp1-lean/pull/44

## 4. 内存

- Lake 能否记录逐模块的峰值内存：【未找到】。在手册和发布说明里都没看到相关功能。
- speedcenter 的 `maxrss` 不是逐文件的值：它取的是所有 lean 进程各自峰值中的最大值，原文 "the maximum of maxima"。【已核】speedcenter Zulip 帖
- 有人提议给每个文件加 `compilation` 一类的指标，维护者回复服务器已接近极限。【已核】同上
- 常见做法【推断，未找到 Lean 专门的出处】：
  - 包一层 lean 调用，用 `/usr/bin/time -v`（Linux）或 `-l`（macOS）读取 Maximum resident set size；
  - 或者每个模块放进独立的 cgroup，读取 `memory.peak`。
  - 两种做法都需要在 Lake 外面单独编译每个模块，或者借助 `moreLeanArgs` 之类的方式套壳。具体可行性需要实测。

## 5. 关键路径 / “longest pole”

- `lake exe pole` 确实存在过：
  - 2023-11 Mathlib 引入，读取 speedcenter 的逐文件指令数，再结合导入图，输出最长链上的模块和累计指令数；
  - 支持 `--to <模块>`；
  - 后来增加了 "parallelism" 列（例如 x18.21）。原文："only reporting the files that occur on the longest pole"。【已核】https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Lake.20parallel.20builds.html
- 现状：
  - 当前 mathlib4 的 `lakefile.lean` 里已经没有 `pole` 这个 `lean_exe`；【已核】https://github.com/leanprover-community/mathlib4/blob/master/lakefile.lean
  - 一些旧 fork 中还能看到 `LongestPole/` 目录。【仅见摘要】
  - 它是否因为 speedcenter 下线而被移除，本次没有核实。
- 论文《The Network Structure of Mathlib》给出：关键路径长 161 个模块，并行度 22.4×。【仅见摘要】https://arxiv.org/html/2604.24797v2

---

## 建议的分析流水线（以下全部为推断）

1. **导入图**：
   - 首选 `lake query --json <Lib>:...` 或模块的 `imports` facet；
   - 如果拿不到，用 `lean --deps`、`ImportGraph.Imports.FromSource`；
   - 最后的备选是 `lake exe graph out.xdot_json`。
   - 产出 `edges.jsonl`，每行 `{"module":M,"imports":[...]}`，只保留直接边。
2. **耗时**：
   - 在一台基准机上做一次冷构建：`lake build -v`，工具链需 ≥4.23；
   - 用正则 `Built (\S+) \((\d+(?:\.\d+)?)(ms|s)\)` 抽出每个模块的耗时，同时丢弃 `Replayed` 行；
   - Mathlib 的依赖部分可以参考 radar 的 instructions，作为相对权重。
3. **历史数据**：用 GitHub API 批量拉最近 N 次 run 的日志，用同一个正则提取，每个模块取中位数和 P90，减少噪声。
4. **内存**：逐模块用 `/usr/bin/time -v` 包一层 lean 调用，或用 cgroup 统计，记录 `peak_rss_mb`。如果没有这一步，用全局 maxrss 作为保守上限。
5. **关键路径**：
   - 在 DAG 上算每个节点的 `bottom_level`，即该节点耗时加上它到任意叶子的最长路径；
   - 再算全局关键路径和总工作量 / 关键路径长度（即理论并行上限），与 `pole` 的思路一致。
6. **交给调度器的格式**：一个 JSON 文件（示意结构如下）。调度器按 `bottom_level` 降序列表调度，再用 `peak_rss_mb` 约束每台机器的并发数。

```json
{"toolchain":"…","commit":"…",
 "modules":[{"name":"A.B","deps":["A.C"],"time_s":12.3,"time_p90_s":15.0,
             "peak_rss_mb":2100,"bottom_level_s":340.5,"source":"ci|local|radar"}],
 "critical_path":["…"],"total_work_s":0,"critical_path_s":0}
```

## 未完成 / 未验证

- `import-graph` 的完整 `--help` 参数，以及大仓库下的性能。
- 各个 module facet 在 `lake query --json` 下的实际输出。
- 4.23 的 `#9677` 和输出格式只见过摘要。
- `lean --profile` / `profiler` 的输出格式。
- radar 是否有 API。
- GitHub job 日志接口和日志保留期。
- `lake exe pole` 何时、为何被移除。

以上都没有实测，本次也没有运行任何代码。
