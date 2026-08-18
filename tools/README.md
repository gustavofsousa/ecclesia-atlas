# tools/

Scripts de ingestão e validação. Comentários em inglês por serem código; ver `../ROADMAP.md` Fase 1 para o contexto.

- `wikidata-circunscricoes.rq` — query SPARQL inicial para popular as circunscrições a partir do Wikidata (bootstrap da Fase 1-A). Classe-base `Q665487` e propriedades P8389/P856 confirmadas na `scripts/synchro.py` do OpenChurch. Ainda **rascunho** para a propriedade do bispo e para o Catholic-Hierarchy ID — conferir no endpoint antes de gerar arquivos em `../data/`.

## Próximos scripts (Fase 1)

- `validate.py` — roda o `jsonschema` contra todos os arquivos em `data/` (vira também um GitHub Action).
- `wikidata-to-json.py` — transforma o CSV do SPARQL em arquivos por circunscrição, já no formato de proveniência (`fonte: wikidata`, `confianca: media`).
- ingestão de território: junta a lista de municípios por circunscrição com a malha do IBGE.
