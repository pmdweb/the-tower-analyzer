# Architecture

## Overview

The Tower Save Analyzer is designed as a modular pipeline:

```
playerInfo.dat
    │
    ▼
GzipParser          decompress the outer GZip wrapper
    │
    ▼
BinaryFormatterParser   decode the .NET BinaryFormatter (MS-NRBF) stream
    │
    ▼
ObjectGraph         resolve object references into a rooted tree
    │
    ▼
SaveDataSerializer  map the object tree to typed Pydantic models
    │
    ▼
SaveData            fully-typed Python representation of the save
```

## Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `parser/gzip_parser.py` | Decompress GZip wrapper |
| `parser/binary_formatter.py` | Parse MS-NRBF stream, extract raw objects |
| `parser/object_graph.py` | Resolve object ID references into a tree |
| `parser/serializer.py` | Map resolved objects to Pydantic models |
| `parser/pipeline.py` | Orchestrate the four stages end-to-end |
| `models/` | Pydantic v2 typed data models |
| `analysis/` | Higher-level analysis (summary, comparison) |
| `reports/` | Report and export generation |
| `cli.py` | Typer-based CLI entry point |

## Adding a New Parser Stage

1. Create a new module in `src/tower_analyzer/parser/`.
2. Implement a class with a clear `parse()` or `transform()` method.
3. Add it to `ParserPipeline` in `pipeline.py`.
4. Export it from `parser/__init__.py`.
5. Add tests in `tests/`.

## Adding a New Report Type

1. Create a new module in `src/tower_analyzer/reports/`.
2. Subclass `BaseReport` and implement `name` and `generate()`.
3. Add a CLI command in `cli.py` if needed.
4. Export from `reports/__init__.py`.
