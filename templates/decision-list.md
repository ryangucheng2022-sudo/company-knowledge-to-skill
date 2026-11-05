# Batch decision list — template

Compile all open conflicts into ONE list and decide them in a single round. Do not drip-ask item by item.

## Summary table

| ID | Topic | Versions in conflict | Impact if undecided | Recommendation |
|---|---|---|---|---|
| D-01 |  |  |  |  |

## Per-item detail

### D-01 — <topic>

- **Version A** (source, date): <claim>
- **Version B** (source, date): <claim>
- **Evidence:** <what supports each side>
- **Options:** 1) adopt A  2) adopt B  3) split by scope/period  4) defer — keep both labeled pending
- **Recommendation:** <option + one-line reason>
- **Decision:** <filled in during the round: option, decider, date>

## Write-back checklist (after the round)

- [ ] Each affected record updated: status, `status_basis` = decision ID + date
- [ ] Superseded versions demoted to `deprecated` with `superseded_by` link (never deleted)
- [ ] Ledger entries below moved to "decided", then "closed" once write-back is verified

---

# Persistent unresolved-items ledger — template

One ledger across runs, not one per merge. States: `open` → `decided` (write-back pending) → `closed`.

| ID | Topic | Raised (date, run) | State | Decision ref | Closed (date) |
|---|---|---|---|---|---|
| U-001 |  |  | open |  |  |
