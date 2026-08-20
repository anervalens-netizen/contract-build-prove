# [Objective]

Overall: ACTIVE
Rigor: STANDARD | HIGH_ASSURANCE
Control state path: [this file/path]

## Goal and boundaries

Goal: [observable user-visible result]

Must not change:
- [protected behavior/non-goal]

Authorization boundaries:
- [push/merge/deploy/prod/destructive/cost boundary]

## Runtime preflight

- Harness: [Codex | DSH | other]
- Builder route/model: [actual resolved route/model]
- Verifier route/model: [actual resolved route/model]
- Fresh verifier context: YES | NO
- Workspace mode: SHARED_WORKSPACE | ISOLATED_ARTIFACT
- Preflight: READY | BLOCKED

## Baseline

- Branch / HEAD: [branch] / [SHA]
- Working tree / protected user-newer work: [concise state]
- Relevant external/runtime state: [only when applicable]

## Acceptance contract

Contract: DRAFT | FROZEN
Frozen before first tracked edit/builder launch: [timestamp or NO]

| ID | Required behavior | Protected behavior | Verification + expected result | Status / evidence |
|---|---|---|---|---|
| AC-1 | [behavior] | [must remain true] | `[probe]` → [expected] | UNVERIFIED |

Amendments: NONE

<!-- After freeze: AC-x — OLD / NEW / REASON / IMPACT / AUTHORIZATION -->

## Workstreams

| Workstream | Owner | Artifact mode | State | Blocker |
|---|---|---|---|---|
| W1 | [builder] | shared | READY | NONE |

## Candidate

- Identity: UNVERIFIED
- Basis: [commit SHA OR BASE_HEAD + patch/untracked fingerprints]
- Control-state exclusions: [paths]
- Builder artifacts integrated: NO
- Candidate frozen: NO

## Last verifier result

- Verifier child/model: UNVERIFIED
- Candidate attested pre/post: UNVERIFIED
- Verdict: UNVERIFIED
- Failed/blocked criteria: NONE | [IDs]
- Largest gap: NONE | [gap]
- Evidence: [concise commands/probes + results]

## External-state recovery — only if applicable

- State identity: N/A
- Recovery required: NO
- Rollback/forward-recovery decision: N/A

## Next action

[One concrete safe action.]
