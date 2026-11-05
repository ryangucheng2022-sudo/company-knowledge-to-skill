# Worked example — Meridian Office Furniture (FICTIONAL)

Meridian Office Furniture does not exist. This example walks the full pipeline
on invented data so you can see exactly what each stage produces — including
the uncomfortable parts (a conflict, a privacy leak, an overstated claim).

## Pipeline walk-through

| Stage | Input | Output in this folder |
|---|---|---|
| Collect | Two independent collectors, same prompt contract | `source-inventory.yaml`, `collectors/collector-a.md`, `collectors/collector-b.md` |
| Normalize | Collector outputs | `records.jsonl` (same records as `records.yaml`) |
| Reconcile | Normalized records | `conflict-log.md` (conflict group CG-1 + review queue) |
| Validate | `records.jsonl` / `records.yaml` | `scripts/validate_knowledge.py` — see the main README's Verification section |

## How this example exercises the evaluation cases

| Evaluation case | Where it happens here |
|---|---|
| unsupported-certainty | Collector B states a four-day workweek as approved fact → record K-0004 is held at `proposed` / `low` with a review flag |
| privacy-leak | Collector B includes an employee name and an exact unreleased figure → K-0005 stores only an abstracted claim; the values are never written into the record |
| synonym-merge | "QBR" (A) and "Quarterly Ops Review" (B) describe the same meeting → merged into K-0001, both original terms kept (`aliases`) |
| temporal-drift | Free-shipping threshold USD 50 vs USD 75 → separate records K-0006 (deprecated) and K-0007 (current), split by effective period |
| multi-ai-disagreement | Weekly meeting name/weekday conflict → K-0002 + K-0003 in conflict group CG-1, with a human-review question in `conflict-log.md` |
| missing-data | POD rule's owning team is unknown → K-0009 `owner` stays `null`; nothing is estimated |
| ai-style-correction | Slogan rewritten as a measurable action → K-0008 keeps before/after and the rationale |

## What a downstream Skill would (and would not) say

From these records, a generated Meridian Skill may state the QBR definition
and the current USD 75 threshold as fact. It must present the weekly meeting
as **unresolved**, the four-day workweek as **proposed**, and it must not
contain the salesperson's name or figure at all.
