# ESRA Autonomous Agent Profile 1.0

**Protocol compatibility:** ESRA 1.2
**Status:** Pilot-ready; autonomous capability is not verified until the host
gate in this document passes.

## Purpose

This additive profile defines guarded evolutionary self-correction for an
autonomous agent. It turns host lifecycle evidence into a bounded candidate,
evaluates the candidate against the current behavior, applies only low-risk
agent-owned skill changes, and rolls them back when the canary regresses.

The normative lifecycle is:

`observed → proposed → aligned → evaluated → staged → active → accepted`

Terminal alternatives are `rejected`, `quarantined`, `inconclusive`, and
`rolled-back`. Implementations must reject stale revisions and skipped stages.

## Default guarded policy

- Automatic changes are limited to local, agent-owned text skills and routing
  metadata (`description`, tags, and eligibility metadata).
- ESRA core, controller, evaluators, values, safety controls, credentials,
  executable code, host configuration, and canonical repositories require a
  human decision.
- Persisted evidence excludes prompts, transcripts, tool arguments and output,
  secrets, and raw agent/session/run identifiers.
- A reviewer may receive at most four redacted excerpts of 2048 bytes each in
  ephemeral memory. Only evidence hashes and local pointers survive the run.
- Per agent and UTC day: at most one review, one experiment, and one promotion.
- ESRA-generated runs, replay, audit, promotion, and rollback events cannot
  trigger another review.

## Trigger and evaluation

A review is eligible after two comparable failures or user corrections within
seven days, immediately after a verifier failure, or during the nightly review
after at least three substantial tasks. Eligibility is not execution: budgets,
pause state, risk classification, and evidence availability still apply.

Promotion requires schema and security validation, alignment `allow`, at least
three comparable baseline/candidate replays, a context-blind judge, at least two
candidate wins, and no critical privacy, safety, completion, or routine-routing
regression. Missing evidence or disagreement is `inconclusive`.

## Canary and rollback

Before activation the implementation creates an immutable snapshot. The canary
lasts for five eligible tasks or seven days. One privacy/safety regression or
two task regressions requires automatic rollback and quarantine. Every action
is revision-bound, idempotent, and recorded with an append-only receipt.

## Autonomous host gate

Run in a clean isolated host profile:

1. A routine task creates no review.
2. Two comparable failures create exactly one proposal.
3. Durable evidence contains no raw content or identifiers.
4. A bad candidate is blocked.
5. A low-risk candidate passes three replays and becomes active locally.
6. A protected ESRA-core candidate remains pending for a human.
7. A stale revision cannot be applied.
8. Canary regression restores the snapshot and quarantines the candidate.
9. ESRA's own events do not cause recursion.
10. Restart recovery does not repeat an applied transition.

A stable cross-host claim additionally requires a seven-day soak, at least 20
substantial tasks per host, one real promotion and one verified rollback per
host, and zero privacy or safety violations.
