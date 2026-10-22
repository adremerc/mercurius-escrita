"""Regras específicas por tema. O revisor lê o tema no cabeçalho do texto:

    ---
    tema: cripto
    ---

Cada tema define:
  obrigatorios: (regex, mensagem) que PRECISAM aparecer no documento (ERRO se faltar)
  proibidos:    (regex, mensagem) que não podem aparecer (ERRO)
  avisos:       (regex, mensagem) que pedem revisão (AVISO)
  max_frase:    limite de palavras por frase (ERRO acima de +10)
  exige_em_resumo: se o bloco "Em resumo" é obrigatório
"""

TEMAS = {
    # Nota ou relatório sobre um criptoativo (BTC, ETH, SOL...)
    "cripto": {
        "descricao": "Perspectiva de criptoativos",
        "obrigatorios": [
            (r"volatilidade[^.]{0,60}\d+(,\d+)?%", "cite a volatilidade esperada ou histórica em %"),
            (r"Dados de \d{1,2} de \w+ de \d{4}|dados de \d{1,2} de \w+ de \d{4}", "falta a data-base ('Dados de 30 de setembro de 2026')"),
            (r"Retorno passado não é garantia", "falta a ressalva de retorno passado"),
            (r"correla", "diga a correlação com outros ativos (ou por que não importa)"),
        ],
        "proibidos": [
            (r"\b(HODL|hodl|WAGMI|FUD|FOMO|shitcoin|pump|dump)\b", "gíria de comunidade; use termo técnico"),
            (r"\bmoeda do futuro\b", "slogan, não análise"),
        ],
        "avisos": [
            (r"(?<![\"“])ouro digital(?![\"”])", "'ouro digital' é rótulo de mercado: use entre aspas e atribua"),
            (r"(?<!^)(?<![.?:]\s)(?<!\*\*)\bBitcoin\b(?! \(rede\))", "padrão: 'bitcoin' (ativo) em minúscula; 'Bitcoin' só para a rede/protocolo"),
            (r"\bpreço[- ]alvo\b", "preço-alvo pede horizonte, cenário e método"),
        ],
        "max_frase": 35,
        "exige_em_resumo": True,
    },
    # Macro: juros, inflação, crescimento, câmbio
    "macro": {
        "descricao": "Macroeconomia e juros",
        "obrigatorios": [
            (r"Dados de|dados de", "falta a data-base"),
        ],
        "proibidos": [
            (r"\bbomba fiscal\b|\bcolapso\b", "linguagem alarmista; descreva o mecanismo e o número"),
        ],
        "avisos": [
            (r"inflação[^.]{0,40}\d+(,\d+)?%(?![^.]{0,25}(a/a|ao ano|em 12 meses|anualizad))", "inflação sem base (a/a, em 12 meses, anualizada)"),
            (r"\bjuros?\b[^.]{0,40}\d+(,\d+)?%(?![^.]{0,15}(a\.a\.|ao ano))", "taxa de juros sem 'a.a.'"),
            (r"\bPIB\b(?![^.]{0,30}(real|nominal))", "diga se o PIB é real ou nominal"),
        ],
        "max_frase": 35,
        "exige_em_resumo": True,
    },
    # DeFi, staking, on-chain
    "defi": {
        "descricao": "DeFi, staking e métricas on-chain",
        "obrigatorios": [
            (r"risco de contrato|contrato inteligente", "toda análise de DeFi menciona o risco de contrato inteligente"),
            (r"Dados de|dados de", "falta a data-base (métricas on-chain mudam por bloco)"),
        ],
        "proibidos": [
            (r"\b(sem risco|risk[- ]free|renda passiva garantida)\b", "não existe rendimento sem risco em DeFi"),
        ],
        "avisos": [
            (r"\bAPY\b(?![^.]{0,80}APR)|\bAPR\b(?![^.]{0,80}APY)", "defina se é APR (simples) ou APY (composto)"),
            (r"\bTVL\b(?![^.]{0,40}US\$)", "TVL sem valor em US$"),
            (r"rendimento[^.]{0,30}\d+(,\d+)?%(?![^.]{0,40}(real|nominal|em token|em US\$))", "rendimento sem dizer se é em token, em US$, real ou nominal"),
        ],
        "max_frase": 35,
        "exige_em_resumo": True,
    },
    # Regulação e política pública
    "regulacao": {
        "descricao": "Regulação",
        "obrigatorios": [
            (r"\b(CVM|BCB|Banco Central|SEC|CFTC|MiCA|Receita Federal|Congresso|Lei|Resolução|Instrução)\b", "cite o órgão ou a norma"),
        ],
        "proibidos": [
            (r"\b(proibiu|liberou geral|acabou com)\b", "descreva o ato normativo com precisão (o que, quem, quando)"),
        ],
        "avisos": [
            (r"\b(em breve|nos próximos dias)\b", "prazo regulatório pede data ou etapa do processo"),
        ],
        "max_frase": 40,
        "exige_em_resumo": False,
    },
    # Alocação e carteira-modelo
    "carteira": {
        "descricao": "Carteira-modelo e alocação",
        "obrigatorios": [
            (r"carteira de referência", "defina a carteira de referência"),
            (r"rebalance", "diga a frequência de rebalanceamento"),
            (r"não constitui recomendação|não é recomendação", "inclua a ressalva de que o material não constitui recomendação individual"),
        ],
        "proibidos": [
            (r"\bcompre\b|\bvenda já\b|\baproveite\b", "imperativo de venda; use 'defendemos' e 'consideramos'"),
        ],
        "avisos": [
            (r"\bSharpe\b(?![^.]{0,60}\d)", "índice de Sharpe sem número"),
        ],
        "max_frase": 35,
        "exige_em_resumo": True,
    },
    # Nota curta de mercado (diária ou semanal)
    "mercado": {
        "descricao": "Nota de mercado diária ou semanal",
        "obrigatorios": [
            (r"\b(\d{1,2}h|horário de Brasília|UTC)\b", "diga o horário de corte dos dados (ex.: 18h, horário de Brasília)"),
        ],
        "proibidos": [],
        "avisos": [
            (r"(sub|ca)iu?\s+\d+(,\d+)?%(?![^.]{0,30}(em 24 horas|na semana|no dia|no mês|no ano|desde))", "variação sem período ('em 24 horas', 'na semana')"),
        ],
        "max_frase": 30,
        "exige_em_resumo": False,
    },
}
