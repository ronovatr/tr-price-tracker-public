# Politeness notes

Defaults here do **not** crawl third-party shops.

## Do

1. Space out requests (`MIN_REQUEST_GAP_SECONDS`).
2. Tell hard ACL/tunnel failures apart from flaky errors.
3. Cool down after repeated hard denials instead of retrying forever.
4. Read robots.txt; if you can’t fetch it, don’t assume allow (`src/robots.py`).
5. Test on fixtures - don’t hit live shops from CI.
6. Keep secrets out of git.

## Don’t put in a public repo

1. Selectors / URL recipes for named marketplaces.
2. How-tos for Cloudflare, CAPTCHAs, or provider ACLs on those sites.
3. “Look like a home user” routing aimed at specific shops.
4. Treating MIT text as permission to scrape.

## Env

See `.env.example`:

- `MIN_REQUEST_GAP_SECONDS` (default `8`)
- `HARD_DENY_STREAK` (default `2`)
- `HARD_DENY_COOLDOWN_SECONDS` (default `3600`)
- `DEMO_FIXTURES_ONLY` (default `true`)

More context in `JOURNEY.md`.
