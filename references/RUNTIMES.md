# Runtime adapters

Read the **common preflight** below plus only the section for the active harness.

Contract-Build-Prove uses the same roles everywhere:

**Coordinator → builder(s) → integrated candidate → clean-context verifier**

`SKILL.md` is normative.

## Common preflight

Record:

```text
HARNESS=<Codex | DSH | other>
BUILDER_ROUTE=<actual tool/role/preset>
BUILDER_MODEL=<resolved model if observable>
VERIFIER_ROUTE=<actual tool/role/preset>
VERIFIER_POLICY=<runtime policy>
VERIFIER_MODEL=<resolved model if observable>
VERIFIER_NEW_CHILD=<YES|NO>
VERIFIER_INHERITS_PARENT_CONTEXT=<must be NO>
WORKSPACE_MODE=<SHARED_WORKSPACE|ISOLATED_ARTIFACT>
PLAN_VISIBLE_NEXT_SESSION=<YES|NO>
RESULT=<READY|BLOCKED>
```

A new child/session ID is **not** enough for independent verification. The final verifier must not inherit the coordinator/builder conversation. If that cannot be guaranteed, choose another route or report `BLOCKED` before implementation.

A prompt saying "use model X" is not proof that the runtime routed model X. Confirm routing from harness-exposed configuration/metadata or another reliable runtime signal when the active policy requires a specific model.

## Workspace/artifact semantics

### SHARED_WORKSPACE

Child writes the same workspace the coordinator can inspect.

Rules:
- one active write-capable child at a time;
- sequential builders are allowed as work packets change;
- coordinator inspects real diff/status after each writer returns;
- no write-capable shared child may remain active at candidate freeze.

### ISOLATED_ARTIFACT

Child works in an isolated branch/worktree/process/workspace.

Rules:
- builder returns an exact commit/patch/deterministic artifact;
- coordinator explicitly integrates it;
- coordinator inspects the integrated diff;
- only the integrated result may become the candidate.

Parallel writers are allowed only when isolation plus integration makes collisions controllable.

## OpenAI Codex

### Coordinator
The current Codex agent/thread running the skill.

### Builders
Start with one bounded work packet. Use additional sequential builders when the remaining scope is materially different or too broad for one reliable handoff.

Model preference for this setup:
1. GPT-5.6 Luna when available and suitable;
2. another strong coding-capable subagent when there is a concrete reason;
3. repository-specific custom builder when configured.

Use `explorer` for discovery. Explorer work does not replace the mandatory implementation builder.

### Verifier policy

Prefer GPT-5.6 Luna for final verification. A stronger/suitable fresh independent fallback is allowed if Luna is unavailable and the deviation is recorded.

Selection when supported:
1. configured `verifier` on Luna;
2. configured `reviewer` on Luna;
3. general-purpose/default child on Luna using `VERIFIER_HANDOFF.md`;
4. strongest available **clean-context** independent verifier fallback.

Whichever route is used, confirm it creates a new child that does **not** inherit the parent conversation. Every remediation attempt uses another new clean-context verifier.

### Candidate access

Before building, determine whether each builder route edits the shared workspace or returns isolated work. Do not infer this from role names.

### Skill location

```text
.agents/skills/contract-build-prove/
```

Optional custom agents live in `.codex/agents/` or `~/.codex/agents/`.

## DeepSeek Harness (DSH)

DSH may expose multiple subagent providers/tool instances. Provider/model selection and parent-context inheritance are configuration-driven; prompt text alone is not routing control.

### Intended profile

- **Builder:** configured execution route; intended setup currently resolves to MiniMax. CBP does not hardcode the MiniMax version.
- **Verifier:** separately configured route resolving to **GPT-5.6 Luna**.

The concrete route names may be anything the harness exposes reliably; `cbp_builder` and `cbp_verifier` are examples only.

### DSH preflight

Confirm before contract freeze/build:

1. actual builder route/provider/model;
2. actual verifier route/provider/model;
3. intended verifier route resolves to `gpt-5.6-luna`;
4. each verifier call creates a new child;
5. verifier **does not inherit the parent conversation**;
6. workspace/artifact mode for each route;
7. plan/control state will be visible to the next expected coordinator session.

A fork-style route that inherits implementation/coordinator history is **not valid as the final verifier**, even if it creates a new child ID. Use a non-inheriting spawn/ACP/provider route or report `BLOCKED`.

If the only visible generic subagent route resolves to MiniMax, do not label it Luna. Configure/use a distinct verifier route or block before implementation.

Process separation does not by itself prove workspace isolation or context independence; attest both properties explicitly.

### Skill location

```text
.agents/skills/contract-build-prove/
```

Provider/model configuration remains harness-owned. CBP requires only that the active profile can be identified and verified.

## Generic harness

Full CBP requires:

- coordinator;
- write-capable builder child;
- final verifier child that is both **new and parent-context-free**;
- known artifact transport mode;
- plan/control state visible to expected future coordinator sessions;
- repository/runtime access sufficient to attest and test the exact candidate.

If any required capability cannot be established at preflight, report `BLOCKED` rather than collapsing silently into single-agent execution.
