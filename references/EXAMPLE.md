# Minimal end-to-end example

Objective: fix `POST /profile` accepting an empty display name with `200` instead of `400`.

Rigor: Standard.

## 1. Preflight + investigation

```text
HARNESS=Codex
BUILDER_ROUTE=worker/Luna
VERIFIER_ROUTE=verifier/Luna
VERIFIER_NEW_CHILD=YES
VERIFIER_INHERITS_PARENT_CONTEXT=NO
WORKSPACE_MODE=SHARED_WORKSPACE
PLAN_VISIBLE_NEXT_SESSION=YES
RESULT=READY
```

Baseline: HEAD `aaa111`, clean workspace, valid profile updates must remain `200`.

Existing behavior reproduces the bug: empty display name returns `200`.

## 2. Freeze contract

| ID | Required behavior | Protected behavior | Verification |
|---|---|---|---|
| AC-1 | empty display name returns `400` | valid profile update unaffected | invalid-name API test |
| AC-2 | valid unicode display name returns `200` | unicode names remain valid | unicode API test |

Coordinator freezes required/protected behavior before launching the implementation builder.

## 3. Builder work packet

One builder changes validation and adds the regression test. It runs focused tests but does not mark criteria PASS.

Coordinator inspects the real shared-workspace diff. No other write-capable child remains active.

Because local commits are permitted, coordinator creates candidate:

```text
bbb222
```

Coordinator does not rerun the builder's entire suite; there is no separate integration risk in this one-builder example.

## 4. Clean-context verifier #1

A new verifier starts with no inherited coordinator/builder conversation.

It attests the exact artifact `bbb222`, tests that same artifact, then re-attests it.

```text
VERDICT: FAIL
CONTRACT: AC-1 -> PASS; AC-2 -> FAIL — valid unicode name returns 400
ARTIFACT: bbb222 — attested before/after; same artifact tested
STATEFUL: N/A
EVIDENCE: invalid-name test passes; unicode test fails
FINDINGS: validation rejects valid non-ASCII display names
LARGEST_GAP: preserve valid unicode display names
```

## 5. Remediation

Coordinator launches a bounded remediation builder.

If the verifier had reported several concrete understood findings that safely belonged to the same scope, they would be repaired in this same pass. `LARGEST_GAP` sets priority; it is not a command to repair only one defect.

Builder fixes the validation and runs focused checks. Coordinator integrates and creates new candidate:

```text
ccc333
```

## 6. Clean-context verifier #2

A different new verifier child attests/tests/re-attests `ccc333`.

```text
VERDICT: PASS
CONTRACT: AC-1 -> PASS; AC-2 -> PASS
ARTIFACT: ccc333 — attested before/after; same artifact tested
STATEFUL: N/A
EVIDENCE: invalid-name and unicode acceptance tests pass
FINDINGS: NONE
LARGEST_GAP: NONE
```

Coordinator performs one cheap final identity check: current source is still `ccc333`, and no shared writer is active.

Overall: `DONE`.

The normal shape remains small:

**preflight → contract → one bounded builder → exact candidate → one clean verifier**

Additional builders/verifiers appear only when actual scope, remediation, or named risk requires them.
