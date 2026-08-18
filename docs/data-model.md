# Data model

## Three orthogonal axes

A parish and a church building are not the same thing. Conflating them is the most common modeling mistake in this space.

```
COMMUNITY (canonical legal person)   ─┐
  diocese, parish, quasi-parish       │
                                       ├── linked by n:n relations
PLACE (building, coordinate)         ─┤    with temporal validity
  mother church, chapel, shrine       │
                                       │
TERRITORY (polygon / coverage)       ─┘
  set of municipalities or sub-areas
```

Two cross-cutting axes:

- **PERSON / OFFICE** — bishop, diocesan administrator, parish priest. Always with a validity window (`valido_de`). A vacant see is a normal state, not an error.
- **EVENT** — mass, confession, adoration. Weekly recurrence plus exceptions driven by the liturgical calendar. This is why a future "mass times" layer would depend on a liturgical calendar engine, not just this dataset.

This split mirrors what [OpenChurch](https://github.com/hozana/openchurch) (Hozana, France) already runs in production: `Community` / `Place`, linked by a `parentCommunityId`.

## Brazilian ecclesiastical hierarchy

```
Holy See
└── Episcopal Conference (CNBB)
    ├── CNBB Regional (19)              ← administrative, NOT canonical
    └── Ecclesiastical Province          ← canonical (metropolitan + suffragans)
        └── Ecclesiastical Circumscription
            ├── Archdiocese / Diocese
            ├── Territorial Prelature
            ├── Eparchy / Archeparchy (Eastern rites)
            ├── Exarchate
            ├── Military Ordinariate
            ├── Ordinariate for Eastern-rite faithful
            └── Personal Apostolic Administration   ← no territory
                └── [internal subdivisions — vary per diocese]
                    ├── Episcopal Region / Vicariate
                    ├── Deanery / Forane vicariate (Can. 553–555)
                    └── Parish (Can. 515)  ← legal person
                        ├── Quasi-parish / pastoral area
                        └── Community / filial chapel
                            └── Building
                                ├── Mother church, chapel, oratory
                                └── Titles: cathedral, co-cathedral, basilica, shrine
```

## Modeling traps this schema accounts for

1. **CNBB Regional ≠ Ecclesiastical Province.** Regional is an administrative grouping of the episcopal conference (19 units, some spanning multiple states); Province is a canonical structure. A Regional contains one or more Provinces — model as independent fields, not a hierarchy. See `regional_cnbb` and `provincia_eclesiastica` in the schema.
2. **Not every circumscription has a territory.** Military Ordinariates and Personal Apostolic Administrations are personal, not territorial. `territorio` is nullable, gated by `tipo_jurisdicao: territorial | pessoal`. See `data/circunscricoes/ordinariado-militar-do-brasil.json` for a worked example.
3. **Personal parishes exist** (Can. 518) — by rite, language, or group. Two parishes can legitimately cover the same geography. Not yet modeled at the parish tier (out of scope for v0), but the circumscription-level schema doesn't assume geographic exclusivity.
4. **Internal subdivision names aren't standardized.** "Forane", "comarca", "deanery", "forane vicariate", "episcopal region" name similar things differently per diocese. Store the local label *and* a normalized type — not modeled yet at v0 (circumscription tier only), flagged for the parish-tier schema.
5. **Territorial granularity is irregular.** Most dioceses are defined by whole municipalities, but some metropolitan areas split sub-municipally (e.g. the Archdiocese of São Paulo is organized into 6 episcopal regions). `granularidade_territorial: municipio | submunicipal | indefinido` flags the exception.
6. **Names change; entities persist.** Dioceses are created, split, renamed, and elevated to archdioceses. The canonical `id` must not be re-derived when the name changes. v0 uses a human-readable slug for the ID (good enough while everything is hand-curated); switching to an opaque stable ID (ULID) if the current-name-derived slug ever becomes ambiguous is a known, deferred follow-up.

## Territory: IBGE municipalities as the atomic unit

Diocesan territory in Brazil is, in practice, defined by the list of municipalities it covers. IBGE's municipal mesh is open, official data. So:

- The atomic record is `circumscription_id × ibge_municipality_code`.
- Any GeoJSON is *derived* by unioning the IBGE mesh — never hand-maintained.
- A boundary update becomes a CSV/JSON row, not a cartography task.
- Known exception: sub-municipal cases (trap #5) — left as `granularidade_territorial: submunicipal` with no geometry in v0.

This is deliberately unvalidated at scale — see the "Open questions" section in the README.

## External identifiers (crosswalk)

A record is only reusable if it has a stable ID plus bridges to identifiers that already exist: Wikidata QID, GCatholic.org, Catholic-Hierarchy.org, and a reserved (currently empty) slot for a future CNBB CDIC identifier. The canonical ID is always our own slug — never an external ID used as primary key, since external IDs can be wrong, missing, or change ownership.
