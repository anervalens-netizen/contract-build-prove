# Stateful / irreversible work

Read this only when the task changes persistent external state: database/schema/data, auth/identity state, deployed infrastructure, queues, external services/resources, or another target that cannot be described by source code alone.

The purpose is to prevent a failed mutation from falling blindly into the normal `FAIL → patch → retry` loop.

## Candidate state tuple

Record only the fields that apply:

```text
SOURCE_ID=<verified source SHA/fingerprint>
ENVIRONMENT_ID=<staging/prod/cluster/account/database/etc.>
DEPLOYED_ID=<artifact/image/release digest or N/A>
EXTERNAL_STATE_ID=<schema version/state marker/resource version or N/A>
```

The verifier must know which tuple it is checking. Source SHA alone is insufficient after an external mutation.

## Before mutation

Require:

- explicit authorization for production/destructive/irreversible action;
- current external-state baseline;
- preconditions/backup where relevant;
- rollback or forward-recovery strategy when failure could leave partial state;
- staging/dry-run proof when realistically available for destructive High-Assurance work.

## After mutation

Re-read the actual external state. Do not assume the intended transition completed.

Update `DEPLOYED_ID` / `EXTERNAL_STATE_ID` from observed state before acceptance verification.

## Recovery gate

If an authorized stateful/irreversible operation fails or leaves ambiguous partial state:

```text
RECOVERY_REQUIRED = YES
```

Then:

1. stop further irreversible mutation;
2. inspect and re-baseline actual external state;
3. determine whether safe rollback is possible;
4. otherwise define an explicit forward-recovery plan from the **current** state;
5. obtain any authorization required for the recovery action;
6. only then create a new source+state candidate and continue.

Do not re-run the original migration/action merely because the source candidate changed.

Clear `RECOVERY_REQUIRED` only after the environment is in a known state with a safe next transition.

## Verification

Final `PASS` for stateful work requires evidence against the current state tuple, not only local source tests.

Examples of useful proof, when applicable:

- deployed artifact digest matches expected source;
- schema/version marker matches expected state;
- data/backfill invariants hold;
- auth/permission boundary behaves correctly;
- health and real user-facing flow pass;
- rollback/forward-recovery status is known.

If production access is unavailable, production state remains unverified; never infer it from staging/local success.
