#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT/scripts/_env.sh"

if [[ ! -f "$ROOT/paper2code_src/codes/1_planning.py" ]]; then
  echo "[INFO] Upstream source missing; bootstrapping first."
  bash "$ROOT/scripts/bootstrap.sh"
fi

python3 "$ROOT/tools/patch_upstream.py" >/dev/null

echo "Model: ${P2C_MODEL:-qwen-plus}"
echo "LangSmith project: ${LANGSMITH_PROJECT:-Paper2Code-repro}"
echo
cd "$ROOT/paper2code_src/scripts"
bash run.sh
