# Runtime adapters

Contract-Build-Prove defines **roles and invariants**, not vendor-specific orchestration APIs. Map the same coordinator/builder/verifier architecture to the capabilities exposed by the active harness.

## Required capability model

For full Standard/High-Assurance operation, the runtime should provide:

1. a primary coordinator context;
2. a way to launch fresh child agents/contexts for bounded implementation;
3. a way to launch a fresh child agent/context that did not implement the candidate for independent verification;
4. repository/file execution access sufficient to inspect and test the candidate.

If #2 is unavailable, the coordinator may implement locally but should record the missing delegation capability.

If #3 is unavailable and there is no equivalent independent repository gate, independent acceptance is unavailable; Standard/High-Assurance completion cannot be reported as fully `DONE` under this method.

## OpenAI Codex

### Coordinator
The current Codex agent/thread running this skill.

### Builders
Prefer a fresh built-in `worker` or a suitable project-specific custom agent for each meaningful self-contained work packet.

Use `explorer` for read-heavy discovery when helpful, not as the default implementation or acceptance authority.

### Verifier
Selection preference:

1. configured custom `auditor`;
2. configured custom `reviewer`;
3. fresh built-in `default` subagent using `AUDITOR_HANDOFF.md`.

Never reuse a builder as verifier for the candidate it implemented.

Custom Codex agents are repository- or user-scoped configuration, not part of the portable skill contract. `references/auditor.example.toml` is optional.

### Skill location

Repository installation:

```text
.agents/skills/contract-build-prove/
```

`agents/openai.yaml` supplies Codex-specific UI/invocation metadata but is not required by the portable core workflow.

## DeepSeek Harness (DSH)

### Coordinator
The current DSH agent/session running the skill. It owns the ExecPlan, contract, decomposition, integration, candidate freeze, and final state.

### Builders
Use DSH's `subagent` capability to delegate self-contained work packets. Each prompt must be standalone because a child agent does not inherit this conversation's context.

DSH can expose different subagent providers depending on configuration. The CBP workflow does not require a specific provider: in-process/forked DSH agents or external Codex/Claude-style providers can all fill the builder role if they can inspect/edit/test the relevant repository scope.

### Verifier
Launch a **new** subagent invocation/context that did not build the candidate. Give it the generic `AUDITOR_HANDOFF.md` contract and the exact candidate identity.

Do not continue the builder's child session and rename it a verifier. Fresh context is the minimum independence boundary.

For High Assurance, if multiple models/providers are already available at reasonable cost, using a different provider/model for final verification can reduce correlated reasoning errors. This is optional; freshness, non-participation in the build, and direct evidence are the required properties.

### Skill location

DSH's local skill system can discover project skills from `.agents/skills`, so the shared repository location is:

```text
.agents/skills/contract-build-prove/
```

No DSH-specific metadata file is required by this skill. DSH is a developer preview, so avoid coupling the workflow to transient plugin/provider configuration names beyond the documented subagent/skill capability.

### Modes without subagents

If the active DSH preset/mode does not expose the subagent capability, the coordinator may still use the contract/plan/local-proof parts. It must not simulate independent verification. Treat Standard/High-Assurance independent proof as unavailable unless an equivalent independent CI/review gate exists.

## Generic agent harness

Map capabilities by role rather than names:

| CBP role | Runtime requirement |
|---|---|
| Coordinator | persistent primary context with repository access |
| Builder | fresh/scoped child agent capable of implementation and local tests |
| Verifier | fresh child context that did not implement the candidate and can inspect/test it |
| External gate | optional CI/runtime/reviewer evidence independent of the builder |

The same agent model may be used for builder and verifier if they run in genuinely separate contexts and the verifier receives no builder confidence/desired verdict. Different models/providers improve diversity but are not required.
