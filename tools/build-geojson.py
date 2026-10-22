#!/usr/bin/env python3
"""Build dist/circunscricoes.geojson from territorio.municipios_ibge + the município mesh.

Fase 1-B (1B.3): one Feature per circunscrição with granularidade_territorial
== "municipio", geometry = union of its municípios' polygons from
tools/municipios-malha.geojson (official IBGE mesh — see
fetch-municipios-malha.py for provenance).
Circunscrições with granularidade_territorial in {submunicipal, indefinido,
null} or an empty município list are skipped — they have no polygon to draw
yet. This is a derived artifact: never hand-edit it, never treat it as a
source of truth. Regenerate after any change to territorio.municipios_ibge.
"""
from __future__ import annotations

import json
from pathlib import Path

from shapely.geometry import shape, mapping
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "data" / "circunscricoes"
MALHA = ROOT / "municipios-malha.geojson"
OUT = ROOT.parent / "dist" / "circunscricoes.geojson"


def repair(code: str, polygon: BaseGeometry) -> BaseGeometry:
    # buffer(0) repairs minor topology defects (self-intersections, holes not
    # cleanly assigned to a shell) in the mesh.
    # INVARIANT: the repair keeps the area. buffer(0) empties a polygon whose
    # rings have the wrong orientation; the old tbrugz mesh lost most of the
    # area of 43 municípios (Rio de Janeiro among them) that way, silently.
    repaired = polygon.buffer(0)
    if repaired.area < 0.99 * abs(polygon.area):
        raise ValueError(
            f"repair of município {code} lost area: {abs(polygon.area)} -> {repaired.area}"
        )
    return repaired


def main() -> int:
    malha = json.loads(MALHA.read_text(encoding="utf-8"))
    polygons_by_code = {
        f["properties"]["id"]: repair(f["properties"]["id"], shape(f["geometry"]))
        for f in malha["features"]
    }

    features = []
    skipped_no_geometry = []
    skipped_missing_codes = {}

    for path in sorted(DATA.glob("*.json")):
        circ = json.loads(path.read_text(encoding="utf-8"))
        if circ.get("granularidade_territorial") != "municipio":
            continue

        codes = circ.get("territorio", {}).get("municipios_ibge", [])
        if not codes:
            skipped_no_geometry.append(circ["id"])
            continue

        polys = []
        missing = []
        for code in codes:
            poly = polygons_by_code.get(code)
            if poly is None:
                missing.append(code)
            else:
                polys.append(poly)

        if missing:
            skipped_missing_codes[circ["id"]] = missing
        if not polys:
            skipped_no_geometry.append(circ["id"])
            continue

        geometry = unary_union(polys)
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "id": circ["id"],
                    "nome": circ["nome"]["valor"],
                    "tipo": circ["tipo"],
                    "n_municipios": len(codes),
                    "n_municipios_sem_geometria": len(missing),
                },
                "geometry": mapping(geometry),
            }
        )

    geojson = {"type": "FeatureCollection", "features": features}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(geojson, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"wrote {len(features)} circunscrição polygons to {OUT.relative_to(ROOT.parent)}")
    if skipped_no_geometry:
        print(f"skipped (no território/geometry available): {skipped_no_geometry}")
    if skipped_missing_codes:
        print("circunscrições with a partial gap (município missing from the mesh):")
        for cid, codes in skipped_missing_codes.items():
            print(f"  {cid}: {codes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
