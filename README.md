# Contract-Build-Prove

A multi-harness skill for substantial repository work where "the code changed" is not enough evidence that the task is complete.

Designed for **Codex, DeepSeek Harness (DSH), and compatible subagent-capable harnesses**.

Core architecture:

**Coordinator → Builder subagent(s) → Integration → Frozen candidate → Fresh verifier subagent → Remediate or close**

The design goal is **minimum process that makes false completion difficult**.

## The rule that matters most

If Contract-Build-Prove is active, **subagents are mandatory**.

Every normal run has:

- one coordinator;
- at least one execution/builder subagent;
- one separate fresh verifier subagent.

The coordinator owns the contract, plan, decomposition, integration, candidate identity, and final state. It should not simply implement the whole task itself. Builders execute bounded work. Verifiers independently decide whether the integrated candidate actually satisfies the frozen acceptance contract.

Small local low-risk edits should use the harness's normal workflow instead of this skill.

## Rigor levels

- **Standard CBP** — coordinator + persistent ExecPlan + frozen contract + builder subagent(s) + one final independent verifier.
- **High Assurance** — Standard plus contract critique, stronger negative/boundary proof, and selective intermediate independent verification for high-impact boundaries.

## Model routing

### DeepSeek Harness

- **Builder/execution:** use the execution subagent provider/model already configured by DSH. In the intended setup this is MiniMax; the skill does not hardcode the concrete MiniMax version.
- **Verifier:** use a fresh **GPT-5.6 Luna** subagent for independent acceptance verification.

This lets DSH own provider/model configuration while CBP owns the orchestration contract.

### Codex

- **Builders:** coordinator chooses subagents according to complexity and specialization, with **GPT-5.6 Luna preferred** when suitable.
- **Verifier:** **GPT-5.6 Luna is the preferred final verifier**. Use a fresh verifier context that did not implement the candidate.

If Luna is unavailable, the strongest available independent verifier may be used, but the deviation should be recorded.

## Files

- `SKILL.md` — compact critical workflow and invariants.
- `agents/openai.yaml` — Codex-specific UI/invocation metadata.
- `assets/EXEC_PLAN_TEMPLATE.md` — persistent plan template.
- `references/RUNTIMES.md` — Codex/DSH/generic role and model routing.
- `references/PLANS.md` — state model, evidence, drift, candidate identity, resume rules.
- `references/BUILDER_HANDOFF.md` — standalone implementation-subagent handoff.
- `references/AUDITOR_HANDOFF.md` — fresh-verifier handoff and verdict semantics.
- `references/EXAMPLE.md` — minimal FAIL → remediation → PASS example.
- `references/auditor.example.toml` — optional Codex custom auditor example.

## Install in a repository

Use:

```text
.agents/skills/contract-build-prove/
```

The same repository location can be used by Codex and DSH.

Explicit Codex invocation:

```text
$contract-build-prove
```

## Core safety properties

- substantial work is orchestrated through subagents, not performed monolithically by the coordinator;
- acceptance criteria cannot be silently weakened after implementation begins;
- builders cannot self-authorize acceptance;
- final acceptance is tied to an exact candidate SHA/fingerprint;
- any post-verification source edit invalidates the prior verdict;
- independent verification does not receive builder confidence or desired verdict;
- user/newer work is protected across resume and integration;
- push/merge/deploy/production mutation requires explicit authorization or repository policy;
- missing required subagent capability blocks CBP rather than silently degrading to single-agent execution.
