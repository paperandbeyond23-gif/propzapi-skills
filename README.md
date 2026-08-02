# propzapi-skills

**Agent skills for template-based image generation and webpage screenshots.** Drop-in skills that let any agent render an image from an HTML/CSS template, snapshot any live URL, and manage a template library — over the [propzapi REST API](https://propzapi.com).

Templates are HTML/CSS with `{{variables}}` and Jinja logic (`{% if %}`, `{% for %}`, filters). Fill the variables with one JSON call and get back a rendered PNG/JPEG/WEBP/PDF at a stable URL — no headless browser to run, no fonts to install. Perfect for Open Graph images, social cards, certificates, invoices, receipts, and data charts.

Free to start — [grab a key](https://propzapi.com/app) (50-image trial, no card required) and you're rendering from Claude, Cursor, Cline, or your own agent loop in under two minutes.

Pure Python standard library. No dependencies. MIT-0 licensed.

## Install

```bash
# Claude Code, Cursor, Cline, etc. — `skills` CLI, installs straight from this repo
npx skills add paperandbeyond23-gif/propzapi-skills --all
# or pick one: npx skills add paperandbeyond23-gif/propzapi-skills --skill propzapi-full

# OpenClaw / ClawHub — published to the ClawHub registry
npx clawhub@latest install propzapi-full
```

## Skills in this repo

| Skill | Purpose |
|---|---|
| [`propzapi-full`](skills/propzapi-full) | Complete toolkit — generate images from templates, capture screenshots, and manage templates |

## Tools

| Tool | Returns |
|---|---|
| `generate_image(template, modifications, format, scale, quality)` | Rendered image `{url, width, height, format, bytes}` |
| `screenshot(url, full_page, width, height, format)` | Screenshot of a live page `{url, ...}` |
| `list_templates()` | Available built-in and custom templates |
| `create_template(name, html, width, height, variables)` | Created template with its `tpl_...` id |
| `embed_url(template, modifications, format)` | Signed GET render URL for `<meta og:image>` |

## Authentication

Set the `PROPZAPI_KEY` environment variable to your propzapi key. It's sent as the `X-API-Key` header — the base URL is hardcoded, so the key never reaches any other host.

```bash
export PROPZAPI_KEY="your_key"
```

**[Get a free key](https://propzapi.com/app)** — 50-image trial, no card required. You can also mint one with `POST /v1/register` → `{api_key, plan, credits}`. The same key works for these skills and direct REST calls.

## Pricing

Each rendered image or screenshot costs 1 credit — the response returns the exact charge in the `X-Credits-Cost` header, and your balance in `X-Credits-Remaining`. Listing and creating templates is free.

| Plan | Price | Images / mo |
|---|---|---|
| Free trial | $0 | 50 |
| Starter | $29/mo | 1,000 |
| Growth | $79/mo | 3,500 |
| Pro | $199/mo | 12,000 |

Prefer pay-as-you-go? Credit packs: **$5 / 150 images** and **$15 / 500 images**. Manage plans at <https://propzapi.com/pricing>.

## Source

- Docs: <https://propzapi.com/docs> · OpenAPI: <https://api.propzapi.com/openapi.json>
- MCP server: <https://api.propzapi.com/mcp> (same key, `X-API-Key` header) — tools `generate_image`, `screenshot_url`, `list_templates`
- Quickstart: get a key at <https://propzapi.com/app>, then call any tool

## Issues and contributions

See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports: [SECURITY.md](SECURITY.md).

## License

[MIT No Attribution](LICENSE). Fork, ship, sublicense — no attribution required.

## Independence

propzapi is an independent developer tool for rendering images from templates and capturing webpage screenshots. Images render from HTML/CSS you supply or select; you are responsible for the content you render and for the rights to any assets, fonts, and pages you screenshot. Comply with the laws of your jurisdiction and the terms of any site you capture.
