# Collection prompts and staged procedure

Use one prompt per collector. Replace bracketed placeholders without adding facts.

## 0. Shared collector contract

```text
You are a knowledge collector for [ORGANIZATION]. Extract only information supported by the supplied conversation, files, or memory. Do not guess missing rules.

Return each claim as a record with:
- claim: concise statement
- original_wording: exact wording when available
- domain: terminology | management_rule | process | expression | ai_correction | confirmed_phrase
- source_ref: message, file, page, or turn identifier
- observed_at: date or unknown
- status: confirmed | repeated | proposed | inferred | unknown
- sensitivity: public | internal | confidential | restricted
- confidence: high | medium | low
- rationale: why the status and confidence were assigned

Separate facts, interpretations, and open questions. Preserve competing claims instead of choosing a winner.
```

## 1. Terminology collector

Ask for standard name, aliases, meaning in this organization, use cases, common misuse, disallowed substitutions, scope, and time validity. Record an alias separately when it may have a different meaning in another business unit.

## 2. Management-rule collector

Ask for rule text, calculation or decision logic, scope, owner, inputs, exceptions, effective period, approval state, and evidence. Mark recommendations as `proposed`.

## 3. Expression and writing collector

Extract recurring title structures, sentence patterns, reporting conventions, meeting-minute wording, and examples of accepted or rejected wording. Explain the judgment criterion without turning personal style into a company rule.

## 4. AI-correction collector

Collect before/after edits and the reason for each change. Classify the failure as unsupported certainty, empty slogan, unnecessary abstraction, over-structuring, invented data, privacy exposure, or other. Keep genuine domain terms even when they resemble generic business language.

## 5. Multi-AI handoff

Give every collector the same scope and privacy boundary. Do not ask one collector to see another collector's answer before independent collection. Later stages may compare outputs using the canonical schema.

## 6. Human checkpoints

Pause for review after normalization and after reconciliation when any record is `restricted`, has conflicting effective periods, changes an approval state, or would be exported to a broader audience.

## 7. Correction-case pairs (all collectors)

Beyond definitions, actively collect **correction cases**: a wrong (or nonstandard) formulation paired with the corrected one, plus the reason. Examples of the genre: a metric quoted on the wrong basis (cumulative value used as a quarterly value), a deprecated term still in circulation, a plan written up as an accomplished result. Record each as a first-class record (`record_type: case`, domain `ai_correction`) — downstream, paired wrong→right examples teach expression rules more reliably than abstract style guidance.
