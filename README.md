# Contract-Build-Prove

A lean multi-agent repository skill for substantial work where "code changed" is not enough evidence that the task is complete.

Designed for **OpenAI Codex, DeepSeek Harness (DSH), and compatible subagent-capable harnesses**.

Core flow:

**Preflight → Contract → Build → Candidate → Prove**

Design goal:

> **Minimum process that makes false completion difficult.**

## Default shape

When CBP is intentionally invoked:

- one coordinator;
- one **active writer** at a time in shared workspace;
- one bounded builder work packet to start, with additional sequential builders only when useful;
- one genuinely independent final verifier with no inherited implementation conversation;
- extra parallel writers only behind explicit isolation/integration controls.

The coordinator owns intent, contract, orchestration, integration, candidate identity, and final state. It is not the implementation monolith and cannot replace independent verification.

Small local low-risk edits should use the harness's normal workflow instead.

## Key properties

- runtime/model/context routing is checked before implementation;
- shared workspace vs isolated returned artifact is explicit;
- verifier independence means **new child + no inherited parent conversation**;
- required/protected behavior freezes before candidate-affecting implementation;
- debugging may refine the verification technique without weakening the frozen requirement;
- builder cannot self-accept;
- **attested artifact == tested artifact**;
- verifier attests candidate identity before and after testing;
- commit SHA is the normal candidate identity;
- uncommitted fallback uses bundled deterministic `scripts/candidate_id.py`, not hand-built hashing;
- builder runs focused tests, coordinator only integration-specific checks, verifier owns acceptance/regression proof;
- understood verifier findings are batched into coherent remediation passes;
- loop control is based on **lack of progress**, not raw verifier-failure count;
- stateful/irreversible failures enter recovery/re-baseline before normal remediation;
- coordinator performs one cheap final identity check before `DONE`;
- external destructive/production actions require authorization.

## Model routing

### DeepSeek Harness

- Builder: actual execution route configured by DSH; intended setup currently resolves to MiniMax.
- Verifier: separately configured **GPT-5.6 Luna** route.
- Final verifier route must create a new child **without inheriting coordinator/builder conversation**. A fork-style inherited-context route is not sufficient.
- If required Luna routing or clean-context verification cannot be confirmed, CBP blocks before implementation.

### Codex

- Builders: coordinator chooses for coding fit/complexity, preferring **GPT-5.6 Luna** when suitable.
- Final verifier: Luna preferred; strongest suitable clean-context independent fallback allowed when Luna is unavailable and the deviation is recorded.

## Candidate identity

Preferred:

```text
exact local commit SHA
```

When the candidate must remain uncommitted:

```text
python3 <skill-root>/scripts/candidate_id.py create --exclude .cbp/PLAN.md
```

The verifier recomputes the same identity with the helper. The helper includes tracked binary diff plus untracked path/type/Git-mode/content semantics.

## Workspace/artifact modes

- `SHARED_WORKSPACE` — builder edits the coordinator-visible workspace; one active write-capable child at a time.
- `ISOLATED_ARTIFACT` — builder returns an exact commit/patch/artifact which the coordinator integrates before candidate freeze.

## Rigor

- **Standard** — lean default flow above.
- **High Assurance** — only for security/auth boundaries, financial/trading logic, destructive/stateful migration, sensitive production data, safety-critical behavior, or unusually costly failure. Add only controls justified by a named risk.

## Files

- `SKILL.md` — normative five-stage workflow.
- `agents/openai.yaml` — Codex metadata; explicit invocation by default.
- `assets/EXEC_PLAN_TEMPLATE.md` — lean durable state.
- `scripts/candidate_id.py` — deterministic uncommitted candidate identity helper.
- `references/RUNTIMES.md` — runtime/model/context preflight + artifact semantics.
- `references/PLANS.md` — lean state, identity usage, progress/resume rules.
- `references/BUILDER_HANDOFF.md` — bounded builder work packet.
- `references/VERIFIER_HANDOFF.md` — clean-context exact-artifact acceptance proof.
- `references/STATEFUL.md` — external-state identity/recovery.
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

Implicit Codex invocation is intentionally disabled because CBP always launches subagents and should be chosen for substantial work rather than applied accidentally to routine edits.
