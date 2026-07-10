---
name: propzapi-props
version: 1.0.0
description: Player props & fixtures via propzapi.com. Two tools — pull normalized player props (points, rebounds, passing yards, etc.) for upcoming games, plus fixtures and live scores. The prop markets most odds APIs skip, in one JSON shape across books.
license: MIT-0
author: propzapi
homepage: https://propzapi.com
repository: https://github.com/paperandbeyond23-gif/propzapi-skills
tags:
  - propzapi
  - player-props
  - sports-odds
  - odds-api
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

# propzapi-props

Player props and fixtures via [propzapi.com](https://propzapi.com). Use when the user **explicitly asks** for player props on an upcoming game, or the schedule/scores for a league — and wants real sourced numbers.

Player props (a player's points, rebounds, passing yards, strikeouts, and the over/under on each) are the markets most odds APIs cover thinly. This skill is built around them, normalized across sportsbooks into one JSON shape.

## When to use this skill

Calls spend propzapi credits (`get_props` costs 5, `get_events` costs 1), so this activates only when the request is genuinely about props or fixtures — not when a player merely comes up.

**DO use when the user:**

- Asks for player props / a player's line (points, rebounds, yards, etc.) → `get_props`
- Asks what games are on, live scores, or the schedule → `get_events`

**Do NOT use** for season stats, historical results, or a betting *pick* — return the numbers, not advice.

## Tools

### `get_props` — player props
Player props for upcoming games. Args: `league` (e.g. `NBA`, `NFL`, `MLB`), `sport` (e.g. `basketball`), `limit` (1–100, default 25). Costs 5 credits.

### `get_events` — fixtures & live scores
Games and live scores, no odds. Args: `league`, `sport`, `status` (`upcoming` | `live` | `final`), `limit` (1–100, default 25). Costs 1 credit.

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
