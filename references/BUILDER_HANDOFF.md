# Builder handoff

Prefer one **coherent end-to-end builder packet** when one child can reliably own the change. Do not split merely because work spans files or layers. Use another sequential builder only when remaining scope is materially different or too broad for one reliable handoff.

`SKILL.md` is normative.

```text
You are an implementation builder for one Contract-Build-Prove work packet.

OBJECTIVE:
[coherent outcome OR coherent verifier findings]

RELEVANT ACCEPTANCE CRITERIA:
[IDs + required behavior]

OWNED OUTCOME / LIKELY AREA:
[what you own; likely components/symbols]

EXCLUSIONS / PROTECTED BEHAVIOR:
[what must not change]

BASELINE:
[relevant HEAD/state/protected pre-existing work]

WORKSPACE MODE:
[SHARED_WORKSPACE | ISOLATED_ARTIFACT]

ARTIFACT RETURN:
[shared workspace diff/status OR exact commit/patch]

EXPECTED FOCUSED CHECKS:
[development tests/probes]

SIDE-EFFECT LIMITS:
[no push/merge/deploy/publish/prod/destructive/paid/irreversible action unless authorized]

Implement the smallest coherent change. For debugging, follow evidence even if the likely area changes; report material scope expansion instead of silently taking unrelated work.

If remediation, address all concrete understood verifier findings that safely belong in this coherent pass.

Do not declare acceptance criteria PASS.

Return:
ARTIFACT: exact commit/patch or SHARED_WORKSPACE
CHANGES: concise summary + paths
CHECKS: exact focused commands/probes + results
DRIFT: NONE or unexpected overlapping change observed
BLOCKERS: NONE or concrete blocker
RISKS: NONE or remaining uncertainty
```

## Rules

- `SHARED_WORKSPACE`: this builder is the only writer. Do **not** spawn additional write-capable shared-workspace subagents; nested agents must be read-only or isolated.
- Report unexpected overlapping user/process drift immediately; do not overwrite or silently absorb it.
- `ISOLATED_ARTIFACT`: exact integratable artifact is mandatory. A prose summary is not integration.
- Strict file ownership is only for isolated parallel work where collision control requires it.
- Adjacent defects are reported unless necessary for the frozen contract/coherent remediation.
- Builder checks are focused development evidence, not independent acceptance. Coordinator should not routinely rerun them.
