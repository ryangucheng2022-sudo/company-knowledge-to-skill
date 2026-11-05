#!/usr/bin/env python3
"""check_consistency.py — drift check between this package and its sources of truth.

The register is the single source of truth and the package is a build artifact.
This script catches the ways a shipped package silently drifts from its own
rules and examples:

  errors (exit 1):
    - a references/*.md or templates/* file exists but is never mentioned in
      SKILL.md (orphan file: shipped but unreachable)
    - SKILL.md cites a references/ or templates/ path that does not exist
    - the worked example no longer validates (validate_knowledge.py must exit 0
      on the example register in both generic and internal modes)
    - references/evaluation-cases.yaml is missing or declares no cases

Usage: python3 scripts/check_consistency.py [package-root]
Output: one JSON object {root, errors, warnings}. Pure stdlib.
"""
import json, os, re, subprocess, sys

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    errors, warnings = [], []
    skill = os.path.join(root, 'SKILL.md')
    if not os.path.isfile(skill):
        print(json.dumps({'root': root, 'errors': ['SKILL.md missing'], 'warnings': []}, indent=1)); return 1
    text = open(skill, encoding='utf-8').read()

    # orphan files: shipped but never mentioned in SKILL.md
    for sub in ('references', 'templates'):
        d = os.path.join(root, sub)
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                stem = os.path.splitext(name)[0]
                if name not in text and stem not in text:
                    errors.append(f'orphan file not mentioned in SKILL.md: {sub}/{name}')
    # cited paths exist
    for rel in sorted(set(x.rstrip('.') for x in re.findall(r'((?:references|templates)/[\w.\-]+)', text))):
        if not os.path.exists(os.path.join(root, rel)):
            errors.append(f'SKILL.md cites missing file: {rel}')

    # worked example still validates
    ex = next((os.path.join(root, 'examples', 'meridian-office-furniture', n)
               for n in ('records.jsonl', 'records.yaml', 'knowledge.jsonl', 'knowledge.yaml')
               if os.path.isfile(os.path.join(root, 'examples', 'meridian-office-furniture', n))), '')
    validator = os.path.join(root, 'scripts', 'validate_knowledge.py')
    if os.path.isfile(ex) and os.path.isfile(validator):
        for profile in ('generic', 'internal'):
            r = subprocess.run([sys.executable, validator, ex, '--export', profile],
                               capture_output=True, text=True)
            if r.returncode != 0:
                msg = (r.stdout.strip() or r.stderr.strip())[:200]
                errors.append(f'worked example fails validation ({profile}): {msg}')
    else:
        warnings.append('worked example or validator missing; example check skipped')

    # evaluation cases present
    cases = os.path.join(root, 'references', 'evaluation-cases.yaml')
    if not os.path.isfile(cases):
        errors.append('references/evaluation-cases.yaml missing')
    elif 'id:' not in open(cases, encoding='utf-8').read():
        errors.append('references/evaluation-cases.yaml declares no cases')

    print(json.dumps({'root': root, 'errors': errors, 'warnings': warnings}, ensure_ascii=False, indent=1))
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
