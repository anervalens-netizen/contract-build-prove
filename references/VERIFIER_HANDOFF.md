# Independent verifier handoff

Use this for every final verification attempt. Each attempt gets a **new child with no inherited coordinator/builder conversation**.

The verifier is acceptance authority, not a repair agent. `SKILL.md` is normative.

## Independence gate

If the verifier can see inherited implementation/coordinator conversation beyond this handoff:

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
- runtime/environment target;
- optional `STATEFUL_TARGET`;
- allowed tools/access + side-effect limits.

Do not pass builder confidence, implementation defense, hidden criteria, or desired verdict.

## Mandatory procedure

### Step 0 — contract coverage

Compare the frozen contract with the supplied objective and protected behavior.

If an **objective-essential requirement is clearly absent**, stop:

```text
VERDICT: BLOCKED
LARGEST_GAP: CONTRACT_COVERAGE_GAP
```

Do not invent new requirements or broaden scope. This gate only prevents certification of an obviously incomplete contract.

### Step 1 — materialize and attest the artifact

> **THE ATTESTED ARTIFACT MUST BE THE TESTED ARTIFACT.**

For a commit candidate, default to a clean isolated worktree/snapshot materialized from the exact SHA.

If testing another workspace, first prove it has no candidate-affecting tracked/untracked differences from that SHA except declared control metadata.

For uncommitted candidates, use `scripts/candidate_id.py verify` from `references/PLANS.md`.

Before tests, independently attest identity **inside the artifact that will be tested**. Mismatch:

```text
VERDICT: BLOCKED
LARGEST_GAP: CANDIDATE_IDENTITY_MISMATCH
```

Never copy the supplied identity into evidence without checking it.

### Step 2 — verify behavior

Evaluate every criterion from direct evidence against the attested artifact.

Candidate-authored tests are evidence only after confirming they actually exercise and assert the frozen behavior. For important criteria, use an independent probe when needed and feasible.

Immutable CI/runtime evidence tied to the exact candidate may replace an expensive rerun when it fully proves the criterion.

Missing required proof is `BLOCKED`, not PASS. Do not implement or repair the candidate.

Normal cache/build/coverage/browser/temp-database writes are allowed in the tested artifact when needed; do not intentionally modify candidate source.

### Step 3 — verify stateful target when present

If `STATEFUL_TARGET != N/A`, verify:

```text
SOURCE_ID=
ENVIRONMENT_ID=
DEPLOYED_ID=
EXTERNAL_STATE_ID=
RECOVERY_REQUIRED=
```

PASS requires the applicable tuple to match and `RECOVERY_REQUIRED=NO`.

### Step 4 — postflight the same artifact

Re-attest the **same artifact that was tested**. Source identity change → `BLOCKED: CANDIDATE_IDENTITY_MISMATCH`, even if tests passed.

## Verdict precedence

Use this order so mixed results are deterministic:

1. independence, candidate-identity, contract-coverage, or unsafe-state blocker → `BLOCKED`;
2. otherwise any criterion `FAIL` → `FAIL`;
3. otherwise any criterion/state target `BLOCKED` → `BLOCKED`;
4. otherwise all required criteria/state targets `PASS` → `PASS`.

## Generic prompt

```text
Act as the independent acceptance verifier for this Contract-Build-Prove candidate.

This is a clean verifier context. You did not implement the candidate. Do not repair it or trust builder claims.

OBJECTIVE:
[objective]

PROTECTED BEHAVIOR / NON-GOALS:
[relevant facts]

FROZEN CONTRACT + AMENDMENTS:
[criteria]

EXPECTED CANDIDATE:
[commit SHA OR cbp2 identity]

TESTED ARTIFACT:
[exact clean worktree/snapshot/workspace/ref]

CONTROL STATE:
[paths or NONE]

STATEFUL_TARGET:
[N/A OR SOURCE_ID / ENVIRONMENT_ID / DEPLOYED_ID / EXTERNAL_STATE_ID / RECOVERY_REQUIRED]

ACCESS:
[commands/services/CI/runtime/sandbox limits]

First check contract coverage. Then attest the exact artifact you will test, verify the contract/state target, and re-attest that same artifact.

Return exactly:
VERDICT: PASS | FAIL | BLOCKED
CONTRACT_COVERAGE: PASS | BLOCKED, with concise reason
CONTRACT: criterion -> PASS | FAIL | BLOCKED, with concise reason
ARTIFACT: tested artifact + independently attested identity pre/post
STATEFUL: N/A | PASS | BLOCKED, with concise reason
EVIDENCE: exact commands/probes/immutable evidence + results
FINDINGS: concrete defects/regressions, highest severity first, or NONE
LARGEST_GAP: highest-priority remediation/unblock target, or NONE
```

`LARGEST_GAP` sets priority only; it does not limit the next coherent remediation pass to one finding.
