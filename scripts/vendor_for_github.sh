#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

bash "$ROOT/scripts/bootstrap.sh"

if [[ -d "$ROOT/paper2code_src/.git" ]]; then
  rm -rf "$ROOT/paper2code_src/.git"
fi

echo "[OK] paper2code_src is now vendored as ordinary files."
echo "You may now git add/commit the whole repository."
