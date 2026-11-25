# Lean 4 大型项目构建与分布式构建：网上事实汇编

- 检索日期：2026-11-22（UTC）。下文所说“检索日”都指这一天。
- 只读网页，没有下载或运行任何仓库代码。
- 凡是“未找到”的条目，就是本次检索中没有找到可靠出处。中途 web_fetch 配额用完，后半部分只能依赖搜索结果摘要，没法全文核对，涉及的条目已注明“仅见摘要”。
- 引文都很短（不超过 15 个英文词）；其余内容是我自己的概括。

---

## A. Lake 自身

### A1. 并行模型与并发数

**事实（带出处）**

1. **Lean 运行时线程池**：Lean 运行时用一个线程池执行 Task。池大小取环境变量 `LEAN_NUM_THREADS`，没设就取本机逻辑处理器数。这个数不是硬上限，为避免死锁可能超出。
   出处：Lean 语言参考 “Tasks and Threads” https://lean-lang.org/doc/reference/latest/IO/Tasks-and-Threads/ （页面无日期，检索日读取）
2. **Lake 没有 `-j/--jobs`**：master 分支 `Lake/CLI/Help.lean` 的帮助文本里只有 `--no-build`、`--fail-fast`、`--rehash/-H` 等选项，找不到 jobs/threads 选项。
   出处：https://github.com/leanprover/lean4/blob/master/src/lake/Lake/CLI/Help.lean （抓取到的版本时间为 2026-10-17）
   - 2023-10-18 Zulip 上 Lake 作者 Mac Malone 说，Lake 自己控制不了线程数，只能用全进程级的 `LEAN_NUM_THREADS` 来限制。同一帖里有人报告：16 线程机器上 `lake clean; lake build` Mathlib 墙钟 23 分钟（用户态 22191 s，CPU 1660%），机器仍有 10–50% 空闲。这是 2023 年的 Mathlib，规模比现在小。
     出处：https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Lake.20parallel.20builds.html
   - 第三方说法（仅见摘要）：Lake 4.35 没有 `-j`，构建 job 是线程池上的普通优先级任务，所以 `LEAN_NUM_THREADS=8` 就把并发 lean 进程限在 8 个。出处：https://github.com/gominimal/pkgs/pull/1244
3. **单个 `lean` 进程也有线程**：Lean 4.35.0 支持 `-j N` / `--threads=N` 和 `LEAN_NUM_THREADS`，命令行编译默认已开启 `Elab.async`（第三方 issue，仅见摘要）。出处：https://github.com/NethermindEth/LeanCIL/issues/431
   另一第三方 issue 指出，Lake 池大小 × 每个子 lean 进程的线程数会叠加，4 vCPU 上最多能到 16 个线程（仅见摘要）。出处：https://github.com/dtumad/sp1-lean/issues/39
4. **单文件内并行的时间线**（官方 release notes）：
   - v4.16.0：每条命令的 linter 放到单独线程跑，算是并行化 elaborator 的第一步（#4460）。https://lean-lang.org/doc/reference/latest/releases/v4.16.0/
   - v4.17.0（2025-03-03）：内核检查与 elaboration 并行（#6368），这是并行 elaboration 的前置工作。https://lean-lang.org/doc/reference/latest/releases/v4.17.0/
   - v4.18.0（2025-04-02）：代码生成与后续 elaboration 并行（#6770），并修了一个 `Elab.async` 回归（#7175）。https://lean-lang.org/doc/reference/latest/releases/v4.18.0/
   - v4.19.0（2025-05-01）：定理证明体可以彼此并行 elaborate，也能和其他 elaboration 任务并行（#7084）。https://lean-lang.org/doc/reference/latest/releases/v4.19.0/
5. **超多核机器上的实测**：Sutherland 在 192 核机器上重建 RH 项目时，脚本注释写着：`LEAN_NUM_THREADS=192` 时 Lake 大部分时间耗在一把内部锁的争用上，最后改用 64–96。
   出处：https://math.mit.edu/~drew/grh/sandbox-build-continue.sh ，时间线 https://math.mit.edu/~drew/grh/sandbox-timeline.txt （2026-11-21）

### A2. 产物缓存（artifact cache）

**事实（带出处）**

1. **trace 是什么**：Lake 为每个产物写一个 trace 文件，内容是输入哈希的 Merkle 式混合。输入都没变就不重建，还会把当时的构建日志重放出来。产物哈希另存在 `.hash` 文件里，`--rehash` 让 Lake 不信任这些文件、全部重算。
   出处：Lake 官方文档 https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/ （检索日读取）
2. **本地 artifact cache 起点**：v4.22.0 引入（#8922），同时按输入和内容寻址，用来在同一仓库的不同 checkout 之间共享 olean；需要 `LAKE_ARTIFACT_CACHE=true` 或 `enableArtifactCache`。出处：https://lean-lang.org/doc/reference/latest/releases/v4.22.0/
   - 官方文档至今仍标注为**实验性**、默认关闭。缓存按 toolchain 分开存放，因为不同 toolchain 的中间产物互不兼容；同一 toolchain 下的所有 workspace 共享。`LAKE_CACHE_DIR` 指定缓存目录：设为空串表示禁用，不设则用 Elan 目录下按 toolchain 划分的共享目录。`restoreAllArtifacts` / `LAKE_RESTORE_ARTIFACTS` 把缓存里的产物复制（能硬链接就硬链接）到构建目录。出处同 Lake 文档。
3. **远程缓存（v4.30.0，2026-05-26 大改）**：
   - 构建时按需从远程缓存下载（#12634）；
   - `lake cache get` 默认连产物一起下载（#12927）；
   - 用 leantar 打包/解包 `.ltar`（#12914）；
   - 新增 `lake cache stage|unstage|put-staged`，对应 Mathlib `lake exe cache` 里的同名命令（#13144）。
   出处：https://lean-lang.org/doc/reference/latest/releases/v4.30.0/
   - v4.31.0（2026-06-13）：修了 Linux aarch64 上 leantar 的打包。https://lean-lang.org/doc/reference/latest/releases/v4.31.0/
   - v4.32.0（2026-07-13）：上传/下载时按哈希去重（#14060）。https://lean-lang.org/doc/reference/latest/releases/v4.32.0/
   - v4.35.0（2026-10-12）：`lake build -o <file> --package <name>` 加 `lake cache put --package` 可以上传依赖包的产物；`put-staged` 必须显式给 `--rev`（#15141）。https://lean-lang.org/doc/reference/latest/releases/v4.35.0/
4. **远程缓存机制**（官方文档）：
   - `lake build -o` 把“输入→产物”的映射写成 JSONL mappings 文件，`lake cache put` 据此上传。
   - 服务分两类：S3 协议（`kind = "s3"`，`artifactEndpoint` + `revisionEndpoint`）和 Reservoir API。产物都按内容哈希寻址；mappings 按 Git 提交存放，路径形如 `REVS/SCOPE/COMMIT.jsonl`，产物路径形如 `ARTS/SCOPE/HASH.art`。
   - 上传用 AWS SigV4，密钥放在 `LAKE_CACHE_KEY`。
   - 系统配置里可以写 `cache.defaultService` 和 `[[cache.service]]`。
   - 文档明说：Lake 目前给产物用的**不是密码学安全哈希**，所以上传时要加 scope 前缀以防碰撞。
   出处：https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/
5. **`--no-build`**：只要有目标不是最新，Lake 立刻以非零码退出。适合拉完缓存后用来验证“缓存是否齐全”。出处同上。
6. **`platformIndependent`**：
   - 设为 false：把 `System.Platform.target` 加进模块 trace，换平台会重新 elaborate；
   - 设为 true：把平台相关项剔出 trace；
   - Lake 不检查这个声明是否属实。
   - 使用 Reservoir 云构建归档的包应当开启它。
   出处同上。
7. **缓存键里有没有绝对路径**：
   - 官方文档对此**未找到**明确说法。
   - 间接证据：Sutherland 用官方 Mathlib 缓存在别的机器上拿到 8,322 个 Mathlib 和 378 个依赖 `.olean`，与参考副本逐字节相同。https://math.mit.edu/~drew/grh/
   - **`.olean` 字节本身与路径有关**：Lean v4.33.1 把每条 linter 消息连同源文件绝对路径存进 olean（`lintLogExt`）。RH 项目 175,187 个 olean 中有 98,219 个含路径；换目录后，这些 olean 的哈希就对不上了。同一页还报告有 1 个模块编译结果不确定：同一台机器上用相同输入编译 6 次，得到两种输出。
     出处：https://math.mit.edu/~drew/grh/ ；https://github.com/leanprover-community/riemann-hypothesis/issues/6 ；https://github.com/leanprover-community/riemann-hypothesis/pull/40 （2026-11-21）
8. **磁盘占用**：Lake 4.33 每个模块会写一个约 6 MB 的 `*.setup.json`，Sutherland 的脚本在模块建完后把它删掉。出处：https://math.mit.edu/~drew/grh/sandbox-build.sh

### A3. Reservoir 与包级缓存

**事实（带出处）**

- 名为 `"reservoir"` 的缓存服务始终可用。`lake cache get` 默认按依赖树逐包向 Reservoir 拉取，非 Reservoir 依赖跳过。Reservoir 上的 scope 目前就等于 GitHub 仓库名。出处：Lake 文档（同上）。
- 另有包级方案“GitHub release 构建”：把整个构建目录打成归档挂在 release 上，相关配置是 `releaseRepo` / `buildArchive` / `preferReleaseBuild`，上传用 `lake upload`。它只对依赖包自动生效；`LAKE_NO_CACHE` 可关闭。出处同上。
- Reservoir 服务端由谁、在什么机器上预编译各个包：**未找到**。

### A4. Mathlib 的 `lake exe cache get`

**事实（带出处）**

- **缓存键**：每个 `.ltar` 用一个缓存哈希命名，通过 `rootHash` 覆盖 toolchain、lakefile 和 manifest；导入者的哈希又依赖被导入模块的哈希，所以一处失效会沿依赖链级联下去（PR #42660，仅见摘要）。https://github.com/leanprover-community/mathlib4/pull/42660
  2023 年 Zulip 上 Mario Carneiro 描述的服务器布局是 `CACHE_URL/f/<hash>.ltar`。https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/lean-cache.3A.20lake.20exe.20cache.20rewrite.html
  结论：缓存**按文件哈希**组织，不按提交。
- **存放位置**：
  - 过去在 Azure Blob（`lakecache.blob.core.windows.net`）；
  - 现在读 `cache.mathlib.org`，后端是 Cloudflare R2：CI 生成短期 S3 凭据，把同一份 staged 集合推到 R2（仅见摘要）。https://github.com/leanprover-community/downstream-reports/pull/94
  - PR #44174 删除了直接读 Azure 的路径，改为读 `cache.mathlib.org` 或 `MATHLIB_CACHE_BASE_URL`。https://github.com/leanprover-community/mathlib4/pull/44174
  - 第三方称：Mathlib 从 v4.35 起默认读 `cache.mathlib.org`；v4.27–v4.33 的项目需要设 `MATHLIB_CACHE_GET_URL`。https://github.com/vidick/MIPRE-formalization/pull/265 ；https://github.com/marco-david/ainfinity-lean/pull/70
- **规模与耗时**：
  - Mathlib v4.33.1 有 8,322 个 `.olean`，依赖另有 378 个（Sutherland 页）。
  - 第三方转述 Mathlib CI 一次冷构建（v4.35.0 toolchain bump PR mathlib4#44806）：9,048 个 job 用了 43 分钟（仅见摘要，属二手信息）。https://github.com/gominimal/pkgs/pull/1244
  - CI runner 的具体规格（核数、内存）：**未找到**。
  - `.olean` 总体积：**未找到**。
  - Mathlib 冷构建的峰值内存：**未找到**。旁证：有人说一个深层模块要映射约 6 GB 的 Mathlib olean（仅见摘要）。https://github.com/borism/riemann-hypothesis/issues/9

---

## B. 分布式/多机构建的已有方案

### B5. Mathlib CI

**事实（带出处）**

- Mathlib 用自托管 runner 池（fleet），每个 job 都在新容器里启动，状态不会带到后续 job。https://github.com/leanprover-community/mathlib4/pull/44357 ；https://github.com/leanprover-community/mathlib4/pull/44603
- 关于 Mathlib 把**一次构建拆到多台机器**：**未找到**任何证据。能看到的模式是单个大 job 加缓存上传（staged → Azure/R2）。
- Hoskinson 资助的 runner 和 bors 的具体规格：本次**未找到**可引用的页面，未核实。

### B6. Nix

**事实（带出处）**

- nixpkgs 手册说，旧的“每模块一个 derivation”方案（2020–2025）已经在上游移除；现在 nixpkgs 的 `buildLakePackage` 架构不同，按**包**粒度，而且依赖可以是固定输出的 derivation。https://nixos.org/manual/nixpkgs/stable/
- 社区项目 lenianiva/lean4-nix 仍提供 `buildLeanPackage` 和各版本的 manifest：v4.22.0 起每个版本要同时有 `bootstrap` 和 `buildLeanPackage`，最低支持 v4.11.0。https://github.com/lenianiva/lean4-nix
- 有人报告：用固定输出 derivation 跑 `lake exe cache get` 拉 Mathlib，两次冷构建结果**不可复现**（仅见摘要）。https://github.com/jmmaloney4/jackpkgs/pull/387
- 借 Nix remote builders 做 Lean 多机构建的实际案例：**未找到**。

### B7. Bazel / 其他

**事实（带出处）**

- `atvrager/rules_lean`：每个 Bazel action 编译一个 Lean 模块；README 拿它和 Lake 对比，称 Lake 只有本地磁盘缓存，而 Bazel 有 disk cache、remote cache 和 remote execution。https://github.com/atvrager/rules_lean
  另有 `pulseengine/rules_lean`（支持 Mathlib）和 `tomato-bazel/rules_lean`（与 Lake 集成）。这些都是社区项目，成熟度未核实。
- Buck2 的 Lean 规则：**未找到**。
- lean4 官方关于“分布式构建 / remote execution”的 RFC：**未找到**。相关的 issue/PR 有：
  - #13913：path 依赖与父 workspace 共享产物；
  - #15870：构建期间发现包的 artifact cache（kim-em）；
  - #15880：构建中途源文件改了，olean 会被存到旧的源哈希下。
  （以上只看了标题和摘要）
- **RH 项目的社区分片构建**（与本任务最接近的先例）：the-omega-institute/riemann-hypothesis 由 CI 把 `Main` 的真实 import 闭包切分后，在 GitHub 托管 runner 上编译，每完成一片就发布成 `lean-parts-v1-*` prerelease（Linux x86-64 产物）。该源码树共 8,490 片、36 层依赖；底层完成后，立刻有 529 个 job 可以并行。协调器负责重试缺失的分片、赶在托管 job 时限前换下一轮，并能从 Releases 恢复进度。https://github.com/the-omega-institute/riemann-hypothesis
- leanprover-community/riemann-hypothesis 的社区缓存用法是 `lake exe cache get` 加 `lake build --no-build`。README 明说缓存里包含不受信任的 PR 和志愿者机器的产物，要建立信任必须独立重建。它征集的自托管 runner 理想配置是 128 GiB 内存、≥250 GiB SSD，并要求 `vm.max_map_count ≥ 1048576`。https://github.com/leanprover-community/riemann-hypothesis ；转述见 https://github.com/jasonyandell/rh-board/issues/19
- borism 的复现记录：4 核约 21–23 个模块/分钟；按其外推，32 核约 12 小时（仅见摘要）。https://github.com/borism/riemann-hypothesis

### B8. 其他证明助手

**事实（带出处）**

- **Isabelle AFP**：Huch 与 Wenzel 在 ITP 2024 发表了分布式并行构建。集群节点之间不共享内存，也不共享文件系统；用 `isabelle build -H hosts` 指定集群；调度按 session 进行，并为多线程任务求解调度优化（几秒内出排程）。总加速比超过 100：Isabelle 发行版 8 分 10 秒，AFP 35 分 40 秒，算上很慢的 session 是 1 小时 59 分 13 秒。在此之前，单节点要 4–8 小时。https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2024.22
- **Coq/Rocq + dune**：dune 有本地共享产物缓存（`dune cache`）。分布式缓存是 2021 年的 issue #4850，状态未核实。https://github.com/ocaml/dune/issues/4850 ；https://dune.readthedocs.io/en/stable/reference/cli.html
- HOL4 / HOL Light 的多机构建：本次未检索，**未找到**。

---

## C. 内核检查与导出

### C9. 各工具

**事实（带出处）**

- **lean4export**：输出 NDJSON，格式版本 3.1.0，开头是一个 meta 对象，记录导出器、Lean 和格式的版本。https://github.com/leanprover/lean4export/blob/master/format_ndjson.md
- **comparator**（leanprover/comparator）：先在沙箱（landrun）里构建并导出 challenge 和 solution，再比对陈述、检查公理，然后跑内核以及配置里的外部内核（如 nanoda）。https://github.com/leanprover/comparator
  - v4.35.0 起 `lake comparator` 随 toolchain 发布，并附带几个独立内核。https://lean-lang.org/doc/reference/latest/releases/v4.35.0/
  - 并行重放：comparator PR #99（可选的 parallel_replay）和 lean4 RFC #15569 提议：定理放进 Task 并行检查，非定理仍按顺序单线程检查。RFC 里的数据是，单线程预计 1–2 周，并行版在一台 342 线程机器上 83 小时完成并通过（RFC 没写明是哪个导出）。FRO 尚未决定官方 replay 是否多线程。https://github.com/leanprover/lean4/issues/15569 （约 2026-10）
- **leanchecker / lean4checker**：
  - 按模块重放 olean 环境；`--fresh` 连导入的常量也一起重放。
  - 源码里有“并行检查的默认 worker 数”，注释提到大项目中每个 worker 都要载入接近完整的环境。https://github.com/leanprover/lean4checker/blob/master/Main.lean
  - 第三方 arXiv 论文说它已在 v4.28.0 并入 Lean，名为 `leanchecker`，原仓库 2026 年归档。https://arxiv.org/html/2606.26442v1
  - 第三方实践：并行重放时，第一个之后的每个副本都要各自载入一份 Mathlib（仅见摘要）。https://github.com/Stavan-Jain/CircuitEq/pull/1
  - 也有人按 olean + trace + toolchain 记账，只重放变动过的模块，即增量检查（仅见摘要）。https://github.com/taco-jpg/p196-algorithm/pull/483
  - 还有人分 6 个分片做月度重放（仅见摘要）。https://arxiv.org/pdf/2606.01356
- **nanoda**：独立的 Rust 内核，读 NDJSON 导出，支持多线程（Kernel Arena 里设为 4 线程）。https://arena.lean-lang.org/round/2026-09/checker/nanoda/
- **lean4lean**：读编译好的 `.olean`，不读导出文件，按模块检查。论文脚注说它可以逐模块并行检查（前提是信任导入），但会碰到内存限制。https://arxiv.org/pdf/2403.14064 ；https://github.com/typhdotcom/lean4lean
- **“分片内核检查”的先例**：
  - leanchecker 与 lean4lean 都是按模块独立检查，各自载入依赖，天然可以分片；
  - Sutherland 的 lean4lean 就是逐模块跑完 175,187 个模块的（见下）。
  - 基于单个导出文件、跨机器分片的 nanoda/comparator：**未找到**。

### C10. RH 项目核验记录（Sutherland 页）

页面 https://math.mit.edu/~drew/grh/ ，标注的最后更新时间为 2026-11-22 02:25 UTC，我在 02:52 UTC 读取。

**事实**

- **规模与版本**：175,187 个模块全部编译通过，用的是 Lean v4.33.1 和 Mathlib v4.33.1。导出（lean4export v4.33.0）的结果是：
  - 1,468,418 个声明；
  - 解压后 61,570,595,788 字节（约 61.6 GB）；
  - zstd 压缩后 7.7 GB。
- **原始构建**：在云机器上直接调用 `lean`，传入的参数与 Lake 相同，没有经过 `lake build`。页面**没有给出**这些机器的核数和内存，也没有给出原始构建的耗时。
- **沙箱重建**：在另一台机器上进行（192 核 AMD EPYC 9R45，内存未给出）。
  - 时间线：`lake build Main` 从 2026-11-21 10:09:47Z 开始，18:07:21Z 结束，约 8 小时；期间多次重启，调整 `LEAN_NUM_THREADS`（96/64/40）和 CPU 绑核。
  - 导出耗时约 1 小时 25 分（18:07→19:32）。
  - 导出结果与发布版逐字节相同；175,187 个 olean 中 175,186 个相同。
  - Mathlib 由官方缓存提供。
  - 出处：https://math.mit.edu/~drew/grh/sandbox-timeline.txt
- **各检查器**：

| 检查器 | 线程 | 用时 | 峰值内存 | 结论 |
|---|---|---|---|---|
| leanchecker 逐模块重放 | 未写明 | 约 18:17 UTC 完成 | 未写明 | 175,187 个全部通过 |
| nanoda（v4.36 自带的 `nanoda_bin`） | 80 | 27 分 42 秒（CPU 利用率仅约 1996%） | 最大 RSS 88,880,436 KB（约 85 GiB） | 接受；[nanoda.log](https://math.mit.edu/~drew/grh/nanoda.log) |
| con-leche master | 64 | 3 分 15 秒（解析 33.9 s，检查 160 s） | 45.62 GiB | 接受；[log](https://math.mit.edu/~drew/grh/con-leche-master.log) |
| con-ron `--compare` | 64 | 7 分 6 秒（单线程解析约 360 s） | 约 44.6 GiB | 五条定理全部成立；[log](https://math.mit.edu/~drew/grh/con-ron-compare.log) |
| lean4lean（逐模块，读 olean） | 未写明 | 约 21:55 UTC 完成 | 未写明 | 全部通过；其中 5 个模块要调高步数上限才过 |
| Lean 默认内核 / paranoid 内核（读导出） | **单线程** | 截至页面更新仍在运行 | — | 尚无结论 |
| `lake comparator`（v4.36.0） | 内核阶段单线程 | 仍在运行 | — | 陈述比对和公理检查已通过 |

- **页面给出的复核资源要求**：约 100 GB 内存、70 GB 磁盘；Lean 内核单线程，要慢得多。

---

## 对多机构建设计的启示（以下全是我的推断，不是网上事实）

1. **调度粒度用模块，分配粒度用“子图”**。Lake 本身只能单机运行，并发由 `LEAN_NUM_THREADS` 决定，不存在 `-j`。多机方案只能放在 Lake 之外：要么按模块直接调 `lean`（Sutherland 的原始构建、rules_lean 都是这样），要么像 omega-institute 那样切分 import 闭包，每台机器跑一次 `lake build <子目标>`。RH 树有 36 层依赖，底层一过就有 529 个可并行的分片，说明宽度足够，瓶颈在关键路径和慢模块。
2. **交换介质用 Lake 自己的 artifact cache 加 S3**。每台 worker 用 `lake build -o` 生成 mappings，再用 `lake cache put` 推到 S3/R2；下游机器靠 `lake cache get --mappings-only` 加构建时按需下载拿依赖。目前的局限有三点：mappings 按 Git 提交组织；哈希不是密码学安全的，所以要用 scope 隔离；整套功能仍标为实验性，而且 issue #15880、#16407 这类缓存一致性问题还在修。
3. **所有机器固定同一个绝对路径**，比如 `/work/src`。v4.33 的 olean 带着源文件绝对路径；虽然 Lake 缓存命中看起来不受路径影响（Mathlib 缓存在异机上能逐字节复用），但如果要做逐字节审计或比对 manifest，目录就必须一致。另外要容忍个别模块编译结果不确定，应当比对导出，而不是比对整个 manifest 的哈希。
4. **单机的内存和磁盘决定每机并发数**。一个深层模块要映射约 6 GB 的 Mathlib olean。RH 社区建议 runner 配 128 GiB。175k 个模块每个约 6 MB 的 setup.json，总量约 1 TB，属于临时文件，要及时清理。192 核单机上，`LEAN_NUM_THREADS` 超过约 96 就开始锁争用。所以“多台中等机器各跑 32–64 个线程”可能比一台巨型机效率更高。
5. **内核检查也应分片**。leanchecker 和 lean4lean 是逐模块的，可以直接按构建分片下发，各机器载入自己的依赖 olean 即可。基于单个 62 GB 导出的检查（Lean 官方内核、comparator）目前是单线程，而且要约 100 GB 内存，是端到端时间里最长的一环，只能等并行 replay（RFC #15569）或改用 nanoda/con-leche 这类多线程检查器。
6. **调度策略可以照搬 Isabelle 的经验**：节点之间不共享文件系统；用历史耗时估计任务时长，提前生成调度计划；优先跑慢任务和关键路径。

---

## 未找到 / 未核实清单

- Mathlib CI runner 的具体规格，以及 Hoskinson、bors 的细节；Mathlib `.olean` 总体积；冷构建峰值内存（只有二手的 43 分钟这一个数）。
- Reservoir 服务端在哪里、用什么机器预编译各个包。
- 借 Nix remote builders 构建 Lean 的实例；Buck2 规则；lean4 官方的分布式构建 RFC。
- HOL4 / HOL Light 的多机构建。
- RH 原始构建所用云机器的规格和耗时；192 核重建机的内存；Lean 官方内核和 `lake comparator` 的最终用时（截至检索时仍在运行）。
