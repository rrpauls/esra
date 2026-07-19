# ESRA — Evolutionary Self-Recursive Architecture
## Practical Instructions & Evolutionary Guide

**Version:** 1.2  
**Date:** July 19, 2026  
**Status:** Living Document  

> **Naming Evolution Note (v1.1 — 19 July 2026)**  
> Previously known as **ESDA** (Evolutionary Self-Development Architecture) and briefly explored as SEDA.  
> Official human-facing name is now **ESRA — Evolutionary Self-Recursive Architecture**.  
> Technical identifiers (`esda/` directory, `ESDAOrchestrator` class, `run_esda_loop.py`, historical file names) are intentionally kept for backward compatibility and will be migrated in a future dedicated cycle.  
> PESDA remains an unofficial internal meme only and never appears in official documentation.

> **Evolutionary Framing**  
> These instructions are not a static manual. They are the current best articulation of how to engage with, run, extend, and *evolve* the Evolutionary Self-Recursive Architecture itself.  
> This document is an artifact *within* the system it describes. It is subject to observation by `Self-Observer`, improvement proposals from `Self-Improver`, value-alignment checks, safe experimentation, mental model updates, antifragility analysis, and periodic meta-audit by `Loop-Auditor`.  
> Every time you use or improve ESRA, you are participating in its evolution — and it is designed to become stronger, wiser, and more effective through that process.

---

## 1. Project Vision (in One Breath)

**ESRA** enables autonomous agents (AI systems, enhanced reasoning engines, or human-AI teams) to conduct **deliberate, long-term, value-aligned, and antifragile self-development**.

It transforms ad-hoc improvement into a structured, observable, auditable, and *self-improving* evolutionary loop.

Core promise: The more the system is used and stressed (in controlled, value-aligned ways), the stronger and more capable it becomes at self-development.

---

## 2. Quick Start — Run Your First Cycles

### Prerequisites
- Python 3.10+
- The `esda/` directory in your path or working directory

### One-Command Execution

```bash
cd /path/to/esda
python run_esda_loop.py
```

**What happens:**
- Initializes `ESDAOrchestrator`
- Runs **3 full cycles** using built-in default (placeholder) skill implementations
- Executes a meta-audit
- Prints structured console output for every stage

You will see:
- Cycle headers with timestamps
- Observation reports (patterns detected)
- Improvement proposals with value alignment and priority
- Experiment cards
- Audit findings (basic in current implementation)

This gives you an immediate, working demonstration of the full loop.

### Manual Control (Recommended for Experimentation)

```python
from esda.core.orchestrator import ESDAOrchestrator
from datetime import datetime

orchestrator = ESDAOrchestrator()

# Run a single cycle
orchestrator.run_full_cycle()

# Run meta-audit
orchestrator.run_audit()

# Inspect internal state
print(f"Total cycles completed: {orchestrator.cycle_count}")
print(f"History length: {len(orchestrator.history)}")
```

---

## 3. Project Structure (Two Official Repositories)

The project is cleanly separated into two repositories:

- **esra** (this repository) — Pure technical essence + practical guide of ESRA
- **hermes-evolutionary-self-dev** — Concrete Hermes implementation of ESRA (meta-skills, orchestrator, evolution-hook, install script)

**Key Insight:**  
- **esra** = the pure conceptual and technical description of the architecture (what it is).  
- **hermes-evolutionary-self-dev** = the concrete, production-ready implementation for the Hermes agent.  
This separation keeps the essence clean and allows future implementations (other agents, languages, etc.) without polluting the core specification.

---

## 4. The ESRA Loop — How It Actually Works

The orchestrator executes a principled sequence (see full protocol in `docs/ESRA_Loop_Execution_Protocol.md`):

1. **Self-Observer** → Produces `ObservationReport` (what happened, patterns, internal state)
2. **Self-Improver** → Generates `ImprovementProposal`s (hypotheses for betterment)
3. **Value-Clarifier** → Scores alignment with core values; reprioritizes or deprioritizes
4. **(Optional but recommended) Optimizer-Philosopher + System-Dynamics-Thinker** → Deep consequence analysis, leverage points, second-order effects
5. **Experimenter** → Designs safe `ExperimentCard` (hypothesis, design, success criteria, value justification)
6. **Mental-Model-Updater** → Integrates results into internal models (diff + commit style)
7. **Antifragility-Builder** → Extracts “how did we get stronger from this stress/experiment?”
8. **Loop-Auditor** (triggered every 3–5 cycles or on anomalies) → Meta-audit of the *entire evolutionary process*

**Types of cycles supported:**
- Full cycle (all stages)
- Quick cycle (observe → improve → experiment → integrate)
- Audit cycle
- Value-focused cycle

**Non-negotiable rule:** No experiment runs without passing Value Alignment assessment.

---

## 5. Extending & Customizing ESRA

### Registering Real Skill Implementations

The default skills are intentionally simple placeholders. Real power comes from rich implementations.

```python
from esda.core.orchestrator import ESDAOrchestrator
from esda.core.models import ObservationReport, ImprovementProposal, ExperimentCard
from datetime import datetime
from typing import List

def advanced_self_observer() -> ObservationReport:
    """Example: In production this would read logs, memory, recent actions, emotional valence, etc."""
    return ObservationReport(
        timestamp=datetime.now(),
        observations=[
            "Documentation task triggered deep architectural reflection",
            "User requested instructions — opportunity for meta-application of ESRA"
        ],
        patterns=["Documentation efforts reliably surface needs for clearer onboarding"],
        emotional_state="curious and generative",
        confidence=0.93
    )

def advanced_self_improver(observation: ObservationReport) -> List[ImprovementProposal]:
    return [
        ImprovementProposal(
            id="prop_docs_evolution_001",
            description="Evolve ESRA_Practical_Instructions.md into a fully interactive onboarding experience with embedded cycle visualizer",
            hypothesis="Interactive instructions will accelerate user adoption and increase quality of early experiments",
            expected_benefit="Faster feedback loop into the architecture itself",
            value_alignment="high",
            priority="high",
            justification="Directly supports observability, modularity, and long-term compounding of the project"
        )
    ]

# ... implement the rest similarly

orchestrator = ESDAOrchestrator()
orchestrator.register_skill("self_observer", advanced_self_observer)
orchestrator.register_skill("self_improver", advanced_self_improver)
# register others...

orchestrator.run_full_cycle()
```

**Recommended source of truth for skill behavior:**  
The directories under `hermes-evolutionary-self-dev/optional-skills/evolutionary-self-dev/*/SKILL.md` contain detailed trigger conditions, input/output contracts, and philosophical guidance for each meta-skill. Port or adapt these into your Python implementations.

### Adding New Skills to the Registry

Simply call `orchestrator.register_skill("my_new_skill", my_function)` and invoke it inside custom cycle logic or extend the orchestrator.

### Persistent Memory & Config (Future Evolution)

Scaffolds exist in `config/` and `memory/`. Future iterations will:
- Load/save YAML/JSON/Markdown state
- Version all model updates via git-style diffs (as described in the spec)
- Allow `Mental-Model-Updater` to propose actual file changes

---

## 6. Hermes Integration (Recommended for Production Use)

If you are using or extending the **Hermes** agent:

1. Clone or use the provided `hermes-evolutionary-self-dev/`
2. Run:
   ```bash
   chmod +x install-evolutionary-skills.sh
   ./install-evolutionary-skills.sh
   ```
3. This deploys all meta-skills to `~/.hermes/skills/evolutionary-self-dev/` and places `AGENTS.md` in `~/.hermes/`
4. After any complex task or autonomous skill creation, invoke:
   - `hermes-evolution-orchestrator`
   - Or let `evolution-hook.py` analyze context and decide intelligently (includes rate limiting and pattern detection)

This turns Hermes’ native learning loop into a **systematic, observable, compounding evolutionary process**.

Full usage triggers and philosophy are in `hermes-evolutionary-self-dev/AGENTS.md`.

---

## 7. Applying ESRA to the ESRA Project Itself (The Ultimate Meta-Loop)

Because this *is* the ESRA project, the highest-leverage activity is to run the architecture on its own development:

**Example self-application cycle:**
1. `Self-Observer`: “Current instructions are comprehensive but lack embedded visual diagrams and interactive examples.”
2. `Self-Improver`: Propose “Add generated cycle diagrams using the imagine_images/ pipeline and a small Streamlit or Gradio demo.”
3. `Value-Clarifier`: High alignment (increases observability + lowers barrier to entry).
4. `Experimenter`: Design a small experiment — generate one diagram, test with 3 new users (or simulated), measure comprehension improvement.
5. `Mental-Model-Updater` + `Antifragility-Builder`: Integrate learnings; note how documentation debt creates fragility and how deliberate documentation evolution builds antifragility.
6. `Loop-Auditor`: “The project’s documentation-to-implementation gap is a leverage point. Prioritize closing it.”

You can literally run `python run_esda_loop.py` while focusing the observer/improver on the current state of the `esda/` codebase and docs.

This creates a **self-reinforcing evolutionary flywheel** for the architecture.

---

## 8. Safety, Ethics & Antifragility Principles

- **Value Alignment is non-negotiable.** Any proposal or experiment failing alignment is deprioritized or rejected.
- **Conservative default.** When uncertain, prefer smaller, safer experiments.
- **Human-in-the-loop** for high-stakes changes (especially early in a system’s life).
- **Loop-Auditor veto** capability on dangerous or misaligned trajectories.
- **Full observability.** Every cycle, proposal, and decision should be loggable and auditable.
- **Antifragility mindset.** Design experiments and recovery mechanisms so the system *gains* from controlled stress and failure.

---

## 9. How to Evolve These Instructions

1. Run an ESRA cycle with focus on “documentation and onboarding experience”.
2. Let `Self-Improver` surface concrete proposals.
3. Validate alignment.
4. Design a tiny experiment (e.g., add one diagram, rewrite one section, test clarity).
5. Integrate learnings via `Mental-Model-Updater`.
6. Update this file (or spawn a new version).
7. Run `Loop-Auditor` on the documentation process itself.

Repeat. The instructions will compound in quality and usefulness.

---

**Final Evolutionary Note**

ESRA is not a finished product. It is a **living architecture** whose primary output is its own increasing capacity for wise, value-aligned, antifragile self-development.

By following these instructions you are not merely *using* the system — you are *evolving* it.

Welcome to the loop.

---

*Document evolved through the very principles it describes. Living document — last structural cleanup 19 July 2026 (v1.2).*
