---
name: contract-build-prove
description: Orchestrate substantial repository work with mandatory builder and verifier subagents, a frozen acceptance contract, exact-candidate verification, and restartable evidence. Use for multi-session, multi-component, migration, deployment, difficult debugging, or high-risk work in Codex, DeepSeek Harness, and compatible subagent harnesses. Do not use for trivial local edits.
---

# Contract-Build-Prove

**Preflight → Contract → Build → Candidate → Prove**

Make false completion difficult without making process the main job.

If this skill is active, subagents are mandatory. Standard CBP normally means **one builder + one fresh final verifier**. Add agents only for genuinely independent work or a named high-risk reason.

`SKILL.md` is normative. References operationalize it; they do not redefine it.

## Invariants

1. **Coordinator orchestrates.** Meaningful behavioral implementation goes to builders. Coordinator edits are limited to mechanical merge/conflict/integration work; behavioral changes return to a builder.
2. **Builder cannot accept itself.** Builder checks are evidence only.
3. **Verifier is fresh.** Every verification attempt uses a new child context that did not implement that candidate.
4. **Contract freezes before implementation.** Read-only investigation may happen first; freeze before the first tracked edit or implementation-builder launch.
5. **Verifier attests the exact candidate.** It independently checks identity before and after tests. Mismatch is `BLOCKED`, never `PASS`.
6. **Protect existing work.** Never overwrite user/newer/unrelated changes.
7. **External side effects require authorization.** No push, merge, deploy, production mutation, destructive migration, deletion, or irreversible action unless explicitly authorized by the user or repository policy.

## 0. Preflight

Before edits, read `references/RUNTIMES.md` and record in the lean plan:

- actual builder route/model;
- actual verifier route/model;
- fresh-context support;
- `SHARED_WORKSPACE` or `ISOLATED_ARTIFACT`.

Do not assume prompt wording selects a model. In the intended DSH setup, the verifier route must actually resolve to **GPT-5.6 Luna**; otherwise CBP is `BLOCKED` before build. Codex prefers Luna but may use the documented fresh-verifier fallback.

Create/reuse one small durable plan from `assets/EXEC_PLAN_TEMPLATE.md`; use `references/PLANS.md`. If the repository already has an equivalent canonical plan, reuse it.

## 1. Contract

Record only the baseline needed for safety: applicable repository instructions, branch/HEAD, working-tree changes to protect, and relevant runtime/external state.

For unknown-root-cause debugging, investigate read-only first; explorer/diagnostic children are allowed and do not count as the mandatory implementation builder. Normal failed hypotheses are investigation, not automatically stagnation.

Acceptance criteria must state:

- observable required behavior;
- protected behavior/non-goals;
- verification method + expected result.

For bug fixes, reproduce the failure before the fix when reasonably possible.

**Freeze the contract immediately before the first tracked implementation/test edit or implementation-builder launch.** After freeze, amendments use `OLD / NEW / REASON / IMPACT`. Explicit user authorization is required to weaken required behavior, protected behavior, or evidence strength.

## 2. Build

Use `references/BUILDER_HANDOFF.md`.

Default: **one builder writer** owning the change end to end.

- Shared workspace: one active write-capable builder at a time.
- Parallel writers: only with isolated worktrees/branches/artifacts or explicit non-overlap + integration controls.
- Debugging scope: owned outcome + likely area + exclusions; do not pretend exact files are known before root cause is known.

Artifact transport must be explicit:

- `SHARED_WORKSPACE` → coordinator inspects the builder's actual workspace diff.
- `ISOLATED_ARTIFACT` → builder returns an exact commit/patch/artifact; coordinator explicitly integrates it.

A prose builder summary is never integration. A builder may self-test but may not mark acceptance criteria `PASS`.

## 3. Candidate

Before final verification, coordinator:

1. confirms all builder artifacts are actually integrated;
2. inspects the real diff/status and relevant regression checks;
3. confirms protected work is intact;
4. creates the exact candidate identity from `references/PLANS.md`;
5. freezes verified source.

Prefer an exact local commit SHA. If uncommitted, use the canonical tracked-patch + untracked-manifest fingerprint.

The ExecPlan is declared **control state**, not verified source. Source/config/test changes after freeze create a new candidate. Control-state-only changes do not, but the verifier must independently confirm that distinction.

## 4. Prove

Use `references/VERIFIER_HANDOFF.md` and a **new verifier child for every attempt**.

The verifier must:

1. independently attest expected candidate identity;
2. verify every required criterion from direct evidence;
3. attest candidate identity again after tests;
4. return `PASS | FAIL | BLOCKED`, criterion results, evidence, findings, and the largest gap.

Tests may use an isolated writable snapshot when caches/build/temp files are necessary. Verified tracked source must remain unchanged.

On `FAIL`: fix the largest demonstrated gap with a builder → integrate → new candidate → **new fresh verifier**.

Circuit breaker: after **3 final-verifier FAILs**, or **2 full cycles without reducing failed criteria/severity**, stop normal remediation and do one fresh root-cause replan. One further non-improving cycle ends `PARTIAL` or `BLOCKED` rather than looping indefinitely.

`PARTIAL` = useful requested work is proven but not every criterion can be completed within current authorized scope. `BLOCKED` = no safe next action exists without missing capability, access, decision, or recovery.

## High Assurance only when needed

Use High Assurance for security/auth boundaries, financial/trading logic, destructive/stateful migrations, sensitive production data, safety-critical behavior, or unusually costly failure.

Add only what a **specific named failure mode** justifies: a fresh contract critique and/or one critical-boundary verification. Do not multiply verifier cycles ceremonially.

If persistent external state is mutated, read `references/STATEFUL.md` before mutation. Source SHA alone is insufficient. A failed/partial irreversible mutation enters recovery: stop mutation, re-baseline actual state, choose rollback or explicit forward recovery, then continue from that real state.

## DONE

Declare `DONE` only when every required criterion is `PASS` for the current attested candidate, relevant regression/runtime proof passes, protected work is intact, and no required stateful recovery remains.

Otherwise report `PARTIAL` or `BLOCKED` with the exact failed/blocked criteria and next safe action.

## References

- `references/RUNTIMES.md` — runtime/model preflight + artifact modes.
- `references/PLANS.md` — lean state + candidate fingerprint + resume.
- `references/BUILDER_HANDOFF.md` — builder contract.
- `references/VERIFIER_HANDOFF.md` — candidate attestation + proof contract.
- `references/STATEFUL.md` — external-state identity/recovery.
- `references/EXAMPLE.md` — minimal example.
- `references/verifier.example.toml` — optional Codex Luna verifier.
