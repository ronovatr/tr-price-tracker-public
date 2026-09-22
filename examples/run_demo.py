#!/usr/bin/env python3
"""Run the fixture-only ExampleMart demo."""

from src.category_tracker import run_query, summarize


def main() -> None:
    offers = run_query("GPU", persist=False)
    print(summarize(offers))
    print()
    print(f"{len(offers)} offer(s) from local fixtures (no network).")


if __name__ == "__main__":
    main()
