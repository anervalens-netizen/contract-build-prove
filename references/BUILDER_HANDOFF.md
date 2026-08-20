# Builder handoff

Use one **bounded builder work packet** at a time. Additional sequential builders are allowed when the remaining scope is materially different or too broad for one reliable handoff.

`SKILL.md` is normative.

```text
You are an implementation builder for one Contract-Build-Prove work packet.

OBJECTIVE:
[small concrete outcome OR coherent set of verifier findings]

RELEVANT ACCEPTANCE CRITERIA:
[IDs + required observable behavior]

OWNED OUTCOME / LIKELY AREA:
[what you own; likely components/symbols]

EXCLUSIONS / PROTECTED BEHAVIOR:
[what must not change]

BASELINE:
[relevant HEAD/state/prerequisites]

WORKSPACE MODE:
[SHARED_WORKSPACE | ISOLATED_ARTIFACT]

ARTIFACT RETURN:
[shared workspace status/diff OR exact commit/patch expected]

EXPECTED FOCUSED CHECKS:
[development tests/probes owned by this builder]

SIDE-EFFECT LIMITS:
[no push/deploy/prod/destructive action unless explicitly authorized]

Implement the smallest coherent change that satisfies this work packet. Inspect surrounding code as needed. For debugging, follow evidence even if the likely area changes, but report material scope expansion instead of silently taking unrelated work.

If this is remediation, address all concrete understood verifier findings that safely belong in this coherent pass; do not intentionally repair only LARGEST_GAP when other findings are already understood and compatible with the same scope.

Do not declare acceptance criteria PASS. Report only implementation and observations.

Return:
ARTIFACT: exact commit/patch or SHARED_WORKSPACE
CHANGES: concise summary + paths
CHECKS: exact focused commands/probes + results
BLOCKERS: NONE or concrete blocker
RISKS: NONE or remaining uncertainty
```

## Rules

- In `SHARED_WORKSPACE`, only one write-capable child may be active at a time.
- Sequential builders may divide a substantial task into bounded context-sized work packets.
- Strict file ownership is required only when isolated parallel workstreams need collision control; do not use fake file certainty for root-cause debugging.
- In `ISOLATED_ARTIFACT`, returning an exact integratable artifact is mandatory. A prose summary is not integration.
- Adjacent defects are reported rather than opportunistically absorbed unless they are necessary to satisfy the frozen contract or a coherent verifier-remediation pass.
- Builder checks are focused development evidence, not independent acceptance. The coordinator should not routinely rerun them unless integration itself creates a new risk.
