# Runtime adapters

Contract-Build-Prove uses the same roles everywhere:

**Coordinator → builder → integrated candidate → fresh verifier**

The runtime adapter must make those roles operational before implementation starts.

## Mandatory preflight

Record:

```text
HARNESS=<Codex | DSH | other>
BUILDER_ROUTE=<actual tool/role/preset>
BUILDER_MODEL=<resolved model if observable>
VERIFIER_ROUTE=<actual tool/role/preset>
VERIFIER_MODEL=<resolved model if observable>
FRESH_CONTEXT_SUPPORTED=<YES|NO>
WORKSPACE_MODE=<SHARED_WORKSPACE|ISOLATED_ARTIFACT>
RESULT=<READY|BLOCKED>
```

A prompt saying "use model X" is not proof that the runtime routed model X. Confirm routing from harness-exposed configuration/metadata or another reliable runtime signal. If a required verifier model cannot be confirmed, block before implementation rather than discovering the problem at the end.

## Workspace/artifact semantics

Never assume child edits automatically appear in the coordinator workspace.

### SHARED_WORKSPACE

The child writes the same workspace the coordinator can inspect.

Rules:
- one active write-capable builder at a time;
- coordinator inspects actual diff/status after return;
- verifier attests the final integrated candidate, not the builder session.

### ISOLATED_ARTIFACT

The child works in an isolated branch/worktree/process/workspace.

Rules:
- builder must return an exact commit, patch, or other deterministic artifact;
- coordinator explicitly integrates it;
- coordinator inspects the resulting integrated diff;
- only the integrated result may become the candidate.

Parallel writers are allowed only when isolation/integration makes collisions controllable.

## OpenAI Codex

### Coordinator
The current Codex agent/thread running the skill.

### Builder
Standard CBP normally starts with one builder. Choose according to task complexity/specialization.

Preference:
1. GPT-5.6 Luna when available and suitable;
2. another strong coding-capable subagent when there is a concrete reason;
3. a repository-specific custom builder when configured.

Use `explorer` for read-only discovery. Explorer work does not replace the mandatory implementation builder.

### Verifier
Prefer GPT-5.6 Luna.

Selection:
1. fresh configured `verifier` on Luna;
2. fresh configured `reviewer` on Luna;
3. fresh general-purpose/default child on Luna using `VERIFIER_HANDOFF.md`;
4. if Luna is unavailable, strongest available fresh independent verifier, with the deviation recorded.

Every retry after remediation uses a **new verifier child**.

### Candidate access

Before building, determine whether the chosen child role edits the shared workspace or returns isolated work. Do not infer this from the role name.

### Skill location

```text
.agents/skills/contract-build-prove/
```

Optional custom agents live in `.codex/agents/` or `~/.codex/agents/`.

## DeepSeek Harness (DSH)

DSH can expose multiple subagent providers/tool instances. Model/provider selection is configuration-driven; the parent prompt alone should not be treated as routing control.

### Intended routing

- **Builder:** use the configured execution route; in the intended setup this resolves to MiniMax. CBP does not hardcode the MiniMax version.
- **Verifier:** use a separately configured route resolving to **GPT-5.6 Luna**.

The two routes should be distinguishable before implementation. Example model-facing names are:

```text
cbp_builder
cbp_verifier
```

Those names are examples only; existing DSH names/presets are valid if the coordinator can identify them reliably.

### DSH preflight

Before contract freeze/build, confirm:

1. the actual execution-subagent tool/preset/provider route;
2. the actual verifier tool/preset/provider route;
3. verifier resolves to `gpt-5.6-luna` in the intended setup;
4. each verifier invocation creates a fresh child context;
5. workspace semantics for each route (`SHARED_WORKSPACE` vs `ISOLATED_ARTIFACT`).

If the only visible generic subagent route resolves to the builder model, **do not call it a Luna verifier**. Configure/use a distinct verifier route or report CBP `BLOCKED` before implementation.

DSH child providers may run in a separate process while still receiving the parent's cwd, or may use other configured cwd/session behavior. Therefore process separation does not by itself prove workspace isolation; record the effective artifact mode explicitly.

### Skill location

```text
.agents/skills/contract-build-prove/
```

Provider/model configuration remains harness-owned. CBP only requires that the resolved role can be attested.

## Generic harness

Full CBP requires:

- a coordinator;
- a write-capable builder child;
- a separate fresh verifier child;
- a known artifact-transport mode;
- enough repository/runtime access to attest and test the final candidate.

If any required capability cannot be established at preflight, report `BLOCKED` rather than collapsing silently into single-agent execution.
