# 生成好的 E1 实例

三个合成工程，直接可建（`lake build`，工具链 `leanprover/lean4:v4.34.0`）；只导入 Lean 核心库，构建它们不执行任何第三方代码。由 `bench/README.md` 第 1 节的命令从 `bench/specs/` 生成，重新生成得到相同的文件。

| 目录 | 模块 | 文件总大小 | 可并行度 W/CP（实测） | 生成命令 |
|---|---:|---:|---:|---|
| `mid/` | 3,156 | 9.1 MB | 31.7 | `python3 bench/gen/e1_gen.py write bench/specs/mid.spec.json.gz bench/instances/mid 0.2 2000` |
| `wide/` | 4,333 | 47.3 MB | 59.5–60.5 | `python3 bench/gen/e1_gen.py write bench/specs/wide.spec.json.gz bench/instances/wide 1.0 2000` |
| `narrow/` | 2,613 | 1.7 MB | 约 5 | `python3 bench/gen/write_narrow.py bench/specs/narrow.dag.json bench/instances/narrow --toolchain v4.34.0` |

模块名沿用黎曼猜想归档的目录结构（前缀 `E1.`；窄图改编号为 `Syn.M<i>`）。窄图最初生成时 `lean-toolchain` 写的是 v4.33.1，E1 的运行用的是 v4.34.0 的工具链，这里统一写 v4.34.0；源文件与原始实例逐字节相同。
