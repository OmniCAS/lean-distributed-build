# Run records of the direct backend

Every `lakeshard build --backend lean` writes, in its work directory:

| file | what |
|---|---|
| `modules.jsonl` | one **run record per attempt** (format below): the input for schedule analysis and for calibrating a simulator |
| `events.jsonl` | the coordinator's log as it happened: `start`, `register`, `dispatch`, `result`, `expired`, `done` |
| `report.json` | totals, per-worker summary (slots, threads, host, clock offset), failures, lower bound |
| `history.json` | measured `lean` seconds per module (input to the next run's priorities) |

## Time base

All `*_t` fields are seconds since the coordinator started (`start` event), **on the
coordinator's clock**. Times measured on a worker are converted with that worker's clock offset:
the worker estimates `offset = (t_send + t_recv) / 2 - t_coordinator` from its lowest-latency
round trip (register, claims, heartbeats; the coordinator stamps each reply), and the error is at
most half that round trip plus any asymmetry (on one machine about 0.5 ms with 1.3 ms round trips;
a worker on the coordinator's own host uses 0). `report.json` keeps each worker's raw estimate
(`clock_offset_estimate_s`) and round trip (`clock_rtt_s`). Durations (`*_s`) are measured on one
clock and need no conversion.

## Fields of one record (`modules.jsonl`)

| field | meaning |
|---|---|
| `module`, `attempt`, `task_id` | the module, the attempt number (1, 2, ...), the task |
| `ok` | the attempt succeeded and its outputs were confirmed by the coordinator |
| `accepted` | the coordinator applied the result (false for a late report of a task already given to another worker) |
| `worker`, `host`, `slots`, `threads` | worker name, its machine's host name, its number of slots, `LEAN_NUM_THREADS` of this `lean` |
| `ready_t` | when the module became ready (its last import confirmed, or a retry queued; 0 for modules without project imports) |
| `dispatch_t` | when the coordinator handed the task to the worker |
| `start_t` | when the worker started the task |
| `lean_start_t`, `lean_end_t` | the `lean` process (and `leanir`, if any) |
| `end_t` | when the worker finished the task (outputs published or uploaded) |
| `report_t`, `done_t` | when the coordinator received the report, and when it had confirmed the outputs and released importers |
| `wait_s` | shared build directory: waiting for the imports' outputs to become visible |
| `fetch_s`, `fetched_files`, `fetched_bytes` | store: fetching the outputs of the import closure that were not yet on this worker |
| `lean_s` | duration of the `lean` process (the per-module time used for lower bounds) |
| `publish_s` | moving outputs into place and, with a store, uploading them |
| `confirm_s` | the coordinator checking the outputs |
| `wall_s` | the whole task on the worker (`end_t - start_t`) |
| `cpu_s`, `max_rss_bytes` | user + system CPU and peak resident memory of the `lean` process |
| `output_bytes` | total size of the module's outputs |
| `clock_offset_s` | the offset used to convert this worker's times |
| `error`, `reason` | why an attempt failed (`reason`: `worker lost` or `overdue` for attempts the coordinator expired; such records have only the coordinator-side times) |

Useful differences: queueing `dispatch_t - ready_t` (no free slot, or held for another worker
after a failure), dispatch latency `start_t - dispatch_t`, input transfer `fetch_s` (+ `wait_s`),
compile `lean_s`, output transfer `publish_s`, release latency `done_t - end_t`.
