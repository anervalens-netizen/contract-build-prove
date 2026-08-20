---
name: contract-build-prove
description: Orchestrate substantial repository work with mandatory builder and verifier subagents, a frozen behavioral contract, exact-candidate verification, and restartable evidence. Use for multi-session, multi-component, migration, deployment, difficult debugging, or high-risk work in Codex, DeepSeek Harness, and compatible subagent harnesses. Do not use for trivial local edits.
---

# Contract-Build-Prove

Protocol version: **5**

**Preflight → Contract → Build → Candidate → Prove**

Make false completion difficult without making process the main job.

If CBP is active, subagents are mandatory. Prefer **one coherent end-to-end builder + one independent final verifier** when one child can reliably own the change. Add sequential builders only when useful; parallel writers require isolation.

`SKILL.md` is normative. References operationalize it.

## Invariants

1. **Coordinator orchestrates.** Behavioral implementation goes to builders; coordinator edits are mechanical integration only.
2. **One shared writer total.** At most one writer may touch a shared workspace, including coordinator and descendants. Nested writers must be isolated.
3. **Builder cannot accept itself.** Builder checks are evidence only.
4. **Verifier is independent.** Every attempt uses a new child that did not implement the candidate and does **not** inherit coordinator/builder conversation.
5. **Freeze what must be proven.** Required/protected behavior freezes before the first candidate-affecting edit or builder launch. Verification method may change only if the new proof is at least as convincing.
6. **Attested artifact = tested artifact.** Attest → test that artifact → re-attest.
7. **Protect work and side effects.** Never overwrite user/newer/unrelated work. No push, merge, deploy, publish/release, production mutation, destructive, paid, or irreversible external action without explicit user or repository authorization.

## 0. Preflight

Read common preflight + only the active harness section in `references/RUNTIMES.md`.

Reuse a prevalidated **trusted runtime profile** when available; confirm its routes/capabilities are still available instead of rediscovering harness semantics. Otherwise establish `AD_HOC` once.

Record: runtime profile, actual builder/verifier routes/policy, verifier new child=`YES`, inherits parent conversation=`NO`, workspace mode, and a plan location visible to the next coordinator session.

Do not infer routing, context isolation, or artifact transport from names/prompts. Missing required capability → `BLOCKED` before build.

Create/reuse one lean durable plan from `assets/EXEC_PLAN_TEMPLATE.md`; see `references/PLANS.md`.

## 1. Contract

Record only the safety baseline: repository instructions, branch/HEAD, protected working-tree changes, relevant runtime/external state.

For unknown-root-cause debugging, investigate first. Pre-freeze tracked diagnostics are allowed only in a disposable investigation workspace that cannot become the candidate; otherwise freeze first.

Acceptance criteria define required behavior, protected behavior/non-goals, and how each result can be proven. Reproduce bugs before fixing when reasonably possible.

Freeze required/protected behavior immediately before the first candidate-affecting edit or builder launch. Weakening it later requires `OLD / NEW / REASON / IMPACT` + explicit user authorization. A proof method may change without amendment only if it is at least as convincing and the frozen requirement is unchanged.

Two consecutive investigation cycles with no fault-domain narrowing or new discriminating evidence require synthesis/replan before another hypothesis.

## 2. Build

Use `references/BUILDER_HANDOFF.md`.

- Prefer one end-to-end builder for one coherent change. **Do not split merely by files or layers.**
- Add a sequential builder when remaining work is materially different or too broad for one reliable handoff.
- `SHARED_WORKSPACE`: one writer total; builders may not spawn nested shared writers.
- Parallel writers require isolation + explicit integration.
- Unexpected overlapping drift before/after a shared builder packet must be reconciled; prefer isolated artifacts when concurrent human/process edits are likely.

A prose summary is never integration.

Test ownership: builder = focused development checks; coordinator = integration-only checks when needed; verifier = acceptance/regression authority. Candidate-bound immutable CI evidence may replace an expensive rerun when it fully proves the criterion.

## 3. Candidate

Before verification: integrate all artifacts, inspect real diff/status, preserve protected work, stop all shared writers, create exact candidate identity, freeze source.

Use an exact local commit SHA whenever permitted. **Default commit verification = clean isolated worktree/snapshot materialized from that exact SHA.** Testing the current workspace instead requires proving no candidate-affecting tracked/untracked differences from the SHA except declared control state.

Unrelated pre-existing user/newer work must not become an implicit dependency. Isolate CBP-owned work, or explicitly record the pre-existing change as an authorized baseline dependency; otherwise `BLOCKED`. Never hide protected source by excluding it from identity.

If uncommitted, use bundled `scripts/candidate_id.py`; unsupported worktree state means use a commit/isolated artifact or block. Do not recreate its fingerprint manually. See `references/PLANS.md`.

Control state is not verified source. Persistent external-state work also uses `references/STATEFUL.md`.

## 4. Prove

Use `references/VERIFIER_HANDOFF.md` and a **new clean-context verifier** for every attempt.

First, verifier compares objective/protected behavior with the frozen contract. A clearly missing objective-essential requirement → `BLOCKED: CONTRACT_COVERAGE_GAP`; do not invent requirements.

Then attest the exact artifact to test, prove every criterion/state target, and re-attest the same artifact. Candidate-authored tests count only after the verifier confirms they actually exercise/assert the frozen behavior.

On `FAIL`: stateful recovery first when required; otherwise batch all concrete understood findings that safely fit one coherent builder pass. Integrate → new candidate → new clean verifier.

If the same failed surface/blocker survives **two consecutive cycles without material improvement or new discriminating evidence**, do one root-cause synthesis/replan. One further non-improving cycle ends `PARTIAL` or `BLOCKED`.

## High Assurance

Use only for security/auth, financial/trading logic, destructive/stateful migrations, sensitive production data, safety-critical behavior, or unusually costly failure. Add only controls justified by a named failure mode. Read `references/STATEFUL.md` before persistent external mutation.

## DONE

After verifier `PASS`, coordinator performs one cheap final identity check and confirms no shared writer is active. Stateful work also requires current accepted state and `RECOVERY_REQUIRED=NO`.

`DONE` only when every required criterion is `PASS`, required runtime proof passes, protected work is intact, and no recovery remains.

`PARTIAL` = some requested outcome is proven, but not all required criteria are complete.  
`BLOCKED` = no safe progress is possible without missing access, capability, authorization, decision, isolation, or recovery.

## References

- `references/RUNTIMES.md` — runtime profiles + preflight.
- `references/PLANS.md` — lean state + candidate helper + resume/version rules.
- `references/BUILDER_HANDOFF.md` — builder packet.
- `references/VERIFIER_HANDOFF.md` — coverage + exact-artifact proof.
- `references/STATEFUL.md` — external-state recovery.
- `references/EXAMPLE.md` — minimal example.
- `references/verifier.example.toml` — optional Codex verifier.
