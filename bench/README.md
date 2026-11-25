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

**注意**：本仓库的 `lakeshard/` 是工具仓库提交 `550e631` 的快照。对照组用到的 `--priority fifo|structure`、`--fetch-delay` 和固定放置文件（`lakeshard assign`）在之后的版本里才有；A0、A1、B1 三类运行用这个快照即可复现。

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
| [`OmniCAS/pfr`](https://github.com/OmniCAS/pfr) | teorth/pfr | 提交 `1899ce8ed95fc310cce53d4c7ecfa2beb20ebec4`（2026-11-23）；工具链 `leanprover/lean4:v4.37.0-rc1`；Mathlib `c47f9ad906c5ec32a953f99911b446cd26dcc123` | **小仓库一档**：默认目标 `PFR`、`PFRPalomar` 共 74 个模块；约 2.2 万行、深 20、按行数估的可并行度约 2.5（2.25–2.6）是按 2026-11-05 的副本 `1ef23c3c` 估的 |
| [`OmniCAS/riemann-hypothesis`](https://github.com/OmniCAS/riemann-hypothesis) | leanprover-community/riemann-hypothesis | 原始提交 `40e56bab026552e089d7afcfeff08d2defb9c005`（2026-11-20，原样镜像所提交的归档） | **E4**（大集群）；导入图（`study/data/rh.trace.json.gz`）与 E1 三个实例的结构来源 |
| [`OmniCAS/riemann-hypothesis-omega`](https://github.com/OmniCAS/riemann-hypothesis-omega) | the-omega-institute/riemann-hypothesis | 提交 `c7d25b3bfd7906388bb8eb0774e027a2b756a7b6`（2026-11-22） | **参考实现**：在 GitHub 托管 runner 上按内容哈希分片构建的脚本（`ci/`、`.github/workflows/`），机制见 `docs/research/precedents-omega-shards.md` |
| [`OmniCAS/CFSG`](https://github.com/OmniCAS/CFSG) | AxiomMath/CFSG | 提交 `965a0775e82217494217503621b843e1b0e1e337`（2026-11-19） | **E4 之后**；尚未分析 |
| [`OmniCAS/TauCeti`](https://github.com/OmniCAS/TauCeti) | TauCetiProject/TauCeti | 提交 `5d7b2806e934a829dab114bb0fe9e6653b54fe66`（2026-11-25） | **候选（RH 之前的中间台阶）**：库内 34,760 个模块、深 50；按 Mathlib 校准的模型（`study/scripts/tauceti_model.py`，只读 import 头）预测 W ≈ 57 核·时、最长链 8–17 分钟、可并行度约 200–450，32 / 128 / 512 核约 1.8 小时 / 27 分钟 / 8–17 分钟（按 2026-11-19 的副本估计，钉住的版本更新） |
| [`OmniCAS/Weil`](https://github.com/OmniCAS/Weil) | AxiomMath/Weil | 提交 `27cdb2049be62ee2911429b47f54774078450e32`（2026-11-06） | **候选**：980 个文件、深 17，按行数估的可并行度约 25（23–28；按 2026-11-19 的副本估计） |

除 Mathlib 外，这些仓库都是第三方代码，其中黎曼猜想归档、TauCeti、Weil、CFSG 是 AI 生成的形式化。**它们只在隔离环境里构建**（容器或沙箱，无外网、无凭据）：编译会执行仓库里的元程序。可并行度的估计只读了 import 头，没有构建。

Mathlib 从源码构建（不用缓存）的做法：`study/scripts/remote/setup_tarballs.py` 按 `lake-manifest.json` 的提交取各依赖的源码包并做成本地快照，`setup2.sh` 让 Lake 离线加载工作区，`build.sh ROOT RUN CPUS THREADS` 跑原版 `lake build` 并用 `procmon.py` 采样每个 `lean` 进程。线程伸缩的重放：`replay.py`、`replay_waves.py`；`import Mathlib` 的开销：`import_cost.sh`。

## 5 预期

见 [`expected.md`](expected.md)：E1–E4 每一格的预测值、容差与当前实测。
