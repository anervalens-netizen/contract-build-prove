# [Objective]

PROTOCOL=contract-build-prove
PROTOCOL_VERSION=5
Overall: ACTIVE
Rigor: STANDARD | HIGH_ASSURANCE
Control state path: [this file/path]
Plan visible to next coordinator session: YES | NO

## Goal / must not change

Goal: [observable user-visible result]

Must not change:
- [protected behavior/non-goal]

Authorization boundaries:
- [push/merge/deploy/publish/prod/destructive/paid/irreversible boundary]

## Runtime profile

- Profile: [trusted profile id | AD_HOC]
- Harness: [Codex | DSH | other]
- Builder route/model: [resolved]
- Verifier route/model/policy: [resolved]
- Verifier new child: YES | NO
- Verifier inherits parent conversation: NO | YES
- Workspace mode: SHARED_WORKSPACE | ISOLATED_ARTIFACT
- Preflight: READY | BLOCKED

## Baseline

- Branch / HEAD: [branch] / [SHA]
- Protected pre-existing user/newer work: [NONE or concise state]
- Authorized baseline dependencies from pre-existing work: [NONE or explicit paths/commits]
- Relevant external/runtime state: [only when applicable]

## Acceptance contract

Contract: DRAFT | FROZEN
Frozen before first candidate-affecting edit/builder launch: [timestamp or NO]

| ID | Required behavior | Protected behavior | Proof method + expected result | Status / evidence |
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
- Basis: [commit SHA OR cbp2 helper identity]
- Control-state exclusions: [paths]
- Protected work isolated/authorized: NO
- Builder artifacts integrated: NO
- No active shared writer: NO
- Candidate frozen: NO
- Verifier artifact strategy: [CLEAN_COMMIT_SNAPSHOT | VERIFIED_WORKSPACE | CBP2_WORKSPACE]

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
- Contract coverage: UNVERIFIED
- Tested artifact: UNVERIFIED
- Candidate attested pre/post: UNVERIFIED
- Stateful target: N/A | PASS | BLOCKED
- Verdict: UNVERIFIED
- Failed/blocked criteria: NONE | [IDs]
- Largest gap: NONE | [priority gap]
- Evidence: [concise commands/probes/immutable evidence + results]

## Next action

[One concrete safe action.]
