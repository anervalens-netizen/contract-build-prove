# Lean ExecPlan reference

The ExecPlan exists only so another coordinator session can resume without reconstructing the conversation. It is **control state**, not the software candidate.

`SKILL.md` is normative.

If the repository already has one canonical planning system for the same objective, reuse it. Otherwise use `assets/EXEC_PLAN_TEMPLATE.md`, normally as `.cbp/PLAN.md` or another repository-approved control-state path.

The plan location must be guaranteed visible to the **next coordinator session expected for this workstream**. Do not call an ephemeral filesystem path durable.

## Minimal state

Keep only:

- protocol + overall status;
- goal / protected behavior;
- active runtime profile;
- frozen acceptance contract;
- current workstreams;
- current candidate/state target;
- last verifier result;
- next safe action.

State vocabularies:

| Layer | States |
|---|---|
| Workstream | `READY`, `BUILDING`, `BUILT`, `BLOCKED` |
| Acceptance criterion | `UNVERIFIED`, `PASS`, `FAIL`, `BLOCKED` |
| Overall | `ACTIVE`, `DONE`, `PARTIAL`, `BLOCKED` |

The verifier reports `PASS | FAIL | BLOCKED`; that is a result, not another lifecycle state machine.

## Update cadence

Update the plan only:

- after runtime preflight;
- **at contract freeze**;
- after an authorized contract amendment;
- after a meaningful failure/discovery that changes the next action;
- at candidate freeze;
- after final verification;
- before interruption/handoff.

Do not maintain a chronological diary. Do not paste large logs.

## Control state versus candidate source

Declare control-state paths explicitly.

Control-state changes do **not** change candidate identity. Source, tests, configuration, migrations, generated source, permissions/modes, or other behavior-affecting repository changes do.

Prefer not to commit control-state updates after candidate freeze. If plan files are tracked, final reporting must still name the exact verified source candidate rather than implying a later metadata-only commit was verified.

## Contract lifecycle

1. Investigation may occur while behavior is draft.
2. Freeze required behavior, protected behavior, and evidence strength before the first candidate-affecting tracked edit or implementation-builder launch.
3. After freeze, weakening any frozen requirement uses `OLD / NEW / REASON / IMPACT / AUTHORIZATION`.
4. The verification technique may be refined without amendment only when equivalent or stronger and the frozen requirement is unchanged.

## Candidate identity

### Normal path: exact local commit

Use an exact local commit SHA whenever local commits are permitted.

The verifier must attest the **artifact it tests**. For a commit-backed writable worktree/snapshot, resolve that snapshot to the expected commit before testing and confirm it still represents the same candidate afterward.

### Fallback: uncommitted candidate

Do **not** implement hashing rules manually.

Use the bundled helper from the skill directory:

```text
python3 <skill-root>/scripts/candidate_id.py create --exclude .cbp/PLAN.md
```

It returns a deterministic `cbp1:<sha256>` identity plus diagnostic components. It covers:

- exact base HEAD;
- binary tracked diff, including tracked mode changes;
- every non-ignored untracked path;
- Git-relevant regular-file executable mode;
- symlink identity/target content;
- declared control-state exclusions.

Add `--exclude` once per control-state path.

Verifier check:

```text
python3 <skill-root>/scripts/candidate_id.py verify <expected-cbp1-id> --exclude .cbp/PLAN.md
```

Exit `0` means match; exit `2` means identity mismatch.

If neither a commit candidate nor the bundled helper can be used reliably, exact uncommitted verification is unavailable; do not invent an ad-hoc fingerprint.

## Artifact identity rule

**The attested artifact must be the tested artifact.**

If verification uses an isolated writable copy, materialize the candidate into that copy and attest the copy itself before tests. Re-attest the same copy afterward. The parent workspace is not a proxy for a different tested snapshot.

## Workspace mode

Record one:

- `SHARED_WORKSPACE` — builder edits the coordinator-visible workspace.
- `ISOLATED_ARTIFACT` — builder works elsewhere and returns an exact integratable artifact.

In shared workspace, one write-capable child at a time. At candidate freeze, no write-capable shared child may remain active.

## Test ownership

- Builder: focused development checks.
- Coordinator: only integration-specific checks when integration creates a real risk; avoid ritual reruns.
- Verifier: acceptance/regression authority.

Trusted immutable CI evidence tied to the exact attested candidate may be independently inspected instead of rerunning an expensive gate when it fully proves the required criterion.

## Evidence

Keep evidence next to the criterion or in the last-verifier block. Enough means:

- exact command/probe or immutable CI/runtime evidence;
- concise result;
- candidate/state identity;
- environment when relevant.

No separate evidence index.

## Progress control

Progress means at least one of these materially improves:

- failed acceptance surface;
- failure severity;
- causal uncertainty/fault-domain size;
- discriminating evidence.

For investigation: two consecutive cycles with no information gain require a fresh synthesis/replan before another hypothesis.

For remediation: if the same failed surface/blocker survives two consecutive cycles without material improvement or new discriminating evidence, perform one fresh root-cause synthesis/replan. One further non-improving cycle ends `PARTIAL` or `BLOCKED`.

Do not trigger replanning merely because several verifier attempts failed while the system is clearly converging.

## Resume

The plan must contain:

```text
PROTOCOL=contract-build-prove
PROTOCOL_STATE=ACTIVE
```

On session resume/context reconstruction, **reload the active CBP skill before acting**, then re-read this plan and check current repository/runtime state against it.

A fresh coordinator should be able to answer:

1. What result is required and what must not change?
2. Which builder/verifier routes, verifier context mode, and workspace mode are active?
3. What is built or blocked?
4. What exact source/state candidate is current?
5. Which criteria are not `PASS`?
6. What was the last verifier result?
7. What is the next safe action?

If the plan answers those, it is detailed enough.
