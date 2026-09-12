# ESRA Data Contracts v1

**Protocol compatibility:** ESRA 1.2

**Schema dialect:** JSON Schema Draft 2020-12
**Status:** Initial normative contract set

## Purpose

These contracts make the core ESRA artifacts portable and testable across host
implementations. They define exchange shapes, not a mandatory storage engine or
agent orchestration mechanism.

## Contract set

| Schema | Purpose |
|---|---|
| `implementation-manifest.schema.json` | Declares implementation and capability maturity |
| `cycle-event.schema.json` | Common auditable event envelope |
| `observation-report.schema.json` | Separates observations, evidence, and assumptions |
| `alignment-assessment.schema.json` | Records the mandatory experiment alignment gate |
| `experiment-card.schema.json` | Defines a bounded experiment before execution |
| `model-update.schema.json` | Records evidence-backed working-rule changes |
| `audit-report.schema.json` | Records scoped findings without inventing missing history |
| `conformance-matrix.schema.json` | Describes portable exporters across implementations |

All schemas live in [`schemas/`](../schemas/).

## Versioning rules

- `protocol_version` identifies the ESRA behavioral protocol. These schemas
  target protocol `1.2`.
- `schema_version` identifies an individual record shape. Initial record
  schemas use `1.0.0`.
- Additive optional fields require a schema minor version.
- Removing a field, changing its meaning, or making an optional field required
  requires a schema major version.
- Implementations must publish `esra-conformance.json` and distinguish
  `implemented`, `verified`, `simulated`, and `planned` capabilities.
- Existing implementation-specific logs need not be rewritten. Adapters may
  map legacy records into these contracts at export boundaries.

## Portable event export

Conforming implementations expose an explicit, read-only exporter that emits
one `cycle-event@1.0.0` JSON object per line. Exporters must:

- preserve the implementation's existing storage format;
- emit deterministic identifiers when a legacy record has no identifier;
- normalize timestamps to RFC 3339 with an offset;
- map unavailable or blocked execution to `not-run` rather than success;
- export only an allowlisted payload and omit prompts, transcripts, raw session
  identifiers, command output, and hidden reasoning;
- identify source records through concise evidence references.

The machine-readable cross-implementation view is
[`conformance/compatibility-matrix.json`](../conformance/compatibility-matrix.json).
Its `verified` status means that repository tests exercise the adapter and its
privacy boundary. It does not prove host-native lifecycle integration.

## Conformance

The repository test suite validates every schema against Draft 2020-12 and
checks positive and negative fixtures. A host implementation is conformant
only for the capabilities and evidence it declares; a manifest is not proof of
host-native execution.
