# Como contribuir

## O modelo de proveniência

Todo fato não-estrutural de um registro — nome, data de ereção, bispo atual, território — é guardado como um pequeno objeto, não um valor solto:

```json
{
  "valor": "...",
  "fonte": "wikidata",
  "fonte_url": "https://www.wikidata.org/wiki/...",
  "verificado_em": "2026-08-18",
  "confianca": "alta | media | baixa | nao_verificado"
}
```

É isso que torna o dataset auditável em vez de "uma planilha na internet": qualquer um vê *quem* afirmou que um fato é verdade e *quando foi verificado pela última vez*, e pode discordar no nível do campo, não do registro inteiro.

## Enviar uma correção

1. Abra uma issue ou PR apontando para o arquivo específico em `data/circunscricoes/`.
2. Diga o campo, o novo valor e uma fonte — uma URL basta (site diocesano oficial, Wikidata, GCatholic, Catholic-Hierarchy, cobertura de imprensa de uma nomeação episcopal etc.).
3. Preencha `confianca` com honestidade. `nao_verificado` é um valor válido e esperado — melhor do que um palpite confiante.
4. Não envie textos litúrgicos, traduções bíblicas ou qualquer coisa com dono licenciado — apenas fatos e regras estruturais (nomes, datas, hierarquia, território), nunca texto protegido. Ver [DATA_LICENSE.md](DATA_LICENSE.md).

## Mudanças no schema

O schema fica em `schema/circunscricao.schema.json` (comentários em inglês, por ser código). Mudanças ali afetam todos os registros existentes — abra uma issue antes de mandar um PR que altere o próprio schema.

## Adicionar uma nova circunscrição

Copie a forma de um arquivo existente em `data/circunscricoes/`, preencha o que puder verificar e deixe o resto com `confianca: "nao_verificado"` em vez de adivinhar. Um registro parcial e honestamente rotulado é útil; um registro cheio e sem fonte não é.
