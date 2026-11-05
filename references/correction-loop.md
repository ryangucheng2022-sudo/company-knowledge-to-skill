# Continuous correction loop

Collecting knowledge once is not enough: a generated package will be used, and in use it will produce wrong terms, stale rules, and unsupported claims. This loop turns those errors into register updates instead of repeated mistakes. It is the mechanism that moves a deployment from one-off extraction toward organizational learning.

## Capture (at use time, keep it cheap)

Anyone using the generated package — human or AI — logs each observed error in one line (`templates/correction-log.md`):

`date · context/task · wrong output (quoted) · expected/correct version · who noticed`

Do not debate the fix at capture time. A wrong term used in a real deliverable, a rule the package got wrong, and a question the package could not answer all count as loggable events. "No basis in package" answers during normal use are gap reports, not failures — log them too.

## Triage (periodic, not per incident)

Classify each logged item by root cause:

- **Slip** — the package was right; the output ignored it. No register change; note and close.
- **Stale source** — the world changed; the record's effective period ended. Update dates, demote the old record to `deprecated` with a `superseded_by` link.
- **Conflict** — two records disagree and use exposed it. Route to the batch decision list; do not fix ad hoc.
- **Missing rule** — the package had no record. Draft one from evidence, mark provenance, rate conservatively.
- **Wrong rule** — the record itself is incorrect. Correct it with `status_basis` citing the correction-log ID.

## Decide and write back

Corrections that touch status, definitions, or scope go through the same batch decision and write-back protocol as merge conflicts (see reconciliation-and-conflicts.md). One-off wording slips may be fixed by the knowledge owner directly, with the log ID as the basis.

## Promote to regression cases

Every corrected error becomes an evaluation case: the original wrong output is the fixture, the corrected behavior is the expectation. Re-run affected cases after each write-back batch. An error that recurs after promotion means the fix landed in the register but not in the generated package — regenerate; never hand-patch the package.

## Metrics worth keeping

- corrections logged per period, by root-cause class
- repeat-error rate (same root cause after promotion — target zero)
- median time from log to write-back

## Authorization note

Capturing errors from real work must respect the same privacy rules as collection: log the minimum excerpt needed to identify the error, never whole conversations by default, and never treat an individual's chat history as a company asset without explicit authorization.
