# Contributing

Pull requests welcome for:

- New skills exposing additional propzapi endpoints
- Bug fixes in existing handlers
- Additional language ports (Node, Go, Rust)
- Documentation improvements

## Ground rules

- **Standard library only.** Handlers must run with a stock Python install — no third-party dependencies.
- **The base URL stays hardcoded.** `PROPZAPI_KEY` must only ever be sent to `api.propzapi.com`. Never add a config option that lets the key go to another host.
- **Every skill ships tests.** Add or update the `tests/` for any handler you touch; network is mocked, so tests run offline.
- **Keep errors structured.** Handlers return a dict; failures carry an `error` key with a helpful `detail`, never a raw traceback.

## Running tests

```bash
cd skills/<skill-name>
python -m unittest discover tests
```

## Releasing

Bump the `version` in the skill's `SKILL.md`, the root `manifest.json`, and `package.json` together.
