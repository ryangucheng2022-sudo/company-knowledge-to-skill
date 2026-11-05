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

## Marker preservation across transformations

Sensitivity is a property of the information, not of the file it sits in. When a record is extracted, quoted, reformatted, or summarized, its sensitivity level and any inline markers (e.g. "internal only") must travel with the content. Dropping a marker during extraction is a redaction failure even when the value itself is later caught — in field practice, values have survived into a self-described "redacted" package precisely because the marker was lost in transit.

## Pre-export value scan (release gate)

Before any export, scan the assembled output — not just the register — for residual sensitive values: percentages and exact figures tied to nonpublic metrics, personal names, customer identifiers, internal system names or addresses, and credential-shaped strings. A register can be perfectly labeled while the generated prose still leaks. The scan is a gate: findings block release until each is abstracted, redacted, or explicitly authorized. The validator supports a heuristic version of this scan (`--scan-values`); it supplements, never replaces, human review.

## Uniform-value heuristic

If a classification field carries the same value on (nearly) every record — all sensitivity `review`, all conflict flags the same sentence, all statuses a placeholder — treat that uniformity itself as a defect signal: it almost always means classification was not actually performed. Report it and re-classify before export.
