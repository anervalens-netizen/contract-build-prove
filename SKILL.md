---
name: contract-build-prove
description: Orchestrate substantial repository work through scoped execution subagents, a falsifiable acceptance contract, restartable planning, independent verification, and evidence-backed completion. Use for multi-session, multi-component, migration, deployment, difficult bugfix, or high-risk work. Supports agent harnesses with skills and subagent delegation, including Codex and DeepSeek Harness.
---

# Contract-Build-Prove

Make substantial repository work hard to falsely declare complete. The primary agent is the **coordinator**: it owns intent, contract, decomposition, integration, candidate identity, and final state. It should delegate bounded implementation to **builder subagents** and acceptance to fresh **verifier subagents** whenever the runtime provides subagent capability.

Core flow:

**Understand → Contract → Delegate build → Integrate → Freeze candidate → Independent verify → Remediate or close**

Do not assume vendor-specific tool or agent names. Map these roles to the current harness using `references/RUNTIMES.md`.

## Core invariants

1. **Coordinator owns truth, not all coding.** For Standard and High Assurance, delegate meaningful self-contained implementation work to subagents when subagent capability exists. The coordinator may handle small integration glue, conflict resolution, or tightly coupled work that cannot be safely delegated.
2. **Protect existing work.** Never overwrite user changes, newer work, or unrelated edits.
3. **Freeze success before building.** Once implementation starts, never silently weaken, remove, or reinterpret an acceptance criterion.
4. **Separate build from acceptance.** Builders may self-test, but they never authorize their own acceptance. Standard and High-Assurance `PASS` requires a fresh verifier or equivalent independent repository gate.
5. **Audit an exact candidate.** Tie acceptance to an exact commit SHA or deterministic workspace fingerprint. Any audited-source change invalidates the previous verdict.
6. **Prove behavior, not edits.** Prefer executable tests and real runtime observations over claims that code "looks correct."
7. **Respect side-effect boundaries.** Do not push, merge, deploy, mutate production data/schema, delete resources, or perform irreversible external actions unless the user or repository policy explicitly authorizes them.

## 1. Choose the rigor level

Use the lowest level that safely fits the work.

### Fast
Use only when all are true: local and reversible; low-risk domain; one-session scope; no migration/deployment/security/auth/financial/production-data boundary; no tightly coupled cross-component coordination; straightforward verification.

Use the normal repository workflow. Subagents are optional. If this skill was explicitly requested, keep the contract concise rather than creating process for its own sake.

### Standard CBP — default
Use when the task is substantial, multi-component, multi-session, difficult to verify, or benefits from restartability.

Require:
- one coordinator;
- one canonical ExecPlan;
- frozen acceptance criteria;
- bounded builder delegation when subagents are available;
- integrated candidate identity;
- one fresh final independent verification of the candidate.

### High Assurance
Use for security, auth/identity, financial/trading logic, destructive migrations, sensitive production data, safety-critical behavior, or unusually costly failure.

Add:
- fresh pre-build critique of critical acceptance criteria;
- negative/boundary/adversarial checks where applicable;
- intermediate independent verification at critical boundaries only when it materially reduces risk;
- final fresh independent verification of the integrated candidate.

If uncertain between Standard and High Assurance, choose High Assurance for irreversible or high-impact failure; otherwise Standard.

## 2. Establish baseline and plan

Before editing:

- Read applicable repository instructions, architecture, runbooks, and any existing plan for the same objective.
- Record branch, exact HEAD, working-tree state, relevant recent history, and protected user/newer work.
- Record relevant runtime/deployed SHA, schema, service health, or external state when the task depends on it. Inaccessible state is `UNVERIFIED`.
- Reuse one existing canonical plan for the objective. Do not create a competing tracker.
- For Standard/High Assurance, if no equivalent plan system exists, create an ExecPlan using `assets/EXEC_PLAN_TEMPLATE.md`. Read `references/PLANS.md` when creating, resuming, or repairing a plan.

Before integration and before final verification, recheck HEAD and working tree. If drift overlaps owned scope, re-evaluate the candidate and contract before continuing. Never overwrite newer/user work.

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

For High Assurance, use a fresh verifier/reviewer subagent to critique the draft contract before building. It critiques testability and missing failure cases; it does not implement.

## 4. Decompose and delegate the build

The coordinator converts the contract into the smallest useful independent work packets.

Each builder handoff must contain enough standalone context to execute without this conversation:

- task objective and owned scope;
- relevant acceptance criteria;
- files/components it may change;
- protected behavior and explicit non-goals;
- expected verification;
- side-effect/authorization limits;
- required return format: changes, checks run, results, blockers, remaining risk.

Rules:

- **Delegation-first for Standard/High Assurance:** if the harness can spawn subagents, delegate meaningful self-contained build tasks rather than doing all implementation in the coordinator context.
- Parallelize only work that does not contend for the same files, state, or sequencing.
- Keep tightly coupled architecture, database, auth, state-management, financial/trading, and cross-layer invariants under one sequential owner unless independence is clear.
- A builder may inspect and test its own work, but may not declare acceptance criteria independently `PASS`.
- The coordinator integrates builder outputs, resolves conflicts, updates the plan, and owns candidate identity.
- Use the current harness's normal file-editing and execution tools; do not require a specific vendor tool name.
- Make the smallest defensible change. Preserve unrelated behavior.

After two materially similar attempts without measurable progress, record the cause, replan once, and try a meaningfully different approach. If that also stalls or essential access is unavailable, mark the affected work `BLOCKED` and state the exact unblock condition.

## 5. Integrate, verify locally, and freeze the candidate

The coordinator:

1. collects completed builder results;
2. reviews the integrated diff/status rather than trusting summaries;
3. runs narrow checks first, then relevant regression gates;
4. rechecks drift and protected work;
5. records candidate identity:
   - prefer an exact commit SHA when repository policy permits commits;
   - otherwise record exact HEAD plus a deterministic fingerprint of relevant workspace changes;
6. freezes the candidate for independent verification.

Builder/local checks are useful evidence but do not authorize Standard/High-Assurance acceptance.

Do not change audited source after candidate freeze. Any source change creates a new candidate and requires affected verification again.

## 6. Verify independently

Use a **fresh subagent/context that did not implement the candidate**. Prefer a configured verifier/auditor/reviewer role; otherwise use a fresh general-purpose subagent with `references/AUDITOR_HANDOFF.md`.

Runtime-specific role mapping is in `references/RUNTIMES.md`.

Default verification pattern:

- **Standard:** one fresh final verifier audits the fully integrated candidate and may authorize multiple criteria in one pass.
- **High Assurance:** optional fresh verifier(s) at critical milestones, plus a fresh final verifier for the fully integrated candidate.

Do not automatically create one verifier per builder task; use intermediate verification only when it improves risk control enough to justify the overhead.

Give the verifier the objective, frozen contract/amendments, relevant baseline, exact candidate identity, verification targets, and access limits. Do **not** give it builder confidence, a defense of the implementation, or the desired verdict. It must inspect the real artifact and reconstruct whether the contract is satisfied.

Prefer read-only tracked source for verification. Temporary test/cache writes are acceptable only in an isolated or disposable location when needed. Never let verification mutate production state.

Require exactly:

```text
VERDICT: PASS | FAIL | BLOCKED
CONTRACT: criterion -> PASS | FAIL | BLOCKED, with reason
EVIDENCE: exact commands/probes, results, paths/URLs, candidate SHA/fingerprint
FINDINGS: concrete defects/regressions, highest severity first
UNVERIFIED: anything not actually observed
LARGEST_GAP: single next remediation target, or NONE
```

The coordinator records the verdict; the verifier does not edit the canonical plan.

If no independent subagent or equivalent independent repository gate is available, do not simulate independence. Complete local verification, record the limitation, and report Standard/High-Assurance work as `PARTIAL` unless the missing independence also prevents the requested result, in which case report `BLOCKED`.

## 7. Remediate and close

On verifier `FAIL`:

- return affected work to building;
- delegate the highest-impact demonstrated gap to an appropriate builder when possible;
- integrate the remediation;
- create a new candidate identity;
- rerun affected local verification;
- use a fresh verification pass on the new candidate.

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

- `references/RUNTIMES.md` — role mapping for Codex, DeepSeek Harness, and generic subagent-capable harnesses.
- `references/PLANS.md` — ExecPlan lifecycle, state mapping, evidence rules, resume procedure.
- `references/AUDITOR_HANDOFF.md` — generic fresh-verifier handoff and independence rules.
- `references/EXAMPLE.md` — minimal end-to-end example, including builder → FAIL → remediation → PASS.
- `references/auditor.example.toml` — optional custom Codex auditor; not required for DSH or generic operation.
