#!/usr/bin/env python3
"""Patch a clean upstream Paper2Code checkout for unified API + LangSmith use."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "paper2code_src"
CODES = SRC / "codes"
SCRIPTS = SRC / "scripts"
RUNTIME_SOURCE = ROOT / "runtime" / "p2c_runtime.py"

API_FILES = {
    "1_planning.py": "Planning LLM",
    "1.2_rag_config.py": "RAG Config LLM",
    "2_analyzing.py": "Analysis LLM",
    "3_coding.py": "Coding LLM",
    "3.1_coding_sh.py": "Coding Shell LLM",
    "4_debugging.py": "Debugging LLM",
    "eval.py": "Evaluation LLM",
}


def patch_client(path: Path, trace_name: str) -> list[str]:
    changes = []
    text = path.read_text(encoding="utf-8")

    if "from p2c_runtime import get_client, traceable" not in text:
        text = text.replace(
            "from openai import OpenAI",
            "from p2c_runtime import get_client, traceable",
            1,
        )
        changes.append("centralized client import")

    patterns = [
        r'client\s*=\s*OpenAI\(\s*api_key\s*=\s*os\.environ\["OPENAI_API_KEY"\]\s*\)',
        r"client\s*=\s*OpenAI\(\s*api_key\s*=\s*os\.environ\['OPENAI_API_KEY'\]\s*\)",
        r'client\s*=\s*OpenAI\(\s*api_key\s*=\s*os\.environ\["DASHSCOPE_API_KEY"\]\s*,\s*base_url\s*=\s*["\'][^"\']+["\']\s*\)',
    ]
    for pattern in patterns:
        text, n = re.subn(pattern, "client = get_client()", text, count=1)
        if n:
            changes.append("centralized client construction")
            break

    if "def api_call(" in text and f'name="{trace_name}"' not in text:
        text = text.replace(
            "def api_call(",
            f'@traceable(name="{trace_name}", run_type="chain", '
            f'tags=["paper2code", "repro"])\ndef api_call(',
            1,
        )
        changes.append("LangSmith api_call trace")

    path.write_text(text, encoding="utf-8")
    return changes


def patch_run_sh(path: Path) -> list[str]:
    changes = []
    text = path.read_text(encoding="utf-8")
    new, n = re.subn(
        r'^GPT_VERSION=.*$',
        'GPT_VERSION="${P2C_MODEL:-qwen-plus}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n:
        text = new
        changes.append("P2C_MODEL shell override")
    path.write_text(text, encoding="utf-8")
    return changes


def patch_debugging(path: Path) -> list[str]:
    changes = []
    text = path.read_text(encoding="utf-8")

    if (
        "args.output_repo_dir" in text
        and '"--output_repo_dir"' not in text
        and "'--output_repo_dir'" not in text
    ):
        anchor = '    parser.add_argument(\n        "--paper_name",'
        if anchor in text:
            insertion = """    parser.add_argument(
        "--output_repo_dir",
        type=str,
        required=True,
        help="Generated repository directory to debug.",
    )
"""
            text = text.replace(anchor, insertion + anchor, 1)
            changes.append("added --output_repo_dir")

    text = text.replace('default="o4-mini",', 'default="qwen-plus",')
    path.write_text(text, encoding="utf-8")
    return changes


def main() -> None:
    if not CODES.exists():
        raise SystemExit(
            f"{CODES} does not exist. Run `bash scripts/bootstrap.sh` first."
        )

    shutil.copy2(RUNTIME_SOURCE, CODES / "p2c_runtime.py")
    print("[OK] installed codes/p2c_runtime.py")

    for filename, trace_name in API_FILES.items():
        path = CODES / filename
        if not path.exists():
            print(f"[WARN] missing upstream file: {path}")
            continue
        changes = patch_client(path, trace_name)
        if filename == "4_debugging.py":
            changes.extend(patch_debugging(path))
        print(
            f"[PATCH] {filename}: "
            f"{', '.join(changes) if changes else 'already patched'}"
        )

    run_sh = SCRIPTS / "run.sh"
    if run_sh.exists():
        changes = patch_run_sh(run_sh)
        print(
            f"[PATCH] run.sh: "
            f"{', '.join(changes) if changes else 'already patched'}"
        )

    print("\nPatch complete.")
    print("Use wrapper: bash scripts/run_qwen.sh")


if __name__ == "__main__":
    main()
