# robots.txt check (2026-09-22)

One GET per site for `/robots.txt` the day we shut the tracker down. Also poked a couple of `llms.txt` / `security.txt` URLs.

This is **not** permission to crawl anyone. Rules change. Private bot is stopped. This repo does not ship scrapers for these hosts.

## Results

| Site | robots fetch | Rough notes |
| --- | --- | --- |
| Hepsiburada | 403 | couldn’t even read it from here |
| Trendyol | 200 | lots of Disallow on query patterns (incl. search-like `q=`) |
| n11 | 403 | couldn’t read |
| Vatan | 200 | blocks `/arama/*`; crawl-delay for some SEO bots |
| Amazon TR | 200 | usual cart/signin/wishlist style Disallows |
| Teknosa | 403 | couldn’t read |
| MediaMarkt TR | 200 | blocks search/filter style paths for `*`; some ads-bot allows |
| PttAVM | 200 | account paths + `q=` style |
| GameGaraj | 200 | cart/account/payment style blocks |
| Pazarama | 200 | `Disallow: /arama` and `/search` |
| Itopya | 200 | cart/account + some search pagination patterns |
| İncehesap | 200 | short file; member/ajax blocked |
| Akakçe | 200 | many Disallows (clicks, account, query junk) |
| Cimri | 403 | couldn’t read |

## Extra

| Probe | Result |
| --- | --- |
| Trendyol `llms.txt` | 200 (LLM category blurb - still not a scrape license) |
| Hepsiburada `llms.txt` | 403 |
| `/.well-known/security.txt` (sampled) | 404 or 403 |

## Takeaway

Several shops fence off search/account style paths. A few won’t even serve robots.txt to a random client. We didn’t publish working extractors for them.

Tracker container stopped same day. DB stays private. Other containers on the host were left alone.
