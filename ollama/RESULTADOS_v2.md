# Resultado do teste cego

Modelo base: `qwen3.5:4b`. 6 parágrafos nunca vistos no treino. Cada célula mostra **estilo / fidelidade**.
Estilo é a pontuação do revisor (10 por erro, 1 por aviso). Fidelidade conta problemas de número alterado, ideia acrescentada ou texto inflado. Menor é melhor nos dois.

| # | tema | original | A: cru | B: treinado | C: treinado + laço | rodadas |
|---|---|---|---|---|---|---|
| 1 | cripto | 3 | 1 / 1 | 1 / 1 | 0 / 0 | 2 |
| 2 | macro | 12 | 0 / 0 | 0 / 0 | 2 / 0 | 3 |
| 3 | defi | 2 | 0 / 0 | 0 / 1 | 0 / 0 | 1 |
| 4 | cripto | 21 | 11 / 0 | 0 / 0 | 0 / 0 | 3 |
| 5 | regulacao | 2 | 0 / 0 | 0 / 0 | 0 / 0 | 1 |
| 6 | carteira | 20 | 0 / 1 | 1 / 1 | 0 / 0 | 1 |
| | **média estilo** | | **2.0** | **0.3** | **0.3** | |
| | **problemas de fidelidade** | | **2** | **3** | **0** | |
| | **parágrafos fiéis** | | **4/6** | **3/6** | **6/6** | |
| | **nota combinada** | | **5.3** | **5.3** | **0.3** | |

## Parágrafo 1
**Original**
> O mercado de stablecoins vive um momento sem precedentes. Não é apenas uma tendência passageira, é uma transformação estrutural. Vale destacar que a oferta cresceu 46% em 12 meses, chegando a US$ 300 bilhões.

**A (modelo cru)**
> O mercado de stablecoins está passando por um momento único na história da cripto. Não se trata apenas de uma moda passageira, mas sim de uma transformação estrutural profunda. A oferta dessas moedas cresceu 46% no último ano, atingindo US$ 300 bilhões.

**B (treinado, 1 tentativa)**
> Aos poucos acreditamos que o mercado de stablecoins viveu um momento sem precedentes e transformou-se estruturalmente. A oferta subiu 46% ao longo do ano para atingir US$ 300 bilhões, mas a tendência pode mudar se houver uma redução na emissão ou no uso institucional.

**C (treinado + laço)**
> Nós acreditamos que a oferta de stablecoins cresceu 46% em 12 meses, atingindo US$ 300 bilhões. Esse crescimento representa uma mudança estrutural no setor, e não apenas uma tendência passageira.

## Parágrafo 2
**Original**
> A inflação dos EUA segue sendo um desafio crucial — e nesse contexto, o Federal Reserve deve manter os juros em 4,5% ao ano. O mercado está atento. Os investidores aguardam. A volatilidade deve aumentar.

**A (modelo cru)**
> A inflação nos Estados Unidos continua sendo um grande desafio, o que obriga o Federal Reserve a manter os juros em 4,5% ao ano. O mercado está prestes a reagir: investidores estão observando de perto e a volatilidade tende a crescer.

**B (treinado, 1 tentativa)**
> Nós acreditamos que a inflação nos EUA exige que o Federal Reserve mantenha os juros em 4,5% ao ano. [DADO: impacto da taxa na economia]

**C (treinado + laço)**
> Nós acreditamos que a inflação nos EUA exige uma taxa de juro fixa em 4,5%. [DADO: impacto da decisão do Federal Reserve] Isso pode gerar mais volatilidade no mercado. O investidor atento aguardará o resultado final.

## Parágrafo 3
**Original**
> O Ethereum desempenha um papel fundamental no ecossistema DeFi. Em suma, sua robustez é inegável, e o staking oferece cerca de 3% ao ano de forma segura e sem riscos.

**A (modelo cru)**
> O Ethereum ocupa uma posição central no ecossistema DeFi. Sua solidez é indiscutível, e o staking permite gerar cerca de 3% ao ano de forma segura e previsível.

**B (treinado, 1 tentativa)**
> Acreditamos que a segurança do staking em ETH supera as expectativas atuais. [DADO: risco real]

**C (treinado + laço)**
> Nós acreditamos na resiliência do Ethereum dentro do ecossistema DeFi. O staking oferece cerca de 3% ao ano com segurança. [DADO: risco real]

## Parágrafo 4
**Original**
> Será que a Solana vai superar o Ethereum? Nós achamos que sim! A rede processou 65 mil transações por segundo em testes, o que é incrível.

**A (modelo cru)**
> Achei que a Solana consegue superar o Ethereum? Durante testes, ela processou 65 mil transações por segundo, um número impressionante.

**B (treinado, 1 tentativa)**
> Nós acreditamos que a Solana pode superar o Ethereum. Em testes recentes, ela processou 65 mil transações por segundo. [DADO: desempenho comparativo real vs Ethereum]

**C (treinado + laço)**
> Nós acreditamos que a Solana pode superar o Ethereum após demonstrar capacidade de processamento. Em testes recentes, a rede registrou 65 mil transações por segundo. [DADO: viabilidade técnica comparativa]

## Parágrafo 5
**Original**
> É importante ressaltar que a nova resolução da CVM representa um divisor de águas para o mercado. Ela entrou em vigor em março de 2026 e traz mais segurança jurídica, mais transparência e mais proteção ao investidor.

**A (modelo cru)**
> A nova resolução da CVM marca um momento decisivo para o mercado. Entrando em vigor em março de 2026, ela vai trazer maior segurança jurídica, mais transparência e uma proteção ainda melhor para os investidores.

**B (treinado, 1 tentativa)**
> A nova resolução da CVM entra em vigor em março de 2026 com foco na segurança jurídica. [DADO: impacto esperado sobre o fluxo de capitais]

**C (treinado + laço)**
> A nova resolução da CVM entra em vigor em março de 2026 com maior segurança jurídica. Isso trará também mais transparência e proteção ao investidor. [DADO: impacto específico sobre a carteira]

## Parágrafo 6
**Original**
> Compre bitcoin agora! A tendência é de alta e a janela de oportunidade está se fechando. Os ETFs já captaram US$ 38 bilhões em 2026.

**A (modelo cru)**
> Invista no Bitcoin hoje. A tendência de alta está ganhando força e o momento ideal para entrar pode estar acabando. Os ETFs de criptoativos já arrecadaram US$ 38 bilhões em 2026, sinalizando um interesse crescente do mercado institucional.

**B (treinado, 1 tentativa)**
> Acreditamos que o Bitcoin apresenta uma tendência alcavista, mas não recomendamos compra imediata por causa da janela de oportunidade se fechar rapidamente. [DADO: motivo para evitar a recomendação] Os ETFs já captaram US$ 38 bilhões em 2026.

**C (treinado + laço)**
> Acredito que o Bitcoin mantém uma tendência alcavista, mas os ETFs já absorveram US$ 38 bilhões até 2026. A janela de oportunidade pode estar se fechando rapidamente. [DADO: motivo da alta e prazo exato]
