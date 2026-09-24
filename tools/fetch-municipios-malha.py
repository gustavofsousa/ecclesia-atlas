#!/usr/bin/env python3
"""Regenerate tools/municipios-malha.geojson from tbrugz/geodata-br.

Fase 1-B (1B.3): geometria dos municípios brasileiros usada por
build-geojson.py para derivar o GeoJSON por circunscrição. Fonte provisória —
CC0, `properties.id` já é o código IBGE de 7 dígitos, sem mapeamento
necessário. Não cobre 7 municípios criados após a geração da malha (ver
ROADMAP.md 1B.3); trocar pela malha oficial do IBGE
(geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais) quando
uma rodada de qualidade maior for justificada.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "municipios-malha.geojson"
URL = (
    "https://raw.githubusercontent.com/tbrugz/geodata-br/master/"
    "geojson/geojs-100-mun.json"
)


def main() -> int:
    with urllib.request.urlopen(URL) as resp:
        raw = resp.read()

    malha = json.loads(raw.decode("utf-8"))
    ids = [f["properties"]["id"] for f in malha["features"]]
    assert all(len(i) == 7 for i in ids), "expected 7-digit IBGE codes"
    assert len(set(ids)) == len(ids), "expected unique IBGE codes"

    OUT.write_text(json.dumps(malha, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(ids)} município polygons to {OUT.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
