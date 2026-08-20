# Minimal end-to-end example

Objective: fix `POST /profile` accepting an empty display name with `200` instead of `400`.

Rigor: Standard.

## 1. Preflight

```text
RUNTIME_PROFILE=codex-default
HARNESS=Codex
BUILDER_ROUTE=worker/Luna
VERIFIER_ROUTE=verifier/Luna
VERIFIER_NEW_CHILD=YES
VERIFIER_INHERITS_PARENT_CONTEXT=NO
WORKSPACE_MODE=SHARED_WORKSPACE
RESULT=READY
```

Baseline: HEAD `aaa111`, clean workspace; valid profile updates must remain `200`.

Existing behavior reproduces the bug.

## 2. Freeze contract

| ID | Required behavior | Protected behavior | Proof |
|---|---|---|---|
| AC-1 | empty display name returns `400` | valid profile update unaffected | invalid-name API probe |
| AC-2 | valid unicode display name returns `200` | unicode names remain valid | unicode API probe |

Coordinator freezes the behavior before launching the builder.

## 3. Builder

One end-to-end builder changes validation and adds a regression test. It runs focused checks but does not mark criteria PASS.

Coordinator inspects the real diff, confirms no protected work was absorbed, and creates candidate commit:

```text
bbb222
```

No shared writer remains active.

## 4. Clean verifier #1

A new verifier starts with no inherited implementation conversation.

First it checks that the contract covers the objective. Then it materializes a **clean isolated worktree at `bbb222`**, attests that worktree, tests it, and re-attests the same worktree.

```text
VERDICT: FAIL
CONTRACT_COVERAGE: PASS
CONTRACT: AC-1 -> PASS; AC-2 -> FAIL — valid unicode name returns 400
ARTIFACT: clean worktree @ bbb222 — attested before/after
STATEFUL: N/A
EVIDENCE: invalid-name probe passes; unicode probe fails
FINDINGS: validation rejects valid non-ASCII display names
LARGEST_GAP: preserve valid unicode display names
```

The verifier also confirms the candidate-authored regression test really exercises the frozen behavior before counting it as evidence.

## 5. Remediation

Coordinator launches one coherent remediation builder. All understood findings that fit that scope are fixed in the same pass.

New candidate:

```text
ccc333
```

## 6. Clean verifier #2

A different clean-context verifier materializes a clean worktree at `ccc333`, checks contract coverage, attests/tests/re-attests it, and returns:

```text
VERDICT: PASS
CONTRACT_COVERAGE: PASS
CONTRACT: AC-1 -> PASS; AC-2 -> PASS
ARTIFACT: clean worktree @ ccc333 — attested before/after
STATEFUL: N/A
EVIDENCE: invalid-name and unicode probes pass
FINDINGS: NONE
LARGEST_GAP: NONE
```

Coordinator performs one cheap final identity check and confirms no shared writer is active.

Overall: `DONE`.

Normal shape:

**preflight → contract → one coherent builder → commit → clean verifier**

Additional agents appear only when actual scope or risk requires them.
