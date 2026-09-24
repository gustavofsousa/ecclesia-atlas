# Roadmap — Ecclesia Atlas

> Documento vivo. Fases não têm data; têm ordem e critério de "pronto".

## Princípios que ordenam tudo

1. **Dado antes de aplicação.** O ativo é o dataset com proveniência. App gera usuários que somem; dado confiável gera dependência positiva no ecossistema.
2. **Regras antes de textos.** Construímos o motor e o esqueleto (livres de direito autoral). Os textos litúrgicos/bíblicos têm dono — são injetados por quem tem licença, nunca redistribuídos aqui.
3. **Uma coisa bem-feita.** O foco é o **Atlas**. Todo o resto é namespace reservado até o Atlas existir de verdade.
4. **Sobreviver à inatividade.** Dado em arquivos versionados, releases imutáveis, zero infra obrigatória. Se ninguém tocar por seis meses, ainda funciona.

## Grafo de dependência

```
                    Ecclesia Atlas  ← raiz, não depende de ninguém
                    (dados)
                         │
        ┌────────────────┼────────────────┐
        │                │                │
       API            Ordo             Scribe
    (leitura)       (regras)         (ingestão)
        │                │
        └───────┬────────┘
                │
              Hora  (horários — mercado já servido, ver Reservado)
                │
            Encontrar  (vitrine — NÃO construir)
```

Leitura: **tudo depende do Atlas.** Começar pelo app (`Encontrar`) ou pela IA (`Scribe`) é começar pela folha. Por isso a ordem abaixo.

Legenda: ✅ feito · 🔜 próximo · 🔮 futuro · 🧊 reservado (talvez nunca) · 🚫 não construir.

---

## Fase 0 — Fundação ✅

Feito em 2026-08-18.

- Schema das circunscrições (`schema/circunscricao.schema.json`) com proveniência por campo, incluindo `metodo: automatico | manual` (o bootstrap nunca sobrescreve curadoria humana).
- Dois registros de exemplo validando os casos-limite: arquidiocese territorial (Bahia) e circunscrição pessoal sem território (Ordinariado Militar).
- Licença dupla: MIT (código) + CC BY 4.0 (dados).
- Modelo de contribuição por issue/PR com `confianca` honesta; política de validade em `docs/staleness.md`.
- Repositório público.

---

## Fase 1 — Atlas: as ~280 circunscrições 🔜 (próximo passo real)

São ~280 circunscrições — ordem de grandeza pequena, curável à mão. Paróquias (milhares) são outra ordem de magnitude e **não** entram aqui.

A Fase 1 tem uma vara longa escondida: montar a lista de municípios por circunscrição (território) é provavelmente maior que todo o resto somado, porque a cobertura do Wikidata para isso é fraca e o restante vira curadoria manual em ~280 páginas. Fazer o `v0.1.0` esperar por essa parte é exatamente o modo de falha documentado. Então a Fase 1 é **quebrada em duas entregas**, e o dataset já é útil na primeira — "quais são as circunscrições e a que regional/província pertencem" já é dado que ninguém tem limpo.

### Fase 1-A — Estrutura, sem território → `v0.1.0`

- **1A.1 Bootstrap via Wikidata (SPARQL). ✅** Classe-base confirmada: `wd:Q665487` (diocese), filtrada por `wdt:P17 = wd:Q155` (Brasil). Popula id, nome, tipo, QID, GCatholic (P8389), site (P856), coordenada (P625), data de ereção (P571). Query em `tools/wikidata-circunscricoes.rq`, transformada por `tools/wikidata-to-json.py`, adaptada da `scripts/synchro.py` do OpenChurch. Tudo que o script escreve entra como `metodo: "automatico"`. Bispo atual ficou `nao_verificado` (P6 é impreciso para bispo diocesano — deferido para curadoria).
  - **Escopo: o padrão e comum** — dioceses e arquidioceses territoriais de rito latino, **mais 3 prelazias territoriais** (Borba, Cametá, Coari) que o Wikidata trazia como diocese e foram reclassificadas na curadoria. **Resultado (2026-08-18): 266 circunscrições** (215 dioceses + 48 arquidioceses + 3 prelazias territoriais), o seed manual de Salvador preservado no merge.
  - Dos 300 itens do Wikidata: **18 descartes de ruído** (sés extintas/suprimidas, diocese anglicana, igreja ortodoxa, províncias) em `tools/wikidata-excluded.csv`; **16 deferidos para fases futuras** em `tools/wikidata-deferred.csv` — prelazias territoriais, eparquias/arquieparquias/exarcado de rito oriental, ordinariado militar e ordinariado oriental. Nada dropado em silêncio. Fazer bem o caso comum primeiro; o resto é escopo declarado de fase futura (não anti-escopo).
- **1A.2 Curadoria manual. ✅ (2026-08-18)** `regional_cnbb` (19 regionais da CNBB) e `provincia_eclesiastica {id, papel}` preenchidos nos 266 a partir das tabelas de província do GCatholic — o bootstrap os deixou `null` de propósito por não haver fonte automática confiável. **Modelo de referência**: `provincia_eclesiastica.id` aponta para o slug da **arquidiocese-sé** (um arquivo que existe); metropolitanas auto-referenciam, sufragâneas apontam para sua sé. Integridade referencial verificada nos 266. Território fica `granularidade_territorial: indefinido`. Ressalva honesta: a fonte marcou `confianca: alta` de forma uniforme, e o schema atual não persiste confiança/fonte para esses dois campos — vale verificação pontual.
- **1A.3 Validação em CI. ✅** `tools/validate.py` (jsonschema + invariantes de domínio) e GitHub Action `.github/workflows/validate.yml` rodando em cada push/PR. Verde no PR #1.
- **1A.4 Release `v0.1.0`** (tag imutável) + divulgação (ver abaixo). ⏳ PR #1 aberto e verde; falta o merge humano em `main` e a tag.

**Pronto quando:** as ~280 circunscrições existem como arquivos válidos, com `regional_cnbb` e `provincia_eclesiastica` preenchidos, e um release imutável publicado.

### Fase 1-B — Território → `v0.2.0`

- **1B.1 Malha do IBGE. ✅ (2026-09-18)** `tools/ibge-municipios.json` — referência oficial dos 5.571 municípios do Brasil (`codigo_ibge` 7 dígitos, `nome`, `uf`), baixada de `servicodados.ibge.gov.br` por `tools/fetch-ibge-municipios.py`. `validate.py` agora confere todo `territorio.municipios_ibge` contra essa lista e garante que nenhum município pertença a duas circunscrições ao mesmo tempo. GeoJSON continua *derivado* por união da malha depois que 1B.2 povoar os dados, nunca desenhado à mão.
- **1B.2 Lista de municípios por circunscrição. ✅ (2026-09-22, reconciliação final)** Cobertura completa das 266 circunscrições (265 + Boa Vista deferida como prelazia, fora do escopo 1-A). **Piloto das 26 capitais estaduais (2026-09-18)**: 24 com `granularidade_territorial: municipio` (468 municípios), 2 sub-municipais genuínas (Macapá, São Paulo). Processo página a página: Wikipédia como primeira fonte, GCatholic `churches/local/<gcatholic_id>` como fallback, todo nome cruzado contra `tools/ibge-municipios.json`. **Curadoria manual das 240 restantes (2026-09-22)**: 121 via Wikipédia, as outras 120 via proxy GCatholic (`confianca: media`, aceito sem checagem individual — débito técnico registrado). **Reconciliação via pesquisa dirigida, 1ª rodada (2026-09-22)**: as 128 circunscrições em `confianca: media` foram revisadas por pesquisa em 13 lotes pequenos (Perplexity, saída JSON estruturada). Uma primeira rodada (v1, lotes markdown maiores) veio contaminada — confundiu tabelas de "província eclesiástica"/dioceses vizinhas da Wikipédia com território real, e trocou nomes de município por nomes de paróquia geograficamente distantes — e foi revertida por completo antes de tocar nos dados. A v2, com lotes menores e prompt proibindo extração de tabelas de vizinhança, veio limpa: dos 128 resultados, só 5 nomes bateram com sé de circunscrição vizinha (2 contaminação real — "Barra" e "Santa Maria", nomes de sé confundidos com município homônimo distante — descartados; 3 já eram o caso conhecido de São Paulo capital). 55 elevadas para `alta`, 16 conflitos resolvidos por adjacência geográfica real. **Reconciliação via pesquisa dirigida, 2ª rodada / final (2026-09-22)**: as 102 circunscrições que restaram em `media` foram fechadas em 12 lotes v3 (mesmo formato JSON estruturado, `fonte_usada`/nomes descartados/nota por item; 6 lotes vieram como `.json`, 6 como `.md` com o mesmo JSON dentro de um bloco de código — extraídos e tratados como equivalentes). 101 elevadas para `alta`; só Diocese de Teófilo Otoni ficou em `media` porque a pesquisa não achou fonte territorial explícita e a lista anterior foi preservada em vez de zerada (regra: pesquisa sem fonte melhor não regride o dado existente). 13 novos conflitos de município resolvidos por adjacência geográfica real e não por confiança declarada, incluindo 2 casos de precedente histórico já documentado (São Valentim do Sul → Diocese de Caxias do Sul desde 1966; Rondolândia/MT → Diocese de Juína, mesmo estado) e 1 sub-municipal novo (Diocese de São Miguel Paulista, enclave na Zona Leste da capital paulistana, `granularidade_territorial: submunicipal`, sem o código de São Paulo para não duplicar com Osasco). **Total final: 5.328 códigos IBGE, 266 arquivos `metodo: manual`, 264 `confianca: alta` / 1 `media` (Teófilo Otoni) / 1 `baixa` (Arquidiocese de Teresina, débito pré-existente fora desta reconciliação).** `validate.py` verde nos 266 arquivos. Débito residual: os pares de nomes ambíguos das duas rodadas ficam registrados aqui como precedente para futura curadoria; Teófilo Otoni e Teresina seguem como candidatos a uma pesquisa dedicada futura.
- **1B.3 GeoJSON derivado. ✅ (2026-09-23)** `tools/build-geojson.py` une (`shapely.ops.unary_union`) os polígonos dos municípios de cada circunscrição com `granularidade_territorial: municipio`, a partir de `tools/municipios-malha.geojson` (baixado por `tools/fetch-municipios-malha.py`). Fonte da malha: `tbrugz/geodata-br` (CC0, `properties.id` = código IBGE de 7 dígitos, sem mapeamento necessário) — **provisória**, escolhida por ser um arquivo único já pronto; não cobre 7 municípios criados após a geração da malha (Mojuí dos Campos/PA, Nazária/PI, Pescaria Brava/SC, Balneário Rincão/SC, Pinto Bandeira/RS, Paraíso das Águas/MS, Boa Esperança do Norte/MT), afetando 5 circunscrições com um município a menos no polígono unido (Santarém, Teresina, Coxim, Criciúma, Tubarão) — buraco pequeno, não invalida a geometria. Trocar pela malha oficial do IBGE (`geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais`) quando uma rodada de qualidade maior for justificada. `dist/circunscricoes.geojson` (262 features, 6,3MB) versionado no git — consistente com o resto do dataset, disponível via raw GitHub/jsDelivr sem esperar release (Fase 2, Nível 0). **Débito descoberto**: Diocese de Santo Amaro tem `granularidade_territorial: municipio` mas `territorio.municipios_ibge: []` (inconsistência pré-existente da rodada `bfb9042`, fora do escopo desta reconciliação) — pulada pelo build, candidata a correção pontual futura. Sub-municipais (Macapá, São Paulo/Osasco, São Miguel Paulista) seguem sem geometria por ora, como previsto.

**Pré-requisito de estudo — CONFIRMADO (2026-09-18):** o `kburchfiel/us_diocese_mapper` já validou a aposta no IBGE (agregação por unidade administrativa, não geometria desenhada à mão) — ABERTO-2 de-riscado por precedente. Reconfirmação direta para o Brasil: query SPARQL testada contra P527 ("has part") e P150 ("contains administrative territorial entity") nas ~280 dioceses/arquidioceses — **0 resultados em ambas**, Wikidata não tem esse relacionamento estruturado para o Brasil. A Wikipédia pt também não é uniforme: algumas páginas trazem a lista em prosa direta (ex. Arquidiocese de São Salvador da Bahia: "abrange os municípios de Itaparica, Lauro de Freitas, Salinas da Margarida, Salvador e Vera Cruz"), outras só têm o dado implícito na tabela de paróquias (ex. Diocese de Criciúma: "26 municípios", sem lista). **Conclusão: não há atalho automático — 1B.2 é curadoria manual página a página, como o roadmap já previa**, sem fonte estruturada única para basear um script de bootstrap.

**Pronto quando:** território municipal preenchido para a maioria das circunscrições, com GeoJSON derivado publicado como artefato de release. ✅ Fase 1-B completa (2026-09-23).

### Divulgação (no release do `v0.1.0`)

O canal mais eficiente não é o `awesome-catholic` — é onde o público do nicho já está:

- Comentar na **issue #17 do `Dancrf/liturgia-diaria`** (194★, pede dumps JSON desde jun/2024) apresentando o Atlas. Escopo não sobrepõe: ele tem texto (com dono), nós temos estrutura.
- Abrir issue/contato no **`allanfrizzo/liturgia-catolica-api`** (recente, OpenAPI bem-feito).
- Submeter ao **`awesome-catholic`**.
- Mandar uma mensagem à **Hozana (OpenChurch)** — custo zero, pode render a coisa mais escassa do projeto: uma segunda pessoa.

---

## Fase 2 — Distribuição e API 🔜

Onde entra a ideia de API. Três níveis, do mais barato ao mais caro — só sobe de nível quando o anterior aperta.

- **Nível 0 — CDN estática (grátis, já disponível).** Ler os JSON via raw GitHub ou jsDelivr. Já é uma API de leitura sem infra. Provavelmente resolve 90% dos consumidores.
- **Nível 1 — Agregados de build.** Passo que compila os registros individuais em `all.json` + GeoJSON derivado do IBGE, publicados como artefatos de release. Continua estático e versionado.
- **Nível 2 — API de query (condicional).** REST/GraphQL serverless, somente leitura, gerada a partir do mesmo dado do Git. **Nunca** fonte da verdade — sempre derivada. Só se houver demanda real por busca/filtro que os arquivos estáticos não atendem.

**Pronto quando:** existe pelo menos o Nível 1 e um exemplo de consumo documentado (já há um snippet no README).

---

## Fase 3 — Ordo (motor litúrgico) 🔮

Calendário, tempos, solenidades, precedência, cores, ciclos A/B/C e I/II. **Regra, não texto** → livre de direito autoral, determinístico, testável. Responde "hoje é a Assunção, solenidade, cor branca, 1ª leitura Ap 11,19a…" — a **referência**, não o texto.

**Decisão em aberto [ABERTO-3]:** contribuir com o Próprio do Brasil upstream no `romcal` vs. motor próprio. Reaproveitar é mais barato e mais provável de sobreviver. Avaliar antes de escrever código.

**Arquitetura a copiar se for motor próprio:** `miggalvez/officium-novum` separa dado, lógica rubrical e apresentação em camadas distintas — estudar antes de projetar. Não abrir agora.

---

## Fase 4 — Scribe (ingestão assistida) 🔮

OCR/IA para extrair dados de boletins, PDFs e comunicados, com fluxo de sugestão que vira PR. **Só depois** de existir modelo de dados estável, política de fontes e gente disposta a validar. Começar por aqui é o erro clássico do nicho.

---

## Reservado — talvez nunca 🧊

Namespaces guardados para não fecharmos a porta, sem plano de construção.

- **Hora — horários de missa/confissão/adoração.** 🚫 Não construir. Depende de Atlas + Ordo, mas o mercado já está servido: **DinDonDan** (https://dindondan.app/), **Horários de Missa** e afins. É o quadrante de maior custo de manutenção e menor defensabilidade.
- **Encontrar — app "ache uma missa perto de você".** 🚫 Não construir, pela mesma razão de `Hora`.
- **Motor de Direito Canônico** — prazos processuais, impedimentos matrimoniais (Cân. 1091), *Computus* pascal com transferências. Público real (tribunais eclesiásticos), nicho estreito, alta exigência de correção jurídica. Não é MVP.
- **Monorepo do Magistério** — Ordinário da Missa (latim/português), orações tradicionais, Próprio dos Santos do Brasil. ⚠️ Verificar licença texto a texto antes de qualquer coisa.
- **Liturgia das Horas** — parser das regras da IGLH (saltério de 4 semanas, antífonas, hinos) para a realidade brasileira.

---

## Não vamos construir (anti-escopo)

- ❌ CRM / sistema de gestão diocesana ou paroquial — o CDIC (CNBB) e o `ecclesiacrm` já ocupam esse espaço.
- ❌ Redistribuição de textos litúrgicos ou traduções bíblicas — direito autoral. Isso inclui **não** citar `bibliaAveMariaJSON` como fonte (circular publicamente não é licença).
- ❌ Ser a fonte oficial/autoritativa — esse é o papel do CDIC. Nós somos a ponte aberta e versionada por cima.

---

## Decisões (registro)

| # | Decisão | Estado |
|---|---|---|
| ABERTO-1 | Nome/namespace | 🟢 **Resolvido:** `gustavofsousa/ecclesia-atlas`. A colisão do nome nu "Ecclesia" (org `ecclesia`, `ecclesiacrm`) é contornada porque o namespace é a **conta pessoal**, não a org `ecclesia`. Só isso já resolve. A marca "Ecclesia Atlas" mora nos releases/docs, não no slug do repo — que é descartável e renomeável. Migra para org quando houver contribuidores de fora. |
| ABERTO-2 | Granularidade territorial (municípios cobrem quanto %?) | 🟢 **De-riscado por precedente** (US mapper agrega por unidade administrativa; casos divididos são minoria manual). Reconfirmar a proporção no Brasil ao entrar na Fase 1-B. |
| ABERTO-4 | Licença de dados | 🟢 **Resolvido:** CC BY 4.0 (revisar juridicamente antes de tratar como definitivo). |
| ABERTO-5 | Standalone vs. OpenChurch | 🟢 **Resolvido: standalone, sem compromisso de compatibilidade.** O OpenChurch é *precedente* (modelo Community/Place, proveniência por campo, bootstrap SPARQL), não um contrato — sustentar compatibilidade fica mais caro conforme o schema cresce. Conversar com a Hozana continua valendo, pela pessoa, não pela interop. |
| ABERTO-10 | Idioma | 🟢 **Resolvido:** dados e nomes de campo em pt-BR (o domínio é brasileiro e "circunscrição eclesiástica" não tem tradução precisa); comentários de código/schema em inglês; README bilíngue. Ver `docs/data-model.md`. |
| ABERTO-3 | `Ordo` próprio vs. `romcal` upstream | 🟡 Estratégico — decidir na Fase 3. |
| ABERTO-6 | Postura frente ao CDIC/CNBB | 🟡 Acompanhar. |
| ABERTO-9 | Governança: mantenedor único → org → associação | 🟢 Depois. |

---

## Janela CDIC

O Centro de Dados da Igreja Católica no Brasil foi aprovado em abril de 2026, com 20 dioceses piloto. O portal público **ainda não saiu** — há uma janela. Quando sair, o Atlas é a camada que o consome, normaliza, versiona e casa com IBGE/Wikidata em formato de desenvolvedor. Por isso o campo `crosswalk.cdic_id` já está reservado no schema desde a Fase 0. O CDIC é *fonte potencial*, não concorrente.

**Precedente concreto para a postura:** na Itália, a conferência episcopal (CEI, `OrariMesse`) e um projeto de voluntários (`OrarioSanteMesse`) coexistem no mesmo mercado há anos sem se aniquilar. Modelo institucional e modelo comunitário não se anulam — é o argumento mais tangível caso um dia haja conversa com a CNBB (vale como argumento, não como código).
