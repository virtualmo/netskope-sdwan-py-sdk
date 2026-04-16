# Contributing

Thanks for contributing to `netskope-sdwan-py-sdk`.

## Development Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Local Checks

```bash
ruff check .
pytest -q
python examples/smoke_all_gets.py
```

## Project Guardrails

- Keep the SDK read-only.
- Prefer v2 endpoints for the main client surface.
- Keep v1-only GET endpoints isolated under `client.v1.*`.
- Avoid broad schema modeling unless there is a confirmed need.

## Pull Requests

- Keep diffs focused and reviewable.
- Update tests and documentation when behavior changes.
- Call out any remaining assumptions or API-spec gaps in the PR description.
