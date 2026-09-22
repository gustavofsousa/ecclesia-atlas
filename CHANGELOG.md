# Changelog

## [Não lançado]

### Adicionado

- `tools/ibge-municipios.json` — referência oficial dos 5.571 municípios do Brasil (Fase 1-B, 1B.1), baixada da API do IBGE via `tools/fetch-ibge-municipios.py`.
- `validate.py` agora confere `territorio.municipios_ibge` contra essa referência e garante que nenhum município seja reivindicado por duas circunscrições.
- **Fase 1-B, 1B.2 (piloto):** `territorio.municipios_ibge` preenchido para as 26 arquidioceses/dioceses-sé de capital estadual (468 municípios ao todo), curado manualmente via Wikipédia/GCatholic cruzado com a referência IBGE. 24 com `granularidade_territorial: municipio`; 2 sub-municipais genuínas (Macapá, São Paulo).
- **Fase 1-B, 1B.2 (completo):** `territorio.municipios_ibge` preenchido para as 240 circunscrições restantes (4.610 códigos IBGE), 121 via curadoria manual página a página (Wikipédia como fonte primária) e 120 via proxy GCatholic aceito diretamente como fonte primária. 8 conflitos de município reivindicado por duas circunscrições resolvidos — incluindo o caso do município de São Paulo capital, removido de 3 dioceses sufragâneas por ser jurisdição sub-municipal (regiões episcopais), não coberta pelo proxy por município. `validate.py` verde nos 266 arquivos; só Boa Vista (prelazia, deferida) segue sem território.
- **Fase 1-B, 1B.2 (reconciliação):** as 128 circunscrições em `confianca: media` (proxy GCatholic) foram revisadas por pesquisa dirigida em lotes pequenos com saída JSON estruturada. Uma primeira rodada contaminada por confusão de tabela wiki/nomes de paróquia foi revertida integralmente antes de aplicar. A rodada final elevou 55 circunscrições para `confianca: alta`, resolveu 16 novos conflitos de município (a maioria nomes homônimos genéricos como São João/São Francisco/Gramado existindo em regiões distantes do mesmo estado) por adjacência geográfica real. Total agora: 5.027 códigos IBGE, 163 `alta` / 102 `media`. `validate.py` verde nos 266 arquivos.

## [v0.1.0] - 2026-09-18

### Adicionado

- Schema inicial (`schema/circunscricao.schema.json`) para circunscrições eclesiásticas.
- Registro de exemplo validando o schema: uma arquidiocese com território (Arquidiocese de São Salvador da Bahia). O exemplo de circunscrição pessoal sem território (Ordinariado Militar do Brasil) foi movido para o backlog deferido na Fase 1-A — o schema segue cobrindo o caso `pessoal`/`sem_territorio`.
- Modelo de proveniência por campo (valor + fonte + data de verificação + confiança) — ver CONTRIBUTING.md.
- Licença MIT para o código, CC BY 4.0 para os dados.
- ROADMAP.md com todas as fases e o anti-escopo; docs públicos em português.
- Query SPARQL inicial para bootstrap das circunscrições a partir do Wikidata (`tools/wikidata-circunscricoes.rq`).
- **Fase 1-A (bootstrap):** 266 circunscrições — dioceses e arquidioceses territoriais de rito latino, o padrão e comum — geradas a partir do Wikidata (`tools/wikidata-to-json.py`), todas com `metodo: "automatico"` e proveniência por campo. Popula nome, tipo, jurisdição, data de ereção (P571), site oficial (P856), coordenada (P625), QID e GCatholic ID (P8389). A curadoria humana existente é preservada — o merge nunca sobrescreve campo `metodo: "manual"`.
- Campos `site_oficial` e `coordenada` (ponto representativo, não fronteira) adicionados ao schema.
- `tools/validate.py` — validação por `jsonschema` + invariantes de domínio (jurisdição pessoal ⇒ sem território; `id` = nome do arquivo; `id`/QID únicos). Serve também como gate de CI.
- CI `.github/workflows/validate.yml` roda a validação em cada push/PR.
- `tools/wikidata-excluded.csv` — 18 itens descartados como ruído (sés extintas/suprimidas, diocese anglicana, igreja ortodoxa, províncias eclesiásticas).
- `tools/wikidata-deferred.csv` — 16 circunscrições católicas válidas porém fora do escopo atual, anotadas para fases futuras (prelazias territoriais, eparquias/exarcado de rito oriental, ordinariado militar e oriental). Nada é descartado em silêncio.
