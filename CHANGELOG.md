# Changelog

## [Não lançado]

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
