# [Objective]

PROTOCOL=contract-build-prove
PROTOCOL_STATE=ACTIVE
Overall: ACTIVE
Rigor: STANDARD | HIGH_ASSURANCE
Control state path: [this file/path]
Plan visible to next expected coordinator session: YES | NO

## Goal / must not change

Goal: [observable user-visible result]

Must not change:
- [protected behavior/non-goal]

Authorization boundaries:
- [push/merge/deploy/prod/destructive/cost boundary]

## Runtime profile

- Harness: [Codex | DSH | other]
- Builder route/model: [actual resolved route/model]
- Verifier route/model/policy: [actual resolved route/model/policy]
- Verifier new child: YES | NO
- Verifier inherits parent conversation: NO | YES
- Workspace mode: SHARED_WORKSPACE | ISOLATED_ARTIFACT
- Preflight: READY | BLOCKED

## Baseline

- Branch / HEAD: [branch] / [SHA]
- Working tree / protected user-newer work: [concise state]
- Relevant external/runtime state: [only when applicable]

## Acceptance contract

Contract: DRAFT | FROZEN
Frozen before first candidate-affecting edit/builder launch: [timestamp or NO]

| ID | Required behavior | Protected behavior | Verification approach + expected result | Status / evidence |
|---|---|---|---|---|
| AC-1 | [behavior] | [must remain true] | `[probe/evidence]` → [expected] | UNVERIFIED |

Amendments: NONE

<!-- After freeze: AC-x — OLD / NEW / REASON / IMPACT / AUTHORIZATION -->

## Workstreams

| Workstream | Owner | Artifact mode | State | Blocker |
|---|---|---|---|---|
| W1 | [builder] | shared | READY | NONE |

## Current candidate / state target

- Source identity: UNVERIFIED
- Identity basis: [commit SHA OR cbp1 helper identity]
- Control-state exclusions: [paths]
- Builder artifacts integrated: NO
- No active shared writer: NO
- Candidate frozen: NO

Stateful target: N/A
<!-- When applicable:
SOURCE_ID=
ENVIRONMENT_ID=
DEPLOYED_ID=
EXTERNAL_STATE_ID=
RECOVERY_REQUIRED=YES|NO
-->

## Last verifier result

- Verifier child/model: UNVERIFIED
- Clean context confirmed: UNVERIFIED
- Tested artifact: UNVERIFIED
- Candidate attested pre/post on same artifact: UNVERIFIED
- Stateful target: N/A | PASS | BLOCKED
- Verdict: UNVERIFIED
- Failed/blocked criteria: NONE | [IDs]
- Largest gap: NONE | [priority gap]
- Evidence: [concise commands/probes/immutable evidence + results]

## Next action

[One concrete safe action.]
