# ESRA — Evolutionary Self-Recursive Architecture

**The pure technical and conceptual description of the architecture.**

> This repository contains the **essence** of ESRA: vision, principles, levels, skill contracts, control flow, and the Loop Execution Protocol.  
> It is deliberately free of any specific runtime implementation (Hermes, Python engine, etc.).

**Official name:** ESRA — Evolutionary Self-Recursive Architecture

---

## What is ESRA?

ESRA is a modular, meta-reflective architecture that enables autonomous agents (and human-AI teams) to perform **deliberate, long-term, value-aligned, and antifragile self-development**.

It turns ad-hoc improvement into a structured, observable, auditable, and self-improving evolutionary process.

Core promise:  
**The more the system is used and stressed in controlled, value-aligned ways, the stronger and more capable it becomes at self-development.**

---

## Core Documents

| Document | Description |
|----------|-------------|
| [ESRA_Technical_Specification.md](docs/ESRA_Technical_Specification.md) | Vision, principles, 8-level architecture, skill contracts, control flow, observability, safety |
| [ESRA_Loop_Execution_Protocol.md](docs/ESRA_Loop_Execution_Protocol.md) | Detailed 8-stage cycle, types of cycles, rules, and constraints |

---

## The 8 Levels (Summary)

| Level | Name                        | Key Skill(s)                          | Role |
|-------|-----------------------------|---------------------------------------|------|
| 0     | Runtime                     | Runtime Agent                         | Execution |
| 1     | Reflective                  | Self-Observer                         | Observation |
| 2     | Value-oriented              | Value-Clarifier                       | Alignment |
| 3     | Deep Analysis               | Optimizer-Philosopher + System-Dynamics-Thinker | Consequences |
| 4     | Experimental                | Experimenter                          | Safe testing |
| 5     | Integrative                 | Mental-Model-Updater                  | Integration |
| 6     | Antifragile                 | Antifragility-Builder                 | Strength from stress |
| 7     | Meta                        | Loop-Auditor                          | Evolution of the architecture itself |

---

## Design Principles

- **Modularity** — every skill is an independent, versionable component
- **Meta-level** — the system can observe and improve its own improvement process
- **Value Alignment** — non-negotiable gate before significant actions
- **Antifragility** — the system must gain from controlled stress and failure
- **Observability & Auditability** — everything is loggable and inspectable
- **Recursivity** — the architecture improves itself through its own loops

---

## Relationship to Implementations

This repository (`esra`) describes **what** the architecture is.

Concrete implementations live in separate repositories:

- **hermes-esra** — production-grade implementation as Hermes skills + orchestrator
- (Future) Standalone Python engine, other runtimes, etc.

---

## How to use this repository

1. Read the Technical Specification for the full conceptual model.
2. Read the Loop Execution Protocol to understand how a single cycle actually runs.
3. Use these documents as the source of truth when implementing or auditing any runtime.

---

**ESRA is a living architecture.**  
This repository evolves together with the system it describes.
