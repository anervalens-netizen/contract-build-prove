# ExecPlan reference

Use this reference for Standard and High-Assurance Contract-Build-Prove work. The ExecPlan is the durable state needed for another session or agent to resume without reconstructing the conversation.

## Canonicality

- Keep one active plan per objective/workstream.
- Reuse an equivalent repository-native planning system instead of creating a duplicate.
- Keep the plan concise: decisions, state, evidence pointers, failures, and next action. Do not paste large raw logs.
- Archive or otherwise close completed plans according to repository policy; do not leave competing active copies.

## State mapping

| Layer | Allowed states | Who changes it |
|---|---|---|
| Task | `BACKLOG`, `READY`, `BUILDING`, `VERIFYING`, `PASS`, `BLOCKED` | Coordinator |
| Acceptance criterion | `UNVERIFIED`, `PASS`, `FAIL`, `BLOCKED` | Coordinator records; fresh verifier authorizes `PASS` |
| Verification | `PASS`, `FAIL`, `BLOCKED` | Fresh verifier |
| Overall outcome | `UNVERIFIED`, `DONE`, `PARTIAL`, `BLOCKED` | Coordinator from recorded evidence |

Rules:

- A task may be `PASS` because its implementation work is complete while one or more acceptance criteria remain `UNVERIFIED`; this does not make the overall outcome `DONE`.
- Verification `FAIL` returns affected tasks to `BUILDING` and increments attempts.
- Verification `BLOCKED` means the verifier could not establish truth because required access/evidence is unavailable; it is not a passing result.
- `DONE` requires the current candidate—not an earlier one—to satisfy every required criterion.

## Baseline

Record enough to detect stale context and accidental overwrite:

- repository and branch;
- exact HEAD;
- `git status` / working-tree changes;
- protected user or newer work;
- relevant recent commits if they affect the objective;
- deployed SHA/digest, schema, service health, or external state when applicable.

Treat inaccessible state as `UNVERIFIED`, never as healthy or unchanged.

## Contract lifecycle

1. Draft falsifiable criteria before implementation.
2. For High Assurance, use a fresh verifier to critique critical criteria for testability and missing failure cases.
3. Freeze the contract at the first implementation edit.
4. After freeze, record amendments as `OLD / NEW / REASON / IMPACT`.
5. A scope reduction or weaker requested outcome requires explicit user authorization. Without it, retain the original criterion and report the limitation as `PARTIAL` or `BLOCKED`.

## Evidence record

Use enough detail for a fresh agent to reproduce or inspect the proof. For important evidence prefer:

- criterion ID;
- exact command/probe or runtime observation;
- exit/result summary;
- candidate SHA/fingerprint;
- relevant environment/service;
- timestamp or durable CI/runtime URL when useful.

Example:

```text
AC-2 — `pytest tests/payments/test_rounding.py -q` → exit 0, 14 passed; candidate 4f9c1ab; local test env; 2026-08-20T18:22:00Z
```

Do not paste bulky output into the plan. Store a sanitized artifact or durable link only if future verification benefits from it.

## Candidate identity

Preferred: exact commit SHA.

When work must remain uncommitted, record exact HEAD plus a deterministic fingerprint covering the relevant candidate changes. The method can be repository-specific, but it must change when verified source changes.

Once final verification begins, consider the candidate frozen. Any source edit after that invalidates prior acceptance and requires a new candidate identity, affected checks, and a new final verification.

## Drift checks

Recheck repository state:

- when resuming;
- before integrating delegated work;
- before freezing the candidate;
- immediately before final verification.

If drift is unrelated, preserve it and continue. If it overlaps owned scope or invalidates baseline assumptions, update the plan and re-evaluate before editing or verifying.

## Stagnation

- Never repeat the same failed approach unchanged.
- After two materially similar attempts with no measurable progress, record the likely cause and replan once.
- The replan must change a meaningful variable: hypothesis, implementation approach, tool, scope decomposition, or verification method.
- If the replanned attempt also stalls, or essential access/information is unavailable, mark the affected work `BLOCKED` and state the exact unblock condition.

## Resume rule

A fresh session should be able to answer these from the plan and repository alone:

1. What is the requested observable outcome?
2. What must not change?
3. What is already built and what failed?
4. What exact candidate/state is current?
5. Which criteria are still unverified or failed?
6. What evidence exists?
7. What is the next exact action?
