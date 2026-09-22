# Journey notes

Personal notes from ~2 months of running (then killing) a TR PC-parts price tracker with Telegram alerts. This is not a scraping tutorial. See `docs/LEGAL.md`.

## Why

I wanted one watchlist across a few Turkish stores + price comparison sites, pinging me when category prices moved. Small AWS box.

## Month 1 - getting anything to work

HTML parsers break constantly. Laptop hit rates looked fine; the server (datacenter IP) did not. Proxy geography mattered more than we wanted to admit.

Biggest time sink: mixing up failure modes. Provider ACL pages (`Access control list denies…` / CONNECT 403) are not Cloudflare. Cloudflare “Just a moment…” is not Amazon’s soft 503 wall. Treating them the same wastes money.

## Month 1.5 - stop hammering closed doors

Instead of fancier fingerprints, we added boring stuff:

- gap between requests
- after repeated destination-level ACL failures, cool that store down so we stop burning the proxy pool

If the path is closed, stop.

## Month 2 - browsers and ops

JS challenges pushed us toward a headless browser. On 4 GB RAM, multiple Chromiums were a joke - one shared browser with a tiny tab limit was the compromise.

Also: old `docker-compose` v1 on the host could delete a healthy container and then fail with `KeyError: ContainerConfig`. We stopped using it and started the bot with a plain `docker run` script.

Monitoring lied a lot. “Pagination broken” was often just a slow sweep or a temporary hit-rate dip.

## Why the public repo is stripped

Private hobby bot was already grey-area vs store ToS / robots themes. Shipping working selectors for named shops would be asking for trouble.

So when cost killed the project we:

1. stopped the container
2. kept the DB private
3. published the story + a fixture demo, not the private engines

## Fixes that actually mattered

| Problem | What we did |
| --- | --- |
| ACL denies one shop on every ISP exit | cool down; ticket the provider; don’t rotate forever |
| CF / soft wall vs hard deny | classify; different cool-downs |
| OOM on tiny VM | one browser, few tabs |
| compose eating the container | avoid broken compose v1 |
| cost | shut down |

## Shutdown (2026-09-22)

Stopped only the price-tracker container. Left other services on the box alone. Disabled auto-restart. DB archived privately, not in this repo.

Build stuff for sites you’re allowed to hit. The robots audit here is a cautionary snapshot, not a map.
