# Mercurius Escrita

Padrão de redação da **Mercurius Research**. O objetivo é que todo relatório, nota de ativo e
projeção saia com o rigor dos *outlooks* institucionais de longo prazo: tese primeiro, número
sempre, revisão medida contra a edição anterior e certeza calibrada.

| Arquivo | Para quê |
|---|---|
| [`GUIA.md`](GUIA.md) | As regras: arquitetura do documento, fórmulas de frase, números, escala de convicção, léxico |
| [`modelos/relatorio-perspectiva.md`](modelos/relatorio-perspectiva.md) | Esqueleto do relatório anual ou semestral |
| [`modelos/nota-de-ativo.md`](modelos/nota-de-ativo.md) | Esqueleto da nota de 1 a 2 páginas sobre um ativo |
| [`exemplos/perspectiva-cripto-2027.md`](exemplos/perspectiva-cripto-2027.md) | Texto de referência escrito no padrão |
| [`exemplos/antes-e-depois.md`](exemplos/antes-e-depois.md) | Frases comuns reescritas, com a regra de cada correção |
| [`ferramentas/revisor.py`](ferramentas/revisor.py) | Revisor automático: aponta erros e avisos |
| [`CLAUDE.md`](CLAUDE.md) | Instruções para escrever com IA no padrão |

## Como usar

1. Copie um modelo para `textos/` e escreva no lugar dos `[colchetes]`.
2. Rode o revisor e zere os erros:
   ```bash
   python ferramentas/revisor.py textos/meu-relatorio.md
   ```
3. Faça o push. O GitHub roda o revisor em todos os arquivos de `textos/` e marca o commit
   com ❌ se houver erro.

## O que o revisor verifica

**Erros** (precisam ser corrigidos):
- palavras banidas e linguagem informal;
- exclamação e emoji;
- primeira pessoa do singular;
- decimal com ponto;
- moeda sem `US$`;
- `bps` no lugar de pontos-base;
- revisão sem tamanho ou destino;
- frases acima de 50 palavras;
- documento com números e sem `Fonte:`.

**Avisos** (pedem revisão humana):
- frases acima de 40 palavras;
- voz passiva em revisões;
- absolutos ("sempre", "nunca");
- intensificadores vagos;
- projeção sem horizonte;
- título de seção sem tese.

## Relação com os gráficos

As figuras seguem o repositório [mercurius-charts](https://github.com/adremerc/mercurius-charts).
O título de cada gráfico segue a mesma regra deste guia: é a conclusão, não o assunto.
