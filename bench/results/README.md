# 已完成的运行

每个运行一个目录：`meta.json`（配置、运行前后各机器的负载、结果汇总）和 `records.tgz`（单机原版 Lake：`ref.history.json` 逐模块秒数 + `ref.log`；本工具：`modules.jsonl` 逐模块运行记录、`events.jsonl` 协调器事件、`report.json`、`manifest.json`；格式见 `lakeshard/docs/run-records.md`）。

公开前做过的处理：机器名换成角色名 worker-1、worker-2、worker-3，内网地址换成 10.0.0.x，用户目录换成中性路径；其余未动。项目名 `e1` 对应本仓库的实例 `mid`，`syn2500` 对应 `narrow`。时间是协调器时钟上的秒数（见 `lakeshard/docs/run-records.md`）。逐模块记录里的 `worker` 字段是工具按 `--hosts` 的顺序编的号，哪台机器看 `host` 字段：三机运行两者一致，两机运行（`wide2-*`、`narrow2-*`、`mathlib2-*`）里工具的 `worker-1`、`worker-2` 分别是机器 worker-2、worker-3。本文件由 `study/scripts/make_public.py` 生成。

| 运行 | 实例 | 方式 | 机器 | 每台核数 | 优先级 | 墙钟（秒） | W（秒） | CP（秒） | 模块 |
|---|---|---|---|---|---|---:|---:|---:|---:|
| `mathlib2-A1-c16-r1` | mathlib | tool | worker-2 | 16 | bl | 2712.74 | 39747.76 | 1196.29 | 8530 |
| `mathlib2-B1-c1616-r1` | mathlib | tool | worker-2, worker-3 | 16 | bl | 1606.05 | 37156.03 | 1119.4 | 8530 |
| `mid-A0-c16-r1` | mid | lake | worker-1 | 16 | bl | 732.98 |  |  | 3156 |
| `mid-A1-c16-r1` | mid | tool | worker-1 | 16 | bl | 773.21 | 10809.2 | 343.1 | 3156 |
| `mid-B1-c16-r1` | mid | tool | worker-1, worker-2, worker-3 | 16 | bl | 419.4 | 12096.34 | 384.33 | 3156 |
| `narrow2-A0-c16-r1` | narrow | lake | worker-2 | 16 | bl | 439.54 |  |  | 2613 |
| `narrow2-A1-c16-r1` | narrow | tool | worker-2 | 16 | bl | 439.06 | 1747.94 | 382.31 | 2613 |
| `narrow2-A1-c4-r1` | narrow | tool | worker-2 | 4 | bl | 688.6 | 1708.73 | 394.88 | 2613 |
| `narrow2-B1-c16-r1` | narrow | tool | worker-2, worker-3 | 16 | bl | 439.48 | 1677.1 | 378.74 | 2613 |
| `narrow2-B1-c4-r1` | narrow | tool | worker-2, worker-3 | 4 | bl | 539.83 | 1671.29 | 385.37 | 2613 |
| `wide-A0-c16-r1` | wide | lake | worker-1 | 16 | bl | 569.93 |  |  | 4333 |
| `wide-A1-c16-r1` | wide | tool | worker-1 | 16 | bl | 564.08 | 8592.08 | 144.32 | 4333 |
| `wide-B1-c16-r1` | wide | tool | worker-1, worker-2, worker-3 | 16 | bl | 248.78 | 9550.77 | 161.73 | 4333 |
| `wide-B1s-c16-r1` | wide | tool | worker-1, worker-2, worker-3 | 16 | structure | 273.38 | 9584.57 | 168.5 | 4333 |
| `wide-B2-c16-r1` | wide | tool | worker-1, worker-2, worker-3 | 16 | bl | 327.02 | 9358.26 | 163.98 | 4333 |
| `wide-B4-c16-r1` | wide | tool | worker-1, worker-2, worker-3 | 16 | fifo | 290.21 | 9672.4 | 154.23 | 4333 |
| `wide2-A1-c16-r1` | wide | tool | worker-2 | 16 | bl | 671.27 | 9778.11 | 165.94 | 4333 |
| `wide2-A1-c4-r1` | wide | tool | worker-2 | 4 | bl | 2503.88 | 9300.5 | 158.71 | 4333 |
| `wide2-A1-c8-r1` | wide | tool | worker-2 | 8 | bl | 1316.12 | 9706.28 | 163.66 | 4333 |
| `wide2-B1-c16-d0.1` | wide | tool | worker-2, worker-3 | 16 | bl | 370.17 | 9355.99 | 159.56 | 4333 |
| `wide2-B1-c16-d1` | wide | tool | worker-2, worker-3 | 16 | bl | 405.85 | 9299.69 | 159.01 | 4333 |
| `wide2-B1-c16-d10` | wide | tool | worker-2, worker-3 | 16 | bl | 894.23 | 9067.64 | 153.32 | 4333 |
| `wide2-B1-c16-r1` | wide | tool | worker-2, worker-3 | 16 | bl | 358.57 | 9447.36 | 161.78 | 4333 |
| `wide2-B1-c4-r1` | wide | tool | worker-2, worker-3 | 4 | bl | 1304.64 | 9359.9 | 163.33 | 4333 |
| `wide2-B1-c8-r1` | wide | tool | worker-2, worker-3 | 8 | bl | 674.89 | 9428.76 | 160.94 | 4333 |
| `wide2-B1s-c16-r1` | wide | tool | worker-2, worker-3 | 16 | structure | 382.81 | 9593.94 | 163.4 | 4333 |
| `wide2-B2-c16-d1` | wide | tool | worker-2, worker-3 | 16 | bl | 440.05 | 9585.06 | 161.46 | 4333 |
| `wide2-B2-c16-d10` | wide | tool | worker-2, worker-3 | 16 | bl | 580.27 | 9549.85 | 160.86 | 4333 |
| `wide2-B2-c16-r1` | wide | tool | worker-2, worker-3 | 16 | bl | 423.29 | 9455.23 | 158.68 | 4333 |
| `wide2-B3-c16-r1` | wide | tool | worker-2, worker-3 | 16 | bl | 359.57 | 9377.62 | 159.76 | 4333 |
| `wide2-B4-c16-r1` | wide | tool | worker-2, worker-3 | 16 | fifo | 441.69 | 9777.48 | 163.61 | 4333 |
| `wide2-B4-c4-r1` | wide | tool | worker-2, worker-3 | 4 | fifo | 1332.2 | 9223.46 | 156.42 | 4333 |
| `wide2-B5-c16-r1` | wide | forward | worker-2, worker-3 | 16 | bl | 908.57 |  |  | None |

“W”“CP”是该次运行里实测的逐模块 `lean` 秒数算出的总工作量与最长链（单机原版 Lake 的运行没有这一栏，它的逐模块秒数在 `ref.history.json`）。预测与容差见 `bench/expected.md`，回测见 `study/t6_calibrate.py`。阶段 1 在 PFR 上的验收输出在 [`step1-pfr/`](step1-pfr/)。
