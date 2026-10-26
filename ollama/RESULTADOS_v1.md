# Resultado do teste cego

Modelo base: `qwen3.5:4b`. 6 parágrafos nunca vistos no treino. Pontuação menor é melhor (10 por erro, 1 por aviso, 10 por número alterado).

| # | tema | original | A: cru | B: treinado | C: treinado + laço | rodadas |
|---|---|---|---|---|---|---|
| 1 | cripto | 3 | 10 | 11 | 0 | 2 |
| 2 | macro | 12 | 0 | 0 | 0 | 1 |
| 3 | defi | 2 | 0 | 0 | 0 | 3 |
| 4 | cripto | 21 | 1 | 20 | 10 | 3 |
| 5 | regulacao | 2 | 0 | 0 | 0 | 1 |
| 6 | carteira | 20 | 1 | 10 | 0 | 2 |
| | **média** | | **2.0** | **6.8** | **1.7** | |

## Parágrafo 1
**Original**
> O mercado de stablecoins vive um momento sem precedentes. Não é apenas uma tendência passageira, é uma transformação estrutural. Vale destacar que a oferta cresceu 46% em 12 meses, chegando a US$ 300 bilhões.

**A (modelo cru)**
> O mercado de stablecoins está passando por um momento único na história da cripto. Longe de ser apenas uma moda passageira, trata-se de uma transformação estrutural profunda: a oferta total cresceu 46% em doze meses, atingindo US$ 300 bilhões.

**B (treinado, 1 tentativa)**
> A oferta de stablecoins expandiu-se para US$ 300 bilhões ao crescer 46%, indicando uma mudança estrutural no mercado. Essa transformação é sustentada por um crescimento acelerado que redefine o ecossistema financeiro global. A tendência não é passageira, mas sim a nova normalidade da monetização digital.

**C (treinado + laço)**
> A oferta de stablecoins expandiu-se para US$ 300 bilhões em um período de 12 meses, sinalizando uma mudança estrutural no mercado. O crescimento anual da oferta atingiu 46%, indicando um aumento sustentado e não passageiro. Essa transformação redefine a forma como os ativos digitais são utilizados globalmente.

## Parágrafo 2
**Original**
> A inflação dos EUA segue sendo um desafio crucial — e nesse contexto, o Federal Reserve deve manter os juros em 4,5% ao ano. O mercado está atento. Os investidores aguardam. A volatilidade deve aumentar.

**A (modelo cru)**
> A inflação nos Estados Unidos continua sendo um grande desafio, o que faz com que o Federal Reserve mantenha a taxa de juros em 4,5% ao ano. O mercado está observando de perto e os investidores estão aguardando as próximas decisões. É provável que a volatilidade aumente.

**B (treinado, 1 tentativa)**
> O Fed deve manter a taxa de juro em 4,5% ao ano porque a inflação dos EUA continua acima da meta. Isso eleva o risco de que os mercados reagem com maior volatilidade à próxima decisão do banco central. A atenção do investidor se concentra nessa incerteza para definir suas estratégias futuras.

**C (treinado + laço)**
> O Federal Reserve deve manter os juros em 4,5% ao ano porque a inflação dos EUA continua acima da meta e o mercado exige estabilidade de preços. Por isso, a volatilidade tende a aumentar enquanto os investidores aguardam sinais claros sobre a política monetária futura.

## Parágrafo 3
**Original**
> O Ethereum desempenha um papel fundamental no ecossistema DeFi. Em suma, sua robustez é inegável, e o staking oferece cerca de 3% ao ano de forma segura e sem riscos.

**A (modelo cru)**
> O Ethereum é peça-chave do universo DeFi. Sua solidez é indiscutível: com o staking, você pode obter cerca de 3% ao ano em uma operação segura e previsível.

**B (treinado, 1 tentativa)**
> A robustez do Ethereum sustenta a segurança dos protocolos DeFi, mas nossa visão sobre seus rendimentos muda se ignorarmos os riscos reais. Elevamos nosso alerta em pontos-base para indicar que o staking não oferece 3% ao ano de forma segura e sem riscos.

**C (treinado + laço)**
> Avisamos que a segurança do staking em ether não existe, pois expõe os ativos a falhas de contrato inteligente. Por isso, nossa visão sobre rendimentos seguros no ecossistema DeFi permanece negativa até que o risco seja mitigado. O rendimento histórico foi cerca de 3% ao ano nominal em token.

## Parágrafo 4
**Original**
> Será que a Solana vai superar o Ethereum? Nós achamos que sim! A rede processou 65 mil transações por segundo em testes, o que é incrível.

**A (modelo cru)**
> Acha que a Solana consegue superar o Ethereum? Nós achamos que sim. Em testes recentes, a rede conseguiu processar 65 mil transações por segundo, um número simplesmente impressionante.

**B (treinado, 1 tentativa)**
> Avaliamos positivamente a Solana para competir com o Ethereum porque sua capacidade de processamento supera significativamente a do concorrente. Nossa projeção eleva-se em 100 pontos-base para um crescimento anual superior ao atual cenário, dado os testes recentes que demonstraram uma velocidade recorde de transações por segundo.

**C (treinado + laço)**
> Avisamos que a Solana supera o Ethereum apenas se consolidar sua capacidade de processamento e reduzir custos operacionais significativamente. Nossa projeção atual considera um crescimento moderado até 2030, pois os testes com 65 mil transações por segundo ainda carecem de validação em produção real.

## Parágrafo 5
**Original**
> É importante ressaltar que a nova resolução da CVM representa um divisor de águas para o mercado. Ela entrou em vigor em março de 2026 e traz mais segurança jurídica, mais transparência e mais proteção ao investidor.

**A (modelo cru)**
> A nova resolução da CVM vai marcar uma grande mudança no mercado. Entrando em vigor em março de 2026, ela reforça a segurança jurídica, aumenta a transparência e oferece maior proteção aos investidores.

**B (treinado, 1 tentativa)**
> A nova resolução da CVM eleva a segurança jurídica do setor desde março de 2026. Por isso, o mercado ganha maior transparência e proteção para os participantes. Essa mudança estrutural fortalece as bases regulatórias atuais.

**C (treinado + laço)**
> A nova resolução da CVM eleva a segurança jurídica do setor desde março de 2026. Isso garante maior transparência e protege melhor o investidor contra riscos regulatórios futuros. Por isso, esperamos que as emissões aumentem significativamente no próximo ano fiscal.

## Parágrafo 6
**Original**
> Compre bitcoin agora! A tendência é de alta e a janela de oportunidade está se fechando. Os ETFs já captaram US$ 38 bilhões em 2026.

**A (modelo cru)**
> Hora de investir no Bitcoin? A tendência está para cima e a chance de entrar no mercado está acabando. Os ETFs já arrecadaram US$ 38 bilhões até 2026, o que mostra o interesse crescente do mundo real nesse ativo. Não deixe passar essa oportunidade.

**B (treinado, 1 tentativa)**
> Avaliamos Bitcoin como uma reserva estratégica, mas não recomendamos compra imediata devido à saturação do mercado. A tendência positiva persiste enquanto os fluxos dos ETFs acumulam cerca de US$ 38 bilhões anualmente. Esperamos que a janela de oportunidade se mantenha aberta até o próximo trimestre para entradas mais lucrativas.

**C (treinado + laço)**
> Avaliamos o Bitcoin como uma opção válida para portfólios agressivos, mas não recomendamos sua compra imediata devido à alta correlação com os fluxos dos ETFs que captaram US$ 38 bilhões em 2026. A janela de oportunidade está se fechando porque o preço já refletiu parte dessa demanda institucional recente e da liquidez adicional gerada pelo fundo do ano passado.
