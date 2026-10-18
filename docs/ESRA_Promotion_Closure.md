# ESRA — Promotion and Propagation Closure

**Applicability:** Additive cross-host improvement-reporting guidance compatible with ESRA 1.2. It does **not** modify existing JSON schemas, the eight-stage loop, or the autonomous host's local promotion rules.

## Why this exists

A lesson recorded in a conversation, a proposed patch, a Git commit, a merged PR, and an installed host policy are different states. Do not say an improvement is "promoted everywhere" when only the reasoning or a repository copy has changed.

## Required target manifest for multi-surface improvements

At proposal/alignment time identify:

- **Scope:** conversation/session, user memory, project repository, installed host, or cross-host;
- **Owner and authoritative source:** canonical policy/specification and the version or evaluated revision;
- **Targets:** explicit repositories/files and the installed host adapters/skill distributions that must consume them; note which are merely optional;
- **Propagation:** permitted update method, authorization boundary, and next synchronization or activation step;
- **Verification:** observable evidence per target (commit or artifact hash, accessible installed file/revision, host discovery or behavior test, deployment receipt, CI result);
- **Rollback:** recovery plan for failed installation or incompatible behavior;
- **Evidence status:** `PENDING`, `PARTIAL`, or `PROMOTED`, plus blockers and the next owner.

Do not persist credentials, transcripts, full prompts, private tool payloads, or raw session identifiers in records. Use minimal allowlisted references and evidence hashes.

## Closure rule

1. **Evaluate:** establish an observable, bounded baseline/candidate test. Passing a conceptual thought experiment is not proof of deployed behavior.
2. **Promote locally:** make only authorized changes to the precisely evaluated revision; preserve existing revision-binding, protected surfaces, snapshot, and rollback constraints. A local `promotion-receipt` remains local.
3. **Propagate:** for every *required* destination, confirm the intended revision is present, discoverable by its host, and, where applicable, effective under a representative invocation. A policy file in Git is not evidence that Codex, Antigravity, or Hermes has loaded it.
4. **Close:** report `PROMOTED` **only** if all declared required targets pass. Report `PARTIAL` when at least one required target is verified and at least one remains incomplete. Report `PENDING` for a proposal, unexecuted change, or absence of verified required targets. Record outstanding work as a bounded handoff, not a false completion.
5. **Learn:** retain the revised working rule, evidence limits, and reconsideration trigger. A partial/pending promotion may yield a valid learning record, but must never be labeled fully deployed.

A target outside current access or authorization is **not** silently removed from required scope. Mark it blocked/pending and request the required action. A user-approved scope reduction must be recorded explicitly before declaring closure.

## Non-recursion and ownership

Promotion checks belong to the *same* ESRA cycle; they must not spawn a review of that review. ESRA defines the improvement and evidence contract, **not** which AI model to assign to a normal engineering task. Model/effort routing stays with the consuming orchestration system (for example, `ai-orchestration/protocol/MODEL_SELECTION.md`).

This guidance creates no autonomous permission to edit repositories, install skills, change security controls, or spend subscription quotas.
