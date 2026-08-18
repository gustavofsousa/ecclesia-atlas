# Modelo de dados

## Três eixos ortogonais

Uma paróquia e um edifício de igreja não são a mesma coisa. Confundir os dois é o erro de modelagem mais comum deste nicho.

```
COMUNIDADE (pessoa jurídica canônica)  ─┐
  diocese, paróquia, quase-paróquia      │
                                          ├── ligadas por relações
LUGAR (edifício, coordenada)           ─┤    n:n com validade temporal
  matriz, capela, santuário              │
                                          │
TERRITÓRIO (polígono / cobertura)      ─┘
  conjunto de municípios ou sub-áreas
```

Dois eixos transversais:

- **PESSOA / OFÍCIO** — bispo, administrador diocesano, pároco. Sempre com janela de validade (`valido_de`). Sé vacante é um estado normal, não um erro.
- **EVENTO** — missa, confissão, adoração. Recorrência semanal mais exceções ditadas pelo calendário litúrgico. É por isso que uma futura camada de "horários de missa" dependeria de um motor litúrgico, não só deste dataset.

Essa separação espelha o que o [OpenChurch](https://github.com/hozana/openchurch) (Hozana, França) já roda em produção: `Community` / `Place`, ligados por `parentCommunityId`.

## Hierarquia eclesiástica brasileira

```
Santa Sé
└── Conferência Episcopal (CNBB)
    ├── Regional CNBB (19)               ← administrativo, NÃO canônico
    └── Província Eclesiástica            ← canônico (metropolitana + sufragâneas)
        └── Circunscrição Eclesiástica
            ├── Arquidiocese / Diocese
            ├── Prelazia Territorial
            ├── Eparquia / Arquieparquia (ritos orientais)
            ├── Exarcado
            ├── Ordinariado Militar
            ├── Ordinariado para orientais
            └── Administração Apostólica Pessoal   ← sem território
                └── [subdivisões internas — variam por diocese]
                    ├── Região Episcopal / Vicariato
                    ├── Decanato / Vicariato Forâneo (Cân. 553–555)
                    └── Paróquia (Cân. 515)  ← pessoa jurídica
                        ├── Quase-paróquia / área pastoral
                        └── Comunidade / capela filial
                            └── Edifício
                                ├── Matriz, capela, oratório
                                └── Títulos: catedral, concatedral, basílica, santuário
```

## Armadilhas de modelagem que este schema trata

1. **Regional CNBB ≠ Província Eclesiástica.** Regional é agrupamento administrativo da conferência (19 unidades, algumas cobrindo vários estados); Província é estrutura canônica. Um Regional contém uma ou mais Províncias — modelar como campos independentes, não como hierarquia. Ver `regional_cnbb` e `provincia_eclesiastica` no schema.
2. **Nem toda circunscrição tem território.** Ordinariado Militar e Administração Apostólica Pessoal são pessoais, não territoriais. `territorio` é nullable, controlado por `tipo_jurisdicao: territorial | pessoal`. Exemplo real em `data/circunscricoes/ordinariado-militar-do-brasil.json`.
3. **Paróquias pessoais existem** (Cân. 518) — por rito, língua ou grupo. Duas paróquias podem cobrir o mesmo espaço geográfico legitimamente. Ainda não modelado no nível de paróquia (fora do escopo da v0), mas o schema de circunscrição não assume exclusividade geográfica.
4. **Nomes de subdivisões internas não são padronizados.** "Foraine", "comarca", "decanato", "vicariato forâneo", "região episcopal" nomeiam coisas parecidas de formas diferentes por diocese. Guardar o rótulo local *e* um tipo normalizado — ainda não modelado na v0 (só o nível de circunscrição), sinalizado para o schema de paróquia.
5. **Granularidade territorial é irregular.** A maioria das dioceses se define por municípios inteiros, mas algumas regiões metropolitanas dividem sub-municipalmente (ex.: a Arquidiocese de São Paulo é organizada em 6 regiões episcopais). `granularidade_territorial: municipio | submunicipal | indefinido` sinaliza a exceção.
6. **Nomes mudam; entidades persistem.** Dioceses são criadas, desmembradas, renomeadas e elevadas a arquidioceses. O `id` canônico não pode ser re-derivado quando o nome muda. A v0 usa um slug legível como ID (suficiente enquanto tudo é curado à mão); trocar por um ID opaco e estável (ULID) caso o slug derivado do nome atual fique ambíguo é um follow-up conhecido e adiado.

## Território: municípios do IBGE como unidade atômica

O território diocesano no Brasil é, na prática, definido pela lista de municípios que cobre. A malha municipal do IBGE é dado aberto e oficial. Então:

- O registro atômico é `circunscricao_id × código_ibge_municipio`.
- Qualquer GeoJSON é *derivado* pela união da malha do IBGE — nunca mantido à mão.
- Atualizar uma fronteira vira uma linha de CSV/JSON, não retrabalho cartográfico.
- Exceção conhecida: casos sub-municipais (armadilha nº 5) — ficam como `granularidade_territorial: submunicipal` sem geometria na v0.

Isso está deliberadamente não-validado em escala — ver "Decisões em aberto" no [ROADMAP.md](../ROADMAP.md) (ABERTO-2).

## Identificadores externos (crosswalk)

Um registro só é reutilizável se tiver ID estável mais pontes para os identificadores que já existem: QID do Wikidata, GCatholic.org, Catholic-Hierarchy.org, e um slot reservado (vazio por ora) para um futuro identificador do CDIC/CNBB. O ID canônico é sempre o nosso próprio slug — nunca um ID externo como chave primária, já que IDs externos podem estar errados, faltando ou mudar de dono.
