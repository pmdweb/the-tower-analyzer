# Architecture

The analyzer follows a staged, read-only pipeline:

```text
Input file
  -> container inspection
  -> bounded decompression
  -> NRBF record scanner
  -> inert object graph
  -> domain mapping
  -> analysis
  -> JSON / Markdown / HTML output
```

## Boundaries

### `parser`

Owns binary parsing, validation, limits and inert intermediate representations. It must not contain gameplay recommendations.

### `models`

Owns typed domain models for account state after field mappings are validated.

### `analysis`

Owns derived metrics such as ROI, progression deltas and farming comparisons.

### `reports`

Owns presentation and export. It must not read binary files directly.

## Non-goals

- Save editing
- Save restoration
- Account automation
- Native BinaryFormatter deserialization
