"""
Run engines for a query. Default: ExampleMart + fixtures.
"""

from __future__ import annotations

from typing import Iterable, List, Sequence

from . import database
from .stores import DEFAULT_ENGINES
from .stores.base import Offer, StoreEngine


def run_query(
    query: str,
    *,
    engines: Sequence[StoreEngine] | None = None,
    limit: int = 20,
    persist: bool = True,
) -> List[Offer]:
    engines = engines or DEFAULT_ENGINES
    found: List[Offer] = []
    for engine in engines:
        found.extend(engine.search(query, limit=limit))
    if persist and found:
        conn = database.connect()
        try:
            database.insert_many(
                conn,
                (
                    {
                        "store": o.store,
                        "title": o.title,
                        "url": o.url,
                        "price": o.price,
                        "currency": o.currency,
                    }
                    for o in found
                ),
            )
        finally:
            conn.close()
    return found


def summarize(offers: Iterable[Offer]) -> str:
    rows = list(offers)
    if not rows:
        return "No offers matched."
    lines = [f"{len(rows)} offer(s):"]
    for o in rows:
        lines.append(f"  [{o.store}] {o.title} - {o.price:.2f} {o.currency} ({o.url})")
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Educational price-tracker demo. Default: local fixtures only. "
            "Do not point this at third-party shops without legal rights."
        )
    )
    parser.add_argument("query", nargs="?", default="GPU", help="Search query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument(
        "--no-persist",
        action="store_true",
        help="Do not write SQLite observations",
    )
    args = parser.parse_args(argv)
    offers = run_query(args.query, limit=args.limit, persist=not args.no_persist)
    print(summarize(offers))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
