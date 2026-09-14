#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT/scripts/_env.sh"

SRC="$ROOT/paper2code_src"
PAPER_NAME="${PAPER_NAME:-Transformer}"
OUTPUT_DIR="${OUTPUT_DIR:-$SRC/outputs/Transformer}"
TARGET_REPO_DIR="${TARGET_REPO_DIR:-$SRC/outputs/Transformer_repo}"
EVAL_RESULT_DIR="${EVAL_RESULT_DIR:-$ROOT/results}"
GENERATED_N="${GENERATED_N:-1}"
EVAL_TYPE="${EVAL_TYPE:-ref_free}"

mkdir -p "$EVAL_RESULT_DIR"

python3 "$SRC/codes/eval.py" \
  --paper_name "$PAPER_NAME" \
  --pdf_json_path "$SRC/examples/${PAPER_NAME}_cleaned.json" \
  --data_dir "$SRC/data" \
  --output_dir "$OUTPUT_DIR" \
  --target_repo_dir "$TARGET_REPO_DIR" \
  --eval_result_dir "$EVAL_RESULT_DIR" \
  --eval_type "$EVAL_TYPE" \
  --generated_n "$GENERATED_N" \
  --gpt_version "${P2C_MODEL:-qwen-plus}" \
  --papercoder
