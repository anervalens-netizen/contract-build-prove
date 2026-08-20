# [TASK-ID] — [Objective]

Status: ACTIVE
Rigor: STANDARD | HIGH_ASSURANCE
Overall outcome: UNVERIFIED
Created: [ISO-8601]
Updated: [ISO-8601]

## Objective

[User-visible result.]

## Non-goals and boundaries

- [Behavior/component that must not change.]
- [Authorization, destructive-action, production-data, cost, security, or deployment boundary.]

## Baseline

- Repository: [path/name]
- Branch / HEAD: [branch] / [SHA]
- Working tree: [clean or exact pre-existing changes]
- Protected user/newer work: [paths/commits or none]
- Relevant runtime/deployed state: [SHA/digest/schema/services/health or N/A/UNVERIFIED]

## Minimal code map

- `[path or symbol]` — [responsibility and relevance]

## Acceptance contract

Contract state: DRAFT | FROZEN
Frozen at: [ISO-8601 or UNVERIFIED]

| ID | Observable behavior | Protected behavior | Verification + expected result | Runtime proof | Evidence | Status |
|---|---|---|---|---|---|---|
| AC-1 | [behavior] | [must not regress] | `[command/probe]` → [expected] | [probe or N/A] | pending | UNVERIFIED |

## Contract amendments

- None.

<!-- After freeze, each amendment must use:
- [ISO-8601] AC-x
  - OLD: ...
  - NEW: ...
  - REASON: ...
  - IMPACT: ...
  - AUTHORIZATION: [user / clarification / not scope-reducing]
-->

## Tasks

| Task | Scope | Depends on | Owner | Attempts | State |
|---|---|---|---|---:|---|
| T1 | [atomic deliverable] | none | [builder] | 0 | READY |

## Progress

- [ISO-8601] Baseline recorded. Next: [one concrete action].

## Failures and discoveries

- [Observation → implication.]

## Decisions

- [Decision → why → evidence/constraint.]

## Candidate

- Candidate identity: UNVERIFIED
- Candidate basis: [commit SHA OR HEAD + workspace fingerprint]
- Frozen for verification: NO
- Drift check: UNVERIFIED
- Integrated diff review: UNVERIFIED
- Relevant regression gates: UNVERIFIED

## Independent verification

- Verifier: UNVERIFIED
- Model/provider: UNVERIFIED
- Verdict: UNVERIFIED
- Candidate verified: UNVERIFIED
- Criteria: UNVERIFIED
- Largest gap: UNVERIFIED

## Evidence index

- AC-1: [command/probe + result + candidate identity + environment/timestamp/URL when useful]

## Deployment/runtime

- Authorized: YES | NO | N/A
- Published SHA/digest: N/A | UNVERIFIED
- Health/logs/user flow: N/A | UNVERIFIED

## Risks and remaining work

- [Known risk or unverified assumption.]

## Next exact step

[One concrete command/action and expected observation.]

## Resume procedure

1. Read repository instructions and this plan.
2. Recheck branch, HEAD, working tree, protected work, and relevant runtime state.
3. Compare current state with `Candidate` and latest progress; record drift before editing.
4. Preserve newer/user work.
5. Continue from `Next exact step`; do not repeat a recorded failed approach unchanged.
