# Company Knowledge to Skill

English | [简体中文](README.zh-CN.md)

A generic, reusable Skill for collecting organization-specific knowledge from multiple AI or human inputs, reconciling differences, applying privacy controls, generating a downstream Skill, and testing the result.

## Why this exists

Most of an organization's valuable knowledge never becomes an organizational capability: it lives in employees' experience, day-to-day work, and past decisions — scattered across people, AI chats, and working documents. This Skill is a pipeline for turning that tacit knowledge into AI capability that is **reusable, verifiable, and continuously improvable**.

It addresses three core problems of enterprise knowledge:

- **Scattered** — knowledge sits in heads, AI memories, files, and systems.
- **Distorted** — inconsistent definitions, version conflicts, and misunderstood context corrupt it in transit.
- **Not executable** — documents describe knowledge but do not standardize how work gets done.

A traditional knowledge base answers "where do I find this knowledge?" A Skill answers the next question: "how do I do this work, following that knowledge?" A knowledge base can tell an AI what a term means; a business Skill specifies how to select the data, apply the rules, judge anomalies, and verify the result.

## Where it fits

| Capability | What it solves |
|---|---|
| Knowledge base | Store, classify, and find knowledge |
| RAG | Retrieve relevant knowledge while answering |
| Agent | Call tools and execute tasks toward a goal |
| **Knowledge-to-Skill (this project)** | Distill scattered knowledge into standards, procedures, judgment rules, and testable Skills |

It complements rather than replaces the other three: it is the knowledge-engineering layer they are missing.

## Typical scenarios

1. **Standardizing enterprise AI use** — employees already use different AIs with inconsistent terminology and style; one collected, normalized knowledge layer gives them a shared standard.
2. **Capturing expert know-how** — how an expert analyzes, judges anomalies, and handles exceptions, converted from personal experience into a repeatable method.
3. **Onboarding and role handover** — not just what the policy says, but the internal terms, real workflows, historical judgments, and responsibility boundaries a newcomer actually needs.
4. **Building professional business Agents** — finance, sales-project, or supply-chain Agents need the company's own metric definitions, business rules, and judgment standards, not generic reasoning alone.
5. **Post-merger integration** — the same term with different definitions across companies or divisions; surface the conflicts, unify what must be unified, keep legitimate differences.
6. **Migrating between AI platforms** — knowledge accumulated in one tool (ChatGPT, Muse, Grok, …) becomes a model-independent asset instead of staying locked in one platform's memory.

## Value levels

| Level | Value | Measurable by |
|---|---|---|
| L1 Efficiency | Less time explaining terms, revising drafts, hunting documents | Task time, rework count |
| L2 Quality | Fewer terminology and factual errors | Term accuracy, major-error rate |
| L3 Reuse | Expert methods used by more people and Agents | Skill reuse count, roles covered |
| L4 Organizational capability | Less key-person dependency, more consistent execution | Onboarding time, handover success, process consistency |

L1–L2 are verifiable quickly; L3–L4 are worth more and take longer to prove. A sensible validation order: (1) terminology and AI expression standards, (2) a professional role's analytical method, (3) role handover and knowledge inheritance.

A packaged Skill is not automatically reliable: it still needs data permissions, tool connections, tests, and human oversight. And collecting employees' AI conversation history requires explicit authorization and data minimization — personal chats are not company assets by default.

> The goal: knowledge no longer lives only in documents and in people's heads, but becomes working capability that the organization and its AIs can keep reusing.


## Method at a glance

| Stage | Input | Output | Human checkpoint |
|---|---|---|---|
| Collect | Scope + source inventory | Independent collector outputs | Scope and sensitivity boundary approved |
| Normalize | Collector outputs | Canonical records with provenance | Spot-check records against sources |
| Reconcile | Records from all collectors | Deduplicated records + conflict log | Batch decision list signed off |
| Specify | Reconciled records | Terminology, rules, expression and correction guides | Ratings reviewed (anti-inflation caps applied) |
| Generate | Validated records | Knowledge package / downstream Skill with a known-gaps section | Hygiene gate: 100% re-rated, no placeholders |
| Evaluate | Package + cases | Behavior results (sufficient / partial / missing, veto failures) | Gaps accepted or sent back |
| Maintain | Errors observed in use | Register updates + new regression cases | Corrections batched, not drip-fed |

## Design principles

- **Independent collectors first.** Diversity before consensus: collectors work from the same contract without seeing each other. Agreement is evidence; disagreement is signal — both are lost if collection starts from one draft.
- **Baseline before merge.** One source is designated the baseline; nothing overrides it silently, and superseded versions are demoted and kept, never deleted.
- **Ratings are earned.** A source's self-rating is a claim, not a fact. Discussion-stage content is capped until formal evidence supports it, and every rating records its basis.
- **Packages are build artifacts.** The register is the single source of truth; a generated package is regenerated from it, never hand-patched — and it ships an honest list of what it does not cover.

## Included

- `SKILL.md` — entrypoint and stage routing
- `references/collection-prompts.md` — independent collector prompts and checkpoints
- `references/knowledge-schema.yaml` — canonical record schema
- `references/reconciliation-and-conflicts.md` — deduplication and conflict rules
- `references/privacy-and-redaction.md` — sensitivity levels and export handling
- `references/evaluation-cases.yaml` — evaluation fixtures and expected safeguards
- `references/evaluation-protocol.md` — behavior evaluation with an independent executor
- `references/field-failure-patterns.md` — failure modes from a real deployment, with detection checks
- `templates/decision-list.md` — batch decision list and persistent unresolved-items ledger
- `templates/` — source inventory, knowledge-package outline, decision list, and correction log
- `references/correction-loop.md` — continuous correction: usage errors to regression cases
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

## What is new in v1.1.0

Hardened with patterns from a real deployment (anonymized in
`references/field-failure-patterns.md`):

- baseline designation and a ban on silent overrides; superseded versions are
  demoted and kept, never deleted
- anti-inflation re-rating: a source's self-rating is a claim; `status_basis`
  records why each rating was assigned; discussion content is capped
- batch decision lists with a write-back protocol, and a persistent
  unresolved-items ledger (open → decided → closed)
- sensitivity-marker preservation across extraction, plus a pre-export value
  scan as a release gate
- a register hygiene gate before generation (100% re-rated, no meta-records,
  no placeholder claims), enforced by new validator checks: duplicate-claim
  report, empty/meta-record detection, uniformity heuristic, `--scan-values`
- correction-case pairs as first-class records; packages ship a known-gaps
  section; evaluation runs an independent-executor protocol

Validator on the worked example now also reports `rated_coverage=9/9`
(default outputs otherwise unchanged: generic `errors=0, warnings=1`;
internal `errors=0, warnings=0`). A synthetic dirty register (placeholder
claim, duplicate claim, meta-record, all-uniform statuses, an unmarked
figure in an exportable record) fails with `errors=1, warnings=7`, exit 1.

All seven cases in `references/evaluation-cases.yaml` are exercised by the
worked example; the mapping is documented in the example's README.
