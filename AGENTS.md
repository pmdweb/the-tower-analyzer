# Contributor instructions

## Principles

- Keep the analyzer strictly read-only.
- Treat every input file as hostile.
- Prefer small, testable parser stages over a monolithic decoder.
- Do not invent field mappings; document evidence for every mapping.
- Never commit raw `playerInfo.dat`, `global-metadata.dat`, or personal account data.

## Quality gates

Before submitting changes, run:

```bash
uv sync --dev
uv run ruff check .
uv run mypy src
uv run pytest
```

## Reverse-engineering documentation

Add discoveries under `docs/reverse-engineering/` using sequential filenames. Include evidence, assumptions, unresolved questions, and the game version when known.
