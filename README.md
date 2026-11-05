# Company Knowledge to Skill

English | [简体中文](README.zh-CN.md)

A generic, reusable Skill for collecting organization-specific knowledge from multiple AI or human inputs, reconciling differences, applying privacy controls, generating a downstream Skill, and testing the result.

## Included

- `SKILL.md` — entrypoint and stage routing
- `references/collection-prompts.md` — independent collector prompts and checkpoints
- `references/knowledge-schema.yaml` — canonical record schema
- `references/reconciliation-and-conflicts.md` — deduplication and conflict rules
- `references/privacy-and-redaction.md` — sensitivity levels and export handling
- `references/evaluation-cases.yaml` — evaluation fixtures and expected safeguards
- `references/evaluation-protocol.md` — behavior evaluation with an independent executor
- `references/field-failure-patterns.md` — failure modes from a real deployment, with detection checks
- `templates/decision-list.md` — batch decision list and persistent unresolved-items ledger
- `templates/` — source inventory and knowledge-package outline
- `scripts/validate_knowledge.py` — JSON/JSONL structural validator
- `agents/openai.yaml` — UI metadata

## Quick start

1. Copy `templates/source-inventory.yaml` and define scope, audience, sources, and sensitivity.
2. Run independent collectors using the shared contract in `references/collection-prompts.md`.
3. Normalize outputs into the schema in `references/knowledge-schema.yaml`.
4. Deduplicate and record conflicts. Use a human checkpoint for approval state, timing, authority, or restricted data.
5. Generate the target knowledge package or downstream Skill with company facts separated from generic method instructions.
6. Validate JSON/JSONL records with `scripts/validate_knowledge.py` and execute all cases in `references/evaluation-cases.yaml`.

The package contains placeholders only. Replace them with authorized, source-backed content for a specific organization.

## Worked example

`examples/meridian-office-furniture/` runs the full pipeline on a fictional
company: two collector outputs, normalized records (`records.jsonl` /
`records.yaml`), and a conflict log. It deliberately includes a multi-AI
conflict, a privacy leak, an overstated claim, a synonym pair, a rule that
changed over time, and a missing owner — one for each evaluation case.

## Verification (run 2026-11-05)

Validator against the worked example (9 records):

```text
$ python3 scripts/validate_knowledge.py examples/meridian-office-furniture/records.jsonl --export generic
records=9  errors=0  warnings=1   (record 5: confidential — abstract/redact/exclude before generic export)
$ python3 scripts/validate_knowledge.py examples/meridian-office-furniture/records.jsonl --export internal
records=9  errors=0  warnings=0
$ python3 scripts/validate_knowledge.py examples/meridian-office-furniture/records.yaml --export generic
records=9  errors=0  warnings=1   (identical to JSONL — YAML input supported, requires PyYAML)
```

Negative test (a file with a missing `provenance`, a duplicate `record_id`,
and a `proposed` record claiming `high` confidence) correctly fails:
`errors=3, warnings=1`, exit code 1.

## What is new in v1.1.0

Hardened with patterns from a real deployment (anonymized in
`references/field-failure-patterns.md`):

- baseline designation and a ban on silent overrides; superseded versions are
  demoted and kept, never deleted
- anti-inflation re-rating: a source's self-rating is a claim; `status_basis`
  records why each rating was assigned; discussion content is capped
- batch decision lists with a write-back protocol, and a persistent
  unresolved-items ledger (open → decided → closed)
- sensitivity-marker preservation across extraction, plus a pre-export value
  scan as a release gate
- a register hygiene gate before generation (100% re-rated, no meta-records,
  no placeholder claims), enforced by new validator checks: duplicate-claim
  report, empty/meta-record detection, uniformity heuristic, `--scan-values`
- correction-case pairs as first-class records; packages ship a known-gaps
  section; evaluation runs an independent-executor protocol

Validator on the worked example now also reports `rated_coverage=9/9`
(default outputs otherwise unchanged: generic `errors=0, warnings=1`;
internal `errors=0, warnings=0`). A synthetic dirty register (placeholder
claim, duplicate claim, meta-record, all-uniform statuses, an unmarked
figure in an exportable record) fails with `errors=1, warnings=7`, exit 1.

All seven cases in `references/evaluation-cases.yaml` are exercised by the
worked example; the mapping is documented in the example's README.
