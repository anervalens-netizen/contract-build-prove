# Stateful / irreversible work

Read this only when the task changes persistent external state: database/schema/data, auth/identity state, deployed infrastructure, queues, external services/resources, or another target that cannot be described by source code alone.

`SKILL.md` is normative.

The purpose is to prevent a failed mutation from falling blindly into the normal remediation loop.

## Stateful target

Record only the fields that apply:

```text
SOURCE_ID=<verified source SHA/cbp1 identity>
ENVIRONMENT_ID=<staging/prod/cluster/account/database/etc.>
DEPLOYED_ID=<artifact/image/release digest or N/A>
EXTERNAL_STATE_ID=<schema version/state marker/resource version or N/A>
RECOVERY_REQUIRED=<YES|NO>
```

Put the same target in the ExecPlan and verifier handoff. Source identity alone is insufficient after an external mutation.

## Before mutation

Require:

- explicit authorization for production/destructive/irreversible action;
- current external-state baseline;
- preconditions/backup where relevant;
- rollback or forward-recovery strategy when failure could leave partial state;
- staging/dry-run proof when realistically available for destructive High-Assurance work.

## After mutation

Re-read actual external state. Never assume the intended transition completed.

Update `DEPLOYED_ID` / `EXTERNAL_STATE_ID` from observed state before final verification.

## Recovery precedence

If an authorized stateful/irreversible operation fails or leaves ambiguous partial state:

```text
RECOVERY_REQUIRED=YES
```

This **overrides the normal `FAIL → builder remediation` path**.

Do not launch ordinary remediation against an assumed starting state. Instead:

1. stop further irreversible mutation;
2. inspect and re-baseline actual external state;
3. determine whether safe rollback is possible;
4. otherwise define an explicit forward-recovery plan from the **current** state;
5. obtain any authorization required for the recovery action;
6. perform the authorized recovery transition;
7. observe the resulting state again;
8. only then clear `RECOVERY_REQUIRED` and create the next source+state candidate.

Do not rerun the original migration/action merely because source changed.

## Verification

Pass the target explicitly to `VERIFIER_HANDOFF.md`:

```text
STATEFUL_TARGET:
SOURCE_ID=...
ENVIRONMENT_ID=...
DEPLOYED_ID=...
EXTERNAL_STATE_ID=...
RECOVERY_REQUIRED=NO
```

Final `PASS` requires evidence against the current target tuple, not only local source tests.

Useful proof may include:

- deployed artifact digest matches expected source;
- schema/version marker matches expected state;
- data/backfill invariants hold;
- auth/permission boundary behaves correctly;
- health and real user-facing flow pass;
- rollback/forward-recovery status is known.

If production access is unavailable, production state remains unverified; never infer it from staging/local success.
