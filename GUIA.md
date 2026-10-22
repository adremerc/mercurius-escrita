# Guia de escrita Mercurius Research

Padrão de redação para relatórios, notas de ativo e projeções da Mercurius. A referência
de rigor é a escrita de *outlooks* institucionais de longo prazo, como o *Long-Term Capital
Market Assumptions* da J.P. Morgan Asset Management: tese primeiro, número sempre, revisão
explícita contra a edição anterior, certeza calibrada e definição de todo termo-chave.

O guia descreve o **método**, não copia o texto de ninguém. Todos os exemplos são da Mercurius.

---

## 1. Os cinco princípios

1. **Tese antes da evidência.** Toda unidade de texto (relatório, seção, parágrafo, bullet) abre
   com a conclusão. A evidência vem depois, nunca antes.
2. **Todo julgamento tem número, horizonte e data-base.** "Elevamos a projeção" não basta.
   O padrão é "Elevamos a projeção em 80 pontos-base, para 7,5%, nos próximos 10 anos".
3. **Toda mudança é medida contra a edição anterior.** O leitor precisa saber o que mudou, quanto
   mudou e por quê.
4. **A certeza é calibrada, não decorativa.** Há uma escala fixa de verbos de convicção (seção 5),
   e cada grau tem uso definido.
5. **Todo conceito próprio é definido.** Temas, siglas e carteiras de referência ganham definição
   em nota de rodapé na primeira ocorrência.

---

## 2. Arquitetura do documento

Todo relatório de perspectiva segue esta ordem. Os modelos estão em [`modelos/`](modelos/).

| Bloco | Função | Tamanho |
|---|---|---|
| **Prefácio** (opcional) | Por que este relatório existe agora; assinado pelo responsável | 150–250 palavras |
| **Principais conclusões** | 5 a 7 conclusões, cada uma com frase-título em negrito e 1 a 3 frases com números | 1 página |
| **Sumário executivo** | Texto corrido com a tese central, os temas e o resultado para a carteira de referência | 1–2 páginas |
| **Seções temáticas** | Cada uma com *Autores*, *Em resumo* e corpo | 2–6 páginas cada |
| **Riscos para a nossa perspectiva** | O que invalidaria a tese, e onde os temas se cruzam | 1 página |
| **Implicações para a carteira** | O que fazer com as projeções | 1–2 páginas |
| **Conclusão** | Retoma a tese em um parágrafo | ½ página |
| **Metodologia e apêndice** | Premissas, matrizes, definições | o necessário |

### 2.1 O bloco "Em resumo"

Toda seção abre com uma caixa **Em resumo**:

- de 4 a 6 bullets;
- cada bullet é uma frase completa de 25 a 50 palavras;
- em seções por classe de ativo, o bullet começa com um **rótulo e dois-pontos**:
  `Câmbio:`, `Crédito:`, `Ações:`, `Bitcoin:`, `Stablecoins:`;
- o primeiro bullet é a conclusão mais importante da seção; o último, a ressalva ou condição.

### 2.2 Títulos

O título de seção é uma **tese em duas partes**, separadas por dois-pontos ou reticências. A
primeira parte nomeia o tema; a segunda, a consequência.

- ✅ `Liquidez em dólar: as stablecoins viram infraestrutura... e alvo de regulação.`
- ✅ `Retornos expressivos, porém concentrados, em um mercado que amadurece.`
- ❌ `Stablecoins` (só o assunto)
- ❌ `O futuro das stablecoins` (promessa vaga)

### 2.3 Temas estruturais

O relatório se organiza em **três temas** (no máximo quatro) que atravessam todas as seções.
Cada tema:

- tem nome curto com substantivo e adjetivo (ex.: *institucionalização do acesso*,
  *escassez programada*, *dolarização digital*);
- é definido em nota de rodapé na primeira ocorrência;
- reaparece nas seções de ativos e de riscos. Os riscos ficam **na interseção** dos temas.

---

## 3. Fórmulas de frase

São os moldes que dão o "som" do texto. Use-os literalmente, trocando só os campos.

### 3.1 Revisão de projeção (a frase mais importante do padrão)

```
[Elevamos | Reduzimos] nossa projeção de [variável] em [N] pontos-base, para [Y]%[, o maior nível desde [referência]].
[Mantemos] nossa projeção de [variável] em [Y]%, [motivo].
```

- ✅ "Elevamos nossa projeção de retorno do bitcoin em 150 pontos-base, para 11,5% ao ano, o maior
  nível desde que começamos a publicar a estimativa."
- ✅ "Mantemos nossa projeção de inflação americana em 2,6%, já que o efeito das tarifas se
  dissipa ao longo do horizonte."
- ❌ "Revisamos para cima a projeção." (sem tamanho, sem destino)
- ❌ "A projeção subiu para 11,5%." (sem sujeito, sem variação)

Regras: variação em **pontos-base** para taxas e retornos; destino em **%** com uma casa
decimal; a referência histórica ("o maior desde...") só quando for verificável.

### 3.2 Causa e consequência

```
[Força A] impulsiona [efeito B]... e [efeito C, geralmente o custo ou risco].
[Fator] sustenta [resultado], mas [contrapeso].
```

- ✅ "A entrada de capital institucional impulsiona a liquidez... e a correlação com ações."

### 3.3 Concessão e contrapeso

Todo argumento forte recebe o contrapeso na mesma frase ou na seguinte:

```
[Afirmação], mas [limite].
[Afirmação]. Ainda assim, [contrapeso].
[Afirmação]. No entanto, caso [condição A] e [condição B], esse cenário pode mudar.
```

A terceira forma é obrigatória sempre que a Mercurius **não** recomenda algo: diga sob quais
condições mudaria de opinião.

### 3.4 Comparação histórica

```
o maior / menor [patamar | nível] em [N anos | duas décadas | desde X]
pela primeira vez, [ação]
pelo [segundo] ano consecutivo, [ação]
```

### 3.5 Posição e recomendação

```
Defendemos [carteiras / alocações] que [característica].
No momento, não defendemos [X] como [papel], devido a [motivo].
Consideramos [X] [classificação: especulativo | estratégico | tático].
Consideramos prematuro [ação], mas examinar [Y] é instrutivo.
```

### 3.6 Horizonte e data-base

Toda projeção diz **o horizonte** e **a data dos dados**:

- "nos próximos 10 anos", "ao longo do nosso horizonte de projeção";
- "estimativas de 30 de setembro de 2026".

---

## 4. Números

| Regra | Correto | Errado |
|---|---|---|
| Variação de taxa ou retorno em pontos-base | "sobe 60 pontos-base, para 7,0%" | "sobe 0,6%" |
| Abreviação após a primeira ocorrência | "pontos-base (pb)" → depois "pb" | "bps", "bp" |
| Percentual com uma casa nas projeções | 7,5% · 11,0% | 7,52% · 11% |
| Moeda com unidade por extenso | US$ 2,5 trilhões · US$ 40 bilhões | $2.5T · 40bi |
| Separadores brasileiros | 1.095 · 0,62 | 1,095 · 0.62 |
| Intervalo de horizonte | 10 a 15 anos | 10–15y |
| Data-base por extenso | 30 de setembro de 2026 | 30/09/26 |
| Retorno com período | 9,1% em 12 meses · 11,5% ao ano | 9,1% |
| Comparação sempre com referência | "220 pb acima da média de 25 anos" | "muito acima da média" |

Toda tabela, gráfico e número de destaque tem uma linha `Fonte:` no formato
`Fonte: [fontes]; Mercurius Research. Dados de [data].`

---

## 5. Escala de convicção

Use **somente** estes graus. Cada um tem um uso.

| Grau | Formas | Quando |
|---|---|---|
| 1. Fato | "O bitcoin caiu 75% entre..." | dado verificável, com fonte |
| 2. Projeção | "Esperamos", "Projetamos", "Prevemos" | número do nosso modelo |
| 3. Julgamento | "Acreditamos", "Consideramos", "Avaliamos" | opinião fundamentada |
| 4. Probabilidade | "provavelmente", "é provável que" | cenário mais provável, sem número |
| 5. Possibilidade | "pode", "poderia", "há risco de" | cenário alternativo ou risco |

Proibido: "certamente", "sem dúvida", "garantido", "com certeza", "inevitavelmente" (exceto
para fatos estruturais, como volatilidade em horizonte longo), "nunca", "sempre" em projeções.

---

## 6. Voz e léxico

- **Primeira pessoa do plural institucional**: "esperamos", "elevamos", "defendemos".
  Nunca "eu"; nunca "a equipe acha".
- **Voz ativa.** O sujeito da revisão somos nós: "Reduzimos", não "Foi reduzida".
- **Frases de 15 a 30 palavras.** Acima de 40, divida.
- **Parágrafos de 3 a 5 frases.** Um parágrafo, uma ideia.
- **Verbos de mecanismo** (preferir): impulsiona, sustenta, eleva, reduz, atenua, compensa,
  pressiona, amplia, concentra, desloca, normaliza.
- **Adjetivos precisos** (preferir): resiliente, desigual, estrutural, cíclico, persistente,
  concentrado, moderado, robusto.
- **Termos em inglês**: só quando não há equivalente consagrado (*hedge fund*, *stablecoin*,
  *staking*), em itálico na primeira ocorrência.

### Banidos (o revisor acusa)

`explosão`, `foguete`, `lua`, `to the moon`, `bombar`, `disparar` (use "subir X%"),
`imperdível`, `oportunidade única`, `revolucionário`, `incrível`, `absurdo`, `garantido`,
`certamente`, `sem dúvida`, ponto de exclamação, emoji, CAIXA ALTA para ênfase.

---

## 7. Notas de rodapé

- Definição de cada tema, sigla e carteira de referência na primeira ocorrência.
- A carteira de referência é sempre definida com composição e índices. Ex.:
  "¹ A carteira de referência cripto representa 70% bitcoin e 30% ether, rebalanceada
  trimestralmente."
- Referências a estudos: autor, título entre aspas, publicação, mês e ano.
- Ressalva obrigatória sob qualquer retorno passado: "Retorno passado não é garantia de
  resultado futuro."

---

## 8. Riscos

A seção de riscos:

1. começa dizendo **onde** os riscos se concentram (na interseção dos temas);
2. trata cada risco em um parágrafo com **mecanismo → efeito no retorno → por que não está no
   cenário-base**;
3. termina com a conclusão sobre o cenário-base ("Ainda assim, não acreditamos que...").

---

## 9. O guia por tema

As regras gerais valem para tudo. Cada tema acrescenta exigências próprias, porque o leitor
de uma nota de DeFi precisa de informações diferentes do leitor de uma nota de juros. Declare o
tema no cabeçalho do arquivo e o revisor aplica as regras dele:

```
---
tema: cripto
---
```

| Tema | Uso | O que o tema exige a mais | Frase máx. | *Em resumo* |
|---|---|---|---|---|
| `cripto` | perspectiva de um criptoativo | volatilidade em %, correlação, data-base, ressalva de retorno passado; "bitcoin" (ativo) em minúscula e "Bitcoin" (rede) em maiúscula; "ouro digital" só entre aspas e atribuído | 35 | obrigatório |
| `macro` | juros, inflação, PIB, câmbio | inflação com base (a/a, em 12 meses), juros com "a.a.", PIB real ou nominal, data-base; sem linguagem alarmista | 35 | obrigatório |
| `defi` | DeFi, *staking*, on-chain | risco de contrato inteligente, APR ou APY definido, TVL em US$, rendimento em token ou em US$; proibido "sem risco" | 35 | obrigatório |
| `regulacao` | normas e política pública | órgão e norma citados, prazo com data ou etapa; proibido "proibiu" ou "liberou" sem o ato | 40 | opcional |
| `carteira` | carteira-modelo e alocação | carteira de referência definida, rebalanceamento, ressalva de que não é recomendação individual; proibido imperativo de venda ("compre") | 35 | obrigatório |
| `mercado` | nota diária ou semanal | horário de corte dos dados, variação sempre com período ("em 24 horas", "na semana") | 30 | opcional |

O tom também muda. A nota de `mercado` fica nos graus 1 e 2 da escala de convicção (fato e
projeção) e quase não opina. Os textos de `cripto` e `carteira` usam os cinco graus. Em
`regulacao`, a regra é descrever o ato antes de interpretá-lo.

As regras de cada tema estão em [`ferramentas/temas.py`](ferramentas/temas.py). Para criar um
tema novo, copie um bloco existente e ajuste.

---

## 10. Conectivos: como ligar frases e parágrafos

O texto institucional soa humano porque cada frase retoma algo da anterior. Há duas formas de
ligar ideias, e a primeira é melhor:

1. **Retomada:** repita ou resuma o termo anterior com um demonstrativo. "A oferta de
   stablecoins chegou a US$ 300 bilhões. **Esse crescimento** veio quase todo do USDT."
2. **Conectivo:** use uma palavra de ligação quando a relação lógica precisar ficar explícita.

Escolha o conectivo pela **função**, nunca pelo som:

| Função | Use | Evite |
|---|---|---|
| Adição | além disso, também, da mesma forma | ademais, outrossim |
| Contraste | no entanto, ainda assim, por outro lado, em contrapartida, mas | todavia (formal demais) |
| Concessão | embora, apesar de, mesmo que | não obstante |
| Causa | porque, já que, uma vez que, isso ocorre porque | haja vista |
| Consequência | por isso, com isso, como resultado, assim | dessa forma (vício de IA quando repetido) |
| Condição | caso, se, desde que | |
| Exemplo | por exemplo, como mostra a Figura N | a título de exemplo |
| Tempo | desde, ao longo de, nos próximos N anos | |

Regras:

- No máximo **um conectivo a cada três ou quatro frases**. Se toda frase abre com conectivo, o
  texto fica mecânico.
- O mesmo conectivo não abre mais de duas frases no documento.
- O parágrafo novo retoma o anterior na primeira frase, com conectivo, demonstrativo ou o mesmo
  termo.
- Três frases curtas seguidas (menos de nove palavras) viram uma ou duas, ligadas por "porque",
  "o que", "mas" ou "e".

O revisor aponta transições abruptas e sugere o conectivo pela relação provável do trecho
(contraste, causa, consequência, exemplo, tempo ou adição). A sugestão é um ponto de partida:
quem escreve decide a relação certa.

---

## 11. Vícios de texto gerado por IA

Estes padrões denunciam texto escrito ou revisado por IA sem edição humana. O revisor aponta
todos.

| Vício | Exemplo | Correção |
|---|---|---|
| Travessão para aposto ou ênfase | "a adoção institucional — impulsionada pelos ETFs — cresce" | vírgulas, parênteses ou duas frases. Limite: 1 a cada 150 palavras; o ideal é nenhum |
| Dois-pontos de efeito | "O motivo é simples: liquidez." | "A liquidez explica o movimento." Dois-pontos só em títulos, rótulos e antes de listas ou fórmulas |
| "Não é X, é Y" | "O bitcoin não é só especulação, é reserva de valor." | afirme Y e prove: "O bitcoin passou a ser usado como reserva de valor por 4,8% das empresas listadas." |
| Pergunta retórica | "O resultado? Volatilidade menor." | "Como resultado, a volatilidade caiu para 48%." |
| Clichês de abertura | "No cenário atual", "Vale ressaltar que", "É importante notar" | apague e comece pelo fato |
| Metáforas gastas | jornada, navegar, mergulhar, divisor de águas, tapeçaria, panorama | verbo concreto |
| Tríades em série | "mais maduro, mais institucional e mais fundamental" | um atributo, com número |
| Adjetivos inflados repetidos | robusto, crucial, fundamental, significativo, essencial | número e comparação |
| Aspas de ênfase | um "novo" bitcoin | sem aspas, ou aspas com atribuição de quem disse |
| Fecho genérico | "Em suma", "Em conclusão" | a última frase é a tese, sem anúncio |
| Frases picotadas | "Os ETFs cresceram. Os fluxos aumentaram. A liquidez melhorou." | "Os ETFs receberam US$ 38 bilhões, o que elevou a liquidez." |
| Negrito em toda frase | **muitos** **destaques** | negrito só no título de conclusão e no rótulo do *Em resumo* |
| Conectivos de enchimento | ademais, nesse sentido, nesse contexto, dessa forma | retomada do termo anterior |

Veja o caso completo em [`exemplos/texto-ia.md`](exemplos/texto-ia.md) e rode o revisor nele.

---

## 12. Checklist antes de publicar

- [ ] O cabeçalho declara o `tema:`.
- [ ] O título de cada seção é uma tese em duas partes.
- [ ] Toda seção tem *Em resumo* com 4 a 6 bullets em frase completa.
- [ ] Toda revisão diz direção, tamanho em pontos-base e destino em %.
- [ ] Todo número tem unidade, período e fonte; toda projeção tem horizonte e data-base.
- [ ] Os temas estão definidos em nota de rodapé e reaparecem em riscos.
- [ ] Toda "não recomendação" diz sob que condições mudaria.
- [ ] Nenhuma palavra banida e nenhuma frase acima do limite do tema.
- [ ] Nenhum travessão de ênfase, nenhum dois-pontos de efeito, nenhum "não é X, é Y".
- [ ] Cada parágrafo retoma o anterior; nenhum conectivo abre mais de duas frases.
- [ ] Rodei `python ferramentas/revisor.py arquivo.md` e zerei os erros.
