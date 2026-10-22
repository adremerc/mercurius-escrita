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

1. Copie um modelo para `textos/`, declare o tema no cabeçalho (`tema: cripto`) e escreva no lugar dos `[colchetes]`.
2. Rode o revisor e zere os erros:
   ```bash
   python ferramentas/revisor.py textos/meu-relatorio.md
   ```
3. Faça o push. O GitHub roda o revisor em todos os arquivos de `textos/` e marca o commit
   com ❌ se houver erro.

## O que o revisor verifica

Quatro camadas, cada achado marcado com a sua:

| Camada | O que aponta |
|---|---|
| `[guia]` | palavras banidas, linguagem informal, "eu", decimal com ponto, moeda sem `US$`, `bps`, revisão sem tamanho ou destino, frases longas, projeção sem horizonte, falta de `Fonte:` |
| `[ia]` | travessões (máx. 1 a cada 150 palavras), dois-pontos de efeito, "não é X, é Y", perguntas retóricas, clichês ("vale ressaltar", "no cenário atual", "jornada"), tríades, adjetivos inflados repetidos, aspas de ênfase, fechos genéricos |
| `[conexão]` | parágrafo que não retoma o anterior (com sugestão de conectivo pela relação lógica), frases picotadas, frases seguidas com o mesmo início, conectivo repetido |
| `[tema]` | exigências do tema declarado no cabeçalho (`cripto`, `macro`, `defi`, `regulacao`, `carteira`, `mercado`) |

Para ver o efeito, compare [`exemplos/texto-ia.md`](exemplos/texto-ia.md), com 26 apontamentos,
e a versão corrigida em [`exemplos/texto-ia-corrigido.md`](exemplos/texto-ia-corrigido.md), sem nenhum.

As camadas `[ia]` e `[conexão]` são heurísticas: indicam onde olhar. Quem escreve decide a
correção.

## Relação com os gráficos

As figuras seguem o repositório [mercurius-charts](https://github.com/adremerc/mercurius-charts).
O título de cada gráfico segue a mesma regra deste guia: é a conclusão, não o assunto.
