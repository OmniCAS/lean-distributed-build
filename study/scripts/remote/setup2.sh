#!/bin/bash
# Tarball-based layout (see setup_tarballs.py), then check that Lake loads the workspace offline.
set -euo pipefail
ROOT=$1
TAG=${2:-v4.34.0}
export PATH=$ROOT/elan/toolchains/leanprover--lean4---$TAG/bin:$PATH
python3 -I "$ROOT/setup_tarballs.py" "$ROOT" "$TAG"
cd "$ROOT/mathlib4"
cat lean-toolchain > "$ROOT/logs/mathlib-rev.txt"
GIT_TERMINAL_PROMPT=0 timeout 900 lake env true
du -sh "$ROOT/mathlib4" "$ROOT/src"
echo SETUP_DONE
