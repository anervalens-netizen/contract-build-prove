---
name: contract-build-prove
description: Orchestrate substantial repository work with mandatory builder and verifier subagents, a frozen behavioral contract, exact-candidate verification, and restartable evidence. Use for multi-session, multi-component, migration, deployment, difficult debugging, or high-risk work in Codex, DeepSeek Harness, and compatible subagent harnesses. Do not use for trivial local edits.
---

# Contract-Build-Prove

**Preflight → Contract → Build → Candidate → Prove**

Make false completion difficult without making process the main job.

If this skill is active, subagents are mandatory. Standard CBP starts with **one bounded builder work packet + one genuinely independent final verifier**. Use additional sequential builders when the remaining work is materially different or too broad for one reliable handoff. Add parallel writers only when isolation makes that safe.

`SKILL.md` is normative. References operationalize it; they do not redefine it.

## Invariants

1. **Coordinator orchestrates.** Behavioral implementation goes to builders. Coordinator edits are limited to mechanical integration/conflict work; behavioral changes return to a builder.
2. **One active shared writer.** In a shared workspace, never keep more than one write-capable child active at once.
3. **Builder cannot accept itself.** Builder checks are evidence only.
4. **Verifier is genuinely independent.** Every verification attempt uses a new child context that did not implement the candidate **and does not inherit the coordinator/builder conversation**.
5. **Behavior freezes before implementation.** Required behavior, protected behavior, and required evidence strength freeze before the first candidate-affecting edit or implementation-builder launch.
6. **The attested artifact is the tested artifact.** The verifier attests the exact artifact it will test, tests that same artifact, then attests that same artifact again.
7. **Protect existing work and external state.** Never overwrite user/newer/unrelated work. Push, merge, deploy, production mutation, destructive migration, deletion, or irreversible external action requires explicit authorization or repository policy.

## 0. Preflight

Read the common preflight plus **only the active harness section** in `references/RUNTIMES.md`.

Record in the lean plan:

- actual builder route/model;
- actual verifier route/model/policy;
- verifier creates a new child: `YES|NO`;
- verifier inherits parent conversation: must be `NO`;
- `SHARED_WORKSPACE` or `ISOLATED_ARTIFACT`;
- plan location is visible to the next expected coordinator session.

Do not assume prompt wording selects a model or clean context. If required routing, verifier independence, artifact transport, or durable plan visibility cannot be established, report `BLOCKED` before implementation.

Create/reuse one small durable plan from `assets/EXEC_PLAN_TEMPLATE.md`; use `references/PLANS.md`. If the repository already has an equivalent canonical plan, reuse it.

## 1. Contract

Record only the safety baseline needed for the task: repository instructions, branch/HEAD, protected working-tree changes, and relevant runtime/external state.

For unknown-root-cause debugging, investigate before implementation. Read-only exploration is preferred. If tracked diagnostic edits are required before the behavioral contract is ready, make them only in a disposable investigation workspace that cannot become the final candidate; otherwise freeze first.

Acceptance criteria define:

- required observable behavior;
- protected behavior/non-goals;
- a verification approach and expected result.

For bug fixes, reproduce the failure before the fix when reasonably possible.

**Freeze required behavior, protected behavior, and evidence strength immediately before the first candidate-affecting edit or implementation-builder launch.** After freeze, weakening any of those requires `OLD / NEW / REASON / IMPACT` plus explicit user authorization.

The exact verification technique may be refined without an amendment when it is equivalent or stronger and does not change what must be proven.

Investigation continues only while it produces information gain. Two consecutive investigation cycles that neither narrow the fault domain nor produce new discriminating evidence require a fresh synthesis/replan before another hypothesis.

## 2. Build

Use `references/BUILDER_HANDOFF.md`.

- Start with one bounded builder work packet.
- Use another **sequential** builder when the remaining scope is materially different or too broad for one reliable handoff.
- In `SHARED_WORKSPACE`, only one write-capable child may be active.
- Parallel writers require isolated worktrees/branches/artifacts or explicit non-overlap plus integration controls.
- For debugging, scope by owned outcome + likely area + exclusions; do not invent exact file certainty before root cause is known.

Artifact transport is explicit:

- `SHARED_WORKSPACE` → coordinator inspects the actual builder-visible diff.
- `ISOLATED_ARTIFACT` → builder returns an exact commit/patch/artifact and coordinator explicitly integrates it.

A prose summary is never integration.

### Test ownership

- **Builder:** focused development tests for its change.
- **Coordinator:** integration-specific checks only when integration itself creates meaningful risk; do not routinely rerun the builder's full suite.
- **Verifier:** acceptance/regression authority. It may independently inspect trusted immutable CI evidence tied to the exact candidate instead of rerunning an expensive gate when that evidence is sufficient.

## 3. Candidate

Before final verification, coordinator:

1. confirms every builder artifact is integrated;
2. inspects the real diff/status;
3. confirms protected work is intact;
4. confirms **no write-capable shared-workspace child remains active**;
5. creates the exact candidate identity;
6. freezes verified source.

Use an exact local commit SHA whenever local commits are permitted. This is the dominant path.

If the candidate must remain uncommitted, use the bundled deterministic `scripts/candidate_id.py`; do not recreate the fingerprint algorithm manually. See `references/PLANS.md`.

The ExecPlan is control state, not verified source. Source/config/test changes after freeze create a new candidate; declared control-state-only changes do not.

For persistent external-state work, the candidate also includes the applicable source/environment/deployed/external-state tuple from `references/STATEFUL.md`.

## 4. Prove

Use `references/VERIFIER_HANDOFF.md` and a **new clean-context verifier child for every attempt**.

The verifier must:

1. attest the artifact it will actually test;
2. verify every required criterion from direct evidence;
3. verify the stateful target too when one exists;
4. attest the **same tested artifact** again after verification;
5. return `PASS | FAIL | BLOCKED`, criterion results, evidence, findings, and `LARGEST_GAP`.

If verification uses a writable snapshot/worktree, materialize the candidate there, attest **that snapshot**, test **that snapshot**, then re-attest **that snapshot**. Never attest the parent workspace and test a different artifact.

### On FAIL

First check recovery precedence:

- if `RECOVERY_REQUIRED=YES`, or an external mutation left state ambiguous, execute `references/STATEFUL.md` recovery **before normal remediation**;
- otherwise remediate **all concrete understood findings that can safely fit one coherent builder pass**. `LARGEST_GAP` is a priority signal, not a one-finding scope limit.

Then integrate → create a new candidate → launch a new clean-context verifier.

### Progress breaker

Do not stop merely because several verifier attempts failed while the failed surface is shrinking.

If the same failed surface/blocker survives **two consecutive remediation cycles without meaningful reduction in failed criteria/severity or new discriminating evidence**, perform one fresh root-cause synthesis/replan. One further non-improving cycle ends `PARTIAL` or `BLOCKED` instead of looping indefinitely.

`PARTIAL` = useful requested work is proven, but not every criterion can be completed within current authorized scope. `BLOCKED` = no safe next action exists without missing capability, access, decision, evidence source, or recovery work.

## High Assurance only when needed

Use High Assurance for security/auth boundaries, financial/trading logic, destructive/stateful migrations, sensitive production data, safety-critical behavior, or unusually costly failure.

Add only what a **specific named failure mode** justifies: at most a focused contract critique and/or one critical-boundary verification. Do not multiply verifier cycles ceremonially.

If persistent external state can change, read `references/STATEFUL.md` before mutation.

## DONE

After verifier `PASS`, coordinator performs one cheap final identity check against the verified candidate and confirms no shared writer is active. For stateful work, `RECOVERY_REQUIRED` must be `NO` and the accepted state tuple must still be the current target.

Declare `DONE` only when every required criterion is `PASS` for that current candidate, relevant runtime proof passes, protected work is intact, and no required recovery remains.

Otherwise report `PARTIAL` or `BLOCKED` with the exact failed/blocked criteria and next safe action.

## References

- `references/RUNTIMES.md` — runtime/model/context preflight + artifact modes.
- `references/PLANS.md` — lean state + candidate identity helper + resume.
- `references/BUILDER_HANDOFF.md` — builder contract.
- `references/VERIFIER_HANDOFF.md` — clean-context candidate attestation + proof contract.
- `references/STATEFUL.md` — external-state identity/recovery.
- `references/EXAMPLE.md` — minimal example.
- `references/verifier.example.toml` — optional Codex verifier configuration.
