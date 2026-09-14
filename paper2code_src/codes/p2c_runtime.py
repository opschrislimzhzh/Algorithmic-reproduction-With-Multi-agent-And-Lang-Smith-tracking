"""Shared Paper2Code API/LangSmith runtime."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

try:
    from langsmith import traceable
    from langsmith.wrappers import wrap_openai
except Exception:
    def traceable(*args, **kwargs):
        def decorator(fn):
            return fn
        return decorator

    def wrap_openai(client):
        return client


def _load_env() -> None:
    here = Path(__file__).resolve()
    candidates = [
        Path.cwd() / ".env",
        here.parent / ".env",
        here.parent.parent / ".env",
        here.parent.parent.parent / ".env",
    ]
    for candidate in candidates:
        if candidate.exists():
            load_dotenv(candidate, override=False)
            break


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def get_model(default: str = "qwen-plus") -> str:
    _load_env()
    return os.getenv("P2C_MODEL", default)


def get_api_key() -> str:
    _load_env()
    key = (
        os.getenv("P2C_API_KEY")
        or os.getenv("DASHSCOPE_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )
    if not key:
        raise RuntimeError(
            "No API key found. Set P2C_API_KEY in .env "
            "(or DASHSCOPE_API_KEY / OPENAI_API_KEY)."
        )
    return key


def get_base_url() -> str | None:
    _load_env()
    value = os.getenv("P2C_BASE_URL", "").strip()
    return value or None


def langsmith_enabled() -> bool:
    _load_env()
    return _truthy(os.getenv("P2C_LANGSMITH_ENABLED", "true")) and _truthy(
        os.getenv("LANGSMITH_TRACING", "true")
    )


def _supports_reasoning_effort(model: str) -> bool:
    m = model.lower()
    return m.startswith(("o1", "o3", "o4", "gpt-5"))


class _CompletionsProxy:
    def __init__(self, inner: Any):
        self._inner = inner

    def create(self, *args, **kwargs):
        model = str(kwargs.get("model") or get_model())
        if "reasoning_effort" in kwargs and not _supports_reasoning_effort(model):
            kwargs.pop("reasoning_effort", None)
        return self._inner.create(*args, **kwargs)


class _ChatProxy:
    def __init__(self, inner: Any):
        self.completions = _CompletionsProxy(inner.completions)


class CompatibleClient:
    def __init__(self, inner: Any):
        self._inner = inner
        self.chat = _ChatProxy(inner.chat)

    def __getattr__(self, name: str):
        return getattr(self._inner, name)


def get_client() -> CompatibleClient:
    _load_env()
    kwargs: dict[str, Any] = {"api_key": get_api_key()}
    base_url = get_base_url()
    if base_url:
        kwargs["base_url"] = base_url

    client = OpenAI(**kwargs)
    if langsmith_enabled():
        client = wrap_openai(client)

    return CompatibleClient(client)


def safe_secret_status() -> dict[str, str | bool]:
    key = get_api_key()
    return {
        "api_key_present": bool(key),
        "api_key_prefix": key[:4] if key else "",
        "base_url": get_base_url() or "OpenAI default",
        "model": get_model(),
        "langsmith_enabled": langsmith_enabled(),
        "langsmith_project": os.getenv("LANGSMITH_PROJECT", ""),
        "langsmith_endpoint": os.getenv("LANGSMITH_ENDPOINT", ""),
    }
