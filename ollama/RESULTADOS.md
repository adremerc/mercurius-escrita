# Resultado do teste cego

Modelo base: `qwen3.5:4b`. 6 parágrafos nunca vistos no treino. Cada célula mostra **estilo / fidelidade**.
Estilo é a pontuação do revisor (10 por erro, 1 por aviso). Fidelidade conta problemas de número alterado, ideia acrescentada ou texto inflado. Menor é melhor nos dois.

| # | tema | original | A: cru | B: treinado | C: treinado + laço | rodadas |
|---|---|---|---|---|---|---|
| 1 | cripto | 3 | 1 / 1 | 0 / 1 | 1 / 0 | 3 |
| 2 | macro | 12 | 0 / 0 | 2 / 1 | 0 / 0 | 2 |
| 3 | defi | 2 | 0 / 0 | 0 / 1 | 0 / 0 | 1 |
| 4 | cripto | 21 | 30 / 0 | 0 / 2 | 0 / 0 | 3 |
| 5 | regulacao | 2 | 0 / 1 | 0 / 0 | 0 / 0 | 1 |
| 6 | carteira | 20 | 1 / 0 | 0 / 3 | 0 / 0 | 1 |
| | **média estilo** | | **5.3** | **0.3** | **0.2** | |
| | **problemas de fidelidade** | | **2** | **8** | **0** | |
| | **parágrafos fiéis** | | **4/6** | **1/6** | **6/6** | |
| | **nota combinada** | | **8.7** | **13.7** | **0.2** | |

## Parágrafo 1
**Original**
> O mercado de stablecoins vive um momento sem precedentes. Não é apenas uma tendência passageira, é uma transformação estrutural. Vale destacar que a oferta cresceu 46% em 12 meses, chegando a US$ 300 bilhões.

**A (modelo cru)**
> O mercado de stablecoins está passando por um momento único na história da cripto. Não se trata apenas de uma moda passageira, mas sim de uma transformação estrutural profunda. Para ilustrar essa magnitude: a oferta global cresceu 46% no último ano, atingindo os impressionantes US$ 300 bilhões.

**B (treinado, 1 tentativa)**
> Nós acreditamos que o mercado de stablecoins vive uma transformação estrutural e não apenas uma tendência passageira. A oferta chegou a US$ 300 bilhões após crescer 46% em doze meses.

**C (treinado + laço)**
> Nós acreditamos que a oferta de stablecoins cresceu 46% em 12 meses, atingindo US$ 300 bilhões. Esse movimento representa uma transformação estrutural no mercado. Não é apenas um momento passageiro, mas uma mudança duradoura na estrutura do setor.

## Parágrafo 2
**Original**
> A inflação dos EUA segue sendo um desafio crucial — e nesse contexto, o Federal Reserve deve manter os juros em 4,5% ao ano. O mercado está atento. Os investidores aguardam. A volatilidade deve aumentar.

**A (modelo cru)**
> A inflação nos Estados Unidos continua sendo um grande desafio, o que leva o Federal Reserve a manter os juros em 4,5% ao ano. O mercado está de olho nisso: investidores estão atentos e aguardando cada decisão. Com isso, é provável que a volatilidade nas bolsas aumente.

**B (treinado, 1 tentativa)**
> Nós esperamos que a inflação nos EUA continue desafiando o Federal Reserve para manter os juros em 4,5%. [DADO: impacto da taxa de juro na economia] O mercado e os investidores já estão atentos à possível maior volatilidade.

**C (treinado + laço)**
> A inflação nos EUA é um desafio para o Federal Reserve manter juros em 4,5% ao ano. O mercado está atento à volatilidade que pode aumentar. [DADO: impacto da taxa de juro]

## Parágrafo 3
**Original**
> O Ethereum desempenha um papel fundamental no ecossistema DeFi. Em suma, sua robustez é inegável, e o staking oferece cerca de 3% ao ano de forma segura e sem riscos.

**A (modelo cru)**
> O Ethereum é essencial para o ecossistema DeFi. Sua solidez é indiscutível, e o staking garante cerca de 3% ao ano de forma segura e previsível.

**B (treinado, 1 tentativa)**
> A robustez do Ethereum é inegável em DeFi, com staking que rende cerca de 3% anualmente. [DADO: risco real]

**C (treinado + laço)**
> Nós acreditamos que a robustez do Ethereum é inegável em DeFi. O staking oferece cerca de 3% ao ano com segurança reduzida. [DADO: risco real]

## Parágrafo 4
**Original**
> Será que a Solana vai superar o Ethereum? Nós achamos que sim! A rede processou 65 mil transações por segundo em testes, o que é incrível.

**A (modelo cru)**
> Achei que a Solana vai superar o Ethereum. Durante os testes, ela conseguiu processar 65 mil transações por segundo, um número simplesmente impressionante.

**B (treinado, 1 tentativa)**
> Nós não recomendamos comparar diretamente as redes de forma especulativa. [DADO: probabilidade real de superação]

**C (treinado + laço)**
> A rede de teste da Solana processou 65 mil transações por segundo.

## Parágrafo 5
**Original**
> É importante ressaltar que a nova resolução da CVM representa um divisor de águas para o mercado. Ela entrou em vigor em março de 2026 e traz mais segurança jurídica, mais transparência e mais proteção ao investidor.

**A (modelo cru)**
> A nova resolução da CVM vai mudar completamente o cenário do mercado. Entrando em vigor em março de 2026, ela oferece maior segurança jurídica, mais transparência e reforça a proteção aos investidores.

**B (treinado, 1 tentativa)**
> A nova resolução da CVM entra em vigor em março de 2026, com foco na segurança jurídica e no investimento. [DADO: impacto esperado sobre a alocação]

**C (treinado + laço)**
> A nova resolução da CVM entra em vigor em março de 2026 com foco na segurança jurídica. [DADO: impacto esperado no setor]

## Parágrafo 6
**Original**
> Compre bitcoin agora! A tendência é de alta e a janela de oportunidade está se fechando. Os ETFs já captaram US$ 38 bilhões em 2026.

**A (modelo cru)**
> Hora de investir no Bitcoin? A tendência de alta continua forte, mas a janela de oportunidade está se fechando. Os ETFs de criptoativos já arrecadaram mais de US$ 38 bilhões apenas em 2026. Não deixe para depois.

**B (treinado, 1 tentativa)**
> Acreditamos que o Bitcoin mantém uma tendência alcavista, mas não recomendamos compra imediata por falta de dados sobre custos de entrada e risco residual. [DADO: custo da operação]

**C (treinado + laço)**
> A tendência do Bitcoin aponta para alta, mas o acesso via ETFs já absorveu US$ 38 bilhões até 2026. [DADO: prazo de janela]
