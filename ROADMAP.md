# Roadmap — Ecclesia Atlas

> Modelo: [ROADMAP-projeto-PADRAO](../_hq/biblioteca/roadmaps/ROADMAP-projeto-PADRAO.md) (versões, features com tag de domínio, débito).
> Documento vivo. Fases não têm data; têm ordem e critério de "pronto".
> Histórico detalhado: [CHANGELOG.md](CHANGELOG.md). Como consumir o dado: [docs/consumo.md](docs/consumo.md).

> - **Status:** ✅ feito · ⚠️ feito com débito · 🔄 em andamento · 🗓️ planejado · ⚪ sem spec · 🔒 bloqueado.
> - **Domínio ≠ Feature:** domínio é a parte durável do dado; feature é a unidade de entrega. Cada linha leva a tag do domínio.
> - **SemVer:** MINOR = entrega de valor no dataset ou na distribuição · `0.x` = Atlas em construção.
> - **Invariante:** no máximo 1 item 🔄 por vez.

**Princípios que ordenam tudo:**
1. **Dado antes de aplicação.** O ativo é o dataset com proveniência.
2. **Regras antes de textos.** Textos litúrgicos têm dono; nunca são redistribuídos aqui.
3. **Uma coisa bem-feita.** O foco é o Atlas. O resto é namespace reservado até o Atlas existir de verdade.
4. **Sobreviver à inatividade.** Dado em arquivos versionados, releases imutáveis, zero infra obrigatória.

**Dependências:** tudo depende do Atlas. Ordo e Scribe dependem do modelo de dados estável.

---

## Visão geral (uma tela)

| Versão | Fase | Alvo da fase | Domínios | Status |
|--------|------|--------------|----------|--------|
| v0.1.0 | Atlas — estrutura | ~280 circunscrições como arquivos válidos, com regional e província | `dados` | ✅ |
| v0.2.0 | Atlas — território | municípios por circunscrição e GeoJSON derivado | `territorio`, `distribuicao` | ✅ |
| v0.3.0 | Distribuição | o dado é lido sem infra: CDN e agregado de build | `distribuicao` | ✅ |
| v0.4 | Consumo | tabelas planas para planilha e análise | `distribuicao` | 🔄 |
| — | Ordo | motor litúrgico (regra, não texto) | `ordo` | ⚪ |
| — | Scribe | ingestão assistida por IA, em PR | `scribe` | ⚪ |

---

## v0.1.0 — Atlas: estrutura ✅ *(release 2026-09-18)*
**Alvo atingido:** as circunscrições existem como arquivos válidos, com `regional_cnbb` e `provincia_eclesiastica` preenchidos.
**Escopo:** o padrão comum (dioceses e arquidioceses territoriais de rito latino, mais 3 prelazias). Eparquias, ordinariados e paróquias ficam para fases futuras.

| Feature | Domínio | Slice | Status |
|---------|---------|-------|--------|
| fundação: schema com proveniência por campo, licença dupla (MIT + CC BY 4.0), contribuição por PR | `dados` | Fase 0 | ✅ |
| bootstrap via Wikidata (SPARQL), 266 circunscrições, descartes e deferidos registrados em CSV | `dados` | 1A.1 | ✅ |
| curadoria de regional CNBB e província eclesiástica | `dados` | 1A.2 | ✅ |
| validação em CI (`validate.py` + GitHub Action) | `— ops` | 1A.3 | ✅ |
| release `v0.1.0` imutável | `— ops` | 1A.4 | ✅ |

## v0.2.0 — Atlas: território ✅ *(release 2026-10-02)*
**Alvo atingido:** cada circunscrição tem a lista de municípios do IBGE que a compõe, e o GeoJSON sai derivado dessa lista.

| Feature | Domínio | Slice | Status |
|---------|---------|-------|--------|
| malha oficial dos 5.571 municípios e validação de unicidade | `territorio` | 1B.1 | ✅ |
| lista de municípios por circunscrição (5.328 códigos IBGE) | `territorio` | 1B.2 | ✅ *(débitos abaixo)* |
| GeoJSON derivado por união da malha (261 polígonos) | `distribuicao` | 1B.3 | ⚠️ *(5 sub-municipais sem geometria; malha provisória)* |

## v0.3.0 — Distribuição ✅ *(release 2026-10-02)*
**Alvo atingido:** o dado é lido sem infra própria.

| Feature | Domínio | Slice | Status |
|---------|---------|-------|--------|
| Nível 0 — leitura pela CDN estática (raw GitHub ou jsDelivr) | `distribuicao` | Fase 2 N0 | ✅ |
| Nível 1 — `all.json` agregado, gerado de forma determinística e checado no CI | `distribuicao` | Fase 2 N1 | ✅ |

## v0.4 — Consumo 🔄 *(sem release)*
**Alvo:** tabelas planas que respondem "a que circunscrição pertence este município?" com uma leitura.

| Feature | Domínio | Slice | Status |
|---------|---------|-------|--------|
| tabelas planas em `dist/` (`circunscricoes.csv`, `municipios.csv`, `municipios.json`) e guia de consumo com contrato de estabilidade | `distribuicao` | — | 🔄 *(branch `feat/tabelas-de-consumo`, não mesclada)* |

## Próximos pilares ⚪

| Feature | Domínio | Status | Gatilho |
|---------|---------|--------|---------|
| Ordo — motor litúrgico: calendário, precedência, cores, ciclos A/B/C e I/II | `ordo` | ⚪ | decidir ABERTO-3 (`romcal` upstream ou motor próprio) antes de escrever código |
| Scribe — OCR/IA para boletins e PDFs, com fluxo de sugestão que vira PR | `scribe` | ⚪ | modelo de dados estável, política de fontes e um validador humano |
| Nível 2 — API de query (REST/GraphQL), somente leitura, derivada do Git | `distribuicao` | ⚪ | demanda real de busca e filtro que os arquivos estáticos não atendem |

---

## Domínios (referência)
- **dados** — schema, proveniência, bootstrap e curadoria das circunscrições.
- **territorio** — malha IBGE, lista de municípios, unicidade entre circunscrições.
- **distribuicao** — CDN, agregados de build, tabelas planas, guia de consumo.
- **ordo** — motor litúrgico (futuro). **scribe** — ingestão assistida (futuro).
- **— ops** — CI, validação, release (suporte).

> Os domínios ainda não têm `dominios.md`. Esta lista é a fonte até lá.

## Débito herdado das fases fechadas

| ID | Origem | Status | Gatilho de revisita |
|----|--------|--------|---------------------|
| Listas incompletas em circunscrições `alta`: 244 municípios sem circunscrição (SC 39, PI 27, PA 25, AM 23, MA 21 e outros) | v0.2.0 | aberto | próxima rodada de pesquisa dirigida, invertida: "a que circunscrição pertence o município Y?" |
| Teófilo Otoni em `media`; Teresina em `baixa` | v0.2.0 | aberto | pesquisa dedicada |
| 5 sub-municipais sem geometria (Arquidiocese de São Paulo, Santo Amaro, Campo Limpo, São Miguel Paulista, Osasco) | v0.2.0 | aberto | schema de geometria parcial ou fonte de malha intra-urbana |
| Malha provisória (`tbrugz/geodata-br`), sem 7 municípios recentes | v0.2.0 | aberto | trocar pela malha oficial do IBGE na próxima rodada de qualidade |
| Municípios divididos entre duas circunscrições ficam com a majoritária | v0.2.0 | aceito | só vira trabalho se o schema ganhar "município parcial" |
| Prelazias territoriais fora de escopo (8 em `tools/wikidata-deferred.csv`) | v0.1.0 | aceito | fase futura de prelazias |

## Fora de escopo (decisão de não fazer)
- 🚫 Horários de missa e app "ache uma missa perto de você" — o mercado já tem DinDonDan e afins. Custo de manutenção alto e pouca defensabilidade.
- 🚫 CRM ou sistema de gestão diocesana ou paroquial — CDIC (CNBB) e `ecclesiacrm` ocupam o espaço.
- 🚫 Redistribuição de textos litúrgicos ou traduções bíblicas — direito autoral. Não citar `bibliaAveMariaJSON` como fonte.
- 🚫 Ser a fonte oficial — esse papel é do CDIC. Nós somos a ponte aberta e versionada por cima.
- 🧊 Motor de Direito Canônico, Liturgia das Horas, Monorepo do Magistério — talvez nunca. Sem plano de construção.

## Divulgação
- ⏳ Comentar na issue #17 do `Dancrf/liturgia-diaria` apresentando o Atlas.
- ⏳ Comentário de atualização sobre o `v0.2.0` na issue #1 do `allanfrizzo/liturgia-catolica-api` (sem resposta desde 2026-09-18).
- ⏳ Submeter ao `CatholicOS/awesome-catholic` (a outra lista ativa; `servusdei2018/awesome-catholic` já listou o projeto).
- ⏳ Mensagem à Hozana (OpenChurch) por contato direto. Repo `hozana/openchurch` não aceita issues de fora.

## Decisões

Tomadas:
- **Nome:** repo em `gustavofsousa/ecclesia-atlas`. A marca "Ecclesia Atlas" mora nos releases e docs.
- **Standalone:** sem compromisso de compatibilidade com o OpenChurch; ele é precedente, não contrato.
- **Idioma:** dados e campos em pt-BR; código e schema em inglês; README bilíngue (`docs/data-model.md`).
- **Licença:** CC BY 4.0 para dados (revisar juridicamente antes de tratar como definitivo).

Em aberto:
- **ABERTO-3** — `Ordo` próprio ou contribuir com o Próprio do Brasil no `romcal`. Decidir na fase Ordo.
- **ABERTO-6** — postura frente ao CDIC/CNBB. Acompanhar; o portal público ainda não saiu.
- **ABERTO-9** — governança: mantenedor único → org → associação. Depois.

## Contexto
O Centro de Dados da Igreja Católica no Brasil (CDIC) foi aprovado em abril de 2026, com 20 dioceses piloto. O portal público ainda não saiu. Quando sair, o Atlas consome, normaliza, versiona e casa com IBGE e Wikidata. Por isso o campo `crosswalk.cdic_id` já está no schema. O CDIC é fonte potencial, não concorrente.
