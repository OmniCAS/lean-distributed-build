# 基准：怎么重新生成、怎么跑、预期是什么

## 1 实例

三个合成实例（E1）：结构取自黎曼猜想归档导入图的子闭包，文件内容由脚本生成、只导入 Lean 核心库，所以构建它们不执行任何第三方代码。每个模块的工作量按原文件的行数加权（重尾），见各生成脚本的文档字符串。**生成好的工程已放在 `instances/`**（mid 9.1 MB、wide 47.3 MB、narrow 1.7 MB），可以直接复制到机器上，不必先跑下面的命令。

| 实例 | 规格文件 | 模块 | 可并行度 W/CP（实测） | 重新生成 |
|---|---|---:|---:|---|
| mid（中图） | `specs/mid.spec.json.gz` | 3,156 | 31.7 | `python3 bench/gen/e1_gen.py write bench/specs/mid.spec.json.gz BASE/src/mid 0.2 2000` |
| wide（宽图） | `specs/wide.spec.json.gz` | 4,333 | 59.5–60.5 | `python3 bench/gen/e1_gen.py write bench/specs/wide.spec.json.gz BASE/src/wide 1.0 2000` |
| narrow（窄图，反例） | `specs/narrow.dag.json` | 2,613 | 约 5 | `python3 bench/gen/write_narrow.py bench/specs/narrow.dag.json BASE/src/narrow --toolchain v4.34.0` |

`write_narrow.py` 写出的源文件与原始实例逐字节相同（已核对）。规格文件本身是这样从归档的导入图得到的（要先取到归档源码，见第 4 节；只读 import 头，不执行代码）：

```bash
python3 -I bench/gen/dag_stats.py RH_SRC OUT/rh-dag    # RH_SRC：归档里 Lean 源码的根目录（含 Main.lean 的那一层）；输出导入图 graph.bin，模块名中的一个禁用词遮成 S··d
python3 -B bench/gen/e1_pick.py OUT/rh-dag/graph.bin pick.json --alpha 0.2 --kmax 2000   # 挑子闭包（mid 用 0.2，wide 用 1.0）
python3 -B bench/gen/e1_gen.py spec OUT/rh-dag/graph.bin ROOT_ID mid.spec.json.gz       # ROOT_ID 见 specs/pick-*.json
python3 -I bench/gen/gen_synthetic.py OUT/rh-dag/graph.bin OUT/narrow --target-closure 1500
```

## 2 机器与工具链

- Linux x86-64；每台机器上同一个绝对目录 `BASE`（例如 `/tmp/lakeshard-e1`），里面放：`lakeshard/`（本仓库的快照）、`tc/v4.34.0/`（官方 Lean v4.34.0 发布包 `lean-4.34.0-linux.tar.zst` 解开）、`src/<实例>/`（第 1 节生成的工程）、`token`（各机器相同的一个随机字符串）。
- 把 `run/hosts.example.json` 复制成 `run/hosts.json`，填每台机器的 SSH 别名、高速网络上的地址和 Python。
- 运行时每台机器把 worker 绑在 CPU 32..31+C 上、`nice -n 10`；协调器与产物库在 `--hosts` 的第一台上，绑 CPU 56–63。

## 3 跑

`run/queue.txt` 是全部配置（一行一次运行，名字在前），按顺序：

```bash
python3 -B bench/run/run_e1.py mid-A0-c16-r1 --hosts-file bench/run/hosts.json --project mid --mode lake --hosts worker-1 --cores 16
```

其余行同样，把 `queue.txt` 里该行的参数接在 `--hosts-file bench/run/hosts.json` 后面。记录落在 `bench/results/runs/<名字>/`。命名：A0 = 单机原版 `lake build`，A1 = 本工具单机，B1 = 本工具三机，B1s = 只按图结构排优先级，B4 = 先就绪先派，B2 / B3 = 预先按目录 / 沿导入链固定放置，`-dX` = 每次跨机取产物人为加 X 秒，`-cC` = 每台 C 个核。

**注意**：本仓库的 `lakeshard/` 是工具仓库提交 `e408d78` 的快照，也就是第 5 节阶段 1 验收用的版本；对照组用到的 `--priority fifo|structure`、`--fetch-delay` 和固定放置文件（`lakeshard assign`）它都有。

分析：

```bash
cd study
uv run --with numpy python t6_calibrate.py mid-A0-c16-r1 mid-B1-c16-r1 mid-A1-c16-r1 ../specs/mid.spec.json.gz   # 回测与最长链分解
uv run --with numpy python e1_expected.py                                                            # 每一格的预测与容差
```

## 4 关联的实验仓库（OmniCAS 下的 fork，钉住的版本）

| 仓库 | 上游 | 钉住的版本 | 用途 |
|---|---|---|---|
| [`OmniCAS/mathlib4`](https://github.com/OmniCAS/mathlib4) | leanprover-community/mathlib4 | 标签 `v4.34.0` = 提交 `5ed2965256430c3649e86755f9576b54eca72435`；工具链 `leanprover/lean4:v4.34.0` | **E2**（真实仓库的三机构建）；本仓库的 Mathlib trace（`study/data/mathlib.trace.json.gz`）就是用这个版本量的 |
| [`OmniCAS/carleson`](https://github.com/OmniCAS/carleson) | fpvandoorn/carleson | 提交 `f7487cc9da4d1e73f009dc0280cd5b958f3e2c78`（2026-11-17）；工具链 `leanprover/lean4:v4.36.0-rc1`；Mathlib `d88814353fcbcc0461c55b2a4585d3f44d903df1` | **小仓库一档**（`TODO.md` 阶段 1，只验正确性）：默认目标 `Carleson` 125 个模块、约 4.95 万行、深 30，按行数估的可并行度约 3（2.9–3.1） |
| [`OmniCAS/pfr`](https://github.com/OmniCAS/pfr) | teorth/pfr | **提交 `1ef23c3c5a83db690fe3b3b5c2e8299fae17b81a`**（上游 2026-11-05，在 fork 默认分支的历史里）；工具链 `leanprover/lean4:v4.36.0-rc2`；Mathlib `8fe7ce475b056f0b266d7107893f2c4d772c712f`，AddCombi `111b61aa52c0740a298d83967ff2394ff20dbbb4` | **小仓库一档，阶段 1 已在这个修订上通过**（第 5 节）：76 个模块、约 2.2 万行、深 20，按行数估的可并行度约 2.5（2.25–2.6）。fork 默认分支上更新的提交 `1899ce8ed95fc310cce53d4c7ecfa2beb20ebec4`（2026-11-23，工具链 v4.37.0-rc1，Mathlib `c47f9ad9…`，74 个模块）**没有验证过** |
| [`OmniCAS/riemann-hypothesis`](https://github.com/OmniCAS/riemann-hypothesis) | leanprover-community/riemann-hypothesis | 原始提交 `40e56bab026552e089d7afcfeff08d2defb9c005`（2026-11-20，原样镜像所提交的归档） | **E4**（大集群）；导入图（`study/data/rh.trace.json.gz`）与 E1 三个实例的结构来源 |
| [`OmniCAS/riemann-hypothesis-omega`](https://github.com/OmniCAS/riemann-hypothesis-omega) | the-omega-institute/riemann-hypothesis | 提交 `c7d25b3bfd7906388bb8eb0774e027a2b756a7b6`（2026-11-22） | **参考实现**：在 GitHub 托管 runner 上按内容哈希分片构建的脚本（`ci/`、`.github/workflows/`），机制见 `docs/research/precedents-omega-shards.md` |
| [`OmniCAS/CFSG`](https://github.com/OmniCAS/CFSG) | AxiomMath/CFSG | 提交 `965a0775e82217494217503621b843e1b0e1e337`（2026-11-19） | **E4 之后**；尚未分析 |
| [`OmniCAS/TauCeti`](https://github.com/OmniCAS/TauCeti) | TauCetiProject/TauCeti | 提交 `5d7b2806e934a829dab114bb0fe9e6653b54fe66`（2026-11-25） | **候选（RH 之前的中间台阶）**：库内 34,760 个模块、深 50；按 Mathlib 校准的模型（`study/scripts/tauceti_model.py`，只读 import 头）预测 W ≈ 57 核·时、最长链 8–17 分钟、可并行度约 200–450，32 / 128 / 512 核约 1.8 小时 / 27 分钟 / 8–17 分钟（按 2026-11-19 的副本估计，钉住的版本更新） |
| [`OmniCAS/Weil`](https://github.com/OmniCAS/Weil) | AxiomMath/Weil | 提交 `27cdb2049be62ee2911429b47f54774078450e32`（2026-11-06） | **候选**：980 个文件、深 17，按行数估的可并行度约 25（23–28；按 2026-11-19 的副本估计） |

除 Mathlib 外，这些仓库都是第三方代码，其中黎曼猜想归档、TauCeti、Weil、CFSG 是 AI 生成的形式化。**它们只在隔离环境里构建**（容器或沙箱，无外网、无凭据）：编译会执行仓库里的元程序。可并行度的估计只读了 import 头，没有构建。

Mathlib 从源码构建（不用缓存）的做法：`study/scripts/remote/setup_tarballs.py` 按 `lake-manifest.json` 的提交取各依赖的源码包并做成本地快照，`setup2.sh` 让 Lake 离线加载工作区，`build.sh ROOT RUN CPUS THREADS` 跑原版 `lake build` 并用 `procmon.py` 采样每个 `lean` 进程。线程伸缩的重放：`replay.py`、`replay_waves.py`；`import Mathlib` 的开销：`import_cost.sh`。

## 5 阶段 1：从一个干净的检出开始（PFR）

`TODO.md` 阶段 1 的四条标准，在 PFR 修订 `1ef23c3c` 上按下面的命令逐条通过（2026-11-25，一台 12 核 macOS 机器，`lakeshard/` 即 `e408d78`；Linux 上还没按这份命令跑过）。需要 git、elan、Python ≥ 3.11，磁盘约 12 GB（大部分是 Mathlib 的源码与缓存）。PFR 是第三方代码，编译会执行它的元程序：在隔离环境里做：不放凭据；除了第 1、5 步取依赖要访问 GitHub 与 Mathlib 的缓存，不联网。

```bash
# 0. 工具（本仓库里的 lakeshard/ 快照，无第三方依赖）
git clone https://github.com/OmniCAS/lean-distributed-build ldb
python3 -m venv ldb/.venv
ldb/.venv/bin/pip install -e ldb/lakeshard
export PATH="$PWD/ldb/.venv/bin:$PATH"

# 1. 仓库钉在验证过的修订；装它的工具链；Lake 克隆依赖并取 Mathlib 的缓存
git clone https://github.com/OmniCAS/pfr pfr
git -C pfr checkout 1ef23c3c5a83db690fe3b3b5c2e8299fae17b81a
(cd pfr && elan toolchain install "$(cat lean-toolchain)" && lake exe cache get)

# 2. 参照：原版 Lake 建一遍，供逐字节比对（AddCombi 不在 Mathlib 的缓存里，这一步顺带把它建了）
lakeshard reference pfr --build-dir ref

# 3. 仓库进、缓存出；中途杀掉一次（Ctrl-C 或 kill），再敲同一条命令
lakeshard run pfr --work work --workers 4 --slots 3 --threads 1
#    work/run.json 的 "build"："from_store"（杀掉前已建好、这次复用的）与 "built"；缓存在 work/cache

# 4. 与原版 Lake 逐字节一致，且 Lake 认它
lakeshard verify pfr --build-dir work/sealed --reference ref
#    "compare"：identical_files 516，different_count 0，missing_count 0；"lake_no_build"：ok

# 5. 另一处的全新检出：取 Mathlib 缓存，单独建 AddCombi，恢复，然后原版 Lake 不编译
git clone https://github.com/OmniCAS/pfr fresh
git -C fresh checkout 1ef23c3c5a83db690fe3b3b5c2e8299fae17b81a
(cd fresh && lake exe cache get && lake build AddCombi)
lakeshard restore work/cache --checkout fresh      # 先核对环境，再复制，最后跑 lake build --no-build
(cd fresh && lake build)                            # "Build completed successfully"，没有 "Built" 行

# 6. 改一个文件，只重建它和它的下游
printf '\ntheorem lakeshard_edit_probe : (2 : Nat) + 2 = 4 := rfl\n' >> pfr/PFR/ApproxHomPFR.lean
lakeshard run pfr --work work --workers 4 --slots 3 --threads 1
#    "build"：built 4（它与 3 个导入它的模块），from_store 72
git -C pfr checkout PFR/ApproxHomPFR.lean
```

| 步 | 实测 |
|---|---|
| 2 | 原版 `lake build` 58 秒，86 个模块（PFR 与 AddCombi） |
| 3 | 11 秒时杀掉，41/76 完成；同一条命令：41 个复用、35 个新建，52.8 秒；缓存 1,108 个文件、90 MB。另外 `lakeshard check-setup` 76/76 条 `lean` 调用与 Lake 一致 |
| 4 | 516/516 个文件一致；`lake build --no-build --rehash` 7,178 个任务全最新 |
| 5 | 全新检出里 AddCombi 建 14 个模块；`restore` 1,108 个文件 0.6 秒，环境一致；之后 `lake build` 编译 0 个模块 |
| 6 | 重建 4 个、复用 72 个，21.0 秒 |

输出在 [`results/step1-pfr/`](results/step1-pfr/)。几点说明：

- `restore` 拒绝工具链、平台、`lake-manifest.json` 或被导入的依赖模块的构建与缓存不一致的检出。第 5 步先建 AddCombi 就是为此：它不在 Mathlib 的缓存里，要由使用方自己建，被导入的那些模块建出来必须一致（实测一致；多建 AddCombi 的其他模块不影响）。
- 检出可以放在任意路径：Lake 的 trace 哈希与路径无关。
- `lakeshard run` 最后用原版 Lake 封口，缓存里是 Lake 自己的 `.trace` 与 `.hash`；Lake 记在 trace 里的命令行（带本机路径）被去掉了。
- Carleson（第 4 节）还没有按这份命令跑过。

## 6 预期

见 [`expected.md`](expected.md)：E1–E4 每一格的预测值、容差与当前实测。
