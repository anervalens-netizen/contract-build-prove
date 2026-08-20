# Runtime adapters

Contract-Build-Prove defines one orchestration pattern across harnesses:

**Coordinator → builder subagent(s) → integration → frozen candidate → fresh verifier subagent → remediation or close**

If the harness cannot provide both execution and verification subagents, a full CBP run is unavailable and must report `BLOCKED` rather than silently degrading to single-agent execution.

## Required capability model

Every CBP run requires:

1. a primary coordinator context;
2. at least one fresh child agent/context capable of bounded implementation;
3. a separate fresh child agent/context that did not implement the candidate and can independently verify it;
4. repository/file execution access sufficient to inspect and test the candidate.

The coordinator may perform small integration glue or conflict resolution, but should not absorb the builder role simply because it is convenient.

## Model routing principles

- **Verification quality has priority over cost.** Prefer GPT-5.6 Luna for the independent verifier whenever available.
- Builder model choice may optimize for coding fit, speed, context, and cost, provided the coordinator preserves the contract and independent-verification boundary.
- A verifier should not be the same child session/context as any builder. Freshness matters even if the same underlying model family is used.
- If the preferred model is unavailable, use the strongest available independent verifier and record the deviation in the ExecPlan.

## OpenAI Codex

### Coordinator
The current Codex agent/thread running this skill.

### Builders
The coordinator chooses builder subagent model/role according to task complexity and specialization.

Preference order:

1. **GPT-5.6 Luna** when available and suitable;
2. another strong coding-capable subagent selected by the coordinator when it has a clear advantage for the specific task;
3. project-specific custom builder when repository policy/configuration defines one.

Use `explorer` only for read-heavy discovery. Exploration does not replace the mandatory implementation builder.

### Verifier
Prefer **GPT-5.6 Luna** as the final verifier.

Role selection when supported:

1. fresh configured `auditor` using GPT-5.6 Luna;
2. fresh configured `reviewer` using GPT-5.6 Luna;
3. fresh general-purpose/default subagent using GPT-5.6 Luna and `AUDITOR_HANDOFF.md`;
4. if Luna is unavailable, the strongest available fresh independent verifier, with the deviation recorded.

Never reuse a builder session as verifier for the candidate it implemented.

### Skill location

```text
.agents/skills/contract-build-prove/
```

`agents/openai.yaml` supplies Codex-specific UI/invocation metadata. Optional Codex custom agents live in `.codex/agents/` or `~/.codex/agents/`; they are adapters, not part of the portable workflow itself.

## DeepSeek Harness (DSH)

### Coordinator
The current DSH agent/session running the skill. It owns the ExecPlan, contract, decomposition, orchestration, integration, candidate freeze, and final state.

### Builders
Use DSH's configured **execution subagent** for implementation work. The harness/project configuration owns the concrete provider and model selection; CBP should not override that routing.

In the intended setup this execution role is backed by **MiniMax**, but the skill refers to the configured execution role rather than hardcoding a specific MiniMax model/version. This lets DSH evolve its provider/model configuration without requiring changes to the workflow.

Each builder invocation must be a scoped child context with a standalone handoff. Use `BUILDER_HANDOFF.md`.

### Verifier
Use a **new GPT-5.6 Luna subagent** for independent verification.

Required properties:

- provider/model route resolves to GPT-5.6 Luna through the DSH configuration;
- invocation is fresh and did not participate in implementation;
- verifier receives `AUDITOR_HANDOFF.md`, the frozen contract, and exact candidate identity;
- it directly inspects/tests the integrated candidate;
- it does not inherit or receive the builder's confidence or desired verdict.

If GPT-5.6 Luna is temporarily unavailable, use the strongest available fresh independent verifier only if the coordinator records the deviation explicitly. If no independent verifier exists, report `BLOCKED`.

### Skill location

DSH can discover project skills from:

```text
.agents/skills/contract-build-prove/
```

No DSH-specific metadata file is required by the portable core. Provider/model routing should remain in DSH's own configuration rather than being duplicated inside this skill.

## Generic subagent-capable harness

Map capabilities by role:

| CBP role | Runtime requirement |
|---|---|
| Coordinator | persistent primary context with repository access |
| Builder | fresh/scoped child agent capable of implementation and local tests |
| Verifier | fresh child context that did not implement the candidate and can inspect/test it |

Prefer GPT-5.6 Luna for verifier when exposed by the harness. Builder selection remains coordinator-controlled unless runtime policy defines a dedicated execution role.
