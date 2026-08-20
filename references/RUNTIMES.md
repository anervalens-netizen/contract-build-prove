# Runtime adapters

Read the **common preflight** plus only the active harness section. `SKILL.md` is normative.

## Common preflight

Record:

```text
RUNTIME_PROFILE=<trusted profile id | AD_HOC>
HARNESS=<Codex | DSH | other>
BUILDER_ROUTE=<actual route>
BUILDER_MODEL=<resolved model if observable>
VERIFIER_ROUTE=<actual route>
VERIFIER_POLICY=<runtime policy>
VERIFIER_MODEL=<resolved model if observable>
VERIFIER_NEW_CHILD=<YES|NO>
VERIFIER_INHERITS_PARENT_CONTEXT=<must be NO>
WORKSPACE_MODE=<SHARED_WORKSPACE|ISOLATED_ARTIFACT>
PLAN_VISIBLE_NEXT_SESSION=<YES|NO>
RESULT=<READY|BLOCKED>
```

### Trusted runtime profile

A trusted profile is harness/environment configuration whose semantics were validated previously. It must already define:

- builder route/model policy;
- verifier route/model policy;
- verifier parent-context inheritance (`NO`);
- artifact/workspace mode.

If a trusted profile is available, each CBP run checks only that the profile and required routes are currently available/resolving as expected. **Do not rediscover stable harness semantics every run.**

If no trusted profile exists, use `AD_HOC`, establish the fields above once, and record them in the plan. A prompt or role name is not proof of model routing, context isolation, or artifact transport.

## Workspace semantics

### SHARED_WORKSPACE
- At most one writer total, including coordinator and every descendant agent.
- Builder descendants that write must be isolated, not shared.
- Coordinator inspects actual diff/status after each writer packet.
- Unexpected overlapping user/process drift must be reconciled before continuing.
- No writer remains active at candidate freeze.

### ISOLATED_ARTIFACT
- Builder returns exact commit/patch/deterministic artifact.
- Coordinator explicitly integrates and inspects it.
- Only the integrated result becomes candidate.
- Parallel writers are allowed only with isolation + controlled integration.

## OpenAI Codex

**Builder:** choose for coding fit/complexity; GPT-5.6 Luna is preferred when suitable. Use `explorer` for discovery only.

**Verifier:** prefer GPT-5.6 Luna. Fallback may use the strongest suitable independent verifier when Luna is unavailable and the deviation is recorded.

Final verifier requirements are model-independent:
- new child;
- no inherited parent implementation conversation;
- exact candidate access;
- ability to inspect/prove the contract.

Optional custom agents live in `.codex/agents/` or `~/.codex/agents/`.

Skill location:

```text
.agents/skills/contract-build-prove/
```

## DeepSeek Harness (DSH)

DSH provider/model/context behavior is configuration-driven. The intended deployment profile is:

- builder route → configured execution agent (currently MiniMax in the intended setup);
- verifier route → separately configured GPT-5.6 Luna;
- verifier context → clean/no parent conversation inheritance.

Concrete route names are harness-owned (`cbp_builder` / `cbp_verifier` are examples only).

A fork-style verifier that inherits coordinator/build history is invalid for final acceptance. Use a clean spawn/ACP/provider route or block.

If a trusted DSH profile has already validated these semantics, preflight checks route/profile availability only. If not, `AD_HOC` preflight must establish them before build.

If the only visible verifier-capable route resolves to the builder model when policy requires Luna, do not relabel it; configure/use the required route or `BLOCKED`.

Skill location:

```text
.agents/skills/contract-build-prove/
```

## Generic harness

Full CBP requires:
- coordinator;
- write-capable builder;
- new parent-context-free verifier;
- known artifact mode;
- persistent/visible control state for expected resume;
- enough repository/runtime access to attest and test the candidate.

Missing required capability → `BLOCKED`, never silent single-agent degradation.
