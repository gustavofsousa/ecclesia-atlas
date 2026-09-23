# Ecclesia Atlas

> Base de dados aberta, versionada e com proveniência por campo da estrutura eclesiástica da Igreja Católica no Brasil.

*Open, versioned, field-sourced dataset of the Catholic Church's ecclesiastical structure in Brazil.*

**Status:** rumo ao `v0.2.0` (ainda não lançado — ver [ROADMAP.md](ROADMAP.md)) — 266 circunscrições (215 dioceses + 48 arquidioceses + 3 prelazias territoriais), com regional CNBB, província eclesiástica e **território municipal completo** (5.027 códigos IBGE, 163 circunscrições em confiança alta / 102 em média). Boa Vista (prelazia) segue sem território, fora de escopo por ora. Repositório pessoal por enquanto; migra para uma organização quando houver contribuidores de fora.

*Heading toward `v0.2.0` (not yet released — see [ROADMAP.md](ROADMAP.md)) — 266 ecclesiastical circumscriptions (215 dioceses + 48 archdioceses + 3 territorial prelatures), each with CNBB region, ecclesiastical province, and **complete municipal territory** (5,027 IBGE municipality codes, 163 circumscriptions at high confidence / 102 at medium). Boa Vista (prelature) still lacks territory, out of scope for now. Personal repo for now; migrates to an org once outside contributors show up.*

## Por que isto existe

Quem quer construir qualquer coisa católica no Brasil — um app de paróquia, uma ferramenta diocesana, um projeto pessoal — acaba reconstruindo a mesma base do zero: quais circunscrições eclesiásticas existem, a que província e regional da CNBB pertencem, quais municípios cobrem, quem é o bispo atual. O dado existe, mas espalhado em sites institucionais, PDFs e Wikipédia, sem identificador estável e sem como saber o quão confiável é cada informação.

O Ecclesia Atlas é essa camada que falta: um **dataset**, não um app. Estrutura e regras primeiro. Textos litúrgicos e traduções da Bíblia estão explicitamente fora de escopo — têm donos licenciados (ver [DATA_LICENSE.md](DATA_LICENSE.md)).

### Why this exists

Anyone building anything Catholic in Brazil — a parish app, a diocesan tool, a side project — ends up rebuilding the same foundation from scratch: which ecclesiastical circumscriptions exist, which CNBB province and region they belong to, which municipalities they cover, who the current bishop is. The data exists, but scattered across institutional websites, PDFs, and Wikipedia, with no stable identifier and no way to know how reliable any given fact is.

Ecclesia Atlas is that missing layer: a **dataset**, not an app. Structure and rules first. Liturgical texts and Bible translations are explicitly out of scope — they have licensed owners (see [DATA_LICENSE.md](DATA_LICENSE.md)).

## O que isto NÃO é

- Não é um super-app (oração + horários de missa + confissão + doação).
- Não é um sistema de gestão paroquial / CRM — ver `ecclesiacrm`, e o próprio projeto CDIC da CNBB (Centro de Dados da Igreja Católica no Brasil, anunciado em abril de 2026), que ocupa esse espaço.
- Não é fonte oficial. É uma camada aberta, com proveniência declarada, que aponta de volta para as fontes primárias (Wikidata, GCatholic, Catholic-Hierarchy e, no futuro, o CDIC quando publicar).
- Não é redistribuição de textos litúrgicos ou traduções bíblicas protegidas por direito autoral.

### What this is NOT

- Not a super-app (prayer + Mass times + confession + donations).
- Not a parish management system / CRM — see `ecclesiacrm`, and CNBB's own CDIC project (Centro de Dados da Igreja Católica no Brasil, announced April 2026), which already occupies that space.
- Not an official source. It's an open layer, with declared provenance, that points back to primary sources (Wikidata, GCatholic, Catholic-Hierarchy, and eventually CDIC once it publishes).
- Not a redistribution of copyrighted liturgical texts or Bible translations.

## Roadmap

O plano completo — todas as fases, o que é reservado e o que não será construído — está em [ROADMAP.md](ROADMAP.md).

The full plan — every phase, what's deferred, and what will never be built — lives in [ROADMAP.md](ROADMAP.md).

## Onde entra a API?

Resumo (detalhe no [ROADMAP.md](ROADMAP.md), Fase 2): a API **não** é a Fase 1 e **nunca** é a fonte da verdade — o dado versionado no Git é. A API é uma camada de consumo derivada, em três níveis:

1. **Nível 0 (já disponível, zero infra):** ler os arquivos JSON direto do GitHub (raw) ou por uma CDN como o jsDelivr. Isto já é uma "API de leitura" estática.
2. **Nível 1:** um passo de build que compila os registros em arquivos agregados (`all.json`, GeoJSON derivado da malha do IBGE), publicados como artefatos de release.
3. **Nível 2 (condicional):** uma API REST/GraphQL serverless de leitura — só se houver demanda que justifique a manutenção.

### Where does the API fit in?

Summary (detail in [ROADMAP.md](ROADMAP.md), Phase 2): the API is **not** Phase 1 and is **never** the source of truth — the versioned Git data is. The API is a derived consumption layer, in three tiers:

1. **Tier 0 (already available, zero infra):** read the JSON files straight from GitHub (raw) or a CDN like jsDelivr. This is already a static "read API."
2. **Tier 1:** a build step that compiles records into aggregate files (`all.json`, GeoJSON derived from the IBGE mesh), published as release artifacts.
3. **Tier 2 (conditional):** a serverless REST/GraphQL read API — only if demand justifies the upkeep.

## Ver o dado agora

O repositório é público; cada circunscrição é um arquivo JSON. Sem instalar nada:

```bash
# via jsDelivr (CDN, com cache)
curl -s https://cdn.jsdelivr.net/gh/gustavofsousa/ecclesia-atlas@main/data/circunscricoes/arquidiocese-de-sao-salvador-da-bahia.json

# ou direto do GitHub (raw)
curl -s https://raw.githubusercontent.com/gustavofsousa/ecclesia-atlas/main/data/circunscricoes/prelazia-de-borba.json
```

```js
const base = "https://cdn.jsdelivr.net/gh/gustavofsousa/ecclesia-atlas@main";
const arq = await fetch(`${base}/data/circunscricoes/arquidiocese-de-sao-salvador-da-bahia.json`)
  .then((r) => r.json());
console.log(arq.nome.valor, "—", arq.tipo);
```

> Dica: fixe uma tag de release (ex.: `@v0.1.0` assim que for lançada) em vez de `@main` para consumo estável.

### See the data now

The repo is public; each circumscription is one JSON file. No install required:

```bash
# via jsDelivr (CDN, cached)
curl -s https://cdn.jsdelivr.net/gh/gustavofsousa/ecclesia-atlas@main/data/circunscricoes/arquidiocese-de-sao-salvador-da-bahia.json

# or straight from GitHub (raw)
curl -s https://raw.githubusercontent.com/gustavofsousa/ecclesia-atlas/main/data/circunscricoes/prelazia-de-borba.json
```

```js
const base = "https://cdn.jsdelivr.net/gh/gustavofsousa/ecclesia-atlas@main";
const arq = await fetch(`${base}/data/circunscricoes/arquidiocese-de-sao-salvador-da-bahia.json`)
  .then((r) => r.json());
console.log(arq.nome.valor, "—", arq.tipo);
```

> Tip: pin a release tag (e.g. `@v0.1.0` once cut) instead of `@main` for stable consumption.

## Sem servidor, de propósito

A v0 é JSON plano em `data/`, validado contra `schema/circunscricao.schema.json`. Sem API obrigatória, sem banco, sem infraestrutura para consumir. Isso é o antídoto contra o modo de falha nº 1 do nicho: o projeto precisa continuar útil mesmo se ficar seis meses sem manutenção.

### Serverless, on purpose

v0 is plain JSON under `data/`, validated against `schema/circunscricao.schema.json`. No mandatory API, no database, no infrastructure needed to consume it. This is the antidote to the niche's #1 failure mode: the project has to stay useful even if it goes unmaintained for six months.

## Modelo de dados

Ver [docs/data-model.md](docs/data-model.md): os três eixos ortogonais (comunidade / lugar / território), a hierarquia eclesiástica brasileira e as armadilhas de modelagem que este schema trata de propósito.

### Data model

See [docs/data-model.md](docs/data-model.md) for the three orthogonal axes (community / place / territory), the Brazilian ecclesiastical hierarchy, and the modeling pitfalls this schema deliberately handles.

## Modelo de proveniência

Todo fato não-estrutural (nome, data de ereção, bispo atual, território) carrega a própria fonte, data de verificação e nível de confiança — não um campo "fonte" único por registro. Ver [CONTRIBUTING.md](CONTRIBUTING.md).

### Provenance model

Every non-structural fact (name, erection date, current bishop, territory) carries its own source, verification date, and confidence level — not a single "source" field per record. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

- **Código** (schema, ferramentas): [MIT](LICENSE).
- **Dados** (`data/`): [CC BY 4.0](DATA_LICENSE.md) — ver o arquivo para o raciocínio e um aviso legal importante.

### License

- **Code** (schema, tools): [MIT](LICENSE).
- **Data** (`data/`): [CC BY 4.0](DATA_LICENSE.md) — see the file for the reasoning and an important legal notice.
