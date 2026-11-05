# Field failure patterns (from a real deployment, anonymized)

Failure modes observed when this pipeline was run on a real company's knowledge base (three source collections, 400+ candidate records). Each pattern includes how to detect it. Treat this file as a pre-flight checklist for the Reconcile and Generate stages.

## 1. Silent override

A non-baseline source's version is recorded as "the latest confirmed version" and the approved baseline version disappears from the register entirely — not even kept as a conflict. The merge *looks* decisive and clean.
**Detect:** for every high-stakes topic, verify the baseline source's version is present in the register (as canonical or as a conflict side). Absence of the baseline version is the tell.

## 2. Grade inflation

Discussion-stage content arrives self-labeled "confirmed" and keeps that label through the merge. Systematically, everything one source produced is one grade too high.
**Detect:** sample records by source; if one source's `confirmed` share is far above others, re-rate that source wholesale with the anti-inflation caps and require `status_basis` evidence for every `confirmed`.

## 3. Boilerplate flags

Every record carries a conflict flag — the *same sentence* on all of them ("check if multi-source or version-sensitive"). Flags exist, so dashboards look green, but no record-specific conflict work was done.
**Detect:** group flag/notes text; if one value covers >50% of records, the flags are decorative. The validator's uniformity check reports this.

## 4. Unrated register shipped as merged

The "merged" register has 100% of records at a placeholder status (candidate/unrated/review). Concatenation was mistaken for reconciliation.
**Detect:** rating coverage report. Coverage of real (non-placeholder) statuses must be 100% before Generate.

## 5. Meta-record pollution

The rating scale's own definitions ("A = confirmed: has a formal document…") were extracted as knowledge records and sit in the register next to real terms.
**Detect:** scan for records whose claim defines the schema, the levels, or the process itself rather than company knowledge. Remove and log them.

## 6. Marker loss in extraction

A source line carried an inline marker ("internal figures — internal version only"); the extraction kept the figures and dropped the marker, so a self-described redacted package still contained internal values.
**Detect:** the pre-export value scan (see privacy-and-redaction.md). Also spot-check extracted records against source lines for dropped qualifiers.

## 7. Garbled keys, real content

Source tables with numbered rows produced records whose key/title is a bare number ("4"), while the definition contains a real, sometimes high-stakes item (e.g. an unresolved conflict). Deleting "junk" rows by key alone would have destroyed it.
**Detect:** before dropping malformed records, scan their content; rescue by deriving the key from the first content segment, and log the rescue.

## 8. Same term, contradictory guidance

The register simultaneously contains a term as valid usage and a correction case banning the same term (both unrated, both plausible). A downstream Skill loaded with both will contradict itself depending on which record it reads.
**Detect:** cross-check every correction-case target against the terminology records for the same term; unresolved pairs must be linked by a conflict group and decided in the batch decision round.

## 9. Package edited instead of regenerated

A generated package copy is patched by hand while the register stays unchanged; the next regeneration silently reverts the fix — or worse, two copies drift apart and nobody knows which is canonical.
**Detect/prevent:** packages are build artifacts. Fixes go into the register, then regenerate. State this rule in the generated package itself.
