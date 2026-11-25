# 参考文献与出处

正文里方括号中的编号对应本文件：**[T…]** 调度理论的论文，**[S…]** 各系统的文档与源码，**[D…]** 公开的构建数据。`docs/scheduling-theory.md` 用“作者 年份”引用论文，对应下面 T 类中同一作者年份的条目；`docs/research/` 的三份笔记在正文里直接给了网址，这些网址都收在 D 类与 S 类里。

每条标明我们读到了什么程度：

- **全文**：读了全文或全部相关章节；
- **相关段落**：读了支撑我们说法的那几段（源码文件、文档的某一节、帖子的某一条）；
- **摘要**：只读了摘要、检索摘要或书目数据库里的条目，结论未对照原文；
- **未重新核对**：凭先前的知识写入，这次没有再查。

T 类各条的作者、题目、出处、DOI 已对照 Crossref、DataCite 或 arXiv 的元数据（另注明的除外）。核对日期：2026-11-25。网址里的提交号是核对时的版本。

## T 调度理论的论文

| 编号 | 作者（年份） | 题目 | 出处 | DOI / 网址 | 阅读程度 |
|---|---|---|---|---|---|
| T1 | R. L. Graham (1966) | Bounds for certain multiprocessing anomalies | Bell System Technical Journal 45(9):1563–1581 | doi:10.1002/j.1538-7305.1966.tb01709.x | 摘要（经典结论，与 T23 综述一致） |
| T2 | R. L. Graham (1969) | Bounds on multiprocessing timing anomalies | SIAM J. Appl. Math. 17(2):416–429 | doi:10.1137/0117039 | 摘要 |
| T3 | T. C. Hu (1961) | Parallel sequencing and assembly line problems | Operations Research 9(6):841–848 | doi:10.1287/opre.9.6.841 | 摘要 |
| T4 | M. Fujii, T. Kasami, K. Ninomiya (1969) | Optimal sequencing of two equivalent processors | SIAM J. Appl. Math. 17(4):784–789 | doi:10.1137/0117070 | 摘要 |
| T5 | E. G. Coffman, R. L. Graham (1972) | Optimal scheduling for two-processor systems | Acta Informatica 1(3):200–213 | doi:10.1007/BF00288685 | 摘要 |
| T6 | E. B. Fernandez, B. Bussell (1973) | Bounds on the number of processors and time for multiprocessor optimal schedules | IEEE Trans. Computers C-22(8):745–751 | doi:10.1109/TC.1973.5009153 | 摘要（下界的形式按 arXiv:1901.07070 第 3.1 节的转述核对） |
| T7 | T. L. Adam, K. M. Chandy, J. R. Dickson (1974) | A comparison of list schedules for parallel processing systems | Communications of the ACM 17(12):685–690 | doi:10.1145/361604.361619 | 全文 |
| T8 | R. P. Brent (1974) | The parallel evaluation of general arithmetic expressions | J. ACM 21(2):201–206 | doi:10.1145/321812.321815 | 相关段落（引理 2） |
| T9 | J. D. Ullman (1975) | NP-complete scheduling problems | J. Computer and System Sciences 10(3):384–393 | doi:10.1016/S0022-0000(75)80008-0 | 摘要 |
| T10 | J. K. Lenstra, A. H. G. Rinnooy Kan (1978) | Complexity of scheduling under precedence constraints | Operations Research 26(1):22–35 | doi:10.1287/opre.26.1.22 | 摘要 |
| T11 | H. Kasahara, S. Narita (1984) | Practical multiprocessor scheduling algorithms for efficient parallel processing（CP/MISF） | IEEE Trans. Computers C-33(11):1023–1029 | doi:10.1109/TC.1984.1676376 | 摘要（Crossref 只有姓，名的缩写未核对） |
| T12 | V. J. Rayward-Smith (1987) | UET scheduling with unit interprocessor communication delays | Discrete Applied Mathematics 18(1):55–71 | doi:10.1016/0166-218X(87)90042-4 | 摘要 |
| T13 | S. J. Kim, J. C. Browne (1988) | A general approach to mapping of parallel computation upon multiprocessor architectures（线性聚类） | Proc. ICPP 1988, vol. 3, pp. 1–8 | 无 DOI | **未重新核对**（常见的二手引法，未找到可核对的目录） |
| T14 | V. Sarkar (1989) | Partitioning and Scheduling Parallel Programs for Multiprocessors（边归零） | Pitman / MIT Press，ISBN 0-262-69130-2 | — | 摘要（只见检索摘要） |
| T15 | J.-J. Hwang, Y.-C. Chow, F. D. Anger, C.-Y. Lee (1989) | Scheduling precedence graphs in systems with interprocessor communication times（ETF） | SIAM J. Comput. 18(2):244–257 | doi:10.1137/0218016 | 摘要 |
| T16 | A. Gerasoulis, T. Yang (1993) | On the granularity and clustering of directed acyclic task graphs | IEEE Trans. Parallel Distrib. Syst. 4(6):686–701 | doi:10.1109/71.242154 | 相关段落（原文未取到；按作者的技术报告 UCSB TR 1994-12 第 5.1 节核对定义与定理） |
| T17 | C. H. Papadimitriou, M. Yannakakis (1990) | Towards an architecture-independent analysis of parallel algorithms | SIAM J. Comput. 19(2):322–328 | doi:10.1137/0219021 | 摘要 |
| T18 | T. Yang, A. Gerasoulis (1994) | DSC: scheduling parallel tasks on an unbounded number of processors | IEEE Trans. Parallel Distrib. Syst. 5(9):951–967 | doi:10.1109/71.308533 | 相关段落（同上技术报告） |
| T19 | J. A. Hoogeveen, J. K. Lenstra, B. Veltman (1994) | Three, four, five, six, or the complexity of scheduling with communication delays | Operations Research Letters 16(3):129–137 | doi:10.1016/0167-6377(94)90024-8 | 摘要 |
| T20 | A. Munier, J.-C. König (1997) | A heuristic for a scheduling problem with communication delays（4/3 近似） | Operations Research 45(1):145–147 | — | **未重新核对** |
| T21 | D. B. Shmoys, J. Wein, D. P. Williamson (1995) | Scheduling parallel machines on-line | SIAM J. Comput. 24(6):1313–1331 | doi:10.1137/S0097539793248317 | **未重新核对**（结论未读原文） |
| T22 | R. D. Blumofe, C. E. Leiserson (1999) | Scheduling multithreaded computations by work stealing | J. ACM 46(5):720–748 | doi:10.1145/324133.324234 | 摘要 |
| T23 | Y.-K. Kwok, I. Ahmad (1999) | Static scheduling algorithms for allocating directed task graphs to multiprocessors | ACM Computing Surveys 31(4):406–471 | doi:10.1145/344588.344618 | 相关段落（综述，用于核对经典结论） |
| T24 | L. Epstein (2000) | A note on on-line scheduling with precedence constraints on identical machines | Information Processing Letters 76(4–6):149–153 | doi:10.1016/S0020-0190(00)00141-1 | 摘要 |
| T25 | Y. Azar, L. Epstein (2002) | On-line scheduling with precedence constraints | Discrete Applied Mathematics 119(1–2):169–180 | doi:10.1016/S0166-218X(01)00272-4 | 摘要 |
| T26 | R. Lepère, D. Trystram, G. J. Woeginger (2002) | Approximation algorithms for scheduling malleable tasks under precedence constraints | Int. J. Found. Comput. Sci. 13(4):613–627 | doi:10.1142/S0129054102001308 | 摘要 |
| T27 | H. Topcuoglu, S. Hariri, M.-Y. Wu (2002) | Performance-effective and low-complexity task scheduling for heterogeneous computing（HEFT） | IEEE Trans. Parallel Distrib. Syst. 13(3):260–274 | doi:10.1109/71.993206 | **未重新核对**（结论） |
| T28 | K. Jansen, H. Zhang (2006) | An approximation algorithm for scheduling malleable tasks under general precedence constraints | ACM Trans. Algorithms 2(3):416–434 | doi:10.1145/1159892.1159899 | 摘要 |
| T29 | O. Svensson (2010 / 2011) | Conditional hardness of precedence constrained scheduling on identical machines（会议版）；Hardness of precedence constrained scheduling on identical machines（期刊版） | STOC 2010, 745–754；SIAM J. Comput. 40(5):1258–1274 | doi:10.1145/1806689.1806791；doi:10.1137/100810502 | 全文（会议版） |
| T30 | M. Zaharia, D. Borthakur, J. Sen Sarma, K. Elmeleegy, S. Shenker, I. Stoica (2010) | Delay scheduling: a simple technique for achieving locality and fairness in cluster scheduling | EuroSys 2010, 265–278 | doi:10.1145/1755913.1755940 | **未重新核对**（结论） |
| T31 | K. Jansen, H. Zhang (2012) | Scheduling malleable tasks with precedence constraints | J. Computer and System Sciences 78(1):245–259 | doi:10.1016/j.jcss.2011.04.003 | 摘要 |
| T32 | C.-Y. Chen, C.-P. Chu (2013) | A 3.42-approximation algorithm for scheduling malleable tasks under precedence constraints | IEEE Trans. Parallel Distrib. Syst. 24(8):1479–1488 | doi:10.1109/TPDS.2012.258 | 摘要 |
| T33 | E. Levey, T. Rothvoss (2016) | A (1+ε)-approximation for makespan scheduling with precedence constraints using LP hierarchies | STOC 2016, 168–177 | doi:10.1145/2897518.2897532；arXiv:1509.07808 | 相关段落（arXiv 版） |
| T34 | R. Grandl, S. Kandula, S. Rao, A. Akella, J. Kulkarni (2016) | GRAPHENE: packing and dependency-aware scheduling for data-parallel clusters | OSDI 2016, 81–97 | https://www.usenix.org/conference/osdi16/technical-sessions/presentation/grandl_graphene | **未重新核对**（结论） |
| T35 | S. Garg (2018) | Quasi-PTAS for scheduling with precedences using LP hierarchies | ICALP 2018, LIPIcs 107, 59 | doi:10.4230/LIPIcs.ICALP.2018.59；arXiv:1708.04369 | 相关段落（arXiv 版） |
| T36 | H. Mao, M. Schwarzkopf, S. B. Venkatakrishnan, Z. Meng, M. Alizadeh (2019) | Learning scheduling algorithms for data processing clusters（Decima） | SIGCOMM 2019, 270–288 | doi:10.1145/3341302.3342080 | **未重新核对**（结论） |
| T37 | J. Kulkarni, S. Li, J. Tarnawski, M. Ye (2020) | Hierarchy-based algorithms for minimizing makespan under precedence and communication constraints | SODA 2020, 2770–2789 | doi:10.1137/1.9781611975994.169；arXiv:2004.13891 | 相关段落（arXiv 版） |
| T38 | C.-Y. Chen (2026) | 可塑任务调度近似比的改进（预印本，未经同行评议） | arXiv:2611.15111 | https://arxiv.org/abs/2611.15111 | 相关段落 |

## S 系统的文档与源码

| 编号 | 系统 | 文档或源码 | 网址（版本） | 支撑的说法 | 阅读程度 |
|---|---|---|---|---|---|
| S1 | Lake | Lean 语言参考手册：Lake 一章（缓存、trace、`lake build -o`、远程缓存服务） | https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/ | 缓存键、映射文件、S3 与 Reservoir 两类服务 | 相关段落 |
| S2 | Lean / Lake | v4.22.0 发行说明（#8922：本地产物缓存） | https://lean-lang.org/doc/reference/latest/releases/v4.22.0/ | 本地产物缓存始于 4.22 | 相关段落 |
| S3 | Lean / Lake | v4.25.0 发行说明；PR #10188 “`lake cache` (& remote cache support)”（2025-09-26 合并） | https://lean-lang.org/doc/reference/latest/releases/v4.25.0/ ；https://github.com/leanprover/lean4/pull/10188 | `lake cache`、`lake build -o`、远程缓存始于 4.25；哈希不抗碰撞 | 相关段落 |
| S4 | Lean / Lake | v4.29.0 发行说明（#12490：系统级远程服务配置） | https://lean-lang.org/doc/reference/latest/releases/v4.29.0/ | — | 相关段落 |
| S5 | Lean / Lake | v4.30.0 发行说明，“Lake Cache Overhaul”（2026-05-26） | https://lean-lang.org/doc/reference/latest/releases/v4.30.0/ | 按需下载、批量取地址、`.ltar`、分段上传 | 相关段落 |
| S6 | Lake | 源码：`src/lake/Lake/Build/Job/Monad.lean`（任务都是默认优先级）、`Lake/CLI/Help.lean`（没有 `-j`）、`Build/Module.lean`、`Build/Actions.lean` | https://github.com/leanprover/lean4/tree/v4.35.0/src/lake （及本地 4.33.1 / 4.35.0 源码） | Lake 的调度、调用 `lean` 的方式、无优先级 | 相关段落 |
| S7 | Lean | 语言参考：Tasks and Threads（`LEAN_NUM_THREADS`） | https://lean-lang.org/doc/reference/latest/IO/Tasks-and-Threads/ | 线程池大小 | 相关段落 |
| S8 | Mathlib | `Cache/README.md`、`Cache/Hashing.lean`、`Cache/Infra.lean` | https://github.com/leanprover-community/mathlib4/tree/56a005855ea17e0b0958f73ec801ae140b0a1679/Cache | `lake exe cache` 的缓存键与存放 | 相关段落 |
| S9 | Ninja | v1.12.0 发行说明；PR #2177（按关键路径排优先级，每条边权重 1）；PR #2686（按 `.ninja_log` 耗时加权，2026-09 并入 master，截至 v1.13.2 未发布）；`src/build.cc` | https://github.com/ninja-build/ninja/pull/2177 ；https://github.com/ninja-build/ninja/pull/2686 | Ninja 只按层数排 | 相关段落 |
| S10 | Bazel | `ResourceManager.java`（本地先进先出）、`RemoteOptions.java`（`--remote_execution_priority`）、`metrics/criticalpath/CriticalPathComputer.java`（只用于报告）；命令行参考 | https://github.com/bazelbuild/bazel/blob/7.4.0/src/main/java/com/google/devtools/build/lib/remote/options/RemoteOptions.java ；https://bazel.build/reference/command-line-reference | Bazel 不按关键路径派发 | 相关段落 |
| S11 | Bazel | Issues #16054、#18686、#16913（输入极多的动作很慢、内存不足） | https://github.com/bazelbuild/bazel/issues/16054 （另两条同） | 大输入树的开销 | 相关段落（正文开头） |
| S12 | Bazel | “Build without the Bytes in Bazel 7”（博客，2023-10-06） | https://blog.bazel.build/2023/10/06/bwob-in-bazel-7.html | 只减少输出下载 | 摘要 |
| S13 | Bazel | Remote Execution Overview | https://bazel.build/remote/rbe | 远程执行的结构 | 全文 |
| S14 | Buck2 | Remote Execution 文档；`host_sharing.rs`；`buck2_critical_path` | https://buck2.build/docs/users/remote_execution/ ；https://github.com/facebook/buck2 | 本地公平排队，关键路径只用于报告 | 全文（文档）/ 相关段落（源码） |
| S15 | Pants | Remote caching & execution（2.33） | https://www.pantsbuild.org/stable/docs/using-pants/remote-caching-and-execution | 使用 Remote Execution API | 全文 |
| S16 | Remote Execution API | `remote_execution.proto` v2.12.0（Action、ExecutionPolicy.priority、ResultsCachePolicy、PriorityCapabilities） | https://github.com/bazelbuild/remote-apis/blob/v2.12.0/build/bazel/remote/execution/v2/remote_execution.proto | 动作的定义与优先级字段 | 相关段落 |
| S17 | Buildbarn | `pkg/scheduler/in_memory_build_queue.go`；`bb_worker.proto`；ADR #9（NFSv4）、#10（文件系统访问缓存） | https://github.com/buildbarn/bb-remote-execution/blob/e9f6d456803e9ef236e6fc3db3107050b63298b1/pkg/scheduler/in_memory_build_queue.go ；https://github.com/buildbarn/bb-adrs | 优先级的含义；大输入根初始化慢 | 相关段落 |
| S18 | BuildGrid | README；`buildgrid/server/scheduler/impl.py`；`execution/service.py` | https://gitlab.com/BuildGrid/buildgrid/-/tree/5297cd639df65298af2b6bb97d89c8c61fa7f45f | 升序优先级、重复请求提升 | 相关段落 |
| S19 | Buildfarm | README；配置文档；`RedisPriorityQueue.java`（2.18.1） | https://github.com/buildfarm/buildfarm/tree/769a6e4c8738b2585ddc4b7e2bce4dff9f8ed12f | `priorityQueue` 默认关闭 | 相关段落 |
| S20 | NativeLink | “Protocol API: intentional deviations”；`running_actions_manager.rs`（v1.9.0） | https://github.com/TraceMachina/nativelink/tree/c44dd8ade2d7582713e425cfa6f14beb4d4cea7d | 数值大的优先级先跑；逐文件硬链接输入 | 相关段落 |
| S21 | recc | README；配置说明（现已并入 buildbox） | https://gitlab.com/BuildGrid/recc/-/tree/0f0115d32236f459b5cfc0f7b82283c92c01ccc6 | 包装 C/C++ 编译命令 | 相关段落 |
| S22 | reclient | README | https://github.com/bazelbuild/reclient/blob/9d90f13c0cb407b2c8e95201044ea3b7c3183341/README.md | rewrapper、reproxy、scandeps | 相关段落 |
| S23 | Chromium / Siso | chromium-dev 公告（2025-06-16）；`build/toolchain` 提交 7e350a0（2025-11-13） | https://groups.google.com/a/chromium.org/g/chromium-dev/c/v-WOvWUtOpg ；https://chromium.googlesource.com/chromium/src/build/toolchain/+/7e350a0af74b5eaeb5cadbd4d5e6e33426b05cc8 | reclient 被 Siso 取代 | 相关段落 |
| S24 | distcc | `man/distcc.1`（pump 模式一节） | https://github.com/distcc/distcc/blob/8d569d192141615e26a3f0b65315822e7c814c3d/man/distcc.1 | 普通与 pump 模式 | 相关段落 |
| S25 | icecream | README | https://github.com/icecc/icecream/blob/37cb407940a18aee5b444cc6d9d75dd2aaccf86d/README.md | 中央调度器、打包编译器环境 | 相关段落 |
| S26 | ccache | ccache(1) 手册 4.14.3 | https://ccache.dev/manual/latest.html | 三种模式、串接 distcc、远程存储 | 相关段落 |
| S27 | sccache | README、`docs/Caching.md`、`docs/Distributed.md`（v0.20.1） | https://github.com/mozilla/sccache/tree/1c7b8fcfd7b5a38d680b2bf8bf76f05902a6e33a | 缓存键、存储后端、sccache-dist | 相关段落 |
| S28 | Nix | 参考手册：Remote Builds；Experimental Features（ca-derivations） | https://nix.dev/manual/nix/stable/advanced-topics/distributed-builds ；https://nix.dev/manual/nix/stable/development/experimental-features.html | 远程构建机；按内容寻址仍是实验特性 | 相关段落 |
| S29 | Hydra | README | https://github.com/NixOS/hydra/blob/master/README.md | Nix 的持续集成 | 相关段落 |
| S30 | Lean 4 的 Nix 构建 | `nix/buildLeanPackage.nix`（移除前的最后版本）；PR #4895（2024-08-02 弃用）、#8335、#9910（2025-08-14 移除） | https://github.com/leanprover/lean4/blob/f86b192ec2/nix/buildLeanPackage.nix ；https://github.com/leanprover/lean4/pull/9910 | 每模块一个 derivation，已移除 | 相关段落 |
| S31 | lean4-nix（社区） | README | https://github.com/lenianiva/lean4-nix | 官方 flake 在 v4.11.0 废弃 | 摘要 |
| S32 | Isabelle | F. Huch, M. Wenzel, “Distributed Parallel Build for the Isabelle Archive of Formal Proofs”, ITP 2024, LIPIcs 309, 22:1–22:19 | doi:10.4230/LIPIcs.ITP.2024.22 | 经典与新引擎、关键 session、线程分档、每 5 分钟重排、AFP 35 分 40 秒 | 全文 |
| S33 | Dask | `dask/order.py`；work stealing 文档 | https://github.com/dask/dask/blob/main/dask/order.py ；https://distributed.dask.org/en/stable/work-stealing.html | 静态排序按结构；按代价偷取 | 相关段落 |
| S34 | Spark | 配置 `spark.locality.wait`（延迟调度） | https://spark.apache.org/docs/latest/configuration.html | 延迟调度是 Spark 的机制 | **未重新核对** |
| S35 | Pegasus | 站点选择器文档（HEFT 可选，默认随机） | https://pegasus.isi.edu/documentation/ | — | 相关段落（第一轮核对；具体页面网址未记录） |
| S36 | GNU make | 手册：Parallel Execution | https://www.gnu.org/software/make/manual/make.html#Parallel | 没有规定派发顺序 | 相关段落 |
| S37 | rules_lean | atvrager/rules_lean、pulseengine/rules_lean、tomato-bazel/rules_lean | https://github.com/atvrager/rules_lean | 每模块一个 Bazel 动作 | 摘要 |
| S38 | Mathlib CI 与缓存 | PR #45594、#45223、#44603、#42660、#44639、#44940、#45096、#45905；lean-action PR #202；Mathlib Initiative 路线图 | https://github.com/leanprover-community/mathlib4/pull/44603 （其余同一仓库）；https://mathlib-initiative.org/roadmap/ | `docs/research/precedents-infra.md` 第 2 节的各条 | 摘要 |
| S39 | Lean | v4.16.0–v4.19.0 发行说明（文件内并行 elaboration 的演进） | https://lean-lang.org/doc/reference/latest/releases/v4.19.0/ | 单个 `lean` 进程的多线程 | 相关段落 |

## D 公开的构建数据

Zulip 链接是 `leanprover.zulipchat.com` 上的消息永久链接（2026 年 11 月的消息不在公开归档里，经 Zulip 的匿名公开接口读取）；黎曼猜想相关的两个话题已于 2026-11-25 移到新频道 “Riemann Hypothesis”，下面用的是当前位置。人名只用于说明出处。

| 编号 | 来源 | 网址（版本或时间） | 支撑的说法 | 阅读程度 |
|---|---|---|---|---|
| D1 | A. Sutherland（MIT），黎曼猜想 Lean 证明的核验页，及 `sandbox-timeline.txt`、`sandbox-build.sh`、`sandbox-build-continue.sh`、`nanoda.log` | https://math.mit.edu/~drew/grh/ （页面注明 2026-11-24 更新） | 原始构建逐模块直接调 `lean`；沙箱重建 192 核约 8 小时、`LEAN_NUM_THREADS` 从 192 降到 64 及锁争用的注释；产物含路径；LocModel 不确定；各内核的耗时与内存 | 全文 |
| D2 | Zulip 话题 “Discussion: Alpöge Proves the Riemann Hypothesis”：A. Sutherland 2026-11-20 16:55:59 UTC（8 台 192 核，一小时出头）；I. Dixit 2026-11-21 07:07:52 UTC（94 核虚拟机 401 分钟）；J. McCarthy 2026-11-20 15:30:39 UTC（192 核 / 235 GB 与 48 核 / 503 GB）；K. Morrison 2026-11-21 11:21:59 UTC（2 台 128 vCPU、1 TB 内存的 CI 机器） | https://leanprover.zulipchat.com/#narrow/channel/658556-Riemann-Hypothesis/topic/Discussion.3A.20Alp.C3.B6ge.20Proves.20the.20Riemann.20Hypothesis/near/642277830 （其余三条把末尾换成 642435200、642254199、642464560） | 多机构建一小时出头；单机各配置的用时 | 全文（各条） |
| D3 | Zulip 话题 “Running CI for the riemann hypothesis”，K. Morrison 2026-11-21 09:46:32 UTC | https://leanprover.zulipchat.com/#narrow/channel/583339-AI-authored-projects/topic/Running.20CI.20for.20the.20riemann.20hypothesis/near/642454231 | CI 机器的要求（Linux、至少 128 GiB 内存、建议 1 TiB SSD、`vm.max_map_count`） | 全文 |
| D4 | Zulip 话题 “Cleaning up the proof”，T. Qi 2026-11-22 12:29:03 UTC | https://leanprover.zulipchat.com/#narrow/channel/658556-Riemann-Hypothesis/topic/Cleaning.20up.20the.20proof/near/642656072 | 家用机构建：从 11-20 19:24 起，发帖时还差 2 个模块（约 41 小时是我们算的） | 全文 |
| D5 | Zulip 同 D2 话题，A. Sutherland 2026-11-22 04:01:48 UTC；lean4 issue #15498、PR #15499（2026-10-08 合并，提交 `64942e142f2cbd3576ad89c3df41f8b6ccee91d9`） | https://leanprover.zulipchat.com/#narrow/channel/658556-Riemann-Hypothesis/topic/Discussion.3A.20Alp.C3.B6ge.20Proves.20the.20Riemann.20Hypothesis/near/642606582 ；https://github.com/leanprover/lean4/pull/15499 | 一个由并行引起的不确定模块，4.36 修复 | 全文 |
| D6 | Zulip 话题 “Lean checkers on FLT”，S. Teżewski 2026-11-16 21:25:00 UTC | https://leanprover.zulipchat.com/#narrow/channel/113488-general/topic/Lean.20checkers.20on.20FLT/near/640875131 | 各内核检查 FLT 导出的耗时 | 全文 |
| D7 | Zulip 话题 “Lake parallel builds”（#lean4），M. Malone 2023-10-18 | https://leanprover-community.github.io/archive/stream/270676-lean4/topic/Lake.20parallel.20builds.html#397357167 | Lake 只能用 `LEAN_NUM_THREADS` 限线程；当年 16 线程机器建 Mathlib 23 分钟 | 相关段落 |
| D8 | leanprover-community/riemann-hypothesis：`verification/NOTES.md`、`verification/CACHE.md`、`verification/CI-RUNNERS.md`（提交 `246656fc62ac80c1214f48550138076c4f278569`）；PR #7（2026-11-21 合并） | https://github.com/leanprover-community/riemann-hypothesis/blob/246656fc62ac80c1214f48550138076c4f278569/verification/NOTES.md ；https://github.com/leanprover-community/riemann-hypothesis/pull/7 | 17.5 万个文件、带路径的产物、导出与路径无关、`.setup.json` 约 1 TB；缓存 4,938,217,979 字节、下载 4 分 47 秒、恢复 91 秒；CI 机器现要求 128 GiB 内存与 250 GiB SSD | 相关段落；PR #7 全文 |
| D9 | the-omega-institute/riemann-hypothesis：`README.md`、`verification/NOTES.md`、`ci/plan.py`、`ci/planning.py`、`ci/schedule.py`、`ci/parts.py`、`ci/groups.py`、`.github/workflows/lean-parts.yml`、`shard-batch.yml`（提交 `c7d25b3bfd7906388bb8eb0774e027a2b756a7b6`） | https://github.com/the-omega-institute/riemann-hypothesis/blob/c7d25b3bfd7906388bb8eb0774e027a2b756a7b6/README.md | 8,490 片、36 层、剩余最长路径优先、分片键与调度机制；48 核预计 7–10 小时 | README 全文；脚本相关段落（`docs/research/precedents-omega-shards.md` 是早先按 main 分支读的） |
| D10 | ishaan2006/rh-lean-reproduction README（提交 `5725b9321c17edae0fca610b4375af2bcfdfc05b`）；Zenodo doi:10.5281/zenodo.24477213 | https://github.com/ishaan2006/rh-lean-reproduction/blob/5725b9321c17edae0fca610b4375af2bcfdfc05b/README.md | 94 个作业、401 分钟；从 `.trace` 取原样 `lean` 命令重放 | 相关段落 |
| D11 | luosiallen/riemann-hypothesis-lean-verify：`README.md`、`VERIFICATION_LOG.md`（提交 `c24dff08c9f2bc2ba46c88cc0cb779d0c3a2a323`）；介绍文章（lilting.ch，2026-11-21） | https://github.com/luosiallen/riemann-hypothesis-lean-verify/blob/c24dff08c9f2bc2ba46c88cc0cb779d0c3a2a323/README.md ；https://lilting.ch/en/articles/riemann-hypothesis-lean-independent-verify | 288 核上 Lake 卡在锁上（30–50 模块/分钟）；自写调度器 1,350–1,700 模块/分钟、2 小时 0 分 33 秒 | 全文 |
| D12 | borism/riemann-hypothesis README（提交 `b0158490f208a20c0c83ad539c1273724650ccdd`）；issues #1、#3 | https://github.com/borism/riemann-hypothesis/blob/b0158490f208a20c0c83ad539c1273724650ccdd/README.md ；https://github.com/borism/riemann-hypothesis/issues/3 | 小机器的速率；约 390 核·时、最长链 201 个模块的估计 | 相关段落；issues 全文 |
| D13 | raissaramaruchti/rh-lean-check README（提交 `dbc0ac1b8260cfbfbdcb873109ee348b7ad01bd6`） | https://github.com/raissaramaruchti/rh-lean-check | 恢复 Omega 的分片后 `leanchecker --fresh`；分片发布进度 | 相关段落 |
| D14 | CFSG：Zulip 话题 “Discussion of Axiom's Classification of Finite Simple Groups” 中 N. Voss 2026-10-29 23:10:04 UTC 与 A. Hill 2026-11-10 22:05:02 UTC；AxiomMath/CFSG README（提交 `965a0775e82217494217503621b843e1b0e1e337`）；Axiom，“Formalizing the Enormous Theorem”（2026-10-26） | https://leanprover.zulipchat.com/#narrow/channel/113488-general/topic/Discussion.20of.20Axiom.27s.20Classification.20of.20Finite.20Simple.20Groups/near/636144990 （另一条 …/near/639291282）；https://github.com/AxiomMath/CFSG/blob/965a0775e82217494217503621b843e1b0e1e337/README.md ；https://axiommath.ai/research/the-enormous-theorem-formalized/ | 产物 208.3 GB；96 vCPU / 3 TB 机器、原版 Lake 32 线程 22.5 小时约 600 美元；重构后 6 小时（换了机型）；约 4,310 万行 | Zulip 全文；README 全文；文章经抓取工具摘要 |
| D15 | lean4 issue #15569（并行内核重放的 RFC，2026-10-08）；comparator PR #99（`parallel_replay`）；Layr-Labs/evm.fast-dev PR #29 | https://github.com/leanprover/lean4/issues/15569 ；https://github.com/leanprover/comparator/pull/99 ；https://github.com/Layr-Labs/evm.fast-dev/pull/29 | 约 100 GB 导出单线程预计 1–2 周，342 线程 83 小时；并行重放的内存 | 全文（前两条）；摘要（第三条） |
| D16 | Commutator-IO/GrothendieckArchivesProofs issue #34；cslib-community/cslib-frontier issue #622 | https://github.com/Commutator-IO/GrothendieckArchivesProofs/issues/34 ；https://github.com/cslib-community/cslib-frontier/issues/622 | 其他 Lean 项目的构建经验 | 摘要 |
| D17 | Zulip 归档话题：“lean-cache: lake exe cache rewrite”（2023）、“Lake hashes are OS dependent”、“build mathlib”（2022）；PalomarRegistry/PalomarSubmission issue #189 | https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/lean-cache.3A.20lake.20exe.20cache.20rewrite.html ；https://github.com/PalomarRegistry/PalomarSubmission/issues/189 | Mathlib 缓存的存放布局与历史 | 摘要 |
| D18 | 黎曼猜想 Lean 归档的原始提交 `40e56bab026552e089d7afcfeff08d2defb9c005`（2026-11-20，“Mirror the submission exactly as published”，两个仓库的根提交）；本组织的 fork `OmniCAS/riemann-hypothesis` | https://github.com/leanprover-community/riemann-hypothesis/commit/40e56bab026552e089d7afcfeff08d2defb9c005 | 本仓库导入图与 E1 结构的来源 | 相关段落（元数据） |

## 没有找到出处的说法

- Sutherland 的 8 台机器上模块怎么分配、产物怎么同步、`lean` 的完整参数：公开材料里没有（D1、D2 只给了“逐模块直接调 `lean`、一小时出头”）。
- Mathlib CI 是否把一次构建拆到多台机器：没找到证据（S38 只见摘要）。
- 各远程执行服务端对“输入根有十几万个文件”的动作有没有上限：没找到文档（S11、S17、S20 只说明开销随输入增长）。
- Lean 读取导入闭包里全部 `.olean`（按需加载省不了多少）：这是我们对 Lean 的理解，没有在这次核对里找到文档。
- T13（Kim–Browne 1988）的书目信息、T20（Munier–König 1997）的出处与结论：未核对。
