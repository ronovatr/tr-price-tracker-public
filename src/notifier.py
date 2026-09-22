"""Optional Telegram notifier (disabled unless env vars are set)."""

from __future__ import annotations

import json
import urllib.request
from typing import Optional

from . import config


def send_message(text: str, chat_id: Optional[str] = None) -> bool:
    token = config.TELEGRAM_BOT_TOKEN
    chat = chat_id or config.TELEGRAM_CHAT_ID
    if not token or not chat:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps(
        {"chat_id": chat, "text": text, "disable_web_page_preview": True}
    ).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return 200 <= getattr(resp, "status", 200) < 300
