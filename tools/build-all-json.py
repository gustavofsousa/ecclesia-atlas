#!/usr/bin/env python3
"""Build dist/all.json — every circunscrição record in one file.

Fase 2, Nível 1: a JSON array of all records, sorted by id, each item
identical to its file in data/circunscricoes/ (provenance included). The
output is deterministic — no timestamps — so the file only changes when the
data does. This is a derived artifact: never hand-edit it, never treat it as
a source of truth.

--check rebuilds in memory and exits non-zero when dist/all.json is stale,
which is how CI keeps the committed aggregate in sync with data/.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "circunscricoes"
OUT = ROOT / "dist" / "all.json"


def build(data_dir: Path) -> str:
    records = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in data_dir.glob("*.json")
    ]
    # Sort by id, not by filename: "x-y.json" < "x.json" but "x" < "x-y".
    records.sort(key=lambda record: record["id"])
    return json.dumps(records, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="fail if dist/all.json differs from a fresh build")
    args = parser.parse_args()

    fresh = build(DATA)
    out = OUT.relative_to(ROOT)

    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else None
        if current != fresh:
            print(f"{out} is stale — run: python3 tools/build-all-json.py",
                  file=sys.stderr)
            return 1
        print(f"OK — {out} matches data/")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(fresh, encoding="utf-8")
    print(f"wrote {len(json.loads(fresh))} circunscrições to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
