#!/usr/bin/env python3
"""Regenerate tools/municipios-malha.geojson from the official IBGE mesh API.

Fase 1-B (1B.3): geometria dos municípios brasileiros usada por
build-geojson.py para derivar o GeoJSON por circunscrição. Fonte: API de
malhas v3 do IBGE, qualidade `intermediaria`, período padrão da API. The
cache keeps only `properties.id` (7-digit IBGE code), normalized from the
API's `codarea`, so build-geojson.py reads one shape regardless of source.
Municípios in ibge-municipios.json that the mesh lacks (created after the
mesh period) are reported, not hidden.
"""
from __future__ import annotations

import gzip
import json
import urllib.request
from pathlib import Path

from ibge_tls import ibge_ssl_context

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "municipios-malha.geojson"
REFERENCE = ROOT / "ibge-municipios.json"
URL = (
    "https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR"
    "?formato=application/vnd.geo%2Bjson&intrarregiao=municipio"
    "&qualidade=intermediaria"
)


def main() -> int:
    request = urllib.request.Request(URL, headers={"Accept-Encoding": "gzip"})
    with urllib.request.urlopen(request, context=ibge_ssl_context()) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)

    malha = json.loads(raw.decode("utf-8"))
    features = [
        {
            "type": "Feature",
            "properties": {"id": f["properties"]["codarea"]},
            "geometry": f["geometry"],
        }
        for f in malha["features"]
    ]
    ids = [f["properties"]["id"] for f in features]
    assert all(len(i) == 7 for i in ids), "expected 7-digit IBGE codes"
    assert len(set(ids)) == len(ids), "expected unique IBGE codes"

    reference = {m["codigo_ibge"] for m in json.loads(REFERENCE.read_text(encoding="utf-8"))}
    unknown = sorted(set(ids) - reference)
    assert not unknown, f"mesh has codes missing from ibge-municipios.json: {unknown}"

    geojson = {"type": "FeatureCollection", "features": features}
    OUT.write_text(json.dumps(geojson, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(ids)} município polygons to {OUT.relative_to(ROOT.parent)}")

    without_geometry = sorted(reference - set(ids))
    if without_geometry:
        print(f"municípios in ibge-municipios.json without geometry in the mesh: {without_geometry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
