# Ecclesia Atlas

> Open, versioned, field-sourced dataset of the Catholic Church's ecclesiastical structure in Brazil.

**Status:** early scaffold — schema and contribution model only, no real dataset yet. Personal project for now; will move to an org once there are outside contributors.

## Why this exists

Anyone building something Catholic in Brazil — a parish app, a diocesan tool, a personal project — ends up rebuilding the same foundation from scratch: which ecclesiastical circumscriptions exist, what province and CNBB regional they belong to, which municipalities they cover, who the current bishop is. The data exists, but it's scattered across institutional sites, PDFs, and Wikipedia, with no stable identifiers and no way to know how reliable any given fact is.

Ecclesia Atlas is that missing layer: a **dataset**, not an app. Structure and rules first. Liturgical texts and Bible translations are explicitly out of scope — those have licensed owners (see [DATA_LICENSE.md](DATA_LICENSE.md)).

## What this is not

- Not a super-app (prayer + mass times + confession + donations).
- Not a parish management / CRM system — see `ecclesiacrm`, and the CNBB's own CDIC project (Centro de Dados da Igreja Católica no Brasil, announced April 2026), which owns that space.
- Not an authoritative registry. It's an open layer with declared provenance, pointing back to primary sources (Wikidata, GCatholic, Catholic-Hierarchy, and eventually CDIC once it publishes).
- Not a redistribution of copyrighted liturgical texts or Bible translations.

## Data model

See [docs/data-model.md](docs/data-model.md): the three orthogonal axes (community / place / territory), the Brazilian ecclesiastical hierarchy, and the modeling traps this schema deliberately accounts for (CNBB Regional vs. Ecclesiastical Province, territorial vs. personal jurisdictions, IBGE municipalities as the atomic territorial unit).

## Provenance model

Every non-structural fact (name, erection date, current bishop, territory) carries its own source, verification date, and confidence level — not one blanket "source" field per record. See [CONTRIBUTING.md](CONTRIBUTING.md).

## No server, on purpose

v0 is flat JSON files under `data/`, validated against `schema/circunscricao.schema.json`. No API, no database, no required infrastructure to consume it — read the files directly from GitHub (raw or via a CDN like jsDelivr) or clone the repo. A read API can sit on top later without changing how the data is stored.

## License

- **Code** (schema, tooling): [MIT](LICENSE).
- **Data** (`data/`): [CC BY 4.0](DATA_LICENSE.md) — see that file for the reasoning and an important disclaimer.

## Open questions

A handful of decisions are deliberately still open and will be resolved in a dedicated roadmap pass rather than guessed at here: how much of Brazil's territorial coverage actually fits the IBGE-municipality assumption, whether to build a liturgical calendar engine (`Ordo`) in-house or contribute upstream to `romcal`, posture toward the CNBB's CDIC project as it matures, and the final MVP cut (parish-level data is a different order of magnitude from diocese-level and is deliberately not started here).
