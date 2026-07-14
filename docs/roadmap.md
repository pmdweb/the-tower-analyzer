# Roadmap

## Phase 1 — Safe container inspection

- [x] Validate GZip header
- [x] Decompress with a size limit
- [x] Calculate SHA-256
- [x] Detect probable NRBF payload
- [ ] Add CLI integration tests

## Phase 2 — NRBF record scanner

- [ ] Parse stream header
- [ ] Enumerate record types
- [ ] Parse libraries and class metadata
- [ ] Track object IDs and references
- [ ] Reject malformed graphs safely

## Phase 3 — PlayerData mapping

- [ ] Identify the root object
- [ ] Export the raw object graph to JSON
- [ ] Map Workshop, Labs, Cards, Modules, UWs, economy and tier progress
- [ ] Sanitize personal identifiers

## Phase 4 — Analysis

- [ ] Generate Markdown reports
- [ ] Compare snapshots
- [ ] Calculate upgrade ROI
- [ ] Recommend farming tiers from run history

## Phase 5 — Presentation

- [ ] Generate HTML reports
- [ ] Add progression charts
- [ ] Provide a local dashboard
