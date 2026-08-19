# tools/

Scripts de ingestão e validação. Comentários em inglês por serem código; ver `../ROADMAP.md` Fase 1 para o contexto.

- `wikidata-circunscricoes.rq` — query SPARQL para popular as circunscrições a partir do Wikidata (bootstrap da Fase 1-A). Classe-base `Q665487`, filtrada por país = Brasil (`P17 = Q155`). A propriedade de bispo (P6) mostrou-se imprecisa e **não** é usada no bootstrap (bispo fica `nao_verificado`).
- `wikidata-to-json.py` — transforma `wikidata-raw.csv` em um arquivo por circunscrição em `../data/circunscricoes/`, no formato de proveniência (`fonte: wikidata`, `confianca: media`, `metodo: automatico`). Mapeamento de tipo explícito e auditável; **nunca sobrescreve campo `metodo: manual`** de um arquivo já curado (só preenche lacunas). Escopo atual = `STANDARD_TIPOS` (diocese + arquidiocese). Ruído → `wikidata-excluded.csv`; circunscrições válidas fora do escopo atual (prelazia, rito oriental, ordinariados) → `wikidata-deferred.csv`, para fases futuras.
- `validate.py` — roda `jsonschema` + invariantes de domínio contra todos os arquivos em `../data/`. É também o gate do CI (`.github/workflows/validate.yml`).
- `requirements.txt` — dependências (jsonschema) para rodar `validate.py` local e no CI.

### Reproduzir o bootstrap

```sh
curl -s -H "Accept: text/csv" \
  --data-urlencode "query@tools/wikidata-circunscricoes.rq" \
  https://query.wikidata.org/sparql > tools/wikidata-raw.csv
python3 tools/wikidata-to-json.py
python3 tools/validate.py
```

`wikidata-raw.csv` e `wikidata-excluded.csv` são artefatos regeneráveis; ficam versionados como evidência da rodada.

## Próximos scripts (Fase 1-B)

- ingestão de território: junta a lista de municípios por circunscrição com a malha do IBGE.
