# Contract-Build-Prove

A lean multi-agent skill for substantial repository work where “code changed” is not enough evidence that the task is complete.

Designed for **OpenAI Codex, DeepSeek Harness (DSH), and compatible subagent-capable harnesses**.

**Protocol v5**

**Preflight → Contract → Build → Candidate → Prove**

Design goal:

> **Minimum process that makes false completion difficult.**

## Default shape

- one coordinator;
- one coherent end-to-end builder when practical;
- at most one writer total in a shared workspace;
- one clean-context final verifier;
- additional sequential builders only when they improve reliability;
- parallel writers only behind isolation + explicit integration.

Small local edits should use the harness's normal workflow instead.

## Key properties

- trusted runtime profiles avoid rediscovering stable harness semantics every run;
- verifier = new child **and** no inherited implementation conversation;
- required/protected behavior freezes before implementation;
- builder cannot self-accept;
- contract coverage is checked before final acceptance;
- **attested artifact == tested artifact**;
- commit candidate → clean isolated verifier worktree/snapshot by default;
- unrelated user/newer work cannot become an implicit candidate dependency;
- uncommitted fallback uses deterministic `scripts/candidate_id.py`;
- helper fails closed on unsafe/ambiguous Git states;
- builder/coordinator/verifier have separate test ownership;
- candidate-authored tests are not trusted until the verifier confirms they test the frozen behavior;
- remediation batches understood findings;
- loop control is based on lack of progress, not raw FAIL count;
- stateful failures enter recovery before generic remediation;
- final identity check closes the post-verifier race;
- push/merge/deploy/publish/production/destructive/paid/irreversible actions require authorization.

## Runtime policy

### DSH

Intended trusted profile:

- builder route → configured execution agent (currently MiniMax in the intended setup);
- verifier route → separately configured **GPT-5.6 Luna**;
- verifier context → clean/no parent-conversation inheritance.

If this profile has already been validated, each run checks availability rather than re-deriving DSH semantics.

### Codex

- builders are chosen for coding fit/complexity, with GPT-5.6 Luna preferred when suitable;
- final verifier prefers Luna; a suitable clean-context independent fallback is allowed when Luna is unavailable and recorded.

Model selection is runtime policy; CBP's core invariant is independent exact-artifact verification.

## Candidate identity

Normal path:

```text
exact local commit SHA
→ clean isolated verifier worktree/snapshot @ that SHA
→ attest → test → re-attest
```

Uncommitted fallback:

```text
python3 <skill-root>/scripts/candidate_id.py create --exclude .cbp/PLAN.md
python3 <skill-root>/scripts/candidate_id.py verify <expected-cbp2-id> --exclude .cbp/PLAN.md
```

Exit `3` means the helper found a worktree state it cannot identify exactly. Use a commit/isolated artifact or block instead of inventing another fingerprint.

Regression tests for the helper live in `tests/test_candidate_id.py`.

## Workspace modes

- `SHARED_WORKSPACE` — at most one writer total, including coordinator and descendants.
- `ISOLATED_ARTIFACT` — builder returns exact commit/patch/artifact for coordinator integration.

Prefer isolation when user/process edits may occur concurrently.

## Rigor

- **Standard** — normal five-stage flow.
- **High Assurance** — only for security/auth, financial/trading logic, destructive/stateful migration, sensitive production data, safety-critical behavior, or unusually costly failure. Add only risk-specific controls.

## Files

- `SKILL.md` — normative workflow.
- `agents/openai.yaml` — Codex metadata; explicit invocation.
- `assets/EXEC_PLAN_TEMPLATE.md` — lean durable state.
- `scripts/candidate_id.py` — exact uncommitted candidate helper.
- `tests/test_candidate_id.py` — helper regression tests.
- `references/RUNTIMES.md` — trusted/ad-hoc runtime profiles.
- `references/PLANS.md` — state, candidate, resume/version rules.
- `references/BUILDER_HANDOFF.md` — builder packet.
- `references/VERIFIER_HANDOFF.md` — coverage + exact-artifact acceptance.
- `references/STATEFUL.md` — external-state recovery.
- `references/EXAMPLE.md` — minimal end-to-end example.
- `references/verifier.example.toml` — optional Codex verifier.

## Install

```text
.agents/skills/contract-build-prove/
```

Codex invocation:

```text
$contract-build-prove
```

Implicit invocation is intentionally disabled because CBP always launches subagents and should be selected for substantial work.
