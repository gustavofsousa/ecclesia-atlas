#!/usr/bin/env python3
"""Validate every circunscrição JSON against the schema. Fase 1-A / task 1A.3.

Also runs the domain invariants the JSON Schema can't express on its own:
  - a 'pessoal' jurisdiction must have territorio.tipo == 'sem_territorio'
  - id must equal the file stem (slugs are stable, files are named by them)
  - ids and wikidata_qids are unique across the dataset

Exit code is non-zero on any failure, so it doubles as the CI gate.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "circunscricao.schema.json"
DATA = ROOT / "data" / "circunscricoes"


def main() -> int:
    validator = Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))
    files = sorted(DATA.glob("*.json"))
    if not files:
        print("no data files found", file=sys.stderr)
        return 1

    errors: list[str] = []
    ids: Counter[str] = Counter()
    qids: Counter[str] = Counter()
    gcatholic: Counter[str] = Counter()

    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        for e in validator.iter_errors(data):
            path = "/".join(map(str, e.path)) or "(root)"
            errors.append(f"{f.name}: {path}: {e.message}")

        if data.get("id") != f.stem:
            errors.append(f"{f.name}: id '{data.get('id')}' != file stem '{f.stem}'")
        ids[data.get("id")] += 1

        if data.get("tipo_jurisdicao") == "pessoal":
            terr = data.get("territorio") or {}
            if terr.get("tipo") != "sem_territorio":
                errors.append(f"{f.name}: pessoal jurisdiction must have "
                              f"territorio.tipo == 'sem_territorio'")

        cw = data.get("crosswalk") or {}
        if cw.get("wikidata_qid"):
            qids[cw["wikidata_qid"]] += 1
        if cw.get("gcatholic_id"):
            gcatholic[cw["gcatholic_id"]] += 1

    for dup, n in ids.items():
        if n > 1:
            errors.append(f"duplicate id '{dup}' in {n} files")
    for dup, n in qids.items():
        if n > 1:
            errors.append(f"duplicate wikidata_qid '{dup}' in {n} files")
    for dup, n in gcatholic.items():
        if n > 1:
            errors.append(f"duplicate gcatholic_id '{dup}' in {n} files "
                          "(likely the same circunscrição twice)")

    if errors:
        print(f"FAIL — {len(errors)} problem(s) across {len(files)} files:")
        for e in errors:
            print("  -", e)
        return 1

    print(f"OK — {len(files)} files valid against {SCHEMA.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
