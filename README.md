# Ecclesia Atlas

> Base de dados aberta, versionada e com proveniência por campo da estrutura eclesiástica da Igreja Católica no Brasil.

*Open, versioned, field-sourced dataset of the Catholic Church's ecclesiastical structure in Brazil.*

**Status:** esqueleto inicial — schema e modelo de contribuição prontos, dataset real ainda não. Repositório pessoal por enquanto; migra para uma organização quando houver contribuidores de fora.

## Por que isto existe

Quem quer construir qualquer coisa católica no Brasil — um app de paróquia, uma ferramenta diocesana, um projeto pessoal — acaba reconstruindo a mesma base do zero: quais circunscrições eclesiásticas existem, a que província e regional da CNBB pertencem, quais municípios cobrem, quem é o bispo atual. O dado existe, mas espalhado em sites institucionais, PDFs e Wikipédia, sem identificador estável e sem como saber o quão confiável é cada informação.

O Ecclesia Atlas é essa camada que falta: um **dataset**, não um app. Estrutura e regras primeiro. Textos litúrgicos e traduções da Bíblia estão explicitamente fora de escopo — têm donos licenciados (ver [DATA_LICENSE.md](DATA_LICENSE.md)).

## O que isto NÃO é

- Não é um super-app (oração + horários de missa + confissão + doação).
- Não é um sistema de gestão paroquial / CRM — ver `ecclesiacrm`, e o próprio projeto CDIC da CNBB (Centro de Dados da Igreja Católica no Brasil, anunciado em abril de 2026), que ocupa esse espaço.
- Não é fonte oficial. É uma camada aberta, com proveniência declarada, que aponta de volta para as fontes primárias (Wikidata, GCatholic, Catholic-Hierarchy e, no futuro, o CDIC quando publicar).
- Não é redistribuição de textos litúrgicos ou traduções bíblicas protegidas por direito autoral.

## Roadmap

O plano completo — todas as fases, o que é reservado e o que não será construído — está em [ROADMAP.md](ROADMAP.md).

## Onde entra a API?

Resumo (detalhe no [ROADMAP.md](ROADMAP.md), Fase 2): a API **não** é a Fase 1 e **nunca** é a fonte da verdade — o dado versionado no Git é. A API é uma camada de consumo derivada, em três níveis:

1. **Nível 0 (já disponível, zero infra):** ler os arquivos JSON direto do GitHub (raw) ou por uma CDN como o jsDelivr. Isto já é uma "API de leitura" estática.
2. **Nível 1:** um passo de build que compila os registros em arquivos agregados (`all.json`, GeoJSON derivado da malha do IBGE), publicados como artefatos de release.
3. **Nível 2 (condicional):** uma API REST/GraphQL serverless de leitura — só se houver demanda que justifique a manutenção.

## Ver o dado agora

O repositório é público; cada circunscrição é um arquivo JSON. Sem instalar nada:

```bash
# via jsDelivr (CDN, com cache)
curl -s https://cdn.jsdelivr.net/gh/gustavofsousa/ecclesia-atlas@main/data/circunscricoes/arquidiocese-de-sao-salvador-da-bahia.json

# ou direto do GitHub (raw)
curl -s https://raw.githubusercontent.com/gustavofsousa/ecclesia-atlas/main/data/circunscricoes/ordinariado-militar-do-brasil.json
```

```js
const base = "https://cdn.jsdelivr.net/gh/gustavofsousa/ecclesia-atlas@main";
const arq = await fetch(`${base}/data/circunscricoes/arquidiocese-de-sao-salvador-da-bahia.json`)
  .then((r) => r.json());
console.log(arq.nome.valor, "—", arq.tipo);
```

> Dica: fixe uma tag de release (`@v0.1.0`) em vez de `@main` para consumo estável.

## Sem servidor, de propósito

A v0 é JSON plano em `data/`, validado contra `schema/circunscricao.schema.json`. Sem API obrigatória, sem banco, sem infraestrutura para consumir. Isso é o antídoto contra o modo de falha nº 1 do nicho: o projeto precisa continuar útil mesmo se ficar seis meses sem manutenção.

## Modelo de dados

Ver [docs/data-model.md](docs/data-model.md): os três eixos ortogonais (comunidade / lugar / território), a hierarquia eclesiástica brasileira e as armadilhas de modelagem que este schema trata de propósito.

## Modelo de proveniência

Todo fato não-estrutural (nome, data de ereção, bispo atual, território) carrega a própria fonte, data de verificação e nível de confiança — não um campo "fonte" único por registro. Ver [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

- **Código** (schema, ferramentas): [MIT](LICENSE).
- **Dados** (`data/`): [CC BY 4.0](DATA_LICENSE.md) — ver o arquivo para o raciocínio e um aviso legal importante.
