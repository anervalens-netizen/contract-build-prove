# Lean ExecPlan reference

The ExecPlan exists only so another session can resume without reconstructing the conversation. It is **control state**, not the software candidate.

If the repository already has one canonical planning system for the same objective, reuse it. Otherwise use `assets/EXEC_PLAN_TEMPLATE.md`, normally as a local `.cbp/PLAN.md` or another repository-approved control-state path.

## Keep only three persistent state vocabularies

| Layer | States |
|---|---|
| Workstream | `READY`, `BUILDING`, `BUILT`, `BLOCKED` |
| Acceptance criterion | `UNVERIFIED`, `PASS`, `FAIL`, `BLOCKED` |
| Overall | `ACTIVE`, `DONE`, `PARTIAL`, `BLOCKED` |

The verifier report has a verdict (`PASS | FAIL | BLOCKED`) but does not create a fourth lifecycle state machine.

## Update cadence

Update the plan only:

- after baseline/runtime preflight;
- when the frozen contract changes through an authorized amendment;
- after a meaningful failure/discovery that changes the next action;
- at candidate freeze;
- after final verification;
- before interruption/handoff.

Do not maintain a chronological progress diary. Do not paste large logs.

## Control state versus candidate source

Declare the plan/control-state path explicitly.

Control-state changes do **not** change candidate identity. Source, tests, configuration, migrations, generated source, or other behavior-affecting repository changes do.

Prefer not to commit control-state changes after candidate freeze. If the repository tracks plan files, the final report must still name the exact verified source candidate rather than implying that a later metadata-only commit was verified.

## Contract lifecycle

1. Read-only investigation may happen while the contract is draft.
2. Freeze immediately before the first tracked repository edit or implementation-builder launch.
3. After freeze, amendments use `OLD / NEW / REASON / IMPACT`.
4. Explicit user authorization is required to weaken observable behavior, protected behavior, or required evidence strength.

## Candidate identity

### Preferred: committed candidate

Use an exact local commit SHA whenever repository policy permits it.

The verifier must independently resolve the expected SHA and confirm that the tested source corresponds to it. Declared control-state files and allowed ignored/temp artifacts may differ; verified source may not.

### Fallback: uncommitted candidate

Record this tuple:

```text
BASE_HEAD=<sha>
TRACKED_PATCH_SHA256=<sha256>
UNTRACKED_MANIFEST_SHA256=<sha256>
CONTROL_STATE_PATHS=<explicit paths>
```

Canonical construction:

1. `BASE_HEAD` is the exact current HEAD.
2. `TRACKED_PATCH_SHA256` is SHA-256 of the raw bytes of `git diff --binary --no-ext-diff --no-textconv HEAD -- .`, excluding only declared control-state paths.
3. Enumerate every non-ignored untracked file from `git ls-files --others --exclude-standard`, excluding only declared control-state paths.
4. Sort those relative paths bytewise. For each file, record `path`, NUL, and SHA-256 of the file bytes. SHA-256 that canonical manifest to produce `UNTRACKED_MANIFEST_SHA256`.
5. Ignored build/cache/temp outputs are not candidate source unless the repository explicitly treats them as deliverables.

The verifier recomputes the same tuple before and after testing. Any mismatch in verified source is `BLOCKED: CANDIDATE_IDENTITY_MISMATCH`.

## Workspace/artifact mode

Record one:

- `SHARED_WORKSPACE` — builder edits the coordinator-visible workspace.
- `ISOLATED_ARTIFACT` — builder works elsewhere and must return an exact commit/patch/artifact for integration.

Never freeze a candidate until every isolated artifact is explicitly integrated and the coordinator has inspected the resulting diff.

## Drift

Do not perform ritual drift checks after every action. Recheck when it matters:

- on resume;
- before integrating a returned isolated artifact;
- at candidate freeze;
- when unexpected repository changes appear.

If drift overlaps verified source or protected user work, stop and reconcile before verification.

## Evidence

Keep evidence next to the acceptance criterion or in the last-verification block. Enough means:

- exact command/probe;
- result/exit summary;
- candidate identity;
- runtime/environment when relevant.

No separate evidence index is required.

## Failure control

Do not call normal hypothesis exploration "stagnation" merely because hypotheses fail.

Escalate when there is no global improvement:

- after 3 final-verifier failures, or
- after 2 full cycles without reducing failed criteria/severity.

Perform one fresh root-cause replan. One further non-improving cycle ends in `PARTIAL` or `BLOCKED`.

## Resume test

A fresh coordinator should be able to answer only these questions:

1. What observable result is required?
2. What must not change?
3. What runtime/subagent routes and workspace mode are active?
4. What is built or blocked?
5. What exact candidate is current?
6. Which criteria are not `PASS`?
7. What was the last verifier result?
8. What is the next safe action?

If the plan answers those, it is detailed enough.
