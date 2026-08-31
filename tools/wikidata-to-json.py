#!/usr/bin/env python3
"""Bootstrap: turn the Wikidata SPARQL CSV into one JSON file per circunscrição.

Fase 1-A / task 1A.1. Reads `tools/wikidata-raw.csv` (produced by the curl in
`tools/wikidata-circunscricoes.rq`) and writes `data/circunscricoes/<slug>.json`.

Two rules that define this script:

1. Every field it writes carries `metodo: "automatico"`. When a target file already
   exists, a value the human curator wrote (present in the existing file) is NEVER
   overwritten — the bootstrap only fills gaps (null/absent fields, empty crosswalk
   ids). This is the guarantee the schema's `metodo` field exists to enforce.
2. The SPARQL base class `Q665487` pulls in noise (extinct/suppressed sees, an
   Anglican diocese, ecclesiastical provinces). Type mapping is explicit and every
   excluded item is written to `tools/wikidata-excluded.csv` — nothing is dropped
   silently.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "tools" / "wikidata-raw.csv"
OUT_DIR = ROOT / "data" / "circunscricoes"
EXCLUDED_REPORT = ROOT / "tools" / "wikidata-excluded.csv"
DEFERRED_REPORT = ROOT / "tools" / "wikidata-deferred.csv"
TODAY = "2026-08-18"  # verificado_em stamp for this bootstrap run

# Current scope: the standard, common circunscrições — territorial Latin-rite dioceses
# and archdioceses. Everything else that is a VALID Brazilian Catholic circunscrição but
# not in this set (territorial prelatures, Eastern-rite eparchies/archeparchies/exarchates,
# military and Eastern ordinariates) is parked in wikidata-deferred.csv for future phases —
# not dropped. Do the common case well first.
STANDARD_TIPOS = {"diocese", "arquidiocese"}

# --- Wikidata type QID -> our schema enum. Confirmed against tools/wikidata-raw.csv. ---
TIPO_MAP = {
    "Q3146899": "diocese",                 # diocese da Igreja Católica
    "Q373074": "diocese",                  # diocese sufragânea (a role; still a diocese)
    "Q105390172": "arquidiocese",          # arquidiocese metropolitana católica romana
    "Q2072238": "arquidiocese",            # arquidiocese
    "Q2633744": "prelazia_territorial",    # territorial prelature
    "Q17305527": "prelazia_territorial",   # Prelazia
    "Q105389481": "eparquia",              # eparquia católica
    "Q20725872": "eparquia",               # Eastern Catholic eparchy
    "Q108822885": "arquieparquia",         # Arquieparquia Metropolitana Católica
    "Q2288631": "arquieparquia",           # archeparchy
    "Q3732788": "exarcado",                # apostolic exarchate
    "Q1531518": "ordinariado_militar",     # military ordinariate
    "Q7100806": "ordinariado_oriental",    # Ordinariato para fiéis de rito oriental
}

# Items carrying ANY of these are not current Brazilian Catholic circunscrições — dropped
# regardless of whatever else they are tagged as (a defunct/Orthodox/Anglican body can also
# carry a generic "archeparchy"/"diocese" tag; the disqualifier wins).
EXCLUDE_HARD = {
    "Q124344656": "suppressed territorial prelature",
    "Q135639685": "suppressed territorial abbey",
    "Q27780831": "extinct roman catholic diocese",
    "Q15893266": "former entity",
    "Q18917976": "anglican diocese (not catholic)",
    "Q1649443": "national church (not catholic — e.g. Orthodox)",
}

# Exclusions keyed by the ITEM QID (not its type). For Wikidata duplicates where the same
# circunscrição is modeled twice: keep the pt-labelled item with the GCatholic id, drop the
# English-fallback twin.
EXCLUDE_ITEMS = {
    "Q137664905": "duplicate of Q137655591 (Diocese de Baturité)",
}

# QIDs that on their own do not constitute a circunscrição (a province is modeled via
# the `provincia_eclesiastica` field, not as its own record). Dropped only when the
# item has no mappable type besides these.
PROVINCE_OR_OTHER = {
    "Q427961": "ecclesiastical province (metropolis)",
    "Q10139375": "eastern catholic ecclesiastical province",
    "Q1081138": "historic heritage",
}

# Status tags that ride along with a real type and must not be treated as the type.
IGNORE_STATUS = {"Q2665272"}  # "immediately subject to the Holy See"

# Most-specific first: how to pick one enum when an item maps to several.
TIPO_PRIORITY = [
    "arquieparquia", "arquidiocese", "exarcado", "eparquia",
    "ordinariado_oriental", "ordinariado_militar", "prelazia_territorial", "diocese",
]
PESSOAL = {"ordinariado_militar", "ordinariado_oriental"}
OFICIO = {
    "arquidiocese": "arcebispo", "arquieparquia": "arcebispo",
    "diocese": "bispo", "prelazia_territorial": "bispo prelado",
    "eparquia": "eparca", "exarcado": "exarca",
    "ordinariado_militar": "ordinário", "ordinariado_oriental": "ordinário",
}


def slugify(name: str) -> str:
    n = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    n = n.lower()
    n = re.sub(r"[^a-z0-9]+", "-", n).strip("-")
    return n


def qid(url: str) -> str:
    return url.rsplit("/", 1)[-1]


def parse_date(raw: str) -> str | None:
    # Wikidata timestamps look like "1676-11-16T00:00:00Z"; keep the date part.
    return raw.split("T", 1)[0] if raw else None


def parse_point(raw: str) -> tuple[float, float] | None:
    # "Point(-38.5 -12.97)" -> (lat, lon)
    m = re.match(r"Point\(([-\d.]+) ([-\d.]+)\)", raw or "")
    if not m:
        return None
    lon, lat = float(m.group(1)), float(m.group(2))
    return lat, lon


def prov(valor, entity_url: str, extra_source: str | None = None) -> dict:
    """A provenanced-string/value block stamped as an automatic Wikidata write."""
    return {
        "valor": valor,
        "fonte": "wikidata" if not extra_source else f"wikidata ({extra_source})",
        "fonte_url": entity_url,
        "verificado_em": TODAY,
        "confianca": "media",
        "metodo": "automatico",
    }


def aggregate(rows: list[dict]) -> dict[str, dict]:
    """Collapse the multi-row-per-item CSV into one record of raw values per item."""
    items: dict[str, dict] = defaultdict(
        lambda: {"tipos": set(), "label": None, "coord": "", "inicio": "",
                 "site": "", "gcatholic": ""}
    )
    for r in rows:
        it = r["item"]
        rec = items[it]
        rec["tipos"].add(qid(r["tipo"]))
        # itemLabel is a Q-number when Wikidata has no pt/en label; prefer a real one.
        lbl = r["itemLabel"]
        if lbl and not re.fullmatch(r"Q\d+", lbl):
            rec["label"] = lbl
        for k in ("coord", "inicio", "site", "gcatholic"):
            if r[k]:
                rec[k] = r[k]
    return items


def classify(tipos: set[str]) -> tuple[str | None, str | None]:
    """Return (enum_tipo, exclusion_reason). Exactly one is non-None."""
    for q in tipos:
        if q in EXCLUDE_HARD:
            return None, EXCLUDE_HARD[q]
    mapped = [TIPO_MAP[q] for q in tipos if q in TIPO_MAP]
    if not mapped:
        others = [PROVINCE_OR_OTHER.get(q, q) for q in tipos if q not in IGNORE_STATUS]
        return None, "no mappable type: " + ", ".join(sorted(others))
    for want in TIPO_PRIORITY:
        if want in mapped:
            return want, None
    return mapped[0], None


def build_record(entity_url: str, raw: dict, tipo: str) -> dict:
    q = qid(entity_url)
    name = raw["label"] or q
    pessoal = tipo in PESSOAL
    rec: dict = {
        "id": slugify(name),
        "nome": prov(name, entity_url),
        "tipo": tipo,
        "tipo_jurisdicao": "pessoal" if pessoal else "territorial",
        "granularidade_territorial": None if pessoal else "indefinido",
        "regional_cnbb": None,          # manual curation (task 1A.2)
        "provincia_eclesiastica": None,  # manual curation (task 1A.2)
    }
    inicio = parse_date(raw["inicio"])
    if inicio:
        rec["ereta_em"] = prov(inicio, entity_url, "P571 inception")
    if raw["site"]:
        rec["site_oficial"] = prov(raw["site"], entity_url, "P856")
    point = parse_point(raw["coord"])
    if point:
        rec["coordenada"] = {
            "lat": point[0], "lon": point[1],
            "fonte": "wikidata (P625)", "fonte_url": entity_url,
            "verificado_em": TODAY, "confianca": "media", "metodo": "automatico",
        }
    rec["bispo_atual"] = {
        "nome": None, "oficio": OFICIO[tipo], "valido_de": None,
        "fonte": None, "fonte_url": None, "verificado_em": None,
        "confianca": "nao_verificado", "metodo": "automatico",
    }
    rec["territorio"] = {
        "tipo": "sem_territorio" if pessoal else "municipios_ibge",
        **({} if pessoal else {"municipios_ibge": []}),
        "fonte": None, "fonte_url": None, "verificado_em": None,
        "confianca": "nao_verificado", "metodo": "automatico",
    }
    rec["crosswalk"] = {
        "wikidata_qid": q,
        "gcatholic_id": raw["gcatholic"] or None,
        "catholic_hierarchy_id": None,
        "cdic_id": None,
    }
    return rec


def is_manual(value) -> bool:
    return isinstance(value, dict) and value.get("metodo") == "manual"


def merge_preserving_manual(old: dict, new: dict) -> dict:
    """Curated file wins. Bootstrap only fills gaps and empty crosswalk ids."""
    out = dict(old)
    for k, v in new.items():
        if k == "crosswalk":
            cw = dict(out.get("crosswalk", {}))
            for ck, cv in v.items():
                if cw.get(ck) is None and cv is not None:
                    cw[ck] = cv
            out["crosswalk"] = cw
        elif k not in out or out[k] is None:
            out[k] = v
        # else: key already present in curated file -> keep it (manual wins).
    return out


def load_existing() -> dict[str, tuple[Path, dict]]:
    existing: dict[str, tuple[Path, dict]] = {}
    for f in OUT_DIR.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        existing[data["id"]] = (f, data)
    return existing


def main() -> int:
    if not RAW.exists():
        print(f"missing {RAW} — run the curl in tools/wikidata-circunscricoes.rq first",
              file=sys.stderr)
        return 1
    rows = list(csv.DictReader(RAW.open(encoding="utf-8")))
    items = aggregate(rows)
    existing = load_existing()

    written, filled, excluded, deferred = 0, 0, [], []
    seen_slugs: dict[str, str] = {}

    for entity_url, raw in sorted(items.items()):
        item_q = qid(entity_url)
        if item_q in EXCLUDE_ITEMS:
            excluded.append((item_q, raw["label"] or "", EXCLUDE_ITEMS[item_q]))
            continue
        tipo, reason = classify(raw["tipos"])
        if tipo is None:
            excluded.append((qid(entity_url), raw["label"] or "", reason))
            continue
        if tipo not in STANDARD_TIPOS:
            deferred.append((qid(entity_url), raw["label"] or "", tipo))
            continue
        rec = build_record(entity_url, raw, tipo)
        slug = rec["id"]
        if slug in seen_slugs and seen_slugs[slug] != entity_url:
            print(f"WARN duplicate slug {slug}: {entity_url} vs {seen_slugs[slug]}",
                  file=sys.stderr)
        seen_slugs[slug] = entity_url

        if slug in existing:
            path, old = existing[slug]
            merged = merge_preserving_manual(old, rec)
            if merged != old:
                path.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
                filled += 1
        else:
            (OUT_DIR / f"{slug}.json").write_text(
                json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            written += 1

    with EXCLUDED_REPORT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["qid", "label", "reason"])
        w.writerows(sorted(excluded))

    with DEFERRED_REPORT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["qid", "label", "tipo"])
        w.writerows(sorted(deferred))

    print(f"items seen         : {len(items)}")
    print(f"new files written  : {written}")
    print(f"existing filled    : {filled} (manual fields preserved)")
    print(f"excluded (noise)   : {len(excluded)} -> {EXCLUDED_REPORT.relative_to(ROOT)}")
    print(f"deferred (future)  : {len(deferred)} -> {DEFERRED_REPORT.relative_to(ROOT)}")
    print(f"total in data/     : {len(list(OUT_DIR.glob('*.json')))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
