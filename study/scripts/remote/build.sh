#!/bin/bash
# Vanilla `lake build` of Mathlib from source, pinned and niced, with a /proc sampler.
# Usage: build.sh ROOT RUN_NAME CPUS THREADS   (e.g. build.sh /var/tmp/x full16 16-31 16)
set -uo pipefail
ROOT=$1
RUN=$2
CPUS=$3
THREADS=$4
export PATH=$ROOT/elan/toolchains/leanprover--lean4---v4.34.0/bin:$PATH
OUT=$ROOT/logs/$RUN
mkdir -p "$OUT"
rm -f "$OUT/STOP"
cd "$ROOT/mathlib4"
python3 "$ROOT/procmon.py" "$ROOT/mathlib4" "$OUT" --interval 0.2 --cpus "$CPUS" &
MON=$!
date +%s.%N > "$OUT/t_start"
env LEAN_NUM_THREADS=$THREADS nice -n 10 taskset -c "$CPUS" lake build > "$OUT/lake.log" 2>&1
echo $? > "$OUT/exit_code"
date +%s.%N > "$OUT/t_end"
touch "$OUT/STOP"
wait $MON
du -sk "$ROOT/mathlib4/.lake" > "$OUT/du_lake.txt" 2>/dev/null
echo BUILD_DONE
