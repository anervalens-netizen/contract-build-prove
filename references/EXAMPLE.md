# Minimal end-to-end example

This example demonstrates the process shape, not a repository-specific implementation.

## Objective

Fix an API bug where `POST /profile` accepts an invalid empty display name and returns `200` instead of `400`.

Rigor: Standard CBP.

## Baseline

- HEAD: `aaa111`
- working tree: clean
- existing unrelated behavior to protect: valid profile updates still return `200`

## Frozen contract

| ID | Behavior | Verification | Status |
|---|---|---|---|
| AC-1 | empty display name returns `400` | API test with `""` | UNVERIFIED |
| AC-2 | valid display name still returns `200` | existing happy-path API test | UNVERIFIED |

Pre-fix reproduction confirms AC-1 currently fails: request returns `200`.

Contract freezes before implementation.

## Build

Worker changes validation in the profile request path and adds a regression test. Local targeted tests pass.

Candidate commit: `bbb222`.

## Independent audit #1

Fresh auditor receives only objective, frozen contract, baseline, candidate `bbb222`, and verification targets.

```text
VERDICT: FAIL
CONTRACT: AC-1 -> PASS; AC-2 -> FAIL
EVIDENCE: invalid-name test returns 400; existing valid unicode-name test now returns 400 on bbb222
FINDINGS: validation rejects valid non-ASCII display names
UNVERIFIED: NONE
LARGEST_GAP: preserve valid unicode display names
```

No criteria are silently rewritten. Task returns to building.

## Remediation

Worker fixes the over-broad validation and reruns affected tests.

New candidate commit: `ccc333`.

The previous audit is now invalid because source changed.

## Independent audit #2

```text
VERDICT: PASS
CONTRACT: AC-1 -> PASS; AC-2 -> PASS
EVIDENCE: targeted API tests pass on ccc333; valid unicode regression passes
FINDINGS: NONE
UNVERIFIED: NONE
LARGEST_GAP: NONE
```

## Close

Relevant regression gate passes on unchanged candidate `ccc333`.

Overall outcome: `DONE`.

Key properties demonstrated:

- red → green bug reproduction;
- frozen criteria;
- builder and auditor separated;
- audit tied to exact candidate;
- source change invalidates earlier audit;
- a failed audit repairs the demonstrated gap instead of redefining success.
