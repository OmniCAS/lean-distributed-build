# 阶段 1 验收：PFR（单机）

`TODO.md` 阶段 1 的四条标准在公开仓库 PFR 上的实测输出。修订 `1ef23c3c5a83db690fe3b3b5c2e8299fae17b81a`（上游 2026-11-05），工具链 `leanprover/lean4:v4.36.0-rc2`，76 个模块，依赖 Mathlib 与 AddCombi；工具为本仓库的 `lakeshard/`（lakeshard `e408d78`）；一台 12 核 macOS 机器，2026-11-25。命令见 `bench/README.md` 第 5 节。路径已换成 `/work`，其余未动。

| 文件 | 内容 |
|---|---|
| `check-setup.json` | 本工具生成的 76 条 `lean` 调用与 Lake 的逐项一致 |
| `reference.json`、`reference.history.json` | 原版 `lake build`：58 秒，86 个模块（PFR 与 AddCombi），逐模块秒数 |
| `steps.log` | 各步时刻：第一次运行 11 秒时杀掉（41/76 完成），同一条命令重跑，比对，恢复，改一个文件 |
| `run-resume.json` | 重跑：41 个来自产物库、建 35 个，52.8 秒；缓存 1,108 个文件、90 MB |
| `verify.json` | 516/516 个文件与原版 `lake build` 逐字节一致；`lake build --no-build --rehash` 7,178 个任务全最新 |
| `fresh-addcombi.log` | 全新检出（另一路径重新克隆、`lake exe cache get`）里单独构建 AddCombi |
| `fresh-restore.json`、`fresh-lake-build.log` | 恢复 1,108 个文件 0.6 秒、环境一致；之后原版 `lake build` 编译 0 个模块 |
| `run-edit.json` | 改 `PFR/ApproxHomPFR.lean`：重建 4 个（它与 3 个下游）、72 个来自产物库，21.0 秒 |
