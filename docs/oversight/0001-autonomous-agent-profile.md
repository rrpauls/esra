# Oversight proposal 0001: Autonomous Agent Profile

## Decision

Define an additive Autonomous Agent Profile for ESRA 1.2. Existing cycle-event
export and host-behavior contracts remain compatible; autonomous lifecycle
claims require their own schemas and host gate.

## Normative boundary

The profile covers guarded evolution of agent-owned skills and routing metadata.
It does not authorize model-weight changes, credential access, host
configuration changes, or automatic modification of ESRA values and safety
controls.

## Evidence required

An implementation must demonstrate native observation, bounded triggering,
revision-bound proposals, alignment, comparable evaluation, atomic local
promotion, post-change monitoring, rollback, privacy, restart recovery, and
recursion suppression before claiming verified autonomous operation.
