# Contract-Build-Prove

A multi-harness skill for substantial repository work where "the code changed" is not enough evidence that the task is complete.

It is designed for **Codex, DeepSeek Harness (DSH), and other skill/subagent-capable agent harnesses**.

Core architecture:

**Coordinator → Builder subagents → Integration → Frozen candidate → Independent verifier subagent → Remediate or close**

The design goal is **minimum process that makes false completion difficult**.

## Agent roles

### Coordinator
Owns the user objective, acceptance contract, decomposition, plan, protected work, integration, candidate identity, and final state. It should not become the default implementation worker for substantial tasks.

### Builder subagents
Receive small standalone work packets, implement them, run local checks, and return evidence/blockers. They do not authorize their own acceptance.

### Verifier subagents
Start in a fresh context, did not implement the candidate, inspect the real integrated artifact, and return `PASS | FAIL | BLOCKED` against the frozen contract.

For **Standard CBP**, normally use one final verifier for the integrated candidate rather than one verifier per builder. For **High Assurance**, add intermediate independent verification only at critical boundaries where the extra cost materially reduces risk.

## Rigor levels

- **Fast** — local/reversible/low-risk work; normal workflow; subagents optional.
- **Standard CBP** — coordinator + ExecPlan + frozen contract + delegated builders when available + one final independent verifier.
- **High Assurance** — Standard plus contract critique, stronger negative/boundary proof, and selective intermediate verification.

## Runtime support

### OpenAI Codex
Uses the same `SKILL.md`. `agents/openai.yaml` provides Codex-specific UI/invocation metadata. Builder and verifier roles map to Codex subagents; optional custom auditors can live under `.codex/agents/` or `~/.codex/agents/`.

### DeepSeek Harness (DSH)
DSH supports skills and a subagent capability. A project may discover this skill from `.agents/skills/contract-build-prove/`, so the same repository installation can be shared with Codex. The coordinator delegates builder and verifier tasks through DSH's configured subagent provider(s).

DSH is currently a developer preview and its APIs/configuration may change; therefore the core skill avoids hardcoding DSH provider names or plugin configuration. Runtime mapping lives in `references/RUNTIMES.md`.

### Other harnesses
If the harness can load `SKILL.md`-style instructions and launch independent child agents/contexts, map its capabilities to the same three roles. If it cannot provide independent verification, Standard/High-Assurance completion must not pretend that independence exists.

## Files

- `SKILL.md` — compact, runtime-neutral critical workflow.
- `agents/openai.yaml` — Codex-specific UI metadata and invocation policy; harmless/optional outside Codex.
- `assets/EXEC_PLAN_TEMPLATE.md` — persistent plan template.
- `references/RUNTIMES.md` — Codex/DSH/generic role mapping.
- `references/PLANS.md` — state model, evidence, drift, candidate identity, resume rules.
- `references/AUDITOR_HANDOFF.md` — generic fresh-verifier prompt and verdict semantics.
- `references/EXAMPLE.md` — minimal FAIL → remediation → PASS example.
- `references/auditor.example.toml` — optional Codex custom auditor example.

## Install in a repository

Use:

```text
.agents/skills/contract-build-prove/
```

This location is compatible with Codex and is also discoverable by DeepSeek Harness.

Explicit Codex invocation:

```text
$contract-build-prove
```

DSH invocation depends on its active skill consumer/UI; once the skill is discovered, load/select `contract-build-prove` through the harness's skill capability.

## Core safety properties

- substantial work is orchestrated, not performed monolithically by the coordinator when subagents exist;
- acceptance criteria cannot be silently weakened after implementation begins;
- builders cannot self-authorize acceptance;
- final acceptance is tied to an exact candidate SHA/fingerprint;
- any post-audit source edit invalidates the prior audit;
- independent verification does not receive builder confidence or desired verdict;
- user/newer work is protected across resume and integration;
- push/merge/deploy/production mutation requires explicit authorization or repository policy;
- missing independent proof is reported as a limitation, never simulated.
