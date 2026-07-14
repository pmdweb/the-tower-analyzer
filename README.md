# The Tower Save Analyzer

> **Read-only** reverse-engineering and analysis tool for save files from  
> [The Tower](https://play.google.com/store/apps/details?id=com.TechTreeGames.TheTower) (TechTreeGames).

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ⚠️ Important

This tool **never modifies save files**.  It is a strictly read-only analysis tool.

---

## Overview

`tower-analyzer` decodes `playerInfo.dat` files (GZip → .NET BinaryFormatter → Unity IL2CPP SaveLoad.PlayerData) and exports structured data for analysis, comparison, and reporting.

**Current status:** Phase 1 – GZip decompression and BinaryFormatter stream header parsing are implemented.  Full field mapping is in progress.  See [docs/reverse_engineering_status.md](docs/reverse_engineering_status.md) for details.

---

## Architecture

```
playerInfo.dat
    │
    ▼ GzipParser
    │   decompress the outer GZip wrapper
    ▼ BinaryFormatterParser
    │   decode the .NET BinaryFormatter (MS-NRBF) stream
    ▼ ObjectGraph
    │   resolve object ID references into a rooted tree
    ▼ SaveDataSerializer
    │   map the resolved tree to typed Pydantic v2 models
    ▼
SaveData (Pydantic)
    ├── PlayerAccount
    ├── Workshop
    ├── Labs
    ├── Cards
    ├── Modules
    ├── UltimateWeapons
    ├── Statistics
    ├── Economy
    └── TierProgress
```

Each stage is an independent module – new parsers can be added without modifying the CLI.

See [docs/architecture.md](docs/architecture.md) for full details.

---

## How to Run

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (`pip install uv`)

### Install

```bash
git clone https://github.com/pmdweb/the-tower-analyzer.git
cd the-tower-analyzer
uv sync
```

### Commands

```bash
# Analyze a save file (terminal summary)
uv run tower-analyzer analyze playerInfo.dat

# Export to structured JSON
uv run tower-analyzer export-json playerInfo.dat --output account.json

# Generate a Markdown report
uv run tower-analyzer report playerInfo.dat --output report.md

# Compare two save snapshots
uv run tower-analyzer compare old.dat new.dat --output diff.md

# Show version
uv run tower-analyzer --version
```

---

## How to Contribute

See [docs/contributing.md](docs/contributing.md) for full guidelines.

Quick start:

```bash
uv sync
uv run pytest          # run tests
uv run ruff check .    # lint
uv run mypy            # type check
```

If you have knowledge of The Tower's save format or can share anonymized save files, please open an issue or PR.

---

## Current Reverse Engineering Status

| Stage | Status |
|-------|--------|
| GZip decompression | ✅ Complete |
| BinaryFormatter header | ✅ Complete |
| BinaryFormatter full decode | ⏳ In progress |
| Unity IL2CPP object graph | ⏳ Stubbed |
| SaveLoad.PlayerData mapping | ⏳ Stubbed |

See [docs/reverse_engineering_status.md](docs/reverse_engineering_status.md) for full details.

---

## Roadmap

### Phase 1 – Read GZip / Decode BinaryFormatter *(current)*
- [x] GZip decompression
- [x] BinaryFormatter stream header parsing
- [ ] Full BinaryFormatter field / object decode
- [ ] Unity IL2CPP type resolution

### Phase 2 – Parse PlayerData
- [ ] Map all PlayerData fields to Pydantic models
- [ ] Populate Workshop, Labs, Cards, Modules, UltimateWeapons
- [ ] Populate Statistics, Economy, TierProgress

### Phase 3 – Export JSON
- [x] JSON exporter infrastructure
- [ ] Fully populated account.json export

### Phase 4 – ROI Engine
- [ ] Workshop ROI calculator
- [ ] Labs ROI calculator
- [ ] Card upgrade ROI calculator

### Phase 5 – Save Comparison
- [x] Comparison infrastructure
- [ ] Full field-level diff

### Phase 6 – HTML Dashboard
- [ ] HTML report generator
- [ ] Interactive charts

---

## Project Structure

```
src/tower_analyzer/
    cli.py              CLI entry point (Typer)
    parser/
        gzip_parser.py  Stage 1: GZip decompression
        binary_formatter.py  Stage 2: .NET BinaryFormatter decode
        object_graph.py Stage 3: Object reference resolution
        serializer.py   Stage 4: Pydantic model mapping
        pipeline.py     Orchestration
    models/
        save_data.py    Root SaveData model
        player_account.py
        workshop.py
        labs.py
        cards.py
        modules.py
        ultimate_weapons.py
        statistics.py
        economy.py
        tier_progress.py
    analysis/
        summary.py      SaveSummary helper
        comparator.py   Two-save diff
    reports/
        base.py         BaseReport abstract class
        markdown_report.py  Markdown report generator
        json_exporter.py    JSON exporter

tests/
docs/
schemas/
examples/
scripts/
```

---

## License

MIT
