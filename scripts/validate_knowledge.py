#!/usr/bin/env python3
"""Validate canonical knowledge records and flag unsafe exports."""
import argparse, json, sys
from pathlib import Path
REQUIRED = {"record_id", "domain", "claim", "status", "confidence", "sensitivity", "provenance"}
ENUMS = {"status": {"confirmed", "repeated", "proposed", "inferred", "unknown", "deprecated"}, "confidence": {"high", "medium", "low"}, "sensitivity": {"public", "internal", "confidential", "restricted"}}
def load(path):
    text = Path(path).read_text(encoding="utf-8")
    if path.endswith('.jsonl'): return [json.loads(line) for line in text.splitlines() if line.strip()]
    if path.endswith(('.yaml', '.yml')):
        try: import yaml
        except ImportError: raise SystemExit("YAML input requires PyYAML (pip install pyyaml); alternatively convert the records to JSON or JSONL")
        return yaml.safe_load(text)
    try: return json.loads(text)
    except json.JSONDecodeError as exc: raise SystemExit(f"Input must be JSON, JSONL, or YAML: {exc}")
import re
PLACEHOLDERS = {"", "—", "——", "-", "tbd", "n/a", "none"}
META_PATTERNS = [r"(?i)confidence (levels?|scale)", r"(?i)status (levels?|scale)", r"(?i)rating scale", r"(?i)\bA\s*[=|]\s*confirmed\b"]
VALUE_PATTERNS = [r"\d+\.\d+\s*%", r"[$€¥£]\s?\d", r"\b\d{4,}[- ]?\d{4,}\b"]
def norm_claim(r):
    return re.sub(r"\s+", " ", (r.get("claim") or "").strip().lower())
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("input"); ap.add_argument("--export", choices=["generic", "internal"], default="generic"); ap.add_argument("--scan-values", action="store_true", help="heuristically scan exportable records for figures/identifiers that may be sensitive"); args = ap.parse_args()
    data = load(args.input); records = data.get("records", data) if isinstance(data, dict) else data
    if not isinstance(records, list): print("ERROR: expected a list of records", file=sys.stderr); return 2
    errors, warnings, ids = [], [], set()
    for i, r in enumerate(records, 1):
        missing = REQUIRED - set(r)
        if missing: errors.append(f"{i}: missing {sorted(missing)}")
        rid = r.get("record_id")
        if rid in ids: errors.append(f"{i}: duplicate record_id {rid}")
        ids.add(rid)
        for field, allowed in ENUMS.items():
            if r.get(field) not in allowed: errors.append(f"{i}: invalid {field}={r.get(field)!r}")
        if r.get("sensitivity") in {"confidential", "restricted"} and args.export == "generic": warnings.append(f"{i}: sensitive record requires abstract/redact/exclude before generic export")
        if r.get("status") in {"proposed", "inferred", "unknown"} and r.get("confidence") == "high": warnings.append(f"{i}: review high confidence on non-confirmed status")
        if not r.get("provenance", {}).get("source_id"): errors.append(f"{i}: provenance.source_id is required")
    # --- register hygiene checks (v1.1) ---
    claims = {}
    for i, r in enumerate(records, 1):
        claim = (r.get("claim") or "").strip()
        if claim.lower() in PLACEHOLDERS: errors.append(f"{i}: empty or placeholder claim")
        nc = norm_claim(r)
        if nc:
            if nc in claims: warnings.append(f"{i}: duplicate claim also at record {claims[nc]} — merge or group as conflict")
            claims.setdefault(nc, i)
        if any(re.search(pat, claim) for pat in META_PATTERNS): warnings.append(f"{i}: possible meta-record (defines the schema/scale itself, not company knowledge)")
        if args.scan_values and r.get("sensitivity") in {"public", "internal"} and any(re.search(pat, claim) for pat in VALUE_PATTERNS):
            warnings.append(f"{i}: possible sensitive figure/identifier in an exportable record — verify before release")
    for field in ("status", "confidence", "sensitivity", "notes"):
        vals = [str(r.get(field)) for r in records if r.get(field) not in (None, "")]
        if len(vals) >= 5 and len(set(vals)) == 1: warnings.append(f"uniform {field}={vals[0]!r} on all {len(vals)} populated records — classification may not have been performed")
    rated = sum(1 for r in records if r.get("status") not in (None, "", "unknown"))
    print(f"rated_coverage={rated}/{len(records)}")
    print(f"records={len(records)}"); print(f"errors={len(errors)}"); print(f"warnings={len(warnings)}")
    for item in errors: print("ERROR", item)
    for item in warnings: print("WARN", item)
    return 1 if errors else 0
if __name__ == "__main__": raise SystemExit(main())
