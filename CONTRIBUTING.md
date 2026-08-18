# Contributing

## The provenance model

Every non-structural fact on a record — name, erection date, current bishop, territory — is stored as a small object, not a bare value:

```json
{
  "valor": "...",
  "fonte": "wikidata",
  "fonte_url": "https://www.wikidata.org/wiki/...",
  "verificado_em": "2026-08-18",
  "confianca": "alta | media | baixa | nao_verificado"
}
```

This is what makes the dataset auditable instead of "a spreadsheet on the internet": anyone can see *who* said a fact was true and *when it was last checked*, and can disagree at the field level instead of the whole record.

## Submitting a correction

1. Open an issue or PR pointing at the specific file in `data/circunscricoes/`.
2. State the field, the new value, and a source — a URL is enough (official diocesan site, Wikidata, GCatholic, Catholic-Hierarchy, news coverage of an episcopal appointment, etc.).
3. Set `confianca` honestly. `nao_verificado` is a valid, expected value — better than a confident guess.
4. Don't submit liturgical texts, Bible translations, or anything else with a licensed owner — facts and structural rules only (names, dates, hierarchy, territory), never copyrighted text. See [DATA_LICENSE.md](DATA_LICENSE.md).

## Schema changes

The schema lives in `schema/circunscricao.schema.json`. Changes there affect every existing record — open an issue first to discuss before sending a PR that changes the schema itself.

## Adding a new circumscription

Copy the shape of an existing file in `data/circunscricoes/`, fill in what you can verify, and leave everything else with `confianca: "nao_verificado"` rather than guessing. A partially-filled, honestly-labeled record is useful; a fully-filled, unsourced one is not.
