---
name: contract-build-prove
description: Orchestrate substantial repository work with mandatory builder and verifier subagents, a frozen behavioral contract, exact-candidate verification, and restartable evidence. Use for multi-session, multi-component, migration, deployment, difficult debugging, or high-risk work in Codex, DeepSeek Harness, and compatible subagent harnesses. Do not use for trivial local edits.
---

# Contract-Build-Prove

**Preflight → Contract → Build → Candidate → Prove**

Make false completion difficult without making process the main job.

If CBP is active, subagents are mandatory. Start with **one bounded builder work packet + one independent final verifier**. Use additional sequential builders when useful; parallel writers require isolation.

`SKILL.md` is normative. References operationalize it.

## Invariants

1. **Coordinator orchestrates.** Behavioral implementation goes to builders; coordinator edits are mechanical integration only.
2. **One active shared writer.** Never keep multiple write-capable children active in one shared workspace.
3. **Builder cannot accept itself.** Builder checks are evidence only.
4. **Verifier is genuinely independent.** Every attempt uses a new child that did not implement the candidate and does **not** inherit coordinator/builder conversation.
5. **Behavior freezes before implementation.** Required behavior, protected behavior, and evidence strength freeze before the first candidate-affecting edit or implementation-builder launch.
6. **Attested artifact = tested artifact.** Verifier attests the artifact it tests, tests that same artifact, then re-attests it.
7. **Protect work/state.** Never overwrite user/newer/unrelated work; external destructive/production actions require explicit authorization or repository policy.

## 0. Preflight

Read the common preflight plus only the active harness section in `references/RUNTIMES.md`.

Record in the lean plan:

- actual builder/verifier routes and active verifier policy;
- verifier new child = `YES`;
- verifier inherits parent conversation = `NO`;
- `SHARED_WORKSPACE` or `ISOLATED_ARTIFACT`;
- plan location is visible to the next expected coordinator session.

Do not infer model routing, context isolation, or artifact transport from prompt wording/role names. If required capability cannot be established, `BLOCKED` before implementation.

Create/reuse one small durable plan from `assets/EXEC_PLAN_TEMPLATE.md`; use `references/PLANS.md`.

## 1. Contract

Record only the safety baseline needed: repository instructions, branch/HEAD, protected working-tree changes, and relevant runtime/external state.

For unknown-root-cause debugging, investigate first. Read-only exploration is preferred. Pre-freeze tracked diagnostic edits are allowed only in a disposable investigation workspace that cannot become the candidate; otherwise freeze first.

Acceptance criteria define required observable behavior, protected behavior/non-goals, and a verification approach. Reproduce bugs before fixing when reasonably possible.

Freeze required/protected behavior and evidence strength immediately before the first candidate-affecting edit or implementation-builder launch. Weakening them later requires `OLD / NEW / REASON / IMPACT` plus explicit user authorization.

Verification technique may be refined without amendment when equivalent or stronger and the frozen requirement is unchanged.

For investigation, two consecutive cycles with no fault-domain narrowing or new discriminating evidence require a fresh synthesis/replan before another hypothesis.

## 2. Build

Use `references/BUILDER_HANDOFF.md`.

- Start with one bounded builder work packet.
- Use another **sequential** builder when remaining work is materially different or too broad for one reliable handoff.
- Shared workspace: one write-capable child at a time.
- Parallel writers: isolated artifacts/worktrees or explicit safe integration controls only.
- Debugging scope: owned outcome + likely area + exclusions.

Artifact transport must be explicit: shared builder diff is inspected directly; isolated builder work must return an exact integratable artifact. A prose summary is never integration.

Test ownership: builder runs focused development checks; coordinator runs only integration-specific checks when needed; verifier owns acceptance/regression proof. Candidate-bound immutable CI evidence may replace an expensive rerun when it fully proves the criterion.

## 3. Candidate

Before final verification, coordinator:

1. confirms all builder artifacts are integrated;
2. inspects real diff/status and protected work;
3. confirms no shared write-capable child remains active;
4. creates exact candidate identity;
5. freezes verified source.

Use an exact local commit SHA whenever permitted. If work must remain uncommitted, use bundled `scripts/candidate_id.py`; do not recreate its fingerprint manually. See `references/PLANS.md`.

ExecPlan/control state is not verified source. Source/config/test changes after freeze create a new candidate.

For persistent external-state work, candidate identity also includes the applicable tuple from `references/STATEFUL.md`.

## 4. Prove

Use `references/VERIFIER_HANDOFF.md` and a **new clean-context verifier child for every attempt**.

Verifier must attest the artifact it will test, prove every criterion, verify any stateful target, then re-attest the **same tested artifact**. If using a writable snapshot/worktree, attest/test/re-attest that snapshot itself—not the parent workspace.

On `FAIL`:

1. if `RECOVERY_REQUIRED=YES` or external state is ambiguous, run `references/STATEFUL.md` recovery first;
2. otherwise remediate all concrete understood findings that safely fit one coherent builder pass; `LARGEST_GAP` is priority, not a one-finding limit;
3. integrate → new candidate → new clean-context verifier.

Progress breaker: if the same failed surface/blocker survives **two consecutive remediation cycles without material improvement or new discriminating evidence**, perform one fresh root-cause synthesis/replan. One further non-improving cycle ends `PARTIAL` or `BLOCKED`. Do not stop merely because several FAILs occurred while the system is converging.

## High Assurance

Use only for security/auth boundaries, financial/trading logic, destructive/stateful migrations, sensitive production data, safety-critical behavior, or unusually costly failure.

Add only controls justified by a **specific named failure mode**: at most a focused contract critique and/or one critical-boundary verification. For persistent external mutation, read `references/STATEFUL.md` before mutation.

## DONE

After verifier `PASS`, coordinator performs one cheap final identity check and confirms no shared writer is active. Stateful work also requires `RECOVERY_REQUIRED=NO` and the accepted state target to remain current.

Declare `DONE` only when every required criterion is `PASS` for that current candidate, required runtime proof passes, protected work is intact, and no recovery remains. Otherwise report `PARTIAL` or `BLOCKED` with the next safe action.

## References

- `references/RUNTIMES.md` — runtime/model/context preflight + artifact mode.
- `references/PLANS.md` — lean state + candidate helper + resume.
- `references/BUILDER_HANDOFF.md` — builder work packet.
- `references/VERIFIER_HANDOFF.md` — clean-context exact-artifact proof.
- `references/STATEFUL.md` — external-state identity/recovery.
- `references/EXAMPLE.md` — minimal example.
- `references/verifier.example.toml` — optional Codex verifier.
