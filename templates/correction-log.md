# Correction log — template

One line per observed error or gap. Triage in batches; do not fix at capture time.

| ID | Date | Context / task | Wrong output or gap (short quote) | Expected / correct | Noticed by | Root cause | Disposition |
|---|---|---|---|---|---|---|---|
| E-001 |  |  |  |  |  | slip / stale / conflict / missing / wrong-rule |  |

Root-cause key: **slip** = package was right, output ignored it · **stale** = source changed · **conflict** = records disagree → batch decision list · **missing** = no record existed · **wrong-rule** = record itself incorrect.

Disposition values: `closed-slip` · `register-updated (record ID)` · `to-decision-list (D-ID)` · `case-promoted (case ID)` · `open`.
