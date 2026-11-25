#!/bin/bash
# Time `lean` on tiny files: no import, `import Mathlib`, and a mid-sized import (3 runs each),
# pinned to one CPU, with Lake's LEAN_PATH. Usage: import_cost.sh ROOT CPU OUT.jsonl
set -uo pipefail
ROOT=$1; CPU=$2; OUT=$3
TC=$ROOT/elan/toolchains/leanprover--lean4---v4.34.0/bin
WS=$ROOT/mathlib4
LP=$(ls -d $WS/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')$WS/.lake/build/lib/lean
D=$ROOT/importtest; mkdir -p $D
printf 'theorem t : 1 + 1 = 2 := rfl\n' > $D/None.lean
printf 'import Mathlib\ntheorem t : 1 + 1 = 2 := rfl\n' > $D/All.lean
printf 'import Mathlib.Algebra.Group.Basic\ntheorem t : 1 + 1 = 2 := rfl\n' > $D/Mid.lean
printf 'import Mathlib.Analysis.SpecialFunctions.Gamma.Basic\ntheorem t : 1 + 1 = 2 := rfl\n' > $D/Big.lean
for f in None Mid Big All; do
  for i in 1 2 3; do
    s=$(date +%s.%N)
    LEAN_PATH=$LP LEAN_NUM_THREADS=1 nice -n 10 taskset -c $CPU $TC/lean -j1 $D/$f.lean -o $D/$f.olean > /dev/null 2>&1
    rc=$?
    e=$(date +%s.%N)
    echo "{\"file\": \"$f\", \"run\": $i, \"exit\": $rc, \"wall_s\": $(echo "$e - $s" | bc)}" >> $OUT
  done
done
echo IMPORT_DONE
