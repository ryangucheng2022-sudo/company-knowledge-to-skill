# Deduplication and conflict handling

## Identity and merge key

Candidate duplicates share the same normalized domain, scope, effective period, and semantic claim. Compare aliases and original wording after Unicode normalization, whitespace cleanup, and unit normalization. Do not merge solely because titles look similar.

## Merge decisions

- `merge_exact` — same meaning and compatible provenance. Keep all source IDs.
- `merge_alias` — one record is an alias or wording variant. Preserve both terms.
- `keep_separate` — scope, period, owner, or exception differs.
- `conflict` — claims cannot both be true under the same scope and period.
- `pending_review` — evidence is insufficient to decide.

The canonical record keeps the most precise wording and appends provenance from every merged record. Never discard a lower-confidence source without recording the merge decision.

## Conflict taxonomy

- **Scope conflict** — different business units or audiences.
- **Temporal conflict** — rules changed over time.
- **Authority conflict** — formal document versus informal statement.
- **Definition conflict** — same term used with different meanings.
- **Evidence conflict** — sources cite incompatible facts.
- **Status conflict** — proposal or discussion presented as approved.

## Resolution order

1. Split by scope or effective period when evidence supports it.
2. Prefer an explicit approved source over an informal summary for the same period.
3. If authority or timing is unclear, retain a conflict group and route to human review.
4. Export only the agreed record, or export both records with visible status labels when the audience is authorized to see the dispute.

## Review queue fields

`conflict_group`, `record_ids`, `conflict_type`, `question_for_reviewer`, `evidence`, `proposed_resolution`, `reviewer`, `reviewed_at`, `decision`.
