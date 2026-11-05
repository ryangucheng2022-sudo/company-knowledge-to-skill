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

## Baseline designation and the silent-override ban

Before merging, designate one source as the **baseline** (normally the most recent formally confirmed material). All other sources are candidates against it. A claim in a non-baseline source must never silently replace a baseline claim — and no record may present itself as "the latest confirmed version" unless a decision record (who decided, when, on what evidence) backs that claim. Version claims without a decision record are treated as `pending_review`. Silent override is the single most damaging merge failure: the output looks complete while an approved position has been replaced by an unapproved one.

## Anti-inflation re-rating

A source's self-assigned status or confidence is a claim, not a fact. During reconciliation, re-rate every record against evidence, and record the basis in `status_basis`. Apply caps: content originating from discussion, proposal, or brainstorming material is capped at `repeated`/`proposed` no matter how the source labeled it, until independent formal evidence supports `confirmed`. A register in which every record still carries a placeholder status (e.g. all `unknown`, all unrated) has not been reconciled — do not proceed to generation.

## Batch decision and write-back protocol

Do not drip-feed conflicts to the decision-maker one at a time. Compile them into a single numbered **decision list** (template: `templates/decision-list.md`): for each item give the competing versions with provenance, the impact of leaving it undecided, the options, and a recommendation. After the decision round:

1. Write the decision back into each affected record: new status, `status_basis` citing the decision ID and date.
2. Demote superseded versions to `deprecated` and link them with `superseded_by`; never delete them. The trace is what prevents the old version from resurfacing as "confirmed" in a later merge.
3. Close the corresponding entries in the persistent unresolved-items ledger (states: open → decided → closed), keeping the decision reference.
