# Contributing

Thank you for your interest in contributing to The Tower Save Analyzer!

## Development Setup

```bash
# Clone the repository
git clone https://github.com/pmdweb/the-tower-analyzer.git
cd the-tower-analyzer

# Install uv (https://docs.astral.sh/uv/)
pip install uv

# Install the project with dev dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

## Running Tests

```bash
uv run pytest
```

## Linting and Type Checking

```bash
uv run ruff check src tests
uv run ruff format src tests
uv run mypy
```

## Project Structure

See [architecture.md](architecture.md) for a full description.

## Contribution Guidelines

1. **Never modify save files.** The project is strictly read-only.
2. Write tests for all new parser stages.
3. Do not invent field values – leave TODOs for unimplemented decoding.
4. Follow PEP 8 and the existing type annotation style.
5. Run `ruff` and `mypy` before opening a PR.
6. Update `docs/reverse_engineering_status.md` when decode progress changes.

## Reverse Engineering

If you have additional knowledge about the save file format, please:

1. Add findings to `docs/reverse_engineering_status.md`.
2. Open an issue with `[RE]` in the title.
3. Provide sample save files (with no personal data) for testing.
