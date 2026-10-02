#!/usr/bin/env python3
"""Regenerate tools/ibge-municipios.json from the official IBGE API.

Fase 1-B (território): esta é a referência contra a qual `validate.py`
confere todo código em `territorio.municipios_ibge`. Rodar de novo só se o
IBGE criar, extinguir ou renomear um município.
"""
from __future__ import annotations

import gzip
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ibge-municipios.json"
URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"


def uf_sigla(m: dict) -> str:
    if m.get("microrregiao"):
        return m["microrregiao"]["mesorregiao"]["UF"]["sigla"]
    # Handful of municípios lack microrregiao (e.g. Boa Esperança do Norte/MT);
    # regiao-imediata always carries the UF as a fallback.
    return m["regiao-imediata"]["regiao-intermediaria"]["UF"]["sigla"]


def main() -> int:
    with urllib.request.urlopen(URL) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        municipios = json.loads(raw.decode("utf-8"))

    reduced = sorted(
        (
            {
                "codigo_ibge": str(m["id"]),
                "nome": m["nome"],
                "uf": uf_sigla(m),
            }
            for m in municipios
        ),
        key=lambda m: m["codigo_ibge"],
    )

    codigos = [m["codigo_ibge"] for m in reduced]
    assert all(len(c) == 7 for c in codigos), "expected 7-digit IBGE codes"
    assert len(set(codigos)) == len(codigos), "expected unique IBGE codes"

    OUT.write_text(
        json.dumps(reduced, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {len(reduced)} municípios to {OUT.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
