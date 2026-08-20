---
name: contract-build-prove
description: Orchestrate substantial repository implementation with a falsifiable acceptance contract, restartable execution plan, bounded building, independent audit, and evidence-backed completion. Use for multi-session, multi-component, migration, deployment, or high-risk work, and when resuming an active plan. Do not use for small local low-risk changes.
---

# Contract-Build-Prove

Make substantial repository work hard to falsely declare complete. Keep the process proportional: define what success means, build against that contract, then let fresh evidence—not builder confidence—authorize completion.

## Core invariants

1. **Protect existing work.** Never overwrite user changes, newer work, or unrelated edits.
2. **Freeze success before building.** Once implementation starts, never silently weaken, remove, or reinterpret an acceptance criterion.
3. **Separate build from acceptance.** The builder may verify locally; for Standard and High-Assurance work, a fresh independent auditor authorizes `PASS`.
4. **Audit an exact candidate.** Tie acceptance to an exact commit SHA or deterministic workspace fingerprint. Any source change after audit invalidates that audit.
5. **Prove behavior, not edits.** Prefer executable tests and real runtime observations over claims that code "looks correct."
6. **Respect side-effect boundaries.** Do not push, merge, deploy, mutate production data/schema, delete resources, or perform irreversible external actions unless the user or repository policy explicitly authorizes them.

## 1. Choose the rigor level

Use the lowest level that safely fits the work.

### Fast lane — outside full CBP
Use only when all are true: local and reversible; low-risk domain; one-session scope; no migration/deployment/security/auth/financial/production-data boundary; no tightly coupled cross-component coordination; straightforward verification.

Follow normal repository workflow and self-verify. If this skill was explicitly requested, state that Fast was selected and keep the contract concise rather than creating process for its own sake.

### Standard CBP — default
Use when the task is substantial, multi-component, multi-session, difficult to verify, or benefits from restartability. Require one canonical ExecPlan, frozen acceptance criteria, candidate identity, and one fresh final independent audit.

### High Assurance
Use for security, auth/identity, financial/trading logic, destructive migrations, sensitive production data, safety-critical behavior, or unusually costly failure. Add pre-build contract critique, negative/boundary tests where applicable, and intermediate independent audits only when they materially reduce risk.

If uncertain between Standard and High Assurance, choose High Assurance for irreversible or high-impact failure; otherwise Standard.

## 2. Establish baseline and plan

Before editing:

- Read applicable `AGENTS.md`, repository instructions, architecture, runbooks, and any existing plan for the same objective.
- Record branch, exact HEAD, working-tree state, relevant recent history, and protected user/newer work.
- Record relevant runtime/deployed SHA, schema, service health, or external state when the task depends on it. Inaccessible state is `UNVERIFIED`.
- Reuse one existing canonical plan for the objective. Do not create a competing tracker.
- For Standard/High Assurance, if no equivalent plan system exists, create an ExecPlan using `assets/EXEC_PLAN_TEMPLATE.md`. Read `references/PLANS.md` when creating, resuming, or repairing a plan.

Before integration and before final audit, recheck HEAD and working tree. If drift overlaps owned scope, re-evaluate the candidate and contract before continuing. Never overwrite newer/user work.

## 3. Write and freeze the acceptance contract

For each criterion define:

- observable behavior;
- protected behavior/non-goals;
- verification method and expected result;
- runtime/API/browser/database/deploy proof when relevant;
- evidence required for `PASS`.

Criteria must be falsifiable. Start them as `UNVERIFIED`.

For bug fixes, reproduce the failure before the fix when reasonably possible, then prove the same observation passes after the fix. If pre-fix reproduction is impossible, record why.

For High Assurance, require at least one useful negative, boundary, or adversarial check for each critical criterion where applicable.

**Contract freeze:** the contract freezes when the first implementation edit begins. Later changes require an explicit amendment recording `OLD`, `NEW`, `REASON`, and `IMPACT`. Never reduce the requested user outcome without explicit user authorization. If a blocker forces reduced scope, report `PARTIAL` or `BLOCKED`; do not redefine success.

For High Assurance, ask a fresh auditor to critique the draft contract before building. It critiques testability and missing failure cases; it does not implement.

## 4. Build with bounded ownership

- Give each builder the smallest self-contained task contract and relevant code scope.
- Prefer the built-in `worker` or an existing project-specific builder.
- Parallelize only independent work that does not contend for the same files, state, or sequencing.
- Keep tightly coupled architecture, database, auth, state-management, financial/trading, and cross-layer invariants under one sequential owner unless independence is clear.
- The primary agent owns integration, plan updates, candidate identity, and authorized external side effects.
- Make the smallest defensible change. Preserve unrelated behavior.
- Do not repeat an unchanged failed approach.

After two materially similar attempts without measurable progress, record the cause, replan once, and try a meaningfully different approach. If that also stalls or essential access is unavailable, mark the affected work `BLOCKED` and state the exact unblock condition.

## 5. Verify locally, then freeze the candidate

Run the narrow checks first, then relevant regression gates. Builder/local checks produce evidence but do not authorize Standard/High-Assurance acceptance.

Before independent audit:

1. Integrate intended changes.
2. Inspect the complete candidate diff/status.
3. Recheck drift and protected work.
4. Record the candidate identity:
   - prefer an exact commit SHA when repository policy permits commits;
   - otherwise record exact HEAD plus a deterministic fingerprint of the relevant workspace changes.
5. Do not change audited source after this point. Any source change creates a new candidate and requires re-verification/re-audit.

## 6. Prove independently

Use one fresh final audit for the integrated candidate by default. It may authorize multiple acceptance criteria in one pass. Add intermediate audits only for High-Assurance boundaries or when early independent proof materially reduces rework.

Auditor selection order:

1. configured custom `auditor`;
2. configured custom `reviewer`;
3. fresh built-in `default` subagent with the audit handoff in `references/AUDITOR_HANDOFF.md`.

Do not use `worker` as acceptance authority for work it implemented. `explorer` is for read-heavy exploration, not the default acceptance fallback.

Give the auditor the objective, frozen contract/amendments, relevant baseline, exact candidate identity, verification targets, and access limits. Do **not** give it the builder's confidence, explanation, or desired verdict. It must inspect the real artifact and reconstruct whether the contract is satisfied.

Prefer read-only tracked source for the auditor. Temporary test/cache writes are acceptable only in an isolated or disposable location when needed. Never let an audit mutate production state.

Require exactly:

```text
VERDICT: PASS | FAIL | BLOCKED
CONTRACT: criterion -> PASS | FAIL | BLOCKED, with reason
EVIDENCE: exact commands/probes, results, paths/URLs, candidate SHA/fingerprint
FINDINGS: concrete defects/regressions, highest severity first
UNVERIFIED: anything not actually observed
LARGEST_GAP: single next remediation target, or NONE
```

The primary agent records the verdict; the auditor does not edit the plan.

If no independent auditor or equivalent independent repository gate is available, do not simulate one. Complete local verification, record the limitation, and report Standard/High-Assurance work as `PARTIAL` unless the missing independence also prevents the requested result, in which case report `BLOCKED`.

## 7. Remediate and close

On audit `FAIL`:

- return affected work to building;
- fix the highest-impact demonstrated gap first;
- create a new candidate identity;
- rerun affected verification;
- audit the new candidate again.

Mark overall `DONE` only when:

- every required acceptance criterion is independently `PASS` for the current candidate;
- relevant regression gates pass;
- required runtime/deployment proof exists;
- no unresolved protected-work or drift conflict remains.

Otherwise report exactly `PARTIAL` or `BLOCKED`, with completed work, failed/unverified criteria, evidence, candidate identity, risks, and the next concrete action.

When deployment is explicitly in scope and authorized, verify the exact deployed SHA/digest plus health and the real user-facing flow. No production access means production verification remains `UNVERIFIED`.

## Evidence hygiene

Record concise, reproducible evidence. Prefer command/probe + result + candidate identity + environment/timestamp when relevant. Store durable sanitized artifacts only when useful.

Never store secrets, credentials, private keys, personal data, sensitive production payloads, or unnecessary raw database/log content in plans, evidence, Git, or chat.

## Supporting references

- `references/PLANS.md` — ExecPlan lifecycle, state mapping, evidence rules, resume procedure.
- `references/AUDITOR_HANDOFF.md` — exact generic auditor handoff and independence rules.
- `references/EXAMPLE.md` — minimal end-to-end example, including FAIL → remediation → PASS.
- `references/auditor.example.toml` — optional custom Codex auditor; copy to `.codex/agents/auditor.toml` or `~/.codex/agents/auditor.toml` if desired.
