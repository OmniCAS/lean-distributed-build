# 先例调研：证明助手 / 大型 Lean 库的批量与分布式构建基础设施

调研日期：2026-11（以抓取时间为准）。标注约定：
- 【原文】我读到了全文或相关段落；
- 【仅见摘要】只看到搜索结果摘要，没打开原页面；
- 【未找到】查了，没找到可靠来源。

引用的原文每处不超过 15 个英文词，其余都是我自己的概括。

---

## 1. Isabelle 分布式构建（Huch & Wenzel, ITP 2024）【原文，全文 PDF】

来源：https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2024.22 （PDF：https://drops.dagstuhl.de/storage/00lipics/lipics-vol309-itp2024/LIPIcs.ITP.2024.22/LIPIcs.ITP.2024.22.pdf ；实验数据与代码：https://github.com/Dacit/isabelle-distributed-build ，这个仓库我没打开）

**动机与目标**
- AFP 约 830 个条目、440 万行。单台高端服务器多线程构建已经要 4–8 h。论文的目标是把总耗时压到 45 min 以内，这个数是“在线等结果”的经验上限（§1）。
- Isabelle 的 ML heap 只能线性叠加，只有分叉、没有合并，所以 session 依赖图是一棵树（§1）。Lean 的模块导入图是 DAG，这一点和 Isabelle 不同。

**集群架构（§2.2）**
- 作者评估过 Slurm，最后放弃。原因有四个：不支持 macOS；部署要 root 权限和统一的 UID；调度器用不上领域知识（线程数、预测耗时）；处理不了 P 核/E 核混合的 CPU（§2.1）。
- 最低要求：所有节点同一平台；主节点通过 SSH 连到各 worker；节点用本地 SSD；**不需要也不建议用网络共享盘**；外加一台 PostgreSQL 服务器，所有节点都能访问。
- 命令行用 `isabelle build -H hosts:options` 指定拓扑。主机和主机组登记在一个 TOML 格式的注册文件里。
- master 和 worker 运行同一个 Isabelle/Scala 程序，共享状态放在数据库表里。作者自己实现了带表锁的事务，以及类似版本控制的增量更新传播。完整加锁的代价是最少约 100 ms、中位数约 1 s。为了少轮询，用 PostgreSQL 的 `LISTEN/NOTIFY` 做异步通知。
- worker 可以中途加入或离开，但目前的实现是在构建开始时固定好节点集合。
- 构建流程分六步：
  1. 分析 ROOT 文件和 theory 依赖，结果写入数据库，路径存成相对路径；
  2. 用 ssh+rsync 把 master 上的 Isabelle 发行版同步到各 worker，其中包括 Scala/Java 产物，这样省掉约 1.5 min；
  3. 各 worker 自行下载组件；
  4. （可选）每个 worker 跑一个基准 session；
  5. worker 从数据库读队列和排程，自主干活。master 默认不参与计算；
  6. 收尾生成 HTML/LaTeX。
- **产物传输**：ML heap 先用 Zstd 压缩，再作为 blob 存进数据库，按约 50 MiB 切片，以绕开 PostgreSQL 单个 blob 2 GB 的上限。worker 需要某个 heap 时从数据库取，本地文件系统当缓存。数据：HOL heap 未压缩约 200 MiB，压缩后约 50 MiB，压缩/解压分别约 0.9 s/0.3 s，提交一个 blob 约 1.5 s；个别 session 的 heap 接近 1 GB。

**耗时预测（§2.3）**
- 数据来自历史 `build_log` 数据库。跨机器换算用一个单线程基准 session 的耗时比值。论文按 MSE 比较后选了 FOLP-ex，约 15 s。
- 线程数插值基于 Amdahl 定律：先由两个已知点解出可并行比例 p，再插值。相对误差从纯线性插值的 0.52 降到 0.42。
- 没有历史数据时，依次退回到：session 的 timeout、全体作业的平均值、全局加速曲线。
- 估计值会故意**略微放大**，避免低估被优化器“利用”。
- 例子：一个只有三行的 locale 解释，在 AFP 里要约 50 h CPU。作者据此说明，不实际跑一遍几乎无法预测耗时。

**调度（§3）**
- 原来的引擎是贪心的：哪个 session 的后继路径上累计耗时最长就先跑哪个，有空闲就开工。新引擎用 `-o build_engine=build_schedule` 选择。
- 问题被建模成多模式资源受限项目调度（MRCPSP）。“模式”就是 主机×线程数 的组合；每台主机有两种资源约束：线程总数不超过核数，并发 session 数有上限。这个问题是强 NP 难的。
- 试过的求解器：精确方法（分支切割、SAT）只能解 28 个活动的小实例；OptaPlanner 能解 132 个活动的中等实例，923 个活动的大实例解不出来；CPLEX 几分钟能给出不错的解，但它是专有软件，不能随 Isabelle 一起分发。
- 最终方案是**启发式的并行调度生成方案（SGS）**：
  - 从依赖图里找出**关键 session**：所在路径的累计耗时超过阈值的 session。阈值可以取绝对值，也可以取关键路径长度的某个比例；
  - 把最快的若干台机器留给关键 session；
  - 非关键 session 的线程数按耗时分档。最好的一组参数是：≤1 min 用 1 线程，≤5 min 用 4 线程，更长的用 8 线程；关键阈值取 10–20 min 的路径长度效果最好；
  - 如果某台主机有空闲核，就把已调度 session 的线程数调高；
  - 最后对参数空间做扫描。即使最大的实例，也能在**几秒内**给出排程。
- 运行中默认**每 5 min 重新计算一次排程**，以吸收实际耗时与估计的偏差。

**实测（§4，表 1、表 2）**
- 发行版数据集使用 Isabelle2024，集群是 4 台 i9-12900K（64 GB）加 4 台 i9-13900K（128 GB）。异构数据集用的是 10 个 Xeon Silver 4316 分片（每片 10 核、44 GB）加 4 台 i9-12900K。
- 发行版数据集的结果（耗时 / CPU 时间）：

  | 构建对象 | 经典引擎 | 启发式排程 |
  |---|---|---|
  | Isabelle 发行版 | 8:10 / 2:49:51 | 9:12 |
  | AFP | 42:16 | 35:40 / 64:57:11 |
  | 含 slow 的 AFP | 49:09 | 40:50 |
  | 完整 AFP | 2:07:10 | 1:59:13 |

  CPU 时间与墙钟时间之比超过 100 倍。并行度越高，CPU 总时间也越多。
- 异构集群上差距更大：完整 AFP 用经典引擎要 5:04:32，用启发式只要 2:07:56。原因是经典引擎会把重要任务分到慢机器上。
- 用 CPLEX 跑 5 min 得到的初始排程，估计的总时长更短，但实际构建反而略慢。论文的解释是：历史数据主要来自启发式常选的那些配置，CPLEX 选的配置估得更不准。
- 冷启动：历史库为空时，要连续跑 7–8 次估计才收敛。所以一次性构建更适合用经典引擎。
- 启发式的前提是“慢机器很多”。如果只给 4 台最快的机器，启发式的解质量会明显下降。
- 论文顺带的 Lean 数据（2024 年）：Mathlib 当时约 140 万行，在作者最快的一台机器上全量构建 28 min，测试另需 7 min。

**失败处理**
- 论文**没有专门讨论**节点宕机或任务失败后的重试机制。能对应上的只有三点：节点集合在构建开始时固定；排程会周期性重算；估计值偏保守。“未来工作”一节提到，可以在构建继续运行的同时，在 IDE 里逐步修复失败。

---

## 2. Mathlib 的 CI 与 `lake exe cache`

**说明**：GitHub 页面抓取被限流，`.github/workflows/build_template.yml`、`Cache/README.md`、`Cache/CI.md` 的原文我都**没能读到**。本节全部来自 PR 页面和 Zulip 的搜索摘要。

**工作流与机器**
- 现行构建模板叫 `build_template.yml`，`build.yml` 和 `build_fork.yml` 调用它【仅见摘要】：https://github.com/leanprover-community/mathlib4/pull/45594 ，https://github.com/leanprover-community/mathlib4/pull/45223
- 来自 fork 的 PR 以 `cache-mode: read` 调用这个模板，GitHub 会拒绝它的写缓存请求【仅见摘要】：同上 #45223。
- 构建跑在自建 runner 机群上，机群里有 16 核和 32 核两种主机，还有一种 “burst host, ccx43”。PR #44603 给的分步耗时：Build 130→100 s，上传缓存约 60–90 s，Post-Build 约 230–375 s；基于 262 次 PR 构建，端到端中位数省了 72 s【仅见摘要】：https://github.com/leanprover-community/mathlib4/pull/44603
- Mathlib Initiative 的路线图里有一项是把构建 runner 从 Hoskinson 迁到 Hetzner，并把缓存迁到可扩展的平台【仅见摘要】：https://mathlib-initiative.org/roadmap/
- Actions 运行列表上，master 分支（由 bors 推送）的 CI 单次耗时约 15–37 min，具体日期不明【仅见摘要】：https://github.com/leanprover-community/mathlib4/actions/workflows/build.yml
- **有没有把一次构建拆到多台机器上**：【未找到】任何证据。从摘要来看，单次构建是在一台 runner 上跑 `lake build`，靠缓存实现增量。这是推断。
- master 构建会从 staging 的 cache-snapshot artifact 预热本地缓存（PR #45169、#44171）【仅见摘要】：https://github.com/leanprover-community/mathlib4/pull/44171

**缓存键与存储布局**
- 每个模块的缓存哈希由四部分组成：`rootHash`（覆盖 toolchain、lakefile 和 manifest）、`pathHash`、文件内容、所有 import 的哈希。产物命名为 `<hash>.ltar`。`cache get` 解包前会比较 `.ltar` 头部里 Lake 的 dep hash 和本地 `.trace` 文件；两者一致就跳过解包【仅见摘要】：https://github.com/leanprover-community/mathlib4/pull/42660
- 2023 年服务器上有两类对象：`f/<hash>.ltar` 按文件存，和具体提交无关；`c/<commit>` 记录某个提交包含哪些文件【仅见摘要】：https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/lean-cache.3A.20lake.20exe.20cache.20rewrite.html
- 早期出过一个坑：Mathlib 的 cache 计算的哈希和 Lake 的哈希不一致，涉及换行归一化，结果跨 OS 不一致【仅见摘要】：https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Lake.20hashes.20are.20OS.20dependent.html
- 现行公开端点是 `https://cache.mathlib.org`，按容器 `mathlib4-{name}` 划分。`mathlib4-master` 只由 master CI 写入，布局为扁平的 `/f/<hash>.ltar`。旧端点是 `lakecache.blob.core.windows.net`（Azure）【仅见摘要】：https://github.com/PalomarRegistry/PalomarSubmission/issues/189 。该 issue 还给出一个规模数：某个 Mathlib 提交需要 9083 个缓存哈希。
- 写入策略：写 `forks` 容器的构建只上传到 Cloudflare R2；写 master 的构建（master、bors staging、`v4.*` 标签）同时上传 Azure 和 R2【仅见摘要】：https://github.com/leanprover-community/mathlib4/pull/44639
- 上传必须用 curl 8.20 以上版本，CI 安装一个固定版本的静态 curl；上传超时 20 min，构建后检查超时 30 min【仅见摘要】：https://github.com/leanprover-community/mathlib4/pull/44940
- 下载失败时会在第二轮“新的一遍”里重试；某个文件始终失败则以非零状态退出【仅见摘要】：https://github.com/leanprover-community/mathlib4/pull/45096
- 下游项目取用：
  - `lean-action` 会把 `MATHLIB_CACHE_GET_URL` 设成 cache.mathlib.org【仅见摘要】：https://github.com/leanprover/lean-action/pull/202
  - 新功能 `lake exe cache get MyProject.Basic` 只拉取该模块传递依赖到的那部分 Mathlib 模块【仅见摘要】：https://github.com/leanprover-community/mathlib4/pull/45905
- 背景数据：2022 年 mathlib3 的 CI 超过 3 h；M1 Max 本地构建约 75 min【仅见摘要】：https://leanprover-community.github.io/archive/stream/113488-general/topic/build.20mathlib.html

---

## 3. Lake 产物缓存（v4.30.0 大改）与 Reservoir【原文】

来源：https://lean-lang.org/doc/reference/latest/releases/v4.30.0/ （2026-05-26 发布）；https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/

**v4.30.0 的“Lake Cache Overhaul”**
- `lake build` 可以在需要时按需从远程缓存下载产物（#12634）。
- `lake cache get` 改成默认就下载产物；加 `--mappings-only` 则只拿映射，产物延后到用时再取（#12927）。
- `cache get/put` 用 `curl --parallel` 并行传输（#12974）。
- 产物 URL 一次批量 POST 从 Reservoir 拿到，不再每个产物走一次重定向。原来的重定向方式会打到 Netlify，既慢又容易被限流（#13164）。
- 通过 `leantar` 打包、解包 `.ltar`（#12914）。
- 新增 `lake cache stage / unstage / put-staged`，对标 Mathlib 的同名命令（#13144）。
- 新增 `fixedToolchain` 选项：用于只支持单一 toolchain 的包（例如 Mathlib），这样映射不必再按 toolchain 版本分开存（#12935）。
- `CacheMap` 开始记录输出是否依赖平台（#12954）。
- 修了一个竞态：两个 facet 产出内容哈希相同的产物时会并发写冲突（#13110）。

**缓存键与机制（Lake 参考手册）**
- trace 文件里存的是输入哈希的 “Merkle tree hash mixture”。trace 同时记录构建日志，命中缓存时把日志回放出来。
- 有两套哈希：文本文件先归一化换行再哈希，其他文件按原样哈希。模块的 `depHash` 覆盖 imports、源码和插件。
- 本地产物缓存**每个 toolchain 一份**，因为不同 toolchain 的中间产物不兼容。可以用 `LAKE_CACHE_DIR` 指定位置。这个功能标注为实验性。
- `lake build -o <file>` 生成 JSONL 格式的 *mappings* 文件，记录每一步的输入到输出，已经是最新的目标也包含在内。`lake cache put` 依据这个文件上传。
- 远程服务分两类：S3 兼容和 Reservoir API。两类都按**内容哈希**索引产物。S3 布局如下：
  - 产物：`ARTS/SCOPE/HASH.art`；
  - 映射：`REVS/SCOPE/COMMIT.jsonl`，按 Git 提交存；
  - 用 `--repo` 时，映射目录还会编码平台和 toolchain；
  - 上传用 AWS SigV4，密钥来自 `LAKE_CACHE_KEY`。
- `lake cache get` 不指定 `--rev` 时，从当前提交往回找最近一个有映射的提交，默认最多回溯 100 个。单个产物下载失败时继续下载其余的，最后以非零状态退出。
- `lake cache stage <mappings> <dir>`：把映射和对应产物复制到一个目录。`put-staged` 上传这个目录，它**不配置 workspace，所以不执行任意用户代码**。
- 包可以声明 `downloadCacheService`。首次构建前先取映射，之后按需取产物。
- 也可以自建 Reservoir 兼容的服务，手册提到适用于需要审计、或因政策不能连 Reservoir 的组织。
- 实测（第三方）：riemann-hypothesis 仓库用 R2 自定义域名提供 Lake 缓存。从空缓存全量 `lake cache get` 拉了 175,187 个归档、约 4.94 GB，用时 4 min 47 s；之前用 r2.dev 域名时遇到了限流【仅见摘要】：https://github.com/leanprover-community/riemann-hypothesis/pull/7

---

## 4. 其他：Nix、Bazel、并行内核重放

**Nix**
- 社区维护的 lean4-nix 说明：官方 Nix flake 在 v4.11.0 时废弃。`buildLeanPackage` 接收 `{name; roots; deps; src}`，依赖需要手工管理【仅见摘要】：https://github.com/lenianiva/lean4-nix
- Sebastian Ullrich 2023 年说，对 Mathlib 来说“一个包一个 derivation”行不通，除非做成固定输出的 derivation（FOD）直接下载缓存【仅见摘要】：https://leanprover-community.github.io/archive/stream/270676-lean4/topic/nix.3A.20buildLeanPackage.20vs.2E.20lakefile.html
- “每个模块一个 derivation”和“配 Nix 远程构建器做多机构建”这两点：【未找到】一手来源确认。我记得旧版官方 Nix 构建是按模块拆分的，但这次没有核实。

**Bazel / Buck2**
- atvrager/rules_lean 每个模块一个 Bazel action。olean 字节一致时，Bazel 会跳过下游的 importer【仅见摘要】：https://github.com/atvrager/rules_lean
- pulseengine/rules_lean 支持 Mathlib：https://github.com/pulseengine/rules_lean 。tomato-bazel/rules_lean 通过 Lake 复用 Mathlib 缓存：https://github.com/tomato-bazel/rules_lean 。两者均【仅见摘要】。
- 这些规则的远程执行和多机实测数据：【未找到】。Buck2 的 Lean 规则：【未找到】。

**并行内核重放（复核环节）**
- lean4 RFC #15569【原文】：https://github.com/leanprover/lean4/issues/15569
  - 提议给 `Environment.replay` 加一个可选的并行模式：每个定理先不检查直接加入环境，再在一个 Task 里对照“它之前那一刻的环境”调用 `addDeclCore` 检查；非定理声明仍然顺序检查；所有 Task 结束后才做 constructor/recursor 的延后检查。
  - 作者说改动约 25 行。由于定理是对照不含它自身的环境检查的，循环依赖仍然不可能出现。
  - 实测：一个约 100 GB、2210 万个常量的导出，单线程预计要 1–2 周；并行版本在一台机器上用 342 线程跑了 83 h，验证通过。
  - 状态：FRO 尚未决定官方 replay 是否要多线程化。
- comparator PR #99【原文，部分】：https://github.com/leanprover/comparator/pull/99
  - 新增 `parallel_replay` 配置项，默认关闭；
  - 测试覆盖有效输入和伪造输入：错误类型的证明、后面被引用的错误引理、循环定理、错误类型的定义，要求与串行 replay 给出相同结论；
  - 审阅者要求尽量 import 而不是复制代码，以缩小可信计算基（TCB）。
- 第三方数据：Layr-Labs 在 6 个 worker 下把一次 replay 从约 17,242 s 降到 2,300 s（约 7.5 倍），峰值内存约 96 GiB；12 个 worker 时因超过 112 GiB 的 cgroup 上限被 OOM 杀掉【仅见摘要】：https://github.com/Layr-Labs/evm.fast-dev/pull/29

**其他 Lean 项目的经验数据**
- 约 5,300 个 Stacks 模块冷构建用了 3 h 50 min，内存不足曾导致 runner 失联【仅见摘要】：https://github.com/Commutator-IO/GrothendieckArchivesProofs/issues/34
- cslib 按编译耗时加权计算关键路径，结论是在 4 核下墙钟时间跟总工作量走，不需要拆导入链；另一个问题是 build 和 test 分成两个步骤，形成了不必要的屏障【仅见摘要】：https://github.com/cslib-community/cslib-frontier/issues/622

---

## 5. 对我们设计的启示（以下均为推断）

**可以直接借用的**
1. **Isabelle 的排程算法**：把每个模块（或模块簇）× 机器 × 线程数建成 MRCPSP 的“模式”。
   - 用历史耗时加 Amdahl 插值估计耗时，估计值略微放大；
   - 按关键路径找出关键节点，把最快的机器留给它们；
   - 非关键节点的线程数按耗时分档（参考档位：1 min / 5 min → 1 / 4 / 8 线程）；
   - 对参数做扫描，构建中每 5 min 重排一次。

   求解只要几秒，不依赖 CPLEX。冷启动时先用贪心策略（按最长后继路径优先），积累 7–8 次构建后再切到排程。
2. **Lake 原生的缓存协议当作节点之间的“产物总线”**：
   - 每个 worker 构建完执行 `lake build -o` 和 `lake cache put`（或 `stage` + `put-staged`），按内容哈希写入一个 S3 兼容的桶（自建 MinIO 或 R2）；
   - 下游 worker 用 `--mappings-only` 加按需下载取上游产物。

   这对应 Isabelle“数据库存 heap、本地盘当缓存”的思路，而且不需要共享文件系统。缓存键直接沿用 Lake 的 depHash（Merkle 混合了源码、imports 和插件，并按 toolchain 隔离），或者 Mathlib 的 `rootHash + pathHash + 内容 + imports`。不建议自己发明一套键。
3. **Mathlib 的信任分级**：可信的 master 容器只允许受控构建写入，PR/fork 只能读或写到单独的容器。分布式 worker 的产物先进“未复核区”，复核通过后再提升到可信区。
4. **复核环节**：汇总后用 comparator 或 lean4checker 做内核重放。并行重放（RFC #15569）可以把复核本身也并行化，但要按内存给 worker 数设上限，参考第三方的 OOM 数据。

**需要注意的差异和风险**
- Isabelle 的单位是 session，几十到几百个，而且依赖图是树。Lean 是几千个模块组成的 DAG，例如一个 Mathlib 提交约 9000 个模块哈希。排程粒度要么把模块聚成簇，要么接受启发式在更大规模上的表现，后者没有先例数据。
- 模块粒度细时，传输和解包开销占比高：Isabelle 的 HOL heap 50 MiB 要 1.5 s 提交，Lake 小文件则靠并行 curl 和批量 URL 获取来摊薄。建议按导入图切分时，只在跨机器的边上传输产物。
- 失败处理没有现成的先例。Isabelle 论文没写；Lake 只有下载失败继续、最后非零退出；Mathlib 有二次重试。需要自己设计：心跳检测、任务超时后重新派发、结果是否幂等（内容哈希天然可以去重）。
- Isabelle 的历史耗时数据库（`build_log`）是排程质量的前提，我们需要从第一天就记录每个模块的耗时、机器和线程数。

---

## 未完成 / 未核实
- Mathlib 的 `build_template.yml`、`Cache/README.md`、`Cache/CI.md` 原文没读到（抓取被限流，工具额度也用完了）。机器规格和全量构建时间只有 PR 摘要里的零散数字。
- Nix 每模块 derivation 和远程构建器、Buck2 规则：无一手证据。
- 各 PR 和 issue 的日期显示为 2026 年。这些只是摘要内容，合并状态没有核实。
