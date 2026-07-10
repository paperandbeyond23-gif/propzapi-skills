# Security policy

## Reporting a vulnerability

Email **support@propzapi.com** with the subject line `SECURITY: propzapi-skills`. Please do not open public issues for security reports.

We will acknowledge receipt within 72 hours and aim to publish a fix or mitigation within 14 days for confirmed issues.

## Scope

These skills are thin, dependency-free HTTP clients for the propzapi REST API. The base URL is hardcoded in each `handler.py`, so your `PROPZAPI_KEY` is only ever sent to `api.propzapi.com` as the `X-API-Key` header — never to any third-party host.

Keep your key secret. If a key is exposed, revoke it and mint a new one in the dashboard at <https://propzapi.com/app>.
