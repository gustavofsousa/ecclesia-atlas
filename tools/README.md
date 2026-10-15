# tools/

Scripts de ingestão e validação. Comentários em inglês por serem código; ver `../ROADMAP.md` Fase 1 para o contexto.

- `wikidata-circunscricoes.rq` — query SPARQL para popular as circunscrições a partir do Wikidata (bootstrap da Fase 1-A). Classe-base `Q665487`, filtrada por país = Brasil (`P17 = Q155`). A propriedade de bispo (P6) mostrou-se imprecisa e **não** é usada no bootstrap (bispo fica `nao_verificado`).
- `wikidata-to-json.py` — transforma `wikidata-raw.csv` em um arquivo por circunscrição em `../data/circunscricoes/`, no formato de proveniência (`fonte: wikidata`, `confianca: media`, `metodo: automatico`). Mapeamento de tipo explícito e auditável; **nunca sobrescreve campo `metodo: manual`** de um arquivo já curado (só preenche lacunas). Escopo atual = `STANDARD_TIPOS` (diocese + arquidiocese). Ruído → `wikidata-excluded.csv`; circunscrições válidas fora do escopo atual (prelazia, rito oriental, ordinariados) → `wikidata-deferred.csv`, para fases futuras.
- `validate.py` — roda `jsonschema` + invariantes de domínio contra todos os arquivos em `../data/`. Também verifica `territorio.municipios_ibge`: todo código deve existir em `ibge-municipios.json`, e nenhum município pode pertencer a mais de uma circunscrição. É também o gate do CI (`.github/workflows/validate.yml`).
- `requirements.txt` — dependências (jsonschema, shapely) para rodar `validate.py`/`build-geojson.py` local e no CI.
- `ibge-municipios.json` — referência oficial dos 5.571 municípios do Brasil (`codigo_ibge` de 7 dígitos, `nome`, `uf`), baixada de `servicodados.ibge.gov.br/api/v1/localidades/municipios`. Usada pelo `validate.py` para checar `municipios_ibge` na Fase 1-B; regenerar com o comando abaixo se o IBGE criar/alterar municípios.
- `fetch-municipios-malha.py` — baixa `municipios-malha.geojson` da API de malhas v3 do IBGE (qualidade `intermediaria`). Normaliza `codarea` para `properties.id` (código IBGE de 7 dígitos). **Não versionado** (12MB, `.gitignore`) — é cache intermediário reproduzível, ao contrário de `ibge-municipios.json`. Relata os municípios de `ibge-municipios.json` sem geometria na malha (hoje só Boa Esperança do Norte/MT, instalado em 2025 e fora de qualquer circunscrição).
- `ibge_tls.py` + `certs/` — contexto TLS dos dois scripts `fetch-*`. O servidor do IBGE não envia o certificado intermediário da Sectigo; o script soma esse intermediário (público, versionado em `certs/`) às raízes do sistema, com a verificação ligada. Remover quando o IBGE servir a cadeia completa.
- `build-geojson.py` — gera `../dist/circunscricoes.geojson` unindo (`shapely.ops.unary_union`) os polígonos dos municípios de cada circunscrição com `granularidade_territorial: municipio`. Falha se o reparo de topologia (`buffer(0)`) apagar a área de um município. Artefato **derivado**: nunca editar à mão, regenerar após qualquer mudança em `territorio.municipios_ibge`. Circunscrições sub-municipais/indefinidas ou sem lista de município ficam de fora (relatado no stdout).
- `build-all-json.py` — gera `../dist/all.json`: array com todos os registros, ordenado por `id`, cada item idêntico ao seu arquivo em `data/` (Fase 2, Nível 1). Determinístico (sem timestamp), então o arquivo só muda quando o dado muda. Artefato **derivado**: nunca editar à mão. `--check` falha se o arquivo estiver desatualizado em relação a `data/`, e roda no CI.

### Reproduzir o bootstrap

```sh
curl -s -H "Accept: text/csv" \
  --data-urlencode "query@tools/wikidata-circunscricoes.rq" \
  https://query.wikidata.org/sparql > tools/wikidata-raw.csv
python3 tools/wikidata-to-json.py
python3 tools/validate.py
```

`wikidata-raw.csv` e `wikidata-excluded.csv` são artefatos regeneráveis; ficam versionados como evidência da rodada.

### Regenerar o GeoJSON derivado

```sh
python3 tools/fetch-municipios-malha.py   # baixa a malha (não versionada, precisa rodar antes do build)
python3 tools/build-geojson.py
```

### Publicar um release

Todo release leva os dois agregados de `dist/` como assets (Fase 2, Nível 1).

```sh
python3 tools/validate.py
python3 tools/build-all-json.py
python3 tools/fetch-municipios-malha.py && python3 tools/build-geojson.py
# CHANGELOG com [vX.Y.Z] - AAAA-MM-DD, via PR; depois do merge em main:
gh release create vX.Y.Z dist/all.json dist/circunscricoes.geojson --target main --notes-file <notas.md>
```
