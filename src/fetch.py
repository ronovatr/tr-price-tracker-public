"""
HTTP helpers + hard-deny cool-down.

No store URL templates. Live fetches stay off while DEMO_FIXTURES_ONLY is true.
"""

from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass
from typing import Optional

from . import config

# Provider-style ACL / tunnel failures: rotating exits cannot help.
_ACL_DENY_RE = re.compile(r"Access control list denies", re.I)
_CONNECT_403_RE = re.compile(
    r"CONNECT tunnel failed.*\b403\b|\b403\b.*CONNECT tunnel failed",
    re.I | re.S,
)

_lock = threading.Lock()
_streak: dict[str, int] = {}
_until: dict[str, float] = {}
_last_request_at = 0.0


@dataclass
class FetchResult:
    ok: bool
    status: Optional[int] = None
    text: str = ""
    hard_deny: bool = False
    skipped_circuit: bool = False
    error: str = ""


def reset_circuits() -> None:
    """Test helper."""
    with _lock:
        _streak.clear()
        _until.clear()


def is_hard_deny_exc(exc: BaseException) -> bool:
    return bool(_CONNECT_403_RE.search(str(exc) or ""))


def is_hard_deny_body(text: str) -> bool:
    if not text:
        return False
    sample = text if len(text) <= 2048 else text[:2048]
    return bool(_ACL_DENY_RE.search(sample))


def circuit_blocks(name: str) -> bool:
    with _lock:
        until = _until.get(name)
        if until is None:
            return False
        if time.time() < until:
            return True
        del _until[name]
        return False


def record_hard_deny(name: str) -> None:
    with _lock:
        n = _streak.get(name, 0) + 1
        _streak[name] = n
        if n >= config.HARD_DENY_STREAK:
            _until[name] = time.time() + config.HARD_DENY_COOLDOWN_SECONDS


def record_success(name: str) -> None:
    with _lock:
        _streak[name] = 0
        _until.pop(name, None)


def _respect_gap() -> None:
    global _last_request_at
    gap = config.MIN_REQUEST_GAP_SECONDS
    if gap <= 0:
        return
    now = time.time()
    wait = (_last_request_at + gap) - now
    if wait > 0:
        time.sleep(wait)
    _last_request_at = time.time()


def fetch_url(name: str, url: str, timeout: float = 20.0) -> FetchResult:
    """
    Fetch a URL the operator explicitly provided.

    Refuses network I/O while DEMO_FIXTURES_ONLY is enabled. Always check
    robots.txt / ToS / law for any host you point this at yourself.
    """
    if config.DEMO_FIXTURES_ONLY:
        return FetchResult(
            ok=False,
            error="DEMO_FIXTURES_ONLY=true - live HTTP disabled. Use fixture loaders.",
        )
    if circuit_blocks(name):
        return FetchResult(ok=False, skipped_circuit=True, error="circuit open")

    _respect_gap()
    try:
        # stdlib only - no TLS fingerprint tricks, no challenge solvers.
        import urllib.request

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "EducationalDemoFetcher/1.0 (respect robots.txt)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            text = raw.decode("utf-8", errors="replace")
            status = getattr(resp, "status", 200)
            if is_hard_deny_body(text):
                record_hard_deny(name)
                return FetchResult(
                    ok=False, status=status, text=text, hard_deny=True, error="ACL body"
                )
            record_success(name)
            return FetchResult(ok=True, status=status, text=text)
    except Exception as exc:  # noqa: BLE001 - demo surface
        if is_hard_deny_exc(exc):
            record_hard_deny(name)
            return FetchResult(ok=False, hard_deny=True, error=str(exc))
        return FetchResult(ok=False, error=str(exc))


def load_fixture(filename: str) -> str:
    path = config.FIXTURES_DIR / filename
    return path.read_text(encoding="utf-8")
