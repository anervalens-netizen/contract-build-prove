# Lean ExecPlan reference

The ExecPlan exists only so another coordinator can resume safely. It is **control state**, not software candidate. `SKILL.md` is normative.

Reuse an equivalent repository-native plan when one already exists. Otherwise use `assets/EXEC_PLAN_TEMPLATE.md`, normally `.cbp/PLAN.md` or another path guaranteed visible to the next expected coordinator session.

## Minimal durable state

Keep only:
- protocol version + overall status;
- goal / protected behavior;
- runtime profile;
- frozen acceptance contract;
- workstreams;
- current candidate/state target;
- last verifier result;
- next safe action.

States:

| Layer | States |
|---|---|
| Workstream | `READY`, `BUILDING`, `BUILT`, `BLOCKED` |
| Criterion | `UNVERIFIED`, `PASS`, `FAIL`, `BLOCKED` |
| Overall | `ACTIVE`, `DONE`, `PARTIAL`, `BLOCKED` |

Update only after preflight, at contract freeze, after authorized amendment, after a material failure/discovery, at candidate freeze, after final verification, and before interruption/handoff. No progress diary.

## Contract

Freeze required/protected behavior before the first candidate-affecting edit or builder launch.

Do not weaken what must be proven. A proof method may change without amendment only when it remains at least as convincing and the frozen requirement is unchanged.

Scope weakening uses `OLD / NEW / REASON / IMPACT / AUTHORIZATION`.

## Candidate identity

### Default: commit candidate

Use an exact local commit SHA whenever permitted.

**Default final-verifier path:** materialize a clean isolated worktree/snapshot from that exact SHA, attest it, test it, then re-attest it.

Testing a non-clean/current workspace instead is allowed only after proving candidate-affecting tracked/untracked state matches the SHA except declared control metadata.

If unrelated protected user/newer changes exist, they must not become an implicit dependency. Either isolate CBP-owned candidate work, explicitly record the pre-existing change as an authorized baseline dependency, or block. Never exclude protected source merely to make identity match.

### Fallback: uncommitted candidate

Use the bundled helper only:

```text
python3 <skill-root>/scripts/candidate_id.py create --exclude .cbp/PLAN.md
python3 <skill-root>/scripts/candidate_id.py verify <expected-cbp2-id> --exclude .cbp/PLAN.md
```

Add `--exclude` once per literal control-state path.

Exit codes:
- `0` = create success / verify match;
- `2` = identity mismatch;
- `3` = `UNSUPPORTED_WORKTREE_STATE`.

The helper intentionally fails closed on Git states it cannot identify exactly, including unresolved conflicts, hidden index states, problematic file-mode configuration, dirty/unavailable submodules, and unsupported untracked types. When exit `3` occurs, use a commit/isolated artifact or report `BLOCKED`; do not invent another fingerprint.

**The attested artifact must be the tested artifact.**

## Control state vs source

Control-state changes do not change candidate identity. Source, tests, config, migrations, generated source, permissions/modes, and other behavior-affecting changes do.

Prefer not to commit control-state updates after candidate freeze. Final reporting always names the exact verified source/state candidate.

## Workspace + drift

Record `SHARED_WORKSPACE` or `ISOLATED_ARTIFACT`.

In shared workspace:
- one writer total;
- coordinator compares actual state around each writer packet;
- unexpected overlapping user/process drift must be reconciled before continuing;
- no writer remains active at candidate freeze.

Prefer isolated artifacts when concurrent human/process edits are likely.

## Test ownership

- Builder: focused development checks.
- Coordinator: integration-specific checks only when integration creates real risk.
- Verifier: acceptance/regression authority.

Immutable CI/runtime evidence tied to the exact candidate may replace an expensive rerun when it fully proves the criterion.

## Progress control

Progress means failed surface/severity or causal uncertainty materially shrinks, or new discriminating evidence appears.

Two consecutive investigation/remediation cycles with no such progress → one fresh synthesis/replan. One further non-improving cycle → `PARTIAL` or `BLOCKED`.

## Resume + protocol version

The plan must contain:

```text
PROTOCOL=contract-build-prove
PROTOCOL_VERSION=5
```

On resume/context reconstruction, reload the active CBP skill before acting.

If plan `PROTOCOL_VERSION` differs from the current skill version, revalidate runtime profile, frozen contract, candidate/state identity, and next action once before continuing; record the migration. Do not silently apply changed semantics to old state.

A fresh coordinator only needs to answer:
1. What is required / protected?
2. Which runtime profile and artifact mode are active?
3. What is built or blocked?
4. What exact candidate/state target is current?
5. Which criteria are not `PASS`?
6. What was the last verifier result?
7. What is the next safe action?
