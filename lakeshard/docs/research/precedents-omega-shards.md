# Omega Institute 的 RH 分片构建：机制（读原文件）

日期：2026-11-23。由本会话派出的网页读取子代理直接读了以下公开文件的原文（未运行任何代码），本文是它的报告整理；行号为子代理按返回文本估计的近似值。

已读：
- https://raw.githubusercontent.com/the-omega-institute/riemann-hypothesis/main/ci/plan.py
- https://raw.githubusercontent.com/the-omega-institute/riemann-hypothesis/main/ci/planning.py
- https://raw.githubusercontent.com/the-omega-institute/riemann-hypothesis/main/ci/schedule.py
- https://raw.githubusercontent.com/the-omega-institute/riemann-hypothesis/main/ci/parts.py
- https://raw.githubusercontent.com/the-omega-institute/riemann-hypothesis/main/ci/groups.py
- https://raw.githubusercontent.com/the-omega-institute/riemann-hypothesis/main/.github/workflows/lean-parts.yml
- https://raw.githubusercontent.com/the-omega-institute/riemann-hypothesis/main/.github/workflows/shard-batch.yml

未读：`.github/workflows/one-shard.yml`、`.github/actions/toolchain`、`ci/Audit.lean`、`ci/large-workspace.sh`。

## 1 导入图

- `plan.py` 的 `graph()`：`git ls-tree -rl HEAD src` 列出 `.lean` 文件（记 blob SHA 与字节数）；`git grep` 抓以可选的 `public`/`private`/`meta` 加 `import` 开头的行，去掉 `--` 之后的注释；只有仓库内的模块成边。未解析且以项目九个顶层命名空间开头的 import 会报错，其余外部 import 忽略。不调用 Lake，没有预计算文件。

## 2 切片（两轮）

- **第一轮 `plan()`**：`height[m]` = 模块以下最长的仓库内导入链（叶子为 0），从 `Main` 递归求，只含 `Main` 可达的模块。`Statements` 与 `BuildAid.*` 叶子组成第 0 片。其余按 `(height, name)` 顺序：若一个模块的仓库内依赖全在某个非 0 的地基片里且未超上限，就并入；上限 `MAX_MODULES = 400` 个模块、`MAX_BYTES = 2_500_000` 字节源码（源码大小，不是编译耗时）。注释说这样复现“最初的十六个地基片”。
- **第二轮 `planning.split_graph()`**（默认 `lanes=500`）：每个模块的“尾权” = `2048 + 源码字节 +` 其导入者中最大的尾权（即到 `Main` 的关键路径权重）。就绪模块（依赖都已有归属）放进按尾权排序的堆；每一波的包大小目标为 `min(180, max(20, ceil(就绪数/500)))` 个模块；从堆里取最重的就绪模块开包，后继模块若其依赖都在本包或更早的波次就并入同包；到目标数或 1,000,000 字节源码即封包；单个超大模块自成一包。包的依赖 = 其模块所依赖模块的归属包；层号 = 1 + 依赖包的最大层号。层数由数据决定（README 说的“36 层”不在这些文件里）。

## 3 片的键

- `config` = SHA-256（`lean-toolchain`、`lake-manifest.json`、`lakefile.toml` 在 `HEAD` 的 blob ID，再加格式标签 `"lake-leanArts/linux-x86_64/v1"`）。
- 片键 = SHA-256（`config`，各模块的 `"模块名:blobSHA"`（按片内顺序），依赖片的键（排序））。按层序计算，上游键折叠进下游键。产物名 `键 + ".tar.zst"`。片内模块顺序会影响键。

## 4 每片怎么建

- `shard-batch.yml` 接收一组片号，生成矩阵，每个元素调用 `one-shard.yml`（未读）；`fail-fast: false`。
- `parts.py build()`：
  1. 求本片模块在片外的仓库内依赖；
  2. `restore()` 用 4 个线程下载这些上游模块所在片的归档，SHA-256 必须与 GitHub 资产摘要一致，`zstd -qdc | tar` 只解出需要的路径；
  3. `lake --no-build build +M:olean …` 确认恢复的产物被 Lake 接受；
  4. `lake build +M:olean …` 建本片模块（**调用 Lake，不是直接调 `lean`**）；
  5. 把各模块在 `lib/lean/` 与 `ir/` 下的输出（不含 `.setup.json`）打成 `<键>.tar.zst`，检查 `.olean` 都在；删掉输出、从归档重新解出、再跑一次 `lake --no-build` 自检。
- 产物存放：GitHub prerelease，标签 `lean-parts-v1-<键的首个十六进制字符>`，共 16 个桶。下载 `curl --retry 4`，失败时退回 Actions artifact；自托管 runner 默认用本地缓存。上传后核对返回的摘要，瞬时错误按 2、5、15、30 秒重试。
- `groups.py`（可选，仓库变量 `RH_GROUP_SHARDS`）：把一片按连通的导入组再拆，各组单独成矩阵任务、单独上传。

## 5 调度（`schedule.py`）

- 优先级：按层逆序算 `tail[i]`，就绪片按 `(-tail, 序号)` 排，剩余关键路径最重的先派。第 0 片先单独派。
- 就绪：片不存在、不在运行、尝试次数 < 3，且依赖片都已存在（或其组归档已齐）。
- 循环：每轮列出 Release 资产、标记已存在的片、写索引，然后用 `gh workflow run shard-batch.yml` 每批派 28 个，轮间睡 60 秒。
- 去重：键命名的资产已存在、或在本次运行的未完成批次里、或 180 秒内刚提交过，都不再派。内容寻址，相同内容同一资产。
- 重试：按批次运行标题统计尝试次数，少于 3 次才再派；没有就绪也没有在跑的片时报错，提示人工检查失败的批次。
- 时限：循环 4 小时后派一个同 session 的新 `lean-parts.yml` 运行并退出，进度保存在 Release 资产与批次标题里，新运行从那里接着做。计划任务超时 330 分钟。
- 全部片都存在后才置完成，随后的发布任务在自托管 runner 上恢复 `Main`、`lake build +Main:olean`、`lake env lean ci/Audit.lean` 检查五个定理与公理白名单（`propext`、`Quot.sound`、`Classical.choice`）。

## 6 大模块与内存

- 文件里没有大内存 runner 的专门路径（README 提到可用仓库变量换大 runner，见 `precedents-rh.md`）。需要 ≥80,000 个模块时，托管 runner 上会跑 `large-workspace.sh`（未读）。`run_lake_ci` 每 60 秒打印耗时与 Lake 及子进程的 RSS。

## 7 文件里没有的

运行时长、runner 数量、片的总数（README 说 8,490 片、36 层、底层完成后 529 个任务可并行）、`one-shard.yml` 的 runner 与命令。

## 8 与我们的方案对照（推断）

- 他们的第二轮切片与我们的动态批次几乎是同一个思路（按到终点的剩余权重取就绪模块、把只差本包的后继并进来），区别在于他们**开跑前静态算好**，用源码字节当权重；我们**运行时凑批**，用实测耗时当权重。
- 他们用 GitHub Release 当产物库、用 `tar.zst` 打包、用内容哈希当键、用 Lake 本身做每片的增量判断与自检，这些都与我们的设计一致，可以直接借鉴“每片建完后删掉输出、从归档恢复、再 `--no-build` 自检”这一步。
- 他们的调度是“每 60 秒轮询一次、每批派 28 个”，受 GitHub API 与托管 runner 的限制；我们的协调器在内存里直接派发，延迟低得多。
