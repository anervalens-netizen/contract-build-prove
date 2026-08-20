---
name: contract-build-prove
description: Orchestrate substantial repository work through execution subagents, a falsifiable acceptance contract, restartable planning, independent verifier subagents, and evidence-backed completion. Use for multi-session, multi-component, migration, deployment, difficult bugfix, or high-risk work. Supports Codex, DeepSeek Harness, and compatible subagent-capable harnesses. Do not use for trivial local low-risk edits.
---

# Contract-Build-Prove

Make substantial repository work hard to falsely declare complete.

The primary agent is the **coordinator**. It owns intent, contract, decomposition, orchestration, integration, candidate identity, and final state. It does **not** act as the default implementation worker or acceptance authority.

Core flow:

**Understand → Contract → Delegate builders → Integrate → Freeze candidate → Fresh verifier → Remediate or close**

If this skill is active, subagent orchestration is mandatory. A normal CBP run requires at least one execution/builder subagent and one separate verifier subagent. Small local low-risk work should not invoke this skill.

Map roles and preferred models to the active harness using `references/RUNTIMES.md`.

## Core invariants

1. **Coordinator orchestrates; subagents execute.** Delegate meaningful implementation to builder subagents. The coordinator may make only small integration glue, conflict-resolution, or orchestration edits that are impractical to delegate.
2. **Builders never accept themselves.** A builder may test its own work, but it cannot authorize acceptance criteria `PASS`.
3. **Verification is fresh and independent.** The verifier must run in a fresh child context that did not implement the candidate. Use the runtime's verifier routing; GPT-5.6 Luna is the preferred verifier in Codex and the required verifier in the intended DSH setup.
4. **Protect existing work.** Never overwrite user changes, newer work, or unrelated edits.
5. **Freeze success before building.** Once implementation starts, never silently weaken, remove, or reinterpret an acceptance criterion.
6. **Verify an exact candidate.** Tie acceptance to an exact commit SHA or deterministic workspace fingerprint. Any verified-source change invalidates the previous verdict.
7. **Prove behavior, not edits.** Prefer executable tests and real runtime observations over claims that code "looks correct."
8. **Respect side-effect boundaries.** Do not push, merge, deploy, mutate production data/schema, delete resources, or perform irreversible external actions unless the user or repository policy explicitly authorizes them.

## 1. Choose rigor: Standard or High Assurance

### Standard CBP — default
Use for substantial, multi-component, multi-session, difficult-to-verify, or restartable work.

Require:
- one coordinator;
- one canonical ExecPlan;
- frozen acceptance criteria;
- one or more bounded builder subagents;
- integrated candidate identity;
- one fresh final verifier subagent for the integrated candidate.

### High Assurance
Use for security, auth/identity, financial/trading logic, destructive migrations, sensitive production data, safety-critical behavior, or unusually costly failure.

Add:
- fresh pre-build critique of critical acceptance criteria;
- negative/boundary/adversarial checks where applicable;
- intermediate independent verification at critical boundaries only when it materially reduces risk;
- fresh final verification of the fully integrated candidate.

If uncertain, choose High Assurance for irreversible or high-impact failure; otherwise Standard.

## 2. Establish baseline and plan

Before editing:

- Read applicable repository instructions, architecture, runbooks, and any existing plan for the same objective.
- Record branch, exact HEAD, working-tree state, relevant recent history, and protected user/newer work.
- Record relevant runtime/deployed SHA, schema, service health, or external state when the task depends on it. Inaccessible state is `UNVERIFIED`.
- Reuse one existing canonical plan for the objective. Do not create a competing tracker.
- If no equivalent plan system exists, create an ExecPlan using `assets/EXEC_PLAN_TEMPLATE.md`. Read `references/PLANS.md` when creating, resuming, or repairing a plan.

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

For High Assurance, launch a fresh verifier subagent to critique the draft contract before building. It critiques testability and missing failure cases; it does not implement.

## 4. Decompose and launch builder subagents

The coordinator converts the contract into the smallest useful independent work packets and launches subagents to execute them.

Each builder handoff must contain enough standalone context to execute without the parent conversation:

- task objective and owned scope;
- relevant acceptance criteria;
- files/components it may change;
- protected behavior and explicit non-goals;
- expected verification;
- side-effect/authorization limits;
- required return format: changes, checks run, results, blockers, remaining risk.

Use `references/BUILDER_HANDOFF.md` when useful.

Rules:

- **At least one builder subagent is mandatory for every CBP run.**
- Start with the smallest useful team, normally 1–3 builders. Add more only when the work decomposes into clearly independent scopes and coordination overhead remains low.
- Parallelize only work that does not contend for the same files, state, or sequencing.
- Keep tightly coupled architecture, database, auth, state-management, financial/trading, and cross-layer invariants under one sequential builder owner unless independence is clear.
- A builder may inspect and test its own work, but may not declare acceptance criteria independently `PASS`.
- The coordinator integrates builder outputs, resolves conflicts, updates the plan, and owns candidate identity.
- Use the current harness's normal file-editing and execution tools; do not require a specific vendor tool name.
- Make the smallest defensible change. Preserve unrelated behavior.

After two materially similar attempts without measurable progress, record the cause, replan once, and launch a meaningfully different builder approach. If that also stalls or essential access is unavailable, mark the affected work `BLOCKED` and state the exact unblock condition.

## 5. Integrate, verify locally, and freeze the candidate

The coordinator:

1. collects builder results;
2. inspects the integrated diff/status rather than trusting summaries;
3. runs or delegates narrow checks first, then relevant regression gates;
4. rechecks drift and protected work;
5. records candidate identity:
   - prefer an exact commit SHA when repository policy permits commits;
   - otherwise record exact HEAD plus a deterministic fingerprint of relevant workspace changes;
6. freezes the candidate for independent verification.

Builder/local checks are useful evidence but do not authorize acceptance.

Do not change verified source after candidate freeze. Any source change creates a new candidate and requires affected verification again.

## 6. Launch the independent verifier subagent

A fresh verifier subagent is mandatory for every CBP run.

Runtime-specific model/provider routing is defined in `references/RUNTIMES.md`.

The verifier must:

- run in a fresh context;
- have taken no implementation role in the candidate;
- receive the objective, frozen contract/amendments, relevant baseline, exact candidate identity, verification targets, and access limits;
- inspect the real integrated artifact;
- reconstruct whether the contract is satisfied from evidence.

Do **not** provide builder confidence, a defense of the implementation, or the desired verdict.

Default verification pattern:

- **Standard:** one fresh final verifier checks the fully integrated candidate and may authorize multiple criteria in one pass.
- **High Assurance:** optional fresh verifier(s) at critical milestones, plus a fresh final verifier for the integrated candidate.

Do not automatically create one verifier per builder task; intermediate verification is selective, not ceremonial.

Use `references/VERIFIER_HANDOFF.md` for the verifier contract.

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

If the required builder or verifier subagent capability is unavailable, do not silently collapse the workflow into a single-agent run. Report `BLOCKED` for CBP execution and state the missing capability.

## 7. Remediate and close

On verifier `FAIL`:

- return affected work to building;
- launch an appropriate builder for the highest-impact demonstrated gap;
- integrate the remediation;
- create a new candidate identity;
- rerun affected local verification;
- launch a fresh verification pass on the new candidate.

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

- `references/RUNTIMES.md` — Codex, DeepSeek Harness, model/provider, and role mapping.
- `references/PLANS.md` — ExecPlan lifecycle, state mapping, evidence rules, resume procedure.
- `references/BUILDER_HANDOFF.md` — standalone implementation-subagent contract.
- `references/VERIFIER_HANDOFF.md` — fresh verifier handoff and independence rules.
- `references/EXAMPLE.md` — minimal builder → FAIL → remediation → PASS example.
- `references/verifier.example.toml` — optional Codex custom verifier configuration.
