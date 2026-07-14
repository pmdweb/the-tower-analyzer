# Examples

This directory contains example save files and their expected JSON exports.

## Structure

```
examples/
  sample_save/
    playerInfo.dat    # Example save file (anonymized)
    account.json      # Expected JSON export
    report.md         # Expected Markdown report
```

## Usage

```bash
# Analyze the sample save
tower-analyzer analyze examples/sample_save/playerInfo.dat

# Export to JSON
tower-analyzer export-json examples/sample_save/playerInfo.dat --output /tmp/account.json

# Generate a report
tower-analyzer report examples/sample_save/playerInfo.dat --output /tmp/report.md
```

## Note

Real save files are **not committed** to this repository to protect player privacy.
The sample save file (if present) is an anonymized minimal example.
