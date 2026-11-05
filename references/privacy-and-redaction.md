# Privacy classification and redaction

## Levels

- `public` — safe for external publication.
- `internal` — ordinary internal terminology or process guidance.
- `confidential` — nonpublic business, financial, customer, personnel, or product information.
- `restricted` — credentials, personal identifiers, security material, unreleased strategy, source code, or highly sensitive technical detail.

## Handling

- Keep `public` and `internal` in a broadly reusable knowledge package when the owner permits.
- Abstract `confidential` records to rules, categories, or placeholders. Remove names, exact figures, customer identifiers, and unreleased dates unless the destination is explicitly authorized.
- Never place `restricted` values in a generic Skill, README, evaluation fixture, filename, or ZIP metadata. Replace with `[REDACTED]` and retain only a review pointer.
- Preserve provenance without copying sensitive content. Use a source ID and access-controlled locator.
- Review derived text, examples, logs, and test fixtures for indirect leakage.

## Export decision

For each record, set `export_action` to `include`, `abstract`, `redact`, or `exclude`. The default for unknown sensitivity is `confidential` until reviewed.
