# The Tower Save Analyzer

Read-only analyzer for Android save files from **The Tower** by TechTreeGames.

## Status

Early reverse-engineering phase. The current target is `playerInfo.dat`, observed as a GZip-compressed .NET NRBF/BinaryFormatter payload whose root object is `SaveLoad+PlayerData`.

## Safety

- Save files are treated as untrusted binary input.
- The analyzer never modifies or restores saves.
- Raw saves, `global-metadata.dat`, account identifiers, and private snapshots must not be committed.
- Parsing must not invoke native .NET BinaryFormatter deserialization.

## CLI

```bash
tower-analyzer inspect playerInfo.dat
tower-analyzer export-json playerInfo.dat
tower-analyzer report playerInfo.dat
tower-analyzer compare old.dat new.dat
```

Only `inspect` is implemented in the first milestone. Other commands will be introduced when their parsers are backed by verified fixtures.

## Roadmap

1. Safe GZip inspection and bounded decompression
2. NRBF record parser
3. Object graph reconstruction
4. `SaveLoad+PlayerData` mapping
5. Sanitized JSON export
6. Markdown reports
7. Save comparison and progression tracking
8. ROI and recommendation engine

## Development

Python 3.12+, `uv`, Typer, Pydantic v2, Rich, pytest, Ruff, and mypy.

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run mypy src
```

Inspect a save without deserializing it:

```bash
uv run tower-analyzer inspect /path/to/playerInfo.dat
```

## Disclaimer

This project is unofficial and is not affiliated with TechTreeGames.
