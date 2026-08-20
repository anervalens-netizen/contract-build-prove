---
name: contract-build-prove
description: Orchestrate substantial repository work with mandatory builder and verifier subagents, a frozen acceptance contract, exact-candidate verification, and restartable evidence. Use for multi-session, multi-component, migration, deployment, difficult debugging, or high-risk work in Codex, DeepSeek Harness, and compatible subagent harnesses. Do not use for trivial local edits.
---

# Contract-Build-Prove

Make false completion difficult without making process the main job.

**Coordinator → preflight/investigate → freeze contract → builder → integrate/freeze candidate → fresh verifier → remediate or close**

If this skill is active, subagents are mandatory. Standard CBP normally means **one builder + one final verifier**. Add agents only for genuinely independent work or a specific high-risk reason.

`SKILL.md` is normative. Files under `references/` operationalize these rules and must not redefine them.

## Non-negotiable invariants

1. **Coordinator orchestrates.** Meaningful behavioral implementation goes to builder subagents. The coordinator may resolve mechanical merge conflicts and make trivial integration-only edits; behavioral changes return to a builder.
2. **Builder cannot accept itself.** Builder checks are evidence inputs only.
3. **Verifier is fresh.** Every verification attempt uses a new child context that did not implement that candidate.
4. **Contract freezes before implementation.** Read-only investigation may happen first; freeze before the first tracked repository edit or implementation-builder launch.
5. **Verifier proves the exact candidate.** It independently attests candidate identity before and after verification. Identity mismatch is `BLOCKED`, never `PASS`.
6. **Protect existing work.** Never overwrite user/newer/unrelated changes.
7. **External side effects require authorization.** No push, merge, deploy, production mutation, destructive migration, deletion, or irreversible external action unless explicitly authorized by the user or repository policy.

## 0. Runtime preflight — before edits

Read `references/RUNTIMES.md` and establish:

- harness/runtime;
- actual builder route/model;
- actual verifier route/model;
- fresh-context support;
- artifact/workspace mode: `SHARED_WORKSPACE` or `ISOLATED_ARTIFACT`;
- repository access needed by both roles.

Do not assume a prompt can select a model the harness did not route. In the intended DSH setup, the verifier route must resolve to **GPT-5.6 Luna**. If required routing/freshness cannot be confirmed, report `BLOCKED` **before implementation**.

For Codex, prefer GPT-5.6 Luna for builders when suitable and especially for final verification; a documented fallback is allowed by `references/RUNTIMES.md`.

## 1. Understand and investigate

Establish only the baseline needed to work safely:

- applicable repository instructions;
- branch and exact HEAD;
- working-tree/user/newer changes to protect;
- relevant runtime/external state when the objective depends on it.

For unknown-root-cause debugging, use read-only exploration before committing to an implementation hypothesis. Explorer/diagnostic subagents are allowed and do not count as the mandatory implementation builder.

Read-only investigation may inspect files, logs, history, tests, and runtime observations. A new regression test, diagnostic instrumentation committed to the repository, or any other tracked edit requires the contract to be frozen first.

Create or reuse one small durable plan using `assets/EXEC_PLAN_TEMPLATE.md`; read `references/PLANS.md`. If the repository already has an equivalent canonical plan system, reuse it instead of creating another tracker.

## 2. Define and freeze success

Write falsifiable acceptance criteria that state:

- observable required behavior;
- protected behavior/non-goals;
- verification method and expected result.

For bug fixes, reproduce the failure before the fix when reasonably possible. If reproduction is impossible, record why.

**Freeze the contract immediately before the first tracked implementation/test edit or implementation-builder launch.**

After freeze, any criterion change records `OLD / NEW / REASON / IMPACT`. Explicit user authorization is required to weaken the observable outcome, protected behavior, **or required evidence strength**. Never redefine success to escape a blocker.

High Assurance is reserved for security/auth boundaries, financial/trading logic, destructive/stateful migrations, sensitive production data, safety-critical behavior, or unusually costly failure. It may add a fresh contract critique and at most one critical-boundary verification when a named failure mode justifies it. Do not add verification ceremony by default.

## 3. Delegate the build

Use `references/BUILDER_HANDOFF.md`.

Default rules:

- **one builder writer at a time**;
- one builder owns a tightly coupled change set end to end;
- parallelize investigation/testing freely;
- parallelize writers only when isolated by worktree/branch/artifact, or when explicit non-overlapping ownership plus integration controls make collisions genuinely unlikely;
- in a shared workspace, never run multiple write-capable builders concurrently;
- for debugging, scope by owned outcome + likely area + exclusions rather than pretending the exact files are already known.

Artifact transport is explicit:

- `SHARED_WORKSPACE`: builder edits the coordinator-visible workspace; coordinator inspects the actual diff.
- `ISOLATED_ARTIFACT`: builder returns an exact commit/patch/artifact; coordinator must integrate it before candidate freeze.

A builder may self-test but may not mark acceptance criteria `PASS`.

## 4. Integrate and freeze the candidate

The coordinator must:

1. confirm every builder artifact is actually present in the integrated workspace;
2. inspect the real integrated diff/status, not only builder summaries;
3. run relevant narrow/regression checks;
4. confirm protected user/newer work remains intact;
5. create the exact candidate identity described in `references/PLANS.md`;
6. freeze that candidate for final verification.

Prefer an exact local commit SHA. If the candidate must remain uncommitted, use the canonical tracked-patch + untracked-manifest fingerprint from `references/PLANS.md`.

The ExecPlan/control-state file is **not verified source** and must be declared as control metadata. Do not commit or mutate verified source after freeze. Source/config/test changes create a new candidate; control-state-only updates do not, provided the verifier independently confirms that distinction.

## 5. Prove with one fresh verifier

Use `references/VERIFIER_HANDOFF.md`.

The verifier must, in order:

1. independently attest that the workspace/artifact matches the expected candidate identity;
2. inspect/test the actual candidate against every required criterion;
3. independently attest candidate identity again after verification;
4. return `PASS`, `FAIL`, or `BLOCKED` with reproducible evidence.

Candidate identity mismatch before or after tests is `BLOCKED: CANDIDATE_IDENTITY_MISMATCH`.

The verifier receives the objective, frozen contract/amendments, protected behavior, candidate identity, runtime target, and access constraints. Do **not** give builder confidence, a defense of the implementation, or a desired verdict.

Verifier execution may use an isolated writable snapshot when tests require caches/build output/temp databases. Tracked candidate source must remain unchanged; production mutation is forbidden during verification unless a separately authorized verification step explicitly requires it.

## 6. Remediate without looping forever

On `FAIL`:

- target the largest demonstrated gap;
- launch an appropriate builder;
- integrate the fix;
- create a new candidate identity;
- launch a **new fresh verifier child**.

Normal debugging failures are not automatically stagnation. Progress means the failed acceptance surface, severity, or causal uncertainty is measurably shrinking.

Global circuit breaker:

- after **3 final-verifier FAILs**, or **2 full cycles with no reduction in failed criteria/severity**, stop normal remediation and perform one fresh root-cause replan/investigation;
- if one further cycle still does not improve the failed surface, report `PARTIAL` or `BLOCKED` instead of continuing indefinitely.

`PARTIAL` means useful requested work is proven but not every criterion can be completed within the current authorized scope. `BLOCKED` means there is no safe next action without missing capability, access, decision, or recovery work.

## 7. High-Assurance external/stateful work

If the task mutates database/schema/auth state, deployed infrastructure, queues, external resources, or other persistent state, read `references/STATEFUL.md` before mutation.

Source SHA alone is not enough. Record source + environment + external-state/deployed identity. If an authorized irreversible/stateful action fails, do **not** enter the generic remediation loop immediately: enter recovery, re-baseline the actual external state, then choose rollback or explicit forward recovery before more mutation.

## DONE rule

Declare `DONE` only when:

- every required acceptance criterion is `PASS` for the current attested candidate;
- relevant regression/runtime proof passes;
- protected work is intact;
- no required stateful recovery remains.

Otherwise report `PARTIAL` or `BLOCKED` with the exact failed/unverified criteria and next safe action.

## References

- `references/RUNTIMES.md` — runtime preflight, DSH/Codex routing, workspace/artifact modes.
- `references/PLANS.md` — lean durable state, candidate identity, resume rules.
- `references/BUILDER_HANDOFF.md` — builder contract.
- `references/VERIFIER_HANDOFF.md` — candidate attestation + final proof contract.
- `references/STATEFUL.md` — external-state identity and recovery gate for High Assurance.
- `references/EXAMPLE.md` — minimal end-to-end example.
- `references/verifier.example.toml` — optional Codex Luna verifier example.
