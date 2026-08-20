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

- Verification quality has priority over cost.
- Builder model choice may optimize for coding fit, speed, context, and cost, provided the coordinator preserves the contract and independent-verification boundary.
- A verifier must not be the same child session/context as any builder. Freshness matters even if the same model family is used.
- Runtime-specific routing below overrides generic preferences.

## OpenAI Codex

### Coordinator
The current Codex agent/thread running this skill.

### Builders
The coordinator chooses builder subagent model/role according to task complexity and specialization.

Preference:

1. **GPT-5.6 Luna** when available and suitable;
2. another strong coding-capable subagent when the coordinator has a concrete reason to prefer it for that task;
3. a project-specific custom builder when repository configuration defines one.

Use `explorer` only for read-heavy discovery. Exploration does not replace the mandatory implementation builder.

### Verifier
Prefer **GPT-5.6 Luna** for final verification.

Role selection when supported:

1. fresh configured `verifier` using GPT-5.6 Luna;
2. fresh configured `reviewer` using GPT-5.6 Luna;
3. fresh general-purpose/default subagent using GPT-5.6 Luna and `VERIFIER_HANDOFF.md`;
4. if Luna is unavailable, the strongest available fresh independent verifier, with the deviation recorded in the ExecPlan.

Never reuse a builder session as verifier for the candidate it implemented.

For High Assurance, the coordinator may raise reasoning effort or choose a stronger verifier if the runtime policy permits it and the risk justifies the cost.

### Skill location

```text
.agents/skills/contract-build-prove/
```

`agents/openai.yaml` supplies Codex-specific UI/invocation metadata. Optional Codex custom agents live in `.codex/agents/` or `~/.codex/agents/`; they are adapters, not part of the portable workflow itself.

## DeepSeek Harness (DSH)

### Coordinator
The current DSH agent/session running the skill. It owns the ExecPlan, contract, decomposition, orchestration, integration, candidate freeze, and final state.

### Builders
Use DSH's configured **execution subagent** for implementation work.

The DSH/project configuration owns the concrete provider and model. In the intended setup this role is backed by **MiniMax**; CBP deliberately does not hardcode the MiniMax model/version because the harness already knows the configured execution route.

Each builder invocation must be a scoped child context with a standalone handoff from `BUILDER_HANDOFF.md`.

### Verifier
Use a **new GPT-5.6 Luna subagent** for independent verification. In the intended DSH setup this routing is mandatory, not merely preferred.

Required properties:

- DSH provider/model routing resolves the verifier to `gpt-5.6-luna`;
- invocation is fresh and did not participate in implementation;
- verifier receives `VERIFIER_HANDOFF.md`, the frozen contract, and exact candidate identity;
- it directly inspects/tests the integrated candidate;
- it does not receive the builder's confidence or desired verdict.

If the configured GPT-5.6 Luna verifier route is unavailable, report the verification phase `BLOCKED` rather than silently substituting another DSH model/provider.

### Skill location

DSH can discover project skills from:

```text
.agents/skills/contract-build-prove/
```

No DSH-specific metadata file is required by the portable core. Provider/model routing remains in DSH's own configuration rather than being duplicated inside this skill.

## Generic subagent-capable harness

Map capabilities by role:

| CBP role | Runtime requirement |
|---|---|
| Coordinator | persistent primary context with repository access |
| Builder | fresh/scoped child agent capable of implementation and local tests |
| Verifier | fresh child context that did not implement the candidate and can inspect/test it |

Prefer GPT-5.6 Luna for verifier when exposed by the harness. Builder selection remains coordinator-controlled unless runtime policy defines a dedicated execution role.
