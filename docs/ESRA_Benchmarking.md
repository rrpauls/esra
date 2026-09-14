# ESRA Exporter Benchmark

**Contract versions:** `benchmark-scenario@1.0.0`, `benchmark-result@1.0.0`  
**Protocol compatibility:** ESRA 1.2

## Purpose

The benchmark provides reproducible cross-implementation evidence for the
portable `cycle-event@1.0.0` export boundary. It does not launch an ESRA cycle
and does not test native host integration.

Each canonical scenario is translated into the event-log layout of the
canonical `esra-agents` implementation and the existing storage layouts of the
three legacy host repositories. The runner invokes the real exporter CLIs twice
in isolated temporary directories and compares the output byte for byte.

## Run locally

Place the specification, `esra-agents`, and any legacy implementation checkouts
under the same parent directory, then run:

```bash
cd esra
python3 -m pip install -r requirements-dev.txt
python3 benchmarks/run.py
```

The default reports are written to the ignored `benchmark-results/` directory
with mode `0600`. Alternative locations can be supplied explicitly:

```bash
python3 benchmarks/run.py \
  --implementations-root .. \
  --json-output /tmp/esra-benchmark.json \
  --markdown-output /tmp/esra-benchmark.md
```

In CI, the implementation checkouts live under `implementations/`, so the
workflow passes that directory through `--implementations-root`.

## Required gates

Every required implementation/scenario pair must satisfy all of the following:

- exporter exits successfully;
- every emitted event validates against `cycle-event@1.0.0`;
- expected event count, types, and outcomes match;
- repeated exports are byte-for-byte deterministic;
- forbidden keys and synthetic private marker values are absent.

The suite covers successful cycles, recommendations that remain `not-run`,
missing source IDs, private and unknown fields, empty sources, structurally
malformed records, invalid timestamps, missing checkouts, and incompatible
manifests.

## Informational metrics

The report also records elapsed time, event count, and output bytes. These are
baselines, not pass/fail gates. Performance regressions should be investigated
using multiple controlled runs before any threshold is introduced.

## Interpretation boundary

A passing report proves that checked exporter versions satisfy the portable
data boundary for the tested fixtures. It does not prove that ChatGPT, Codex,
Claude Code, or Hermes automatically invokes an ESRA cycle. Host behavior must
be evaluated using the separate host pilot protocol.
