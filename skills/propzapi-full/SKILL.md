---
name: propzapi-full
version: 1.0.0
description: Live sports odds & player props via propzapi.com. Four tools — pull moneyline/spreads/totals odds grouped by sportsbook, player props for upcoming games, fixtures & live scores, and the list of covered books, normalized across books so you don't scrape each one.
license: MIT-0
author: propzapi
homepage: https://propzapi.com
repository: https://github.com/paperandbeyond23-gif/propzapi-skills
tags:
  - propzapi
  - sports-odds
  - odds-api
  - player-props
  - sports-betting
  - moneyline
  - spreads
  - totals
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

# propzapi-full

Live sports odds and player props via [propzapi.com](https://propzapi.com). Use when the user **explicitly asks** for real sportsbook odds, player props, lines, or fixtures/scores for a game or league — and wants sourced numbers rather than a guess.

Odds live behind a dozen different sportsbook sites, each with its own markup and its own idea of a "market." propzapi normalizes moneyline, spreads, totals and player props across books into one JSON shape, so your agent gets a line it can trust in one call.

## When to use this skill

Each tool call spends propzapi credits (1 for a single market, 3 for all game markets, 5 for player props), so this skill activates only when the request is genuinely about live odds — not when a team or league merely comes up in passing.

**DO use when the user:**

- Asks for the odds / moneyline / spread / total on a game or league → `get_odds`
- Asks for player props (points, rebounds, passing yards, etc.) → `get_props`
- Asks what games are on, live scores, or the schedule → `get_events`
- Asks which sportsbooks are covered → `get_books`

**Do NOT use when:**

- A team or league appears incidentally (news, small talk, a fantasy roster)
- The user wants historical results or season stats — propzapi is live/upcoming odds, not a stats archive
- The user is asking for betting *advice* or a *pick* — return the numbers, not a recommendation

When intent is ambiguous, confirm the league before calling.

## Tools

### `get_odds` — game odds grouped by book
Moneyline, spreads and totals for upcoming games, grouped by sportsbook. Args: `league` (e.g. `NBA`, `NFL`, `MLB`, `NHL`, `EPL`, `MLS`), `sport` (e.g. `basketball`), `market` (`h2h` | `spreads` | `totals` | `player_props`; omit for all game markets), `limit` (1–100, default 25). Costs 1 credit for a single market, 3 for all.

### `get_props` — player props
Player props for upcoming games — the markets most odds APIs skip. Args: `league`, `sport`, `limit` (1–100, default 25). Costs 5 credits.

### `get_events` — fixtures & live scores
Games and live scores, no odds. Args: `league`, `sport`, `status` (`upcoming` | `live` | `final`), `limit` (1–100, default 25). Costs 1 credit.

### `get_books` — covered sportsbooks
The sportsbooks currently normalized. No args. Costs 1 credit.

## Authentication

Set `PROPZAPI_KEY` to your propzapi key. Keys are `pk_live_...` strings, sent as the `X-API-Key` header.

```bash
export PROPZAPI_KEY="pk_live_..."
```

Get a free key (500 free credits, no card required) at <https://propzapi.com/app>.

## Pricing

Calls are metered by market — the response returns the exact charge in the `X-Credits-Cost` header. Credits never expire.

| Plan | Price | Credits / mo |
|---|---|---|
| Free | $0 | 500 |
| Indie | $19/mo | 25,000 |
| Pro | $49/mo | 100,000 |
| Scale | $149/mo | 1,000,000 |

Manage plans at <https://propzapi.com/pricing>.

## Errors

All functions return a Python dict. On success it's the API response; on failure it has an `error` key:

- `{"error": "auth_required", ...}` — `PROPZAPI_KEY` not set (includes `signup_url`)
- `{"error": "auth_invalid", ...}` — key rejected; mint a new one at `/app`
- `{"error": "out_of_credits", ...}` — credit balance exhausted; includes `upgrade_url`
- `{"error": "not_found", ...}` — no match for that league/event
- `{"error": "rate_limit_exceeded", ...}` — plan request limit or too many free keys from this IP
- `{"error": "upstream_unavailable", ...}` — an odds source was briefly unreachable; retry
- `{"error": "invalid_argument", ...}` — bad `market` or `status` value
- `{"error": "network" | "HTTP <code>" | "unexpected", ...}` — transport / other failures

## API reference

- Docs: <https://propzapi.com/docs>
- OpenAPI spec: <https://api.propzapi.com/openapi.json>
- Pricing: <https://propzapi.com/pricing>

## Independence

propzapi is an independent developer tool that aggregates publicly listed sportsbook odds. It is not a sportsbook, does not accept wagers, and does not provide betting advice. Odds are informational and may be delayed. Comply with the laws of your jurisdiction and each sportsbook's terms.
