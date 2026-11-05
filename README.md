# Company Knowledge to Skill

A generic, reusable Skill for collecting organization-specific knowledge from multiple AI or human inputs, reconciling differences, applying privacy controls, generating a downstream Skill, and testing the result.

## Included

- `SKILL.md` — entrypoint and stage routing
- `references/collection-prompts.md` — independent collector prompts and checkpoints
- `references/knowledge-schema.yaml` — canonical record schema
- `references/reconciliation-and-conflicts.md` — deduplication and conflict rules
- `references/privacy-and-redaction.md` — sensitivity levels and export handling
- `references/evaluation-cases.yaml` — evaluation fixtures and expected safeguards
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

All seven cases in `references/evaluation-cases.yaml` are exercised by the
worked example; the mapping is documented in the example's README.
