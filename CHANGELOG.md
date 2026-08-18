# Changelog

## [Não lançado]

### Adicionado

- Schema inicial (`schema/circunscricao.schema.json`) para circunscrições eclesiásticas.
- Dois registros de exemplo validando o schema: uma arquidiocese com território (Arquidiocese de São Salvador da Bahia) e uma circunscrição pessoal, sem território (Ordinariado Militar do Brasil).
- Modelo de proveniência por campo (valor + fonte + data de verificação + confiança) — ver CONTRIBUTING.md.
- Licença MIT para o código, CC BY 4.0 para os dados.
- ROADMAP.md com todas as fases e o anti-escopo; docs públicos em português.
- Query SPARQL inicial para bootstrap das circunscrições a partir do Wikidata (`tools/wikidata-circunscricoes.rq`).
