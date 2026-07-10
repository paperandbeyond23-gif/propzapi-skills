# propzapi-skills

**Agent skills for live sports odds and player props.** Drop-in skills that let any agent pull moneyline/spreads/totals grouped by sportsbook, player props for upcoming games, fixtures and live scores — over the [propzapi REST API](https://propzapi.com).

Odds live behind a dozen sportsbook sites, each with its own markup and its own idea of a "market." propzapi normalizes moneyline, spreads, totals and player props across books into one JSON shape — so your agent gets a line it can trust in one call.

Free to start — [grab a key](https://propzapi.com/app) (500 free credits, no card required) and you're pulling odds from Claude, Cursor, Cline, or your own agent loop in under two minutes.

Pure Python standard library. No dependencies. MIT-0 licensed.

## Install

```bash
# Claude Code, Cursor, Cline, etc. — `skills` CLI, installs straight from this repo
npx skills add paperandbeyond23-gif/propzapi-skills --all
# or pick one: npx skills add paperandbeyond23-gif/propzapi-skills --skill propzapi-full

# OpenClaw / ClawHub — published to the ClawHub registry
npx clawhub@latest install propzapi-full   # also: propzapi-props, propzapi-odds
```

## Skills in this repo

| Skill | Purpose |
|---|---|
| [`propzapi-full`](skills/propzapi-full) | Complete toolkit — odds, player props, fixtures/scores, and covered books |
| [`propzapi-props`](skills/propzapi-props) | Player props + fixtures — the markets most odds APIs skip |
| [`propzapi-odds`](skills/propzapi-odds) | Game odds (moneyline/spreads/totals) + fixtures + books |

Install the bundled `propzapi-full` for agents that need broad coverage. Install the focused variants when you want minimum tool surface.

## Tools

| Tool | Returns |
|---|---|
| `get_odds(league, sport, market, limit)` | Moneyline, spreads & totals grouped by sportsbook |
| `get_props(league, sport, limit)` | Player props for upcoming games |
| `get_events(league, sport, status, limit)` | Fixtures and live scores |
| `get_books()` | Sportsbooks currently covered |

## Authentication

Set the `PROPZAPI_KEY` environment variable to your propzapi key (format `pk_live_...`). It's sent as the `X-API-Key` header — the base URL is hardcoded, so the key never reaches any other host.

```bash
export PROPZAPI_KEY="pk_live_..."
```

**[Get a free key](https://propzapi.com/app)** — 500 free credits, no card required. The same key works for these skills and direct REST calls.

## Pricing

Calls are metered by market — the response returns the exact charge in the `X-Credits-Cost` header. Credits never expire.

| Plan | Price | Credits / mo |
|---|---|---|
| Free | $0 | 500 |
| Indie | $19/mo | 25,000 |
| Pro | $49/mo | 100,000 |
| Scale | $149/mo | 1,000,000 |

Manage plans at <https://propzapi.com/pricing>.

## Source

- Docs: <https://propzapi.com/docs> · OpenAPI: <https://api.propzapi.com/openapi.json>
- MCP server: <https://api.propzapi.com/mcp> (same key, `X-API-Key` header)
- Quickstart: get a key at <https://propzapi.com/app>, then call any tool

## Issues and contributions

See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports: [SECURITY.md](SECURITY.md).

## License

[MIT No Attribution](LICENSE). Fork, ship, sublicense — no attribution required.

## Independence

propzapi is an independent developer tool that aggregates publicly listed sportsbook odds. It is not a sportsbook, does not accept wagers, and does not provide betting advice. Odds are informational and may be delayed. Comply with the laws of your jurisdiction and each sportsbook's terms.
