"""Runtime configuration for the educational demo skeleton."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = ROOT / "fixtures" / "html"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

DATABASE_PATH = os.getenv("DATABASE_PATH", str(ROOT / "data" / "demo_tracker.db"))

try:
    MIN_REQUEST_GAP_SECONDS = max(0.0, float(os.getenv("MIN_REQUEST_GAP_SECONDS", "8")))
except ValueError:
    MIN_REQUEST_GAP_SECONDS = 8.0

try:
    HARD_DENY_STREAK = max(1, int(os.getenv("HARD_DENY_STREAK", "2")))
except ValueError:
    HARD_DENY_STREAK = 2

try:
    HARD_DENY_COOLDOWN_SECONDS = max(60, int(os.getenv("HARD_DENY_COOLDOWN_SECONDS", "3600")))
except ValueError:
    HARD_DENY_COOLDOWN_SECONDS = 3600

DEMO_FIXTURES_ONLY = os.getenv("DEMO_FIXTURES_ONLY", "true").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
