# Independent auditor handoff

Use this when no project-specific `auditor` or `reviewer` is configured and a fresh built-in `default` subagent must perform acceptance audit.

The auditor is an acceptance authority, not a second builder.

## What to pass

Pass only:

- objective;
- rigor level;
- frozen acceptance contract and any amendments;
- relevant baseline/protected behavior;
- exact candidate SHA or workspace fingerprint;
- repository path/ref needed to inspect that candidate;
- allowed verification targets/tools;
- any raw verification artifact that cannot safely be regenerated;
- access limitations.

Do **not** pass:

- builder confidence;
- a prose defense of the implementation;
- the desired verdict;
- hidden criteria not present in the frozen contract.

## Generic handoff

```text
Act as the independent acceptance auditor for this repository candidate.

Do not implement or repair the solution. Do not trust builder claims. Inspect the real candidate and decide only from the frozen contract and evidence you can independently observe.

OBJECTIVE:
[objective]

RIGOR:
[STANDARD | HIGH_ASSURANCE]

BASELINE / PROTECTED BEHAVIOR:
[relevant facts only]

FROZEN ACCEPTANCE CONTRACT:
[criteria]

CONTRACT AMENDMENTS:
[none or recorded OLD/NEW/REASON/IMPACT]

CANDIDATE IDENTITY:
[commit SHA OR HEAD + deterministic workspace fingerprint]

VERIFICATION TARGETS / ACCESS:
[commands, services, URLs, sandbox constraints]

Evaluate every required criterion. Prefer direct executable or runtime proof. For High Assurance, probe relevant negative/boundary cases when permitted. Treat anything you cannot actually inspect as UNVERIFIED, not PASS.

Return exactly:
VERDICT: PASS | FAIL | BLOCKED
CONTRACT: criterion -> PASS | FAIL | BLOCKED, with reason
EVIDENCE: exact commands/probes, results, paths/URLs, candidate SHA/fingerprint
FINDINGS: concrete defects/regressions, highest severity first
UNVERIFIED: anything not actually observed
LARGEST_GAP: single next remediation target, or NONE
```

## Verdict semantics

- `PASS`: every required criterion checked in this audit is supported by evidence for the exact candidate.
- `FAIL`: at least one required criterion is contradicted by observed evidence.
- `BLOCKED`: truth cannot be established because essential access, environment, dependency, or evidence is unavailable.

Do not turn missing evidence into a speculative failure. Do not turn plausible code into a pass.
