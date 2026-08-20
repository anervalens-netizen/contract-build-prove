# Independent verifier handoff

Use this for every final verification attempt. Each attempt gets a **new child with no inherited coordinator/builder conversation**.

The verifier is acceptance authority, not a repair agent.

`SKILL.md` is normative.

## Independence gate

This handoff is valid only when the verifier context is clean.

If the verifier can see inherited parent/coordinator implementation conversation beyond this handoff, stop with:

```text
VERDICT: BLOCKED
LARGEST_GAP: VERIFIER_CONTEXT_NOT_INDEPENDENT
```

A new child ID alone is insufficient.

## What to pass

Pass only:

- objective;
- frozen acceptance contract + authorized amendments;
- protected behavior/non-goals;
- exact expected candidate identity;
- declared control-state paths;
- exact artifact/workspace/ref to verify;
- runtime/environment verification target;
- optional `STATEFUL_TARGET`;
- allowed tools/access and side-effect limits.

Do not pass builder confidence, implementation defense, hidden criteria, or desired verdict.

## Mandatory invariant

> **THE ATTESTED ARTIFACT MUST BE THE TESTED ARTIFACT.**

If tests require an isolated writable snapshot/worktree:

1. materialize the exact candidate into that snapshot;
2. attest the snapshot itself;
3. run tests against that snapshot;
4. re-attest that same snapshot.

Never attest the parent workspace and test a different copy.

## Mandatory procedure

### Step 0 — attest the tested artifact

Before acceptance testing:

1. independently resolve/recompute identity **inside the artifact that will be tested** using `references/PLANS.md`;
2. compare with the coordinator-supplied identity;
3. confirm differences are only declared control state or allowed ignored/temp outputs;
4. on mismatch, stop with `BLOCKED: CANDIDATE_IDENTITY_MISMATCH`.

Never copy a supplied SHA/fingerprint into evidence without checking it.

### Step 1 — verify the contract

Evaluate every required criterion from direct evidence against the attested artifact.

Prefer executable/runtime evidence. Trusted immutable CI evidence tied to the exact candidate may be independently inspected instead of rerunning an expensive gate when it fully proves the criterion.

Treat missing required proof as `BLOCKED`, not PASS. Do not implement or repair the candidate.

Normal cache/build/coverage/browser/temp-database writes are allowed in the tested artifact when needed, but do not intentionally modify tracked candidate source.

### Step 2 — verify stateful target when present

If `STATEFUL_TARGET` is not `N/A`, verify the applicable tuple:

```text
SOURCE_ID=
ENVIRONMENT_ID=
DEPLOYED_ID=
EXTERNAL_STATE_ID=
RECOVERY_REQUIRED=
```

`PASS` requires both the source candidate and applicable external-state tuple to match the accepted target, with `RECOVERY_REQUIRED=NO`.

### Step 3 — postflight the same artifact

After verification, recompute/re-resolve identity in the **same artifact that was tested**.

If verified source changed, return `BLOCKED: CANDIDATE_IDENTITY_MISMATCH` even if tests passed.

## Generic prompt

```text
Act as the independent acceptance verifier for this frozen Contract-Build-Prove candidate.

This must be a clean verifier context. You did not implement the candidate. Do not repair it and do not trust builder claims.

OBJECTIVE:
[objective]

PROTECTED BEHAVIOR / NON-GOALS:
[relevant facts]

FROZEN ACCEPTANCE CONTRACT + AMENDMENTS:
[criteria]

EXPECTED CANDIDATE IDENTITY:
[commit SHA OR cbp1 identity]

TESTED ARTIFACT / WORKSPACE:
[exact repo/worktree/snapshot/ref]

CONTROL-STATE PATHS:
[paths or NONE]

STATEFUL_TARGET:
[N/A OR SOURCE_ID / ENVIRONMENT_ID / DEPLOYED_ID / EXTERNAL_STATE_ID / RECOVERY_REQUIRED]

VERIFICATION TARGET / ACCESS:
[commands/services/CI/runtime/sandbox limits]

First attest the artifact you will actually test. Verify every criterion against that same artifact. If STATEFUL_TARGET exists, verify it too. Finally re-attest the same tested artifact.

Return exactly:
VERDICT: PASS | FAIL | BLOCKED
CONTRACT: criterion -> PASS | FAIL | BLOCKED, with concise reason
ARTIFACT: tested artifact + independently attested identity pre/post
STATEFUL: N/A | PASS | BLOCKED, with concise reason
EVIDENCE: exact commands/probes/immutable evidence + results
FINDINGS: concrete defects/regressions, highest severity first, or NONE
LARGEST_GAP: highest-priority remediation/unblock target, or NONE
```

## Verdict semantics

- `PASS`: every required criterion is proven for the same attested/tested artifact; applicable stateful target also passes.
- `FAIL`: identity is valid, but evidence contradicts one or more criteria.
- `BLOCKED`: truth cannot safely be established because independence, identity, access, environment, dependency, state, or required proof is unavailable.

`LARGEST_GAP` sets priority only. It does **not** mean the next remediation pass should intentionally ignore other understood findings.
