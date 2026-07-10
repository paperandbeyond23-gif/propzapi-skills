---
name: propzapi-odds
version: 1.0.0
description: Live game odds & fixtures via propzapi.com. Three tools — pull moneyline/spreads/totals grouped by sportsbook, fixtures and live scores, and the list of covered books. Normalized across books so you don't scrape each one.
license: MIT-0
author: propzapi
homepage: https://propzapi.com
repository: https://github.com/paperandbeyond23-gif/propzapi-skills
tags:
  - propzapi
  - sports-odds
  - odds-api
  - moneyline
  - spreads
  - totals
  - sports-betting
  - api
  - mcp
metadata:
  openclaw:
    primaryEnv: PROPZAPI_KEY
    homepage: https://propzapi.com
    requires:
      env:
        - PROPZAPI_KEY
---

# propzapi-odds

Live game odds and fixtures via [propzapi.com](https://propzapi.com). Use when the user **explicitly asks** for the odds/moneyline/spread/total on a game or league, or the schedule/scores — and wants real sourced numbers.

Odds live behind a dozen sportsbook sites, each with its own markup. This skill normalizes moneyline, spreads and totals across books into one JSON shape.

## When to use this skill

Calls spend propzapi credits (`get_odds` 1 for a single market / 3 for all game markets; `get_events` and `get_books` 1 each), so this activates only when the request is genuinely about live odds.

**DO use when the user:**

- Asks for the odds / moneyline / spread / total on a game or league → `get_odds`
- Asks what games are on, live scores, or the schedule → `get_events`
- Asks which sportsbooks are covered → `get_books`

**Do NOT use** for player props (use `propzapi-props` / `propzapi-full`), season stats, or a betting *pick*.

## Tools

### `get_odds` — game odds grouped by book
Moneyline, spreads and totals for upcoming games. Args: `league` (e.g. `NBA`, `NFL`, `MLB`, `NHL`, `EPL`, `MLS`), `sport`, `market` (`h2h` | `spreads` | `totals`; omit for all game markets), `limit` (1–100, default 25). Costs 1 credit for a single market, 3 for all.

### `get_events` — fixtures & live scores
Games and live scores, no odds. Args: `league`, `sport`, `status` (`upcoming` | `live` | `final`), `limit`. Costs 1 credit.

### `get_books` — covered sportsbooks
The sportsbooks currently normalized. No args. Costs 1 credit.

## Authentication

Set `PROPZAPI_KEY` to your propzapi key (`pk_live_...`), sent as the `X-API-Key` header.

```bash
export PROPZAPI_KEY="pk_live_..."
```

Get a free key (500 free credits, no card) at <https://propzapi.com/app>.

## Pricing

Metered by market; the exact charge is returned in the `X-Credits-Cost` header. Free 500/mo · Indie $19 (25k) · Pro $49 (100k) · Scale $149 (1M). See <https://propzapi.com/pricing>.

## Errors

Each function returns a dict; on failure it has an `error` key: `auth_required`, `auth_invalid`, `out_of_credits` (with `upgrade_url`), `not_found`, `rate_limit_exceeded`, `upstream_unavailable`, `invalid_argument`, `network`, or `HTTP <code>`.

## Independence

propzapi is an independent developer tool that aggregates publicly listed sportsbook odds. It is not a sportsbook, does not accept wagers, and does not provide betting advice. Odds are informational and may be delayed.
