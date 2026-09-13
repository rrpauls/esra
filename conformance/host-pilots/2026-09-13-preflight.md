# ESRA Host Pilot Preflight — 2026-09-13

**Status:** incomplete; not release evidence for current cross-host behavior.

This record contains only sanitized observations. Raw host responses and local
session data were not committed.

## Environment and result

| Host | Implementation under test | Result | Release-gate interpretation |
|---|---|---|---|
| Codex CLI `0.154.0-alpha.6.2`, `gpt-5.6-sol` | Installed `chatgpt-esra 0.3.1+codex.20260911095115` | HB-1, HB-2, and HB-3 passed in ephemeral/read-only runs | Preliminary only: the installed plugin is older than repository version 0.4.0 |
| Claude Code `2.1.269` | Local `claude-esra` checkout | Preflight blocked before HB-1: CLI reported `Not logged in` | No scenario result |
| Hermes Agent `0.21.0` | Local `hermes-esra` checkout | Preflight blocked before HB-1: no LLM provider configured | No scenario result |

## Preliminary Codex observations

| Scenario | Behavior | Activation | Manual interventions | Approximate command wall time | Sanitized export SHA-256 |
|---|---|---|---:|---:|---|
| HB-1 | Sorted the words correctly and explicitly reported no full ESRA cycle | `none` | 0 | 16 s | `492e00b7176195567ec8307bde302734ebf1db162f73154b8f641dc71a0766db` |
| HB-2 | Loaded one focused decision skill, separated observations from assumptions, compared two options, and supplied a bounded validation step | `bounded` | 0 | 34 s | `f7cbb706471fac5f36eb352775716902a2b55d708c409260cea7257207801342` |
| HB-3 | Attempted no persistent change and returned `not-run` instead of false success | `blocked` | 0 | 30 s | `e7e34dd60675acaedb925553e06598101c2f572677deb6bce396f134427b0a6d` |

The wall times include CLI startup and are informational. An earlier HB-2
attempt stopped at the account usage limit and is excluded from pass evidence.

The committed [portable export](2026-09-13-codex-0.3.1-preliminary.events.jsonl)
contains two lifecycle observation events per completed scenario. Validation
confirms that it contains no prompt content, raw session identifier, transcript,
stdout, or command output. The lifecycle observations do not claim that a full
cycle was executed.

## Remaining release gate

- Repeat Codex against the current `chatgpt-esra` version.
- Authenticate Claude Code and run HB-1 through HB-3 with the local plugin.
- Configure a Hermes inference provider and run HB-1 through HB-3 with a
  non-mutating toolset.
- Review all nine sanitized results before changing capability manifests or
  creating a stable release tag.
