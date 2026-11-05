# Changelog

## 1.2.0 — 2026-11-05
- Continuous correction loop: new Maintain mode, `references/correction-loop.md`, and a correction-log template; corrected errors are promoted to regression cases.
- READMEs: full value narrative (problems addressed, scenarios, value levels, how this differs from knowledge bases / RAG / Agents).

## 1.1.0 — 2026-11-05
- Field-hardened pipeline from a real deployment: baseline designation and silent-override ban, anti-inflation re-rating with `status_basis`, batch decision lists with write-back protocol, persistent unresolved-items ledger.
- Privacy: sensitivity-marker preservation across extraction; pre-export value scan as a release gate; uniformity heuristic.
- Register hygiene gate before generation; validator adds duplicate-claim report, empty/meta-record detection, uniformity checks, `--scan-values`, and a rated-coverage report.
- New: `references/field-failure-patterns.md`, `references/evaluation-protocol.md`, `templates/decision-list.md`; correction-case pairs as first-class records.
- Chinese README (`README.zh-CN.md`) with a language switch in the English README.

## 1.0.0 — 2026-11-05
- Initial release: seven operating modes (Collect / Normalize / Reconcile / Specify / Generate / Evaluate / Full pipeline), canonical record schema, reconciliation and privacy references, evaluation cases, and a worked example on a fictional company.
- Validator supports JSON, JSONL, and YAML inputs.
