#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/paper2code_src"
UPSTREAM_REPO="${P2C_UPSTREAM_REPO:-https://github.com/going-doer/Paper2Code.git}"
UPSTREAM_REF="${P2C_UPSTREAM_REF:-master}"

if [[ ! -d "$SRC/.git" ]]; then
  if [[ -e "$SRC" ]] && [[ -n "$(find "$SRC" -mindepth 1 -maxdepth 1 ! -name .gitkeep -print -quit)" ]]; then
    echo "[ERROR] $SRC contains files but is not a git checkout."
    exit 1
  fi
  rm -rf "$SRC"
  echo "[1/3] Cloning upstream Paper2Code..."
  git clone --depth 1 --branch "$UPSTREAM_REF" "$UPSTREAM_REPO" "$SRC"
else
  echo "[1/3] Upstream checkout already exists."
fi

echo "[2/3] Applying reproducibility/API/LangSmith patch..."
python3 "$ROOT/tools/patch_upstream.py"

echo "[3/3] Done."
echo
echo "Next:"
echo "  cp .env.example .env"
echo "  edit .env"
echo "  python scripts/doctor.py"
echo "  bash scripts/run_qwen.sh"
