# Changelog

All notable changes to the ESRA specification and conformance tooling are
documented here. The project follows semantic versioning for published data
contracts; the overall specification remains pre-1.0.

## Unreleased

### Added

- `benchmark-scenario@1.0.0` and `benchmark-result@1.0.0` contracts.
- A deterministic cross-implementation exporter benchmark with JSON and
  Markdown reports.
- Synthetic scenarios for success, `not-run`, missing IDs, privacy filtering,
  empty input, malformed records, and invalid timestamps.
- A separate host behavior pilot protocol for ChatGPT/Codex, Claude Code, and
  Hermes Agent.

### Changed

- The technical roadmap now reports evidence-backed maturity instead of
  labeling the historical foundation phase as current.

### Release gate

- No stable tag is created until the nine host-pilot cases are completed,
  sanitized evidence is reviewed, and capability manifests are reconciled.
