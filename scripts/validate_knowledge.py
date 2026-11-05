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
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("input"); ap.add_argument("--export", choices=["generic", "internal"], default="generic"); args = ap.parse_args()
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
    print(f"records={len(records)}"); print(f"errors={len(errors)}"); print(f"warnings={len(warnings)}")
    for item in errors: print("ERROR", item)
    for item in warnings: print("WARN", item)
    return 1 if errors else 0
if __name__ == "__main__": raise SystemExit(main())
