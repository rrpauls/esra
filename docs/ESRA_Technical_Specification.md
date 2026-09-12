# ESRA — Evolutionary Self-Recursive Architecture
**Technical Specification v1.2**

**Date:** 21 July 2026  
**Status:** Primary Specification  
**Author:** Grok (in co-authorship with the user)

---

## 1. Vision & Principles

**Evolutionary Self-Recursive Architecture (ESRA)** is a modular, meta-reflective architecture for creating autonomous agents capable of long-term, deliberate, and antifragile self-development.

### Core Principles:

- **Modularity** — every skill is an independent, versionable component.
- **Meta-level** — presence of a component capable of analysing and improving the development system itself (`Loop-Auditor`).
- **Value Alignment** — mandatory check of action consistency with values before significant actions.
- **Game Theory + Systems Thinking** — analysis of skill interactions as a repeated game and search for leverage points.
- **Antifragility** — the architecture must become stronger from stress, errors, and uncertainty.
- **Observability** — all interactions are logged and available for audit.
- **Evolvability** — the system is capable of reinforcing successful interaction patterns over time.
- **Recursivity** — the architecture improves itself through its own cycles.

---

## 2. Architecture Levels

ESRA is organised into 8 levels:

| Level | Name                        | Purpose                                           | Key Skill(s)                                      | Meta-role   |
|-------|-----------------------------|---------------------------------------------------|---------------------------------------------------|-------------|
| 0     | Runtime                     | Task execution and tool interaction               | Runtime Agent                                     | —           |
| 1     | Reflective                  | Observation and analysis of own behaviour         | Self-Observer                                     | —           |
| 2     | Value-oriented              | Maintenance and evolution of values and direction | Value-Clarifier                                   | High        |
| 3     | Deep Analysis               | Philosophical and systemic analysis of consequences | Optimizer-Philosopher + System-Dynamics-Thinker | High        |
| 4     | Experimental                | Design and testing of hypotheses                  | Experimenter                                      | Medium      |
| 5     | Integrative                 | Updating of mental models                         | Mental-Model-Updater                              | High        |
| 6     | Antifragile                 | Development of resilience to stress               | Antifragility-Builder                             | Medium      |
| 7     | Meta                        | Audit and evolution of the architecture itself    | Loop-Auditor                                      | **Critical**|

---

## 3. Components and Their Contracts

### 3.1 Skill Contract (Common Skill Interface)

Every skill must implement the following contract:

```markdown
## Input
- Structured input (Pydantic model or JSON Schema)

## Output
- Structured output + 
- Confidence score (0.0–1.0)
- Reasoning trace (optional, but recommended)

## Required output fields
- `result`: primary result
- `confidence`: confidence level
- `justification`: brief rationale
- `suggested_next_skills`: list of skills to which control should be passed
```

### 3.2 Key Skills

#### `Loop-Auditor` (Level 7) — The Most Important Component

**Responsibilities:**
- Conduct periodic and on-demand audits of the entire loop.
- Analyse skill interactions as a repeated game.
- Search for suboptimal Nash equilibria.
- Identify leverage points in the current architecture.
- Propose structural changes to interaction rules.

**Input:** Access to logs, call histories, current skill models.

**Output:** Structured Audit Report with prioritised recommendations.

#### `Experimenter` (Level 4)

**Mandatory check:**
- Before designing an experiment, `Value-Clarifier` must be invoked.
- At low alignment levels the experiment receives reduced priority.

---

## 4. Control Flow

A **hybrid approach** is recommended:

1. **Main flow** proceeds through levels 0 → 7 (see the companion document for the exact stage sequence, inputs/outputs and cycle types).
2. `Loop-Auditor` may intervene at any stage (especially after significant changes).
3. When problems are detected, `Loop-Auditor` may:
   - Propose changes to interaction rules.
   - Lower the priority of certain skills.
   - Initiate special "remedial" experiments.

**Authoritative cycle definition:**  
The detailed 8-stage Loop Execution Protocol (stages, data contracts, cycle variants, rules) lives in  
`docs/ESRA_Loop_Execution_Protocol.md`.  
This Specification deliberately does not duplicate that content.

---

## 5. State Storage and Versioning

- All skill models and knowledge are stored in **Markdown** (convenient for LLMs).
- Changes are versioned via Git (or equivalent).
- `Mental-Model-Updater` works through a `diff` + commit mechanism.
- `Loop-Auditor` may propose changes in the form of ready-made diffs.

---

## 6. Observability and Logging

**Must be logged:**
- All skill invocations (input → output)
- Experiment results
- `Loop-Auditor` reports
- Changes to values and models

It is recommended to store logs in structured form (`JSONL` + indexing).
Normative portable record shapes and versioning rules are defined in
`docs/ESRA_Data_Contracts.md` and `schemas/`.

---

## 7. Safety and Fault-Tolerance Principles

- When in doubt the system must prefer **conservative behaviour**.
- `Loop-Auditor` has the right of "veto" over dangerous changes.
- All significant changes must pass through a confirmation mechanism (human-in-the-loop in early stages).
- A history of all architecture changes is maintained.

---

## 8. Implementation Maturity and Roadmap

Maturity is reported from reproducible evidence rather than inferred from the
architecture diagram or the presence of a skill file.

| Area | Current maturity | Evidence and boundary |
|---|---|---|
| Foundation and governance | Verified | Apache-2.0 licensing, contribution rules, this specification, and repository CI |
| Portable data contracts | Verified | Draft 2020-12 schemas, positive/negative fixtures, and ESRA 1.2 conformance manifests |
| Portable cycle-event export | Verified for synthetic fixtures | Cross-implementation exporter tests and the [benchmark](ESRA_Benchmarking.md); this does not prove native lifecycle integration |
| Bounded host behavior | Pilot-ready, not cross-host verified | The [host pilot protocol](ESRA_Host_Pilot_Protocol.md) defines nine required host/scenario cases; results are not yet claimed |
| Living-cycle orchestration | Implementation-specific | Skill-based orchestration exists, while automatic execution is not assumed and Hermes native lifecycle integration remains planned |
| Depth and evolutionary dynamics | Proposed or implementation-specific | `Optimizer-Philosopher`, `System-Dynamics-Thinker`, mental-model updating, and antifragility require host evidence before architecture-wide maturity claims |

The next release gate is completion of the host pilot, reconciliation of its
evidence with implementation manifests, and maintainer review. An Event Bus or
separate Codex implementation should be introduced only if runtime evidence
shows that existing adapters cannot preserve the protocol boundary.

---

**The document will be updated as the architecture develops.**

---

*This specification is a living document. All changes should pass through discussion and, preferably, through `Loop-Auditor`.*
