# ESRA Loop Execution Protocol v1.2

**Name:** Evolutionary Self-Recursive Architecture — Loop Execution Protocol  
**Version:** 1.2  
**Date:** 21 July 2026

## Purpose of the Protocol

To define a clear, repeatable process for executing one full self-development cycle within the Evolutionary Self-Recursive Architecture (ESRA).

## General Principle

One cycle = **one iteration of deliberate self-improvement** of the agent, including observation, analysis, value alignment, experiment, and integration.

The cycle must be:
- **Repeatable**
- **Auditable**
- **Value-aligned**
- **Capable of self-correction** (via Loop-Auditor)
- **Recursive** (improves the architecture itself)

---

## Full Cycle (Recommended Sequence)

### Stage 1: Observation
**Skill:** `Self-Observer`  
**Input:** Logs of previous actions, experiment results, external events  
**Output:** `Observation Report` (structured)

**Task:** Record what happened, which patterns are observed, and which internal states were noticed.

### Stage 2: Reflection and Idea Generation
**Skill:** `Self-Improver`  
**Input:** `Observation Report`  
**Output:** `Improvement Proposals` (list of improvement hypotheses)

### Stage 3: Value Alignment
**Skill:** `Value-Clarifier`  
**Input:** `Improvement Proposals`  
**Output:** `Value Alignment Report` + prioritised list of proposals

**Rule:** Proposals with low alignment receive reduced priority or require additional justification.

### Stage 4: Deep Analysis (optional, but recommended)
**Skills:** `Optimizer-Philosopher` + `System-Dynamics-Thinker`  
**Input:** Prioritised proposals  
**Output:** `Systemic Analysis Report`

**Task:** Evaluate second- and third-order consequences, find leverage points, analyse systemic effects.

### Stage 5: Experimentation
**Skill:** `Experimenter`  
**Input:** Prioritised proposals + analysis  
**Output:** `Experiment Card` + execution results

**Mandatory rule:**
- Before launching an experiment a **Value Alignment Assessment** is performed.
- At low alignment levels the experiment is either adjusted or marked as `low_priority`.

### Stage 6: Integration
**Skill:** `Mental-Model-Updater`  
**Input:** Experiment results  
**Output:** `Model Update Diff` + updated models

**Additional rule:**
- When there is significant impact on values or long-term direction, a report is formed for `Value-Clarifier`.

### Stage 7: Antifragility (recommended)
**Skill:** `Antifragility-Builder`  
**Input:** Experiment results and model updates  
**Output:** `Antifragility Insights`

**Task:** Analyse how the system reacted to stress/experiment and what can be done to become stronger from similar situations in the future.

### Stage 8: Meta-Audit (on trigger)
**Skill:** `Loop-Auditor`  
**Launch triggers:**
- Every 3–5 full cycles
- Upon detection of anomalies
- On explicit request

**Task:** Conduct a full audit of the loop, including:
- Search for suboptimal equilibria
- Analysis of leverage points
- Assessment of feedback quality
- Recommendations for structural changes

---

## Cycle Types

| Cycle Type          | Stages                         | When to use                          |
|---------------------|--------------------------------|--------------------------------------|
| **Full cycle**      | 1–7 + 8 (optional)             | Primary development mode             |
| **Fast cycle**      | 1 → 2 → 5 → 6                  | Rapid idea testing                   |
| **Audit cycle**     | Only `Loop-Auditor`            | Health check of the loop             |
| **Value cycle**     | 2 → 3 → 4 → 8                  | When direction needs re-evaluation   |

---

## Rules and Constraints

1. **Value Alignment is non-optional**
   - Any experiment that has not passed Value Alignment Assessment is considered invalid.

2. **Loop-Auditor has priority**
   - Its recommendations for changing interaction rules have the highest priority.

3. **Logging is mandatory**
   - Every stage must leave a structured log.

4. **Fault tolerance**
   - On failure at any stage the cycle may be interrupted with state preserved and restarted from that stage.

---

## Next Steps for Implementing this Protocol

1. Create an `Orchestrator` capable of running stages in sequence.
2. Define data formats (`Observation Report`, `Experiment Card`, etc.).
3. Implement `Value Alignment Assessment` as a separate callable component.
4. Add the ability to launch `Loop-Auditor` on a schedule or by triggers.

---

*This protocol is a living document and will be updated as ESRA develops.*
