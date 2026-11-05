# Evaluation protocol

Static fixtures (evaluation-cases.yaml) verify that safeguards *exist*. This protocol verifies that a generated package *behaves* correctly when used.

## Independent-executor protocol

1. Give the evaluation cases to an executor (a fresh AI session or a human) who may read **only the generated package** — not the source collections, not the register, not this Skill.
2. Every answer must cite the package file and record it relied on. If the package has no basis for an answer, the executor must say so explicitly ("no basis in package") and stop there — filling gaps from outside knowledge is a test failure, because it hides exactly the gaps the test exists to find.
3. Score each case: **sufficient** (correct behavior, fully backed), **partial** (correct behavior, but a gap forced a stop or a caveat), **missing** (no basis in package). Any fabricated rule, silently resolved conflict, or leaked restricted value is a **veto failure** regardless of other scores.
4. Record gaps as first-class output. The generated package ships with a **known-gaps section** listing what it does not cover (missing topics, undecided conflicts, procedures awaiting formal documents). A package that claims completeness it does not have fails evaluation even if every answer was right.

## What to re-run when

- After any register change that touches a case's topic: re-run that case.
- After a decision round (write-back): re-run all conflict and version cases.
- Before any export to a wider audience: re-run the privacy cases plus the pre-export value scan.
- After each correction write-back batch: re-run the cases promoted from corrected errors (see correction-loop.md).
