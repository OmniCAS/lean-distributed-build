# 已完成的运行

每个运行一个目录：`meta.json`（配置、运行前后各机器的负载、结果汇总）和 `records.tgz`（单机原版 Lake：`ref.history.json` 逐模块秒数 + `ref.log`；本工具：`modules.jsonl` 逐模块运行记录、`events.jsonl` 协调器事件、`report.json`、`manifest.json`；格式见 `lakeshard/docs/run-records.md`）。

公开前做过的处理：机器名换成角色名 worker-1、worker-2、worker-3，内网地址换成 10.0.0.x，用户目录换成中性路径；其余未动。项目名 `e1` 对应本仓库的实例 `mid`，`syn2500` 对应 `narrow`。时间是协调器时钟上的秒数（见 `lakeshard/docs/run-records.md`）。本文件由 `study/scripts/make_public.py` 生成。

| 运行 | 实例 | 方式 | 机器 | 每台核数 | 优先级 | 墙钟（秒） | W（秒） | CP（秒） | 模块 |
|---|---|---|---|---|---|---:|---:|---:|---:|
| `mid-A0-c16-r1` | mid | lake | worker-1 | 16 | bl | 732.98 |  |  | 3156 |
| `mid-A1-c16-r1` | mid | tool | worker-1 | 16 | bl | 773.21 | 10809.2 | 343.1 | 3156 |
| `mid-B1-c16-r1` | mid | tool | worker-1, worker-2, worker-3 | 16 | bl | 419.4 | 12096.34 | 384.33 | 3156 |
| `wide-A0-c16-r1` | wide | lake | worker-1 | 16 | bl | 569.93 |  |  | 4333 |
| `wide-A1-c16-r1` | wide | tool | worker-1 | 16 | bl | 564.08 | 8592.08 | 144.32 | 4333 |
| `wide-B1-c16-r1` | wide | tool | worker-1, worker-2, worker-3 | 16 | bl | 248.78 | 9550.77 | 161.73 | 4333 |
| `wide-B1s-c16-r1` | wide | tool | worker-1, worker-2, worker-3 | 16 | structure | 273.38 | 9584.57 | 168.5 | 4333 |
| `wide-B2-c16-r1` | wide | tool | worker-1, worker-2, worker-3 | 16 | bl | 327.02 | 9358.26 | 163.98 | 4333 |
| `wide-B4-c16-r1` | wide | tool | worker-1, worker-2, worker-3 | 16 | fifo | 290.21 | 9672.4 | 154.23 | 4333 |

“W”“CP”是该次运行里实测的逐模块 `lean` 秒数算出的总工作量与最长链（单机原版 Lake 的运行没有这一栏，它的逐模块秒数在 `ref.history.json`）。预测与容差见 `bench/expected.md`，回测见 `study/t6_calibrate.py`。
