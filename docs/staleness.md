# Política de validade (staleness)

`verificado_em` sozinho não diz nada — um `bispo_atual` verificado em 2026 e o mesmo campo verificado em 2031 são idênticos na tela e epistemicamente muito diferentes. O que envelhece depende do **tipo** de campo. Data de ereção não muda nunca; nomeação episcopal muda.

Esta tabela define a **meia-vida** por campo: a partir de quando um valor deve ser tratado como "pode ter mudado" e revalidado, mesmo que a `confianca` registrada seja `alta`.

| Campo | Muda? | Meia-vida sugerida | Observação |
|---|---|---|---|
| `ereta_em` | Nunca | ∞ | Fato histórico. Verificado uma vez, verificado para sempre. |
| `nome` | Raríssimo | ~10 anos | Só muda em renomeação/elevação de circunscrição. |
| `tipo`, `tipo_jurisdicao` | Raro | ~10 anos | Elevação diocese→arquidiocese é evento raro. |
| `provincia_eclesiastica` | Raro | ~10 anos | Muda em reorganização de província. |
| `regional_cnbb` | Raro | ~10 anos | Mudança administrativa da CNBB. |
| `crosswalk.*` | Estável | ~5 anos | IDs externos podem ser depreciados ou fundidos. |
| `territorio` (municípios) | Ocasional | ~5 anos | Muda em desmembramento/criação de circunscrição. Revalidar a cada release maior. |
| `bispo_atual` | Volátil | ~12 meses | Sé muda por nomeação, renúncia, morte. Sé vacante pode surgir a qualquer momento. |

## Como isso vira mecanismo (Fase 1+)

A meia-vida não é só documentação: é a base de uma GitHub Action que, periodicamente, abre uma issue automática para cada registro cujo `verificado_em` passou da meia-vida do campo — priorizando `bispo_atual`. É esse laço que faz o dataset **sobreviver ao mantenedor**: em vez de depender de alguém lembrar de checar, o próprio repositório aponta o que envelheceu.

Enquanto a Action não existe, a tabela serve de guia para curadoria manual e para quem consome o dado decidir o quanto confiar em cada campo pela idade.
