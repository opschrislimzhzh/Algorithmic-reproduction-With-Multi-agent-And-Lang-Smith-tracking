#!/usr/bin/env python3
"""Fast environment/API/LangSmith smoke test. Never prints full keys."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from p2c_runtime import get_client, get_model, safe_secret_status  # noqa: E402


def main() -> int:
    print("===== Paper2Code doctor =====")
    try:
        status = safe_secret_status()
    except Exception as exc:
        print(f"[FAIL] config: {exc}")
        return 1

    print(json.dumps(status, indent=2, ensure_ascii=False))

    try:
        client = get_client()
        response = client.chat.completions.create(
            model=get_model(),
            messages=[{"role": "user", "content": "Reply exactly: P2C_API_OK"}],
        )
        text = (response.choices[0].message.content or "").strip()
        print(f"[API] {text}")
        if "P2C_API_OK" not in text:
            print("[WARN] API worked but response text differed.")
    except Exception as exc:
        print(f"[FAIL] LLM API: {type(exc).__name__}: {exc}")
        return 2

    enabled = str(os.getenv("P2C_LANGSMITH_ENABLED", "true")).lower()
    if enabled in {"1", "true", "yes", "on"}:
        try:
            from langsmith import Client
            Client()
            print("[OK] LangSmith client initialized.")
        except Exception as exc:
            print(f"[FAIL] LangSmith: {type(exc).__name__}: {exc}")
            return 3

    print("[OK] environment ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
