# Contract-Build-Prove

A lean multi-agent repository skill for substantial work where "code changed" is not enough evidence that the task is complete.

Designed for **OpenAI Codex, DeepSeek Harness (DSH), and compatible subagent-capable harnesses**.

Core flow:

**Preflight → Investigate → Freeze contract → Builder → Integrate/freeze candidate → Fresh verifier → Remediate or close**

Design goal:

> **Minimum process that makes false completion difficult.**

## Default shape

When CBP is intentionally invoked:

- one coordinator;
- **one builder by default**;
- **one fresh final verifier**;
- more agents only for genuinely independent work or a named high-risk failure mode.

The coordinator owns intent, contract, orchestration, integration, candidate identity, and final state. It is not the default implementation worker and cannot replace independent verification.

Small local low-risk edits should use the harness's normal workflow instead.

## What v3 protects

- runtime/model routing is checked before implementation;
- child artifact semantics are explicit: shared workspace vs isolated returned artifact;
- contract freezes before the first tracked edit/builder launch;
- one writer at a time is the safe shared-workspace default;
- builder cannot self-accept;
- candidate identity is independently attested by the verifier before **and after** testing;
- uncommitted candidates have a canonical tracked-patch + untracked-file fingerprint;
- plan/control metadata is separated from verified source;
- repeated verification/remediation has a global circuit breaker;
- stateful/irreversible failures enter recovery/re-baseline rather than blindly retrying;
- external destructive/production actions still require authorization.

## Model routing

### DeepSeek Harness

- Builder: actual execution subagent route configured by DSH; intended setup currently resolves to MiniMax.
- Verifier: a separately configured **GPT-5.6 Luna** route.
- CBP preflights the real routes/model resolution before implementation. If Luna verification cannot be confirmed, the run is `BLOCKED` before build rather than silently using the builder route.

### Codex

- Builders: coordinator chooses for coding fit/complexity, preferring **GPT-5.6 Luna** when suitable.
- Final verifier: Luna preferred; strongest fresh independent fallback allowed if Luna is unavailable and the deviation is recorded.

## Workspace/artifact modes

Every run records one:

- `SHARED_WORKSPACE` — builder edits the coordinator-visible workspace; one active writer at a time.
- `ISOLATED_ARTIFACT` — builder returns an exact commit/patch/artifact which the coordinator integrates before candidate freeze.

## Rigor

- **Standard** — default: one builder + one final verifier.
- **High Assurance** — only for security/auth boundaries, financial/trading logic, destructive/stateful migration, sensitive production data, safety-critical behavior, or unusually costly failure. Adds only risk-justified critique/boundary verification and stateful recovery rules where relevant.

## Files

- `SKILL.md` — normative workflow and invariants.
- `agents/openai.yaml` — Codex metadata; explicit invocation by default.
- `assets/EXEC_PLAN_TEMPLATE.md` — lean durable state template.
- `references/RUNTIMES.md` — preflight, Codex/DSH routing, workspace semantics.
- `references/PLANS.md` — lean state model, candidate fingerprint, resume rules.
- `references/BUILDER_HANDOFF.md` — builder assignment contract.
- `references/VERIFIER_HANDOFF.md` — independent candidate attestation and acceptance proof.
- `references/STATEFUL.md` — High-Assurance external-state/recovery protocol.
- `references/EXAMPLE.md` — minimal end-to-end example.
- `references/verifier.example.toml` — optional Codex Luna verifier configuration.

## Install

Repository skill location:

```text
.agents/skills/contract-build-prove/
```

Explicit Codex invocation:

```text
$contract-build-prove
```

Implicit Codex invocation is disabled intentionally because CBP always launches subagents and should be chosen for substantial work, not accidentally applied to routine edits.
