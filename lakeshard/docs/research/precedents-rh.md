# 先例调研：RH Lean 归档（175,187 模块）的批量 / 分布式构建

调研时间：2026-11-22。只读了网页和原文件文本，没有运行任何代码。
标注说明：没标的条目都读过原文；"仅见摘要"表示只看到搜索引擎返回的片段，没抓到原页面；"未找到"表示在已读材料里没有这项信息。
网页抓取额度在读完约 12 个页面后用完，所以 Omega 的工作流 YAML 和 `ci/plan.py` 原文**没有读到**（见第 1 节末尾）。

---

## 1. The Omega Institute：8,490 片内容寻址分片构建

来源：README https://github.com/the-omega-institute/riemann-hypothesis （已读原文）；构建笔记 https://github.com/the-omega-institute/riemann-hypothesis/blob/main/verification/NOTES.md （已读原文）

**怎么切分**
- CI 对 `Main` 的**实际导入闭包**做分区（README "How the fork publishes compiled shards" 一节）。
- 在当前源码树上切出 8,490 片、36 个依赖层；地基层完成后，马上就有 529 个可以独立开工的作业（README）。
- 每片的键是一个哈希，输入包括：源文件 blob、前置分片的键、构建配置、工具链、钉住的依赖包（README）。所以键是递归的内容寻址：上游哪一片变了，下游所有键都跟着变；没变的部分可以跨 commit 复用。
- 每片多大、按什么规则合并模块：README 没写；`ci/plan.py` 没读到，**未找到**。按平均算是 175,187 / 8,490 ≈ 20.6 个模块一片（这是我自己除出来的，不是来源给的数字）。
- `ci/plan.py` 和 `lean-parts.yml` 这两个文件名来自 riemann-hypothesis-book 仓库的 README（仅见摘要：https://github.com/the-omega-institute/riemann-hypothesis-book ）。

**产物格式与传输**
- 编译产物按 Linux x86-64 打包，发布在 `lean-parts-v1-*` 这组 GitHub **prerelease** 里；最终的 `build-<commit>` release 里放完整依赖计划、各分片 URL 和校验和，以及五个定理的公理报告（README）。
- 搜索结果里能看到的标签有 `lean-parts-v1-1/-4/-6/-8/-9/-e/-f`，单个 release 下有 171–195 个资产，例如 v1-8 显示 "Assets 195"（仅见摘要：https://github.com/the-omega-institute/riemann-hypothesis/releases/tag/lean-parts-v1-8 ）。book 仓库提到"16 个十六进制"，但片段被截断了（仅见摘要）。**推断**：分片按键的第一个十六进制字符分到 16 个 prerelease 里，这样能避开单个 release 的资产数上限。
- 本地 `./verify`：先拉 Mathlib 官方缓存；每个下载的分片都对照 Release 上的 SHA-256 校验；然后恢复所选模块需要的文件，跑 `lake --no-build build` 和 `lake env leanchecker --fresh`（README "Verify locally" 一节）。还有 `--build-missing Main`：先恢复已发布的依赖，再在本地编译缺的模块。
- 每片的构建是调 `lake build` 还是直接调 `lean`：README 没明说。PR 摘要里说构建作业会"用 Lake 下载并校验分组及其传递导入"，打包出规范归档后"再用 Lake 检查解包结果"（仅见摘要：https://github.com/the-omega-institute/riemann-hypothesis/pull/17 ）。**推断**：分片作业用的是 Lake，靠 trace 文件判断是否最新。

**调度、重试与时限**
- 调度器每分钟一次，根据已发布的依赖哈希找出可以开工的分片，分派到多个相互独立的 Actions matrix 上；每片完成后立刻发布（README）。
- 优先级：离 `Main` 剩余路径越长的分片越先派（README 原话 "Longer remaining paths to Main are dispatched first"）。也就是关键路径优先。
- 去重：同一个分片哈希同时只允许一个活跃 workflow；作业在**安装工具链之前**先查 Release，已经有产物就直接跳过，这样重叠的多次运行可以复用彼此的成果（README）。
- 协调器会重试缺失的分片；在托管 job 时限到之前**主动滚动**到新的协调器实例；进度从 Releases 和正在跑的 Actions 批次里重建，不靠本地状态。协调器中断后，手动再 dispatch 一次就能续跑（README）。
- runner：默认 Ubuntu 24.04 x86-64 托管 runner。仓库变量 `RH_LINUX_RUNNER` 可以换成内存或磁盘更大的 Linux runner（README）。这是 README 里唯一和内存不够的顶端模块有关的机制；具体哪些模块要用大 runner，**未找到**。
- PR #14：发布前沿上有 8 个被阻塞的分片，其中 74 个模块自身的导入已经发布了。这个 PR 允许父分片先把这些"连通组"拿出来提前构建，组 workflow 和父 workflow 共用同一个 concurrency key，父分片之后恢复这些组，**只校验 Lake trace、不重新编译**，再产出原来的规范归档（仅见摘要：https://github.com/the-omega-institute/riemann-hypothesis/pull/14 ）。
- PR #17：`Main` 附近有 6 个分片，它们的每个目标都已经有发布好的分组归档，可以直接组装，不必等其余分片编完（仅见摘要：上面 PR #17 链接）。

**规模与耗时**
- 总用时、runner 总数：**未找到**。README 只说 GitHub 分配可用的 runner。
- 第三方仓库 raissaramaruchti/rh-lean-check 记录：2026-11-20 约 20:57 UTC 时，已发布 5,891 / 8,490 片（仅见摘要：https://github.com/raissaramaruchti/rh-lean-check ）。
- Omega 的单机参考数字（NOTES.md "Building"）：48 核、503 GB 内存的机器上，预计 7–10 小时；容器限内存 `--memory 440g`，`/tmp` 给 64g tmpfs（NOTES.md "Sandbox"）。
- Lake 给每个模块写一个 `.setup.json`，里面列出该模块的整个导入闭包，平均约 6 MB，175,187 个加起来约 1 TB。模块编完后可以删，删了不影响"已是最新"的判断；NOTES.md 给了一个旁路循环脚本，按 `.trace` 比 setup 文件新来判断能不能删。

**没读到的**：`.github/workflows/lean-parts.yml`、`ci/plan.py` 原文。raw 地址被工具判为不在上下文里，`tree/` 页面又被拒绝访问，所以分片大小规则、单片调用的命令行、超时数值都**未找到**。

---

## 2. MIT Andrew Sutherland 的核验页

来源：https://math.mit.edu/~drew/grh/ （已读）、https://math.mit.edu/~drew/grh/sandbox-timeline.txt 、https://math.mit.edu/~drew/grh/sandbox-build.sh 、https://math.mit.edu/~drew/grh/sandbox-build-continue.sh 、https://math.mit.edu/~drew/grh/nanoda.log （都已读原文）

**第一次构建（原始构建）**
- 在云机器上跑，没有沙箱。每个文件**直接调 `lean`**，传入 lake 本来会给的同一组输入：模块名、包名、lakefile 里的选项。没有走 `lake build`（页面 "Caveats" 第一条）。
- 每台构建机上，归档的 `lean/` 目录都放在 `/home/ubuntu/grh/src/lean`，源文件以绝对路径 `.../src/<Module/Path>.lean` 交给 Lean（Provenance 表）。这里写的是 "every build machine"，说明不止一台机器。
- 编译全部完成于 16:43:21 UTC（Summary 表）。
- "8 台 192 核、一小时出头"：**页面未给出**。机器台数、核数、总耗时、`lean` 的完整参数、模块怎么分到各台、产物怎么同步，页面都没写。
- 编排者 "Fable 5.2"：**页面未给出**，页面只写了 "checks run with Claude Code"。我也没在其他已读来源里找到这一说法的出处。
- 绝对路径会进 `.olean`：175,187 个文件中有 98,219 个嵌了源文件路径（来自 linter 消息）。所以逐文件哈希只有在同一路径下构建才可比（Caveats 第二条）。
- 有 1 个模块（`.../RankPointCounts/LocModel`）多线程编译时结果不确定：并行 elaboration 下自动生成的等式引理会出现竞态。用 `lean -j1` 编六次，六次结果一致。修复见 lean4 PR #15499，首次发布于 v4.36.0（Caveats）。

**沙箱重建（第二台机器）**
- 机器：`ip-172-31-65-247`，192 核 AMD EPYC 9R45（timeline 第 1 行）。
- 阶段 A（有网）：并发下载 14 个分卷并校验 sha256，`lake exe cache get` 最多重试 3 次（遇到 "decompression(s) failed" 就重试），然后逐文件比对 Mathlib 8,322 个和依赖 378 个 `.olean`，最后 `lake build Mathlib` 确认不需要重编（sandbox-build.sh）。
- 文件描述符上限：脚本开头先 `ulimit -n 1048576`，注释说 192 核上 Mathlib 缓存工具会耗尽默认的 1024 个描述符。
- 阶段 B：bubblewrap 沙箱，参数是 `--unshare-all`、根目录只读、源码只读、只有 `.lake` 可写，加 `LEAN_ABORT_ON_PANIC=1`；在沙箱里跑 `lake build Main`。旁边另跑一个循环，每 60 秒删掉已构建模块的 `.setup.json`。
- `LEAN_NUM_THREADS` 调整（timeline 原文时间点，2026-11-21 UTC）：
  - 10:09:47 开始，不设该变量；
  - 10:22:31 改成 96；
  - 10:25:54 改成 64；
  - 11:59:49 改成 64，并 `taskset` 绑到 CPU 0-95；
  - 12:05:21 改成 40，绑 0-47；
  - 12:10:44 改成 96，绑 0-95；
  - 12:16:13 改成 64，绑 0-95，一直跑到 18:07:21 退出码 0。
  每次调整都是中断后靠 lake 增量续跑（sandbox-build-continue.sh 注释）。
- Lake 锁争用的原话在 `sandbox-build-continue.sh` 第 4 行注释："with 192 it spends most of its time contending on an internal lock"。同一行注释还说明该变量限制的是 lake 自己的 worker 线程数。
- 总耗时：10:09:47 → 18:07:21，约 7 小时 58 分（自己算的）。
- 导出：18:07:21 → 19:32:56，约 1 小时 25 分，产出 61,570,595,788 字节，与公开导出一致；175,187 个 `.olean` 里有 175,186 个逐字节一致（timeline）。

**导出与各内核的机器配置**
- nanoda：80 线程，27 分 42 秒，CPU 利用率 1996%，峰值 RSS 约 88.9 GB（nanoda.log）。
- con-leche：64 线程，3 分 15 秒；con-ron：64 线程，7 分 6 秒（Summary 表）。
- 自己复核需要约 100 GB 内存、70 GB 磁盘；con-leche 单独跑约需 50 GB 内存（"Check it yourself" 一节）。
- Lean 默认内核和 paranoid 内核都是单线程，跑了一天多还没出结果（Summary 表）。
- 具体机型、导出那一步的内存：**页面未给出**。borism 的 issue 转述 Sutherland 报告过导出单线程约 1 小时 20 分、峰值 163 GB（仅见摘要：https://github.com/borism/riemann-hypothesis/issues/3 ）。

---

## 3. luosiallen/riemann-hypothesis-lean-verify（不在原清单里，但机制最相关）

来源：二手报道 https://lilting.ch/en/articles/riemann-hypothesis-lean-independent-verify （已读原文）。原仓库 https://github.com/luosiallen/riemann-hypothesis-lean-verify **未读**。
- Run 1：128 核、503 GB，直接用 Lake，约 400 模块/分钟。Run 2：288 核、1 TB，Lake 反而掉到 30–50 模块/分钟。
- Run 2 慢的原因：Lake 自己吃掉约 225 个核，同时只有 7–47 个 `lean` 进程在跑。`perf` 显示约 270 个 Lake worker 线程有 85% 的时间在等共享构建状态的锁（`lean_st_ref_take`）。
- 解决办法：自写 `scripts/sched.py` 替换 Lake 的调度。先解析全部 import 头，得到 753,569 条边、无环、最长链 203；调度时优先最长链，保持 288 个 `lean` 进程满载；编译选项照抄 lakefile；Mathlib 走缓存。
- 踩坑：第一版漏了 `-R`（源码根目录参数），模块名都变成了 `src.<path>`。自动生成的实例名依赖模块名，结果下游 425 个模块报 `Unknown identifier`。最后丢弃约 105,700 个已编模块，从头再来。
- 重跑：1,350–1,700 模块/分钟，`sched.py` 阶段用时 2 小时 0 分 33 秒，0 失败。

## 4. ishaan2006/rh-lean-reproduction

来源：https://github.com/ishaan2006/rh-lean-reproduction （README 已读）
- Google Cloud VM，377 GB 内存，94 个并行作业，`lake build Main`，用时 **401 分钟**（README 第 6 节）。构建路径是 `/mnt/rh_ram/...`，从名字看可能是内存盘（推断）。
- 逐模块耗时日志：README 里**未找到**。只提到 `results/build_check_summary.txt` 和 `results/olean_comparison.txt`，这两个文件没读。
- 有一个有用的机制：`scripts/11_path_sample.sh` 从每个模块的 `.trace` 里取出 Lake 记录的**原样 `lean` 命令**来重放，只改输出位置和源码前缀。随机抽 300 个模块，300 个都与 Sutherland 的清单逐字节一致。
- 用 lean4export 导出花了 89 分钟，结果逐字节一致。

## 5. borism/riemann-hypothesis

来源：搜索片段（仅见摘要）：https://github.com/borism/riemann-hypothesis 、https://github.com/borism/riemann-hypothesis/issues/1 、https://github.com/borism/riemann-hypothesis/issues/3
- 机器 4 核 / 15 GB 内存 / 59 GB 磁盘：README 写 21–23 模块/分钟，issue #1 有一处写约 27/分钟、另一处写约 21/分钟。外推总时长 124–150 小时。
- 单模块平均约 8 核·秒，其中约 4 核·秒花在导入 Mathlib `.olean` 上（约 6 GB mmap，约 15 万次缺页）。每个 `lean` 进程私有内存 0.2–0.6 GB，Mathlib 的页面由各进程共享。
- 产物约 0.94 MB/模块，外推全量 130–155 GB。
- 总工作量约 390 核·时；关键路径 201 个模块，估计 35–70 分钟。深度分布：1–25 层 60,217 个，26–50 层 41,477 个……126 层以上约 2,400 个。超过约 300 核以后，这条窄尾和关键路径就成了瓶颈。
- 导出不能并行（编号表是全局共享的）；内核只能每台机器跑一个，没法按声明区间切开。
- 注意：borism 的模块总数是 164,464，和其他来源的 175,187 对不上，原因**未找到**。

## 6. Deicyde/riemann-hypothesis

原文**未读**（额度用完）。从 Omega README 只能知道：它是源码镜像，加了 `Challenge.lean` 和 `comparator.json`，CI 会重新下载 tarball 比对。复现协议的细节**未找到**。

---

## 7. 对我们设计的启示（以下全部是推断）

1. **单机 Lake 在 100 核以上会卡在锁上**。Sutherland 把线程从 192 降到 64，luosiallen 在 288 核上掉到 30–50 模块/分钟，两边是同一个现象。所以每台机器上要么限制 `LEAN_NUM_THREADS`，要么像 Sutherland 原始构建和 `sched.py` 那样绕开 Lake 直接调 `lean`。直接调时必须原样复制 Lake 的参数，尤其是 `-R` 和模块名、包名。最稳的做法是从 `.trace` 里抽出命令（ishaan 的做法）。
2. **调度用关键路径优先**。最长链 201–203，`Main` 附近的层很窄。Omega 和 luosiallen 都按到 `Main` 的剩余路径长度排优先级，我们也应该这样。
3. **产物按递归内容哈希寻址**（源码 + 上游键 + 工具链 + 配置）。这样能幂等、能续跑、多次运行之间能去重。"开工前先查产物是否已存在"放在安装工具链之前，可以省掉大量重复工作。
4. **协调器不保存状态**：进度从产物仓库重建，所以中断或超时后可以直接重启。
5. **分片粒度**：Omega 平均约 20 个模块一片；每个模块导入 Mathlib 的固定开销约占一半，所以片太小不划算。另外每台机器都要先恢复全部依赖产物，磁盘要按 130–155 GB 加上 Mathlib 来准备。
6. **路径要固定**：所有机器用同一个绝对构建路径，否则 98k 个 `.olean` 的哈希没法交叉核对。线程数不同可能带来个别不确定输出，校验时应该比导出哈希，而不是比整份清单的哈希。
7. 必须定时清理 `.setup.json`（全量约 1 TB）；文件描述符上限要调高。
8. 导出和内核检查是单机串行的长尾，要单独安排大内存节点：导出约 163 GB，nanoda 约 89 GB。
