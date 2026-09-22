<p align="center">
  <img src="assets/banner.svg" alt="tr-price-tracker" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/python-3.10%2B-yellow.svg" alt="Python"></a>
  <a href="https://github.com/ronovatr/tr-price-tracker-public/actions/workflows/tests.yml"><img src="https://github.com/ronovatr/tr-price-tracker-public/actions/workflows/tests.yml/badge.svg" alt="tests"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="JOURNEY.md">Journey</a> ·
  <a href="docs/LEGAL.md">Legal</a> ·
  <a href="#what's-missing">What's missing</a>
</p>

Personal price tracker I ran for about two months, then killed when hosting + proxies stopped making sense. This repo is the leftover notes and a **fixture-only** demo - not something you point at real shops.

```python
from src.category_tracker import run_query, summarize

print(summarize(run_query("GPU", persist=False)))
```

```text
2 offer(s):
  [ExampleMart] ExampleMart GPU Alpha 8GB - 12499.00 TRY (...)
  [ExampleMart] ExampleMart GPU Beta 12GB - 18990.50 TRY (...)
```

Default mode never leaves your machine. Fake store, local HTML.

---

## Quick start

```bash
git clone https://github.com/ronovatr/tr-price-tracker-public.git
cd tr-price-tracker-public
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
cp .env.example .env

python examples/run_demo.py
python -m unittest discover -s tests -v
```

## Repo map

| Path | What it is |
| --- | --- |
| [`examples/`](examples/) | one-command demo |
| [`src/`](src/) | cool-downs, SQLite stub, ExampleMart parser |
| [`fixtures/`](fixtures/) | sample HTML only |
| [`JOURNEY.md`](JOURNEY.md) | ACL vs Cloudflare, RAM, compose footguns |
| [`docs/`](docs/) | architecture, robots snapshot, legal |

## What's missing

On purpose:

- no live retailer engines / selectors / search URLs
- no proxy lists or production database
- no Cloudflare bypass writeups

Private side kept that offline. See [`docs/NEVER_PUBLISH.md`](docs/NEVER_PUBLISH.md) and [`docs/LEGAL.md`](docs/LEGAL.md).

## More reading

- [Journey](JOURNEY.md)
- [Architecture](docs/architecture.md)
- [Politeness notes](docs/safer-crawler.md)
- [Robots audit (2026-09-22)](docs/robots-audit.md)

## License

[MIT](LICENSE) covers this repo. It does not cover third-party sites or their data.
