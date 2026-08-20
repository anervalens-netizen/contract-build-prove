# Contract-Build-Prove

A Codex skill for substantial repository work where "the code changed" is not enough evidence that the task is complete.

It uses a simple discipline:

**Contract → Build → Freeze candidate → Independent proof → Close**

The design goal is **minimum process that makes false completion difficult**.

## When it helps

Use it for multi-session or multi-component work, migrations, deployments, difficult bug fixes, and high-risk domains where another agent should independently verify the result.

Small local low-risk edits stay on the normal fast lane.

## Rigor levels

- **Fast** — normal repository workflow; local/reversible/low-risk work.
- **Standard CBP** — persistent ExecPlan + frozen acceptance contract + one final independent audit.
- **High Assurance** — adds pre-build contract critique, stronger negative/boundary proof, and intermediate audits only where risk justifies them.

## Files

- `SKILL.md` — critical workflow and invariants loaded when the skill runs.
- `agents/openai.yaml` — Codex/ChatGPT UI metadata and invocation policy.
- `assets/EXEC_PLAN_TEMPLATE.md` — persistent plan template.
- `references/PLANS.md` — state model, evidence, drift, candidate identity, resume rules.
- `references/AUDITOR_HANDOFF.md` — generic fresh-auditor prompt and verdict semantics.
- `references/EXAMPLE.md` — minimal FAIL → remediation → PASS example.
- `references/auditor.example.toml` — optional custom Codex auditor.

## Install as a repository skill

Place this directory at:

```text
.agents/skills/contract-build-prove/
```

Then invoke explicitly with:

```text
$contract-build-prove
```

The skill also allows implicit invocation when the task matches its description.

## Optional custom auditor

The skill does **not** require a custom auditor. It falls back to a fresh built-in `default` subagent when no configured `auditor` or `reviewer` exists.

For a dedicated auditor, copy:

```text
references/auditor.example.toml
```

to either:

```text
.codex/agents/auditor.toml
```

for one repository, or:

```text
~/.codex/agents/auditor.toml
```

for the user account.

The example intentionally does not pin a model, so it can inherit the current Codex subagent model policy.

## Core safety properties

- acceptance criteria cannot be silently weakened after implementation begins;
- final acceptance is tied to an exact candidate SHA/fingerprint;
- any post-audit source edit invalidates the audit;
- independent audit does not receive the builder's confidence or intended conclusion;
- user/newer work is protected across resume and integration;
- push/merge/deploy/production mutation requires explicit authorization or repository policy;
- missing independent proof is reported as a limitation, never simulated.
