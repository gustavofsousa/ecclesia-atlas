# Changelog

## [Não lançado]

### Adicionado

- `tools/ibge-municipios.json` — referência oficial dos 5.571 municípios do Brasil (Fase 1-B, 1B.1), baixada da API do IBGE via `tools/fetch-ibge-municipios.py`.
- `validate.py` agora confere `territorio.municipios_ibge` contra essa referência e garante que nenhum município seja reivindicado por duas circunscrições.
- **Fase 1-B, 1B.2 (piloto):** `territorio.municipios_ibge` preenchido para as 26 arquidioceses/dioceses-sé de capital estadual (468 municípios ao todo), curado manualmente via Wikipédia/GCatholic cruzado com a referência IBGE. 24 com `granularidade_territorial: municipio`; 2 sub-municipais genuínas (Macapá, São Paulo).
- **Fase 1-B, 1B.2 (completo):** `territorio.municipios_ibge` preenchido para as 240 circunscrições restantes (4.610 códigos IBGE), 121 via curadoria manual página a página (Wikipédia como fonte primária) e 120 via proxy GCatholic aceito diretamente como fonte primária. 8 conflitos de município reivindicado por duas circunscrições resolvidos — incluindo o caso do município de São Paulo capital, removido de 3 dioceses sufragâneas por ser jurisdição sub-municipal (regiões episcopais), não coberta pelo proxy por município. `validate.py` verde nos 266 arquivos; só Boa Vista (prelazia, deferida) segue sem território.
- **Fase 1-B, 1B.2 (reconciliação):** as 128 circunscrições em `confianca: media` (proxy GCatholic) foram revisadas por pesquisa dirigida em lotes pequenos com saída JSON estruturada. Uma primeira rodada contaminada por confusão de tabela wiki/nomes de paróquia foi revertida integralmente antes de aplicar. A rodada final elevou 55 circunscrições para `confianca: alta`, resolveu 16 novos conflitos de município (a maioria nomes homônimos genéricos como São João/São Francisco/Gramado existindo em regiões distantes do mesmo estado) por adjacência geográfica real. Total agora: 5.027 códigos IBGE, 163 `alta` / 102 `media`. `validate.py` verde nos 266 arquivos.
- **Fase 1-B, 1B.2 (reconciliação final):** as 102 circunscrições que restaram em `confianca: media` foram resolvidas por uma segunda rodada de pesquisa dirigida (12 lotes pequenos, JSON estruturado, fonte declarada por item — Wikipédia própria/it/es, site oficial da diocese ou GCatholic como último recurso, com nomes descartados por serem distrito/vizinho já sinalizados na própria pesquisa). 101 circunscrições elevadas para `confianca: alta`; 1 (Diocese de Teófilo Otoni) manteve `confianca: media` por não haver fonte territorial explícita disponível — mantida a lista anterior em vez de zerá-la. 13 novos conflitos de município duplicado resolvidos por adjacência geográfica real e não por confiança declarada, incluindo dois casos de precedente histórico documentado (São Valentim do Sul, transferido para Caxias do Sul em 1966; Rondolândia, MT, mantida em Juína) e um caso sub-municipal (Diocese de São Miguel Paulista, enclave na Zona Leste de São Paulo capital, `granularidade_territorial: submunicipal`). Total agora: 5.328 códigos IBGE, 264 `alta` / 1 `media` / 1 `baixa` (Teresina, débito pré-existente fora desta reconciliação). `validate.py` verde nos 266 arquivos.
- **Fase 1-B, 1B.3 (GeoJSON derivado):** `tools/fetch-municipios-malha.py` baixa `tools/municipios-malha.geojson` do `tbrugz/geodata-br` (CC0, id = código IBGE de 7 dígitos, fonte provisória — não cobre 7 municípios criados após a geração da malha). `tools/build-geojson.py` une os polígonos por circunscrição (`shapely`) e gera `dist/circunscricoes.geojson` (262 features, 6,3MB), versionado no git. Descoberto en passant: Diocese de Santo Amaro tem `granularidade_territorial: municipio` com `territorio.municipios_ibge` vazio (débito pré-existente, fora do escopo desta reconciliação) — pulada pelo build. Fecha o critério de "pronto" da Fase 1-B.

### Corrigido

- README (PT/EN) e `docs/data-model.md` apontavam `data/circunscricoes/ordinariado-militar-do-brasil.json` como exemplo — arquivo nunca existiu na v0 (Ordinariado Militar ficou deferido desde a Fase 1-A, ver `tools/wikidata-deferred.csv`). Exemplo de `curl` no README trocado para `prelazia-de-borba.json` (existe, tipo `prelazia_territorial`); nota em `data-model.md` esclarece que a v0 ainda não tem um registro real do caso `pessoal`.

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
