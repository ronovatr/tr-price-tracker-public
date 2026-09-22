"""SQLite schema for the demo. No production data."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Optional

from . import config


SCHEMA = """
CREATE TABLE IF NOT EXISTS price_observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    price REAL NOT NULL,
    currency TEXT NOT NULL DEFAULT 'TRY',
    observed_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_obs_url_time ON price_observations(url, observed_at);
"""


def connect(path: Optional[str] = None) -> sqlite3.Connection:
    db_path = Path(path or config.DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(SCHEMA)
    return conn


def insert_observation(
    conn: sqlite3.Connection,
    *,
    store: str,
    title: str,
    url: str,
    price: float,
    currency: str = "TRY",
) -> None:
    conn.execute(
        "INSERT INTO price_observations (store, title, url, price, currency) "
        "VALUES (?, ?, ?, ?, ?)",
        (store, title, url, price, currency),
    )
    conn.commit()


def insert_many(conn: sqlite3.Connection, rows: Iterable[dict]) -> int:
    n = 0
    for row in rows:
        insert_observation(
            conn,
            store=row["store"],
            title=row["title"],
            url=row["url"],
            price=float(row["price"]),
            currency=row.get("currency", "TRY"),
        )
        n += 1
    return n
