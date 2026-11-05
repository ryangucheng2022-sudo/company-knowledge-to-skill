---
name: company-knowledge-to-skill
description: Build a reusable, privacy-aware company knowledge package and downstream Skill from multi-AI collection inputs. Use when a user needs to collect, normalize, reconcile, validate, and test organization-specific terminology, management rules, writing conventions, or AI correction guidance.
metadata:
  short-description: Convert multi-AI company knowledge into a tested reusable Skill
---

# Company Knowledge to Skill

Use this skill to turn heterogeneous AI or human knowledge-collection outputs into a reusable company-knowledge package and, when requested, a downstream Skill. Keep company-specific facts in the user-supplied knowledge layer. The default package must remain generic and must not invent organizational facts.

## Operating modes

Select the smallest mode that satisfies the request.

- **Collect** — prepare prompts and a source inventory for one or more AI collectors.
- **Normalize** — map outputs into the canonical record schema and preserve provenance.
- **Reconcile** — deduplicate records, detect conflicts, and assign confidence and status.
- **Specify** — extract terminology, management rules, expression patterns, AI-correction rules, and confirmed phrases.
- **Generate** — produce a company-specific knowledge package or a downstream Skill from validated records.
- **Evaluate** — run the evaluation cases and report failures, unresolved conflicts, privacy leaks, or unsupported certainty.
- **Full pipeline** — run the stages in order, allowing a human checkpoint between stages.

## Required behavior

1. Start with a scope statement, source inventory, sensitivity boundary, and chosen mode. If inputs are incomplete, create an explicit pending-input list instead of filling gaps.
2. Treat each collector output as evidence. Preserve source ID, author or model, date, quoted claim, and location when available.
3. Separate facts from interpretations. Every record gets a status such as `confirmed`, `repeated`, `proposed`, `inferred`, or `unknown`, plus confidence and sensitivity.
4. Normalize synonyms without erasing the original wording. Merge only when the meaning, scope, and time period are compatible.
5. Detect conflicts before drafting prose. Keep incompatible records side by side, state the conflict, and route it to human review.
6. Never convert a proposal, historical practice, or inferred summary into an approved company rule. Do not estimate missing facts.
7. Apply privacy classification before export. Redact or abstract personal data, customer identifiers, financial details, unreleased strategy, credentials, and technical secrets unless the user explicitly supplies an authorized internal destination.
8. Generate downstream instructions that are modular and source-backed. Keep generic method guidance in the Skill and company facts in references or a separate knowledge file.
9. Run the supplied validator and evaluation cases. Report unresolved items and any assumptions in the final package README.
10. Before Generate, pass the register hygiene gate: every record re-rated with a `status_basis` (no placeholder statuses), meta-records and empty claims removed, duplicates merged or grouped, classification fields actually varied (a single uniform value across all records means classification was not performed). See references/field-failure-patterns.md.
11. Generate packages as build artifacts of the register: fix the register and regenerate, never hand-patch a generated copy. Ship a known-gaps section in every generated package, and treat sensitivity layers as separate files so an export removes files instead of editing content.

## Stage outputs

- Collect: `source-inventory` and one prompt run per collector.
- Normalize: canonical records in YAML or JSONL.
- Reconcile: deduplicated records, conflict log, and review queue.
- Specify: terminology dictionary, rules catalog, expression guide, and AI-correction guide.
- Generate: `SKILL.md`, references, templates, and README for the target company or a generic template.
- Evaluate: machine-readable results plus a short human-review summary.

## References

Read only the references needed for the current mode.

- Collection prompts and staged operating procedure: [references/collection-prompts.md](references/collection-prompts.md)
- Canonical record schema and field definitions: [references/knowledge-schema.yaml](references/knowledge-schema.yaml)
- Deduplication, conflict handling, and review states: [references/reconciliation-and-conflicts.md](references/reconciliation-and-conflicts.md)
- Privacy classification and export rules: [references/privacy-and-redaction.md](references/privacy-and-redaction.md)
- Reusable templates for source inventory and knowledge outputs: [templates/](../templates/)
- Evaluation cases and expected safeguards: [references/evaluation-cases.yaml](references/evaluation-cases.yaml)
- Behavior evaluation protocol (independent executor, citation-required): [references/evaluation-protocol.md](references/evaluation-protocol.md)
- Failure patterns observed in a real deployment, with detection checks: [references/field-failure-patterns.md](references/field-failure-patterns.md)
- Batch decision list and persistent unresolved-items ledger templates: [templates/decision-list.md](templates/decision-list.md)
- Worked example on a fictional company (full pipeline: collect → normalize → reconcile → validate): [examples/meridian-office-furniture/](examples/meridian-office-furniture/)

## Quality gate

Before delivery, verify that:

- no default example contains a real company, person, customer, credential, or confidential number
- every nontrivial claim has provenance or is clearly marked as an inference or pending item
- duplicate records have a merge decision and retained source links
- conflicts have not been silently resolved
- sensitivity labels are present and export rules were applied
- the generated Skill has valid frontmatter, a discriminating description, and discoverable references
- evaluation cases cover unsupported certainty, privacy leakage, synonym merging, temporal drift, and multi-AI disagreement
- register hygiene gate passed: 100% of records re-rated with a recorded basis, no meta-records, no empty or placeholder claims
- generated package carries a known-gaps section, and no hand-edits diverge it from the register
