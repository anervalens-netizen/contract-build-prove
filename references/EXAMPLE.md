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

## Builder subagent

The coordinator launches a scoped builder subagent. It changes validation in the profile request path, adds a regression test, runs targeted checks, and returns its handoff.

The coordinator inspects/integrates the result and freezes candidate commit `bbb222`.

## Independent verification #1

A fresh verifier receives only the objective, frozen contract, relevant baseline, candidate `bbb222`, and verification targets.

```text
VERDICT: FAIL
CONTRACT: AC-1 -> PASS; AC-2 -> FAIL
EVIDENCE: invalid-name test returns 400; existing valid unicode-name test now returns 400 on bbb222
FINDINGS: validation rejects valid non-ASCII display names
UNVERIFIED: NONE
LARGEST_GAP: preserve valid unicode display names
```

No criteria are silently rewritten. The affected task returns to building.

## Remediation

The coordinator launches a builder to fix the demonstrated over-broad validation and rerun affected local checks.

After integration, the new candidate commit is `ccc333`.

The previous verification is invalid because verified source changed.

## Independent verification #2

A fresh verifier checks `ccc333`.

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
- coordinator delegates implementation;
- builder and verifier are separate contexts;
- verification is tied to an exact candidate;
- source changes invalidate earlier verification;
- a failed verification repairs the demonstrated gap instead of redefining success.
