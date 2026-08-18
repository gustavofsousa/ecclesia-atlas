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

- Schema das circunscrições (`schema/circunscricao.schema.json`) com proveniência por campo.
- Dois registros de exemplo validando os casos-limite: arquidiocese territorial (Bahia) e circunscrição pessoal sem território (Ordinariado Militar).
- Licença dupla: MIT (código) + CC BY 4.0 (dados).
- Modelo de contribuição por issue/PR com `confianca` honesta.

---

## Fase 1 — Atlas v1: as ~280 circunscrições 🔜 (é o próximo passo real)

O único entregável que importa agora. São ~280 circunscrições — ordem de grandeza pequena, curável à mão em poucos dias. Paróquias (milhares) são outra ordem de magnitude e **não** entram aqui.

**É aqui que entra o "scraping das dioceses"** — mas a primeira fonte não é HTML frágil, e sim dado estruturado:

- **1a. Bootstrap via Wikidata (SPARQL).** Mesmo caminho que o OpenChurch usa. Popula id, nome, tipo, QID, coordenada, província e bispo atual onde existir. Query inicial em `tools/wikidata-circunscricoes.rq`.
- **1b. Território via malha do IBGE.** Tabela `circunscricao × código IBGE de município`. GeoJSON é *derivado* por união da malha, nunca desenhado à mão. Onde o Wikidata não cobre a lista de municípios, cai para curadoria manual a partir da Wikipédia (campo *Territory*) e sites diocesanos — **este** é o "scraping" residual, e é o menor pedaço.
- **1c. Curadoria manual dos ~280.** Preencher lacunas, marcar `confianca` honesta, resolver as armadilhas de modelagem (Regional CNBB ≠ Província, jurisdição pessoal vs. territorial, granularidade submunicipal).
- **1d. Validação em CI.** GitHub Action rodando o `jsonschema` contra todos os arquivos em cada PR.
- **1e. Primeiro release público.** Tag `v0.1.0`, tornar o repositório público, submeter ao `awesome-catholic`.

**Pronto quando:** as ~280 circunscrições existem como arquivos válidos, com `regional_cnbb` e `provincia_eclesiastica` preenchidos, e um release imutável publicado.

---

## Fase 2 — Distribuição e API 🔜

Onde entra a ideia de API. Três níveis, do mais barato ao mais caro — só sobe de nível quando o anterior aperta.

- **Nível 0 — CDN estática (grátis, já disponível).** Ler os JSON via raw GitHub ou jsDelivr. Já é uma API de leitura sem infra. Provavelmente resolve 90% dos consumidores.
- **Nível 1 — Agregados de build.** Passo que compila os registros individuais em `all.json` + GeoJSON derivado do IBGE, publicados como artefatos de release. Continua estático e versionado.
- **Nível 2 — API de query (condicional).** REST/GraphQL serverless, somente leitura, gerada a partir do mesmo dado do Git. **Nunca** fonte da verdade — sempre derivada. Só se houver demanda real por busca/filtro que os arquivos estáticos não atendem.

**Pronto quando:** existe pelo menos o Nível 1 e um exemplo de consumo documentado.

---

## Fase 3 — Ordo (motor litúrgico) 🔮

Calendário, tempos, solenidades, precedência, cores, ciclos A/B/C e I/II. **Regra, não texto** → livre de direito autoral, determinístico, testável. Responde "hoje é a Assunção, solenidade, cor branca, 1ª leitura Ap 11,19a…" — a **referência**, não o texto.

**Decisão em aberto [ABERTO-3]:** contribuir com o Próprio do Brasil upstream no `romcal` vs. motor próprio. Reaproveitar é mais barato e mais provável de sobreviver. Avaliar antes de escrever código.

---

## Fase 4 — Scribe (ingestão assistida) 🔮

OCR/IA para extrair dados de boletins, PDFs e comunicados, com fluxo de sugestão que vira PR. **Só depois** de existir modelo de dados estável, política de fontes e gente disposta a validar. Começar por aqui é o erro clássico do nicho.

---

## Reservado — talvez nunca 🧊

Namespaces guardados para não fecharmos a porta, sem plano de construção.

- **Hora — horários de missa/confissão/adoração.** 🚫 Não construir. Depende de Atlas + Ordo, mas o mercado já está servido: **DinDonDan** (https://dindondan.app/), **Horários de Missa** e afins. É o quadrante de maior custo de manutenção e menor defensabilidade. Se algum dia fizer sentido, é consumindo/complementando esses, não competindo.
- **Encontrar — app "ache uma missa perto de você".** 🚫 Não construir, pela mesma razão de `Hora`.
- **Motor de Direito Canônico** — prazos processuais, impedimentos matrimoniais (Cân. 1091), *Computus* pascal com transferências. Público real (tribunais eclesiásticos), mas nicho estreito e alta exigência de correção jurídica. Não é MVP.
- **Monorepo do Magistério** — Ordinário da Missa (latim/português), orações tradicionais, Próprio dos Santos do Brasil. ⚠️ Verificar licença texto a texto antes de qualquer coisa.
- **Liturgia das Horas** — parser das regras da IGLH (saltério de 4 semanas, antífonas, hinos) para a realidade brasileira.

---

## Não vamos construir (anti-escopo)

Registrar isto evita meses de deriva.

- ❌ CRM / sistema de gestão diocesana ou paroquial — o CDIC (CNBB) e o `ecclesiacrm` já ocupam esse espaço.
- ❌ Redistribuição de textos litúrgicos ou traduções bíblicas — direito autoral.
- ❌ Ser a fonte oficial/autoritativa — esse é o papel do CDIC. Nós somos a ponte aberta e versionada por cima.

---

## Decisões em aberto (carregadas do documento-mãe)

| # | Decisão | Bloqueia | Estado |
|---|---|---|---|
| ABERTO-2 | Cobertura territorial: % de circunscrições que fecham exatamente por município IBGE | Modelo de território | 🟡 Pesquisa na Fase 1 |
| ABERTO-3 | `Ordo` próprio vs. contribuir com `romcal` | Fase 3 | 🟡 Estratégico |
| ABERTO-5 | Standalone vs. fundir com OpenChurch (Hozana) | Escopo | 🟢 Resolvido: standalone compatível |
| ABERTO-6 | Postura frente ao CDIC/CNBB | Posicionamento | 🟡 Acompanhar |
| ABERTO-9 | Governança: mantenedor único → org → associação | Sustentabilidade | 🟢 Depois |
| ABERTO-4 | Licença de dados | Publicação | 🟢 Resolvido: CC BY 4.0 (revisar juridicamente) |

---

## Janela CDIC

O Centro de Dados da Igreja Católica no Brasil foi aprovado em abril de 2026, com 20 dioceses piloto. O portal público **ainda não saiu** — há uma janela. Quando sair, o Atlas é a camada que o consome, normaliza, versiona e casa com IBGE/Wikidata em formato de desenvolvedor. Por isso o campo `crosswalk.cdic_id` já está reservado no schema desde a Fase 0. O CDIC é *fonte potencial*, não concorrente — se o posicionamento for construído certo desde o início.
