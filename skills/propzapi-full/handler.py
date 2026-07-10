"""
propzapi-full skill handler — live sports odds & player props over the propzapi
REST API: get_odds, get_props, get_events, get_books.

Pure standard library. API key in PROPZAPI_KEY, sent as the X-API-Key header.
The base URL is hardcoded, so the key never reaches any other host.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.propzapi.com"  # hardcoded: the API key is never sent to any other host
USER_AGENT = "propzapi-skills/1.0.0 (+https://github.com/paperandbeyond23-gif/propzapi-skills)"
TIMEOUT_SECONDS = 60

SIGNUP_URL = "https://propzapi.com/app"
KEYS_URL = "https://propzapi.com/app"
PRICING_URL = "https://propzapi.com/pricing"

MARKETS = ("h2h", "spreads", "totals", "player_props")
STATUSES = ("upcoming", "live", "final")


def _key():
    k = os.environ.get("PROPZAPI_KEY", "").strip()
    if not k:
        raise RuntimeError(
            "PROPZAPI_KEY environment variable is not set. "
            "Get a free key (500 free credits, no card) at " + SIGNUP_URL + ", "
            "then export PROPZAPI_KEY=pk_live_..."
        )
    return k


def _http_error(e):
    try:
        detail = e.read().decode("utf-8")[:1000]
    except Exception:
        detail = ""
    if e.code == 401:
        return {
            "error": "auth_invalid",
            "detail": "PROPZAPI_KEY was rejected. Mint a new key at " + KEYS_URL + ".",
            "keys_url": KEYS_URL,
            "http_status": 401,
        }
    if e.code == 402:
        return {
            "error": "out_of_credits",
            "detail": "Out of propzapi credits. Top up a pack or subscribe at " + PRICING_URL + ".",
            "upgrade_url": PRICING_URL,
            "http_status": 402,
        }
    if e.code == 403:
        return {
            "error": "forbidden",
            "detail": "This propzapi origin rejected the request. Use a direct key against the public host.",
            "http_status": 403,
        }
    if e.code == 404:
        return {
            "error": "not_found",
            "detail": "No match for that request. Check the league/event id (e.g. NBA, NFL, MLB, NHL, EPL, MLS).",
            "http_status": 404,
        }
    if e.code == 429:
        return {
            "error": "rate_limit_exceeded",
            "detail": "Request limit hit (or too many free keys from this IP). Back off, or upgrade at " + PRICING_URL + ".",
            "upgrade_url": PRICING_URL,
            "http_status": 429,
        }
    if e.code in (502, 503):
        return {
            "error": "upstream_unavailable",
            "detail": "An upstream odds source was briefly unreachable. Retry shortly.",
            "http_status": e.code,
        }
    return {"error": "HTTP " + str(e.code), "detail": detail}


def _get(path, params=None):
    try:
        qs = ""
        if params:
            clean = {k: v for k, v in params.items() if v is not None and v != ""}
            if clean:
                qs = "?" + urllib.parse.urlencode(clean)
        req = urllib.request.Request(
            API_BASE + path + qs,
            method="GET",
            headers={
                "X-API-Key": _key(),
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        return _http_error(e)
    except urllib.error.URLError as e:
        return {"error": "network", "detail": str(e.reason)}
    except RuntimeError as e:
        return {"error": "auth_required", "detail": str(e), "signup_url": SIGNUP_URL}
    except Exception as e:
        return {"error": "unexpected", "detail": str(e)}


def get_odds(league=None, sport=None, market=None, limit=25):
    """
    Live game odds — moneyline, spreads and totals — grouped by sportsbook.

    league: e.g. "NBA", "NFL", "MLB", "NHL", "EPL", "MLS" (optional).
    sport:  e.g. "basketball", "soccer" (optional; use league or sport).
    market: "h2h" | "spreads" | "totals" | "player_props" (optional; omit for all game markets).
    limit:  number of events to return, 1-100 (default 25).
    Costs 1 credit for a single market, 3 for all game markets.
    Returns a dict of events with book-grouped odds, or an {"error": ...} dict.
    """
    if market is not None and market not in MARKETS:
        return {"error": "invalid_argument", "detail": "market must be one of " + ", ".join(MARKETS) + "."}
    return _get("/v1/odds", {"league": league, "sport": sport, "market": market, "limit": limit})


def get_props(league=None, sport=None, limit=25):
    """
    Player props for upcoming games — the markets most odds APIs skip.

    league: e.g. "NBA", "NFL", "MLB" (optional).
    sport:  e.g. "basketball" (optional).
    limit:  number of events to return, 1-100 (default 25).
    Costs 5 credits. Returns a dict of events with player-prop selections, or an {"error": ...} dict.
    """
    return _get("/v1/props", {"league": league, "sport": sport, "limit": limit})


def get_events(league=None, sport=None, status=None, limit=25):
    """
    Fixtures and live scores (no odds).

    league: e.g. "EPL", "NBA" (optional).
    sport:  e.g. "soccer" (optional).
    status: "upcoming" | "live" | "final" (optional).
    limit:  number of events to return, 1-100 (default 25).
    Costs 1 credit.
    """
    if status is not None and status not in STATUSES:
        return {"error": "invalid_argument", "detail": "status must be one of " + ", ".join(STATUSES) + "."}
    return _get("/v1/events", {"league": league, "sport": sport, "status": status, "limit": limit})


def get_books():
    """
    The sportsbooks currently covered. Costs 1 credit.
    """
    return _get("/v1/books")
