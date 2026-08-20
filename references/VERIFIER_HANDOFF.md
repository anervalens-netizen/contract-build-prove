# Independent verifier handoff

Use this for every final verification attempt. Each attempt gets a **new child context**.

The verifier is acceptance authority, not a repair agent.

## What to pass

Pass only:

- objective;
- frozen acceptance contract + authorized amendments;
- protected behavior/non-goals;
- exact expected candidate identity;
- declared control-state paths;
- repository/workspace/ref needed to inspect it;
- runtime/environment verification target;
- allowed tools/access and side-effect limits.

Do not pass builder confidence, a defense of the implementation, or the desired verdict.

## Mandatory procedure

### Step 0 — candidate attestation

Before any acceptance test:

1. independently resolve/recompute candidate identity using `references/PLANS.md`;
2. compare it with the coordinator-supplied identity;
3. confirm any workspace differences are limited to declared control state or allowed ignored/temp artifacts;
4. on mismatch, stop with:

```text
VERDICT: BLOCKED
LARGEST_GAP: CANDIDATE_IDENTITY_MISMATCH
```

Never copy the supplied SHA/fingerprint into evidence without independently checking it.

### Step 1 — verify the contract

Inspect the real candidate and evaluate every required criterion from direct evidence. Prefer executable tests/runtime probes. Treat missing proof as `BLOCKED`, not PASS. Do not implement or repair the candidate.

When tests need writes, use an isolated writable snapshot/worktree/sandbox if available. Test caches, build output, coverage, browser artifacts, and temporary databases may be written there. Do not intentionally modify tracked candidate source.

### Step 2 — candidate postflight

After tests, recompute/re-resolve candidate identity again.

If verified source changed during verification, return `BLOCKED: CANDIDATE_IDENTITY_MISMATCH` even if tests passed.

## Generic prompt

```text
Act as the independent acceptance verifier for this frozen Contract-Build-Prove candidate.

You did not implement it. Do not repair it. Do not trust builder claims.

OBJECTIVE:
[objective]

PROTECTED BEHAVIOR / NON-GOALS:
[relevant facts]

FROZEN ACCEPTANCE CONTRACT + AMENDMENTS:
[criteria]

EXPECTED CANDIDATE IDENTITY:
[commit SHA OR canonical uncommitted tuple]

CONTROL-STATE PATHS:
[paths or NONE]

VERIFICATION TARGET / ACCESS:
[repo/ref/commands/services/sandbox limits]

First independently attest candidate identity using the CBP plan rules. Then verify every criterion from direct evidence. Finally attest candidate identity again.

Return exactly:
VERDICT: PASS | FAIL | BLOCKED
CONTRACT: criterion -> PASS | FAIL | BLOCKED, with concise reason
EVIDENCE: exact commands/probes + results + independently attested candidate identity
FINDINGS: concrete defects/regressions, highest severity first, or NONE
LARGEST_GAP: single next remediation/unblock target, or NONE
```

## Verdict semantics

- `PASS`: every required criterion is supported by direct evidence and candidate identity matched before/after verification.
- `FAIL`: the candidate identity is valid, but observed evidence contradicts at least one criterion.
- `BLOCKED`: truth cannot safely be established because candidate identity, access, environment, dependency, or required proof is unavailable.
