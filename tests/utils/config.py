"""Configuration loader for E2E tests.

Reads environment variables (from .env if present) and config.yaml, resolves defaults,
and provides a simple dataclass-like object for access.
"""
from __future__ import annotations
import os, yaml
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv(override=True)

def env_bool(x: str|None, default: bool=False) -> bool:
    if x is None: return default
    return str(x).lower() in {"1","true","yes","on"}

@dataclass
class Settings:
    base_url: str
    api_url: str
    headless: bool
    browsers: list[str]
    default_locale: str
    slowmo_ms: int
    trace: str
    video: str
    screenshot: str

def load_settings() -> Settings:
    cfg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "config", "config.yaml")
    with open(cfg_path, "r") as f:
        raw = yaml.safe_load(os.path.expandvars(f.read()))
    return Settings(
        base_url=raw.get("base_url", "http://localhost:5173"),
        api_url=raw.get("api_url", "http://localhost:8000/api/v1"),
        headless=env_bool(str(raw.get("headless","true")), True),
        browsers=[x.strip() for x in str(raw.get("browsers","chromium")).split(",") if x.strip()],
        default_locale=str(raw.get("default_locale","en-US")),
        slowmo_ms=int(raw.get("slowmo_ms", 0)),
        trace=str(raw.get("trace","retain-on-failure")),
        video=str(raw.get("video","off")),
        screenshot=str(raw.get("screenshot","off")),
    )
