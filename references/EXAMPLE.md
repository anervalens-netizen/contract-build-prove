# Minimal end-to-end example

Objective: fix `POST /profile` accepting an empty display name with `200` instead of `400`.

Rigor: Standard.

## 1. Preflight + investigation

```text
HARNESS=Codex
BUILDER_ROUTE=worker/Luna
VERIFIER_ROUTE=verifier/Luna
FRESH_CONTEXT_SUPPORTED=YES
WORKSPACE_MODE=SHARED_WORKSPACE
RESULT=READY
```

Baseline: HEAD `aaa111`, clean workspace, valid profile updates must remain `200`.

Existing behavior reproduces the bug: empty display name returns `200`.

## 2. Freeze contract

| ID | Required behavior | Protected behavior | Verification |
|---|---|---|---|
| AC-1 | empty display name returns `400` | valid profile update unaffected | invalid-name API test |
| AC-2 | valid unicode display name returns `200` | unicode names remain valid | existing unicode API test |

The coordinator freezes this contract **before** launching the implementation builder.

## 3. Builder

One builder changes validation and adds the regression test. It self-tests but does not mark criteria PASS.

Coordinator inspects the actual shared-workspace diff, runs relevant regression checks, and creates candidate commit:

```text
bbb222
```

## 4. Fresh verifier #1

Before tests, the verifier independently resolves the workspace source to `bbb222`.

```text
VERDICT: FAIL
CONTRACT: AC-1 -> PASS; AC-2 -> FAIL — valid unicode name returns 400
EVIDENCE: candidate bbb222 attested pre/post; invalid-name test passes; unicode test fails
FINDINGS: validation rejects valid non-ASCII display names
LARGEST_GAP: preserve valid unicode display names
```

The candidate identity still matches after verification, so this is a real functional FAIL rather than an identity problem.

## 5. Targeted remediation

Coordinator launches a builder for the demonstrated gap only. After integration and checks, the new candidate is:

```text
ccc333
```

The earlier verdict no longer applies because verified source changed.

## 6. Fresh verifier #2

A **new** verifier child independently attests `ccc333`, runs the contract checks, then attests the candidate again.

```text
VERDICT: PASS
CONTRACT: AC-1 -> PASS; AC-2 -> PASS
EVIDENCE: candidate ccc333 attested pre/post; targeted API tests pass
FINDINGS: NONE
LARGEST_GAP: NONE
```

Overall: `DONE`.

The example demonstrates the intended normal shape: **one builder, one final verifier attempt unless remediation is actually required**.
