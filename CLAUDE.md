# Instruções para escrever no padrão Mercurius Research

Antes de escrever qualquer texto neste repositório, leia `GUIA.md` inteiro. Ele prevalece sobre
qualquer preferência de estilo sua.

## Fluxo obrigatório

1. Escolha o modelo em `modelos/` (relatório de perspectiva ou nota de ativo) e mantenha a
   ordem dos blocos.
2. Escreva cada unidade (seção, parágrafo, bullet) com a **tese na primeira frase**.
3. Use as fórmulas da seção 3 do guia literalmente, em especial a de revisão:
   "[Elevamos | Reduzimos] nossa projeção de [variável] em [N] pontos-base, para [Y]%".
4. Não invente números. Se o usuário não forneceu o dado, escreva `[DADO: descrição]` e
   liste as pendências ao final da resposta.
5. Rode `python ferramentas/revisor.py <arquivo>` e corrija até zerar os erros. Explique os
   avisos que decidir manter.

## Regras que mais falham

- Toda projeção tem horizonte ("nos próximos 10 anos") e data-base ("dados de 30 de setembro
  de 2026").
- Toda não recomendação diz sob que condições a visão mudaria.
- Use apenas os graus de convicção da seção 5. Nada de "certamente" ou "sem dúvida".
- Defina cada tema e cada carteira de referência em nota de rodapé na primeira ocorrência.
- Frases de 15 a 30 palavras e parágrafos de 3 a 5 frases.
- Não copie frases de relatórios de terceiros. Adapte o método, nunca o texto.
