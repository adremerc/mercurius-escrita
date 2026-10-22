"""Revisor do padrão de escrita Mercurius Research.

    python ferramentas/revisor.py texto.md [outro.md ...]
    python ferramentas/revisor.py texto.md --tema cripto      # força o tema
    python ferramentas/revisor.py --temas                      # lista os temas

O tema também pode vir no cabeçalho do arquivo:
    ---
    tema: cripto
    ---

Quatro camadas de verificação:
  [guia]    regras gerais do GUIA (números, convicção, revisões, fontes)
  [ia]      vícios típicos de texto gerado por IA (travessões, dois-pontos de efeito,
            "não é X, é Y", clichês, perguntas retóricas, tríades)
  [conexão] transições abruptas, frases picotadas, conectivos repetidos; sugere o conectivo
            pela função lógica do trecho
  [tema]    exigências do tema (cripto, macro, defi, regulacao, carteira, mercado)

ERRO quebra o padrão (código de saída 1). AVISO pede leitura humana.
As verificações de conexão e de IA são heurísticas: indicam onde olhar, não reescrevem.
"""

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from temas import TEMAS  # noqa: E402

# ----------------------------------------------------------------- vocabulário
BANIDOS = [
    "explosão", "explodir", "explodiu", "foguete", "to the moon", "bombar", "bombou", "disparou",
    "disparar", "imperdível", "oportunidade única", "revolucionário", "revolucionária",
    "incrível", "absurdo", "absurda", "garantido", "garantida", "certamente", "sem dúvida",
    "com certeza", "obviamente", "claramente", "game changer", "hype",
]
INFORMAL = ["pra", "pro", "tá", "né", "tipo assim", "galera", "vai bombar"]
VAGOS = ["muito", "bastante", "enorme", "gigante", "forte alta", "forte queda"]
ABSOLUTOS = ["sempre", "nunca", "inevitavelmente", "jamais"]

CLICHES_IA = [
    "vale ressaltar", "vale destacar", "vale lembrar", "vale notar", "é importante notar",
    "é importante destacar", "é importante ressaltar", "é fundamental destacar",
    "nesse sentido", "neste sentido", "nesse contexto", "neste contexto", "no cenário atual",
    "no atual cenário", "em um mundo cada vez mais", "cada vez mais", "desempenha um papel",
    "papel crucial", "papel fundamental", "mergulhar", "mergulho profundo", "navegar por",
    "navegar em", "jornada", "tapeçaria", "panorama", "divisor de águas", "sem precedentes",
    "paradigma", "em última análise", "ademais", "outrossim", "por fim, mas não menos",
    "não é exagero", "a verdade é que", "o ponto é que", "em outras palavras",
    "isso significa que", "a chave para", "o segredo", "no fim das contas", "de forma geral",
    "de modo geral", "como um todo", "lança luz", "abre caminho", "pavimenta",
]
INFLADOS = ["robusto", "robusta", "crucial", "fundamental", "significativo", "significativa",
            "essencial", "notável", "sólido", "sólida", "dinâmico", "dinâmica"]
ABERTURAS_GENERICAS = ["em suma", "em resumo,", "em conclusão", "concluindo", "resumindo",
                       "em síntese"]

CONECTIVOS = {
    "adição": ["além disso", "também", "soma-se a isso", "da mesma forma"],
    "contraste": ["no entanto", "ainda assim", "por outro lado", "em contrapartida", "mas",
                  "porém", "contudo", "todavia"],
    "concessão": ["embora", "apesar de", "apesar disso", "mesmo que", "mesmo assim"],
    "causa": ["porque", "já que", "uma vez que", "devido a", "isso ocorre porque", "como"],
    "consequência": ["por isso", "assim", "como resultado", "com isso", "portanto",
                     "dessa forma", "consequentemente"],
    "condição": ["caso", "se", "desde que"],
    "exemplo": ["por exemplo", "como mostra", "como mostram"],
    "tempo": ["desde", "depois", "antes", "enquanto", "ao longo", "nos próximos", "em 20"],
    "conclusão": ["em conjunto", "no saldo", "somados"],
}
TODOS_CONECTIVOS = sorted({c for v in CONECTIVOS.values() for c in v}, key=len, reverse=True)
RETOMADA = re.compile(r"^(\w+\s){0,5}?(esse|essa|esses|essas|isso|nesse|nessa|neste|nesta|"
                      r"desse|dessa|deste|desta|este|esta|estes|estas|tal|tais|o mesmo|a mesma)\b",
                      re.I)
STOP = set("""a o os as um uma uns umas de do da dos das em no na nos nas por para com sem
que se e ou mas mais menos muito como ao aos à às seu sua seus suas nosso nossa nossos nossas
é são foi foram ser ter tem têm está estão esse essa isso este esta isto já não sim também
entre sobre até após desde quando onde qual quais cada todo toda todos todas outro outra
outros outras ainda pode podem deve devem esperamos acreditamos ano anos""".split())

SECOES_FIXAS = {
    "principais conclusões", "sumário executivo", "em resumo", "autores", "conclusão", "notas",
    "metodologia", "apêndice", "prefácio", "riscos para a nossa perspectiva",
    "implicações para a carteira", "referências", "fontes", "o que mudou desde a última nota",
    "o que mudou desde a última edição", "papel na carteira", "corpo",
}
VERBOS_REVISAO = r"\b(Elevamos|Reduzimos|Aumentamos|Cortamos|Revisamos|Rebaixamos)\b"
VERBOS_PROJECAO = r"\b(Esperamos|Projetamos|Prevemos|Estimamos)\b"
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
ROTULO = re.compile(r"^\s*[-*•]?\s*\*\*[^*]{1,40}[:.]\*\*|^\s*(Fonte|Nota|Notas|Autores|Dados de)\b")


# ----------------------------------------------------------------- utilidades
def frases(paragrafo):
    p = paragrafo.replace("**", "")
    p = re.sub(r"\b(Sr|Sra|Dr|Dra|ex|p\.ex|vs|aprox)\.", r"\1§", p)
    partes = re.split(r"(?:(?<=[.?;!])|(?<=[.?;!][¹²³⁴⁵⁶⁷⁸⁹]))\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ\"“(¹²³⁴⁵])", p)
    return [x.replace("§", ".").strip() for x in partes if x.strip()]


def palavras(s):
    return re.findall(r"[A-Za-zÀ-ÿ0-9]+", s)


def raizes(s):
    return {w.lower()[:6] for w in palavras(s) if len(w) >= 6 and w.lower() not in STOP}


def comeca_com_conectivo(frase):
    f = frase.lower().lstrip("¹²³⁴⁵⁶⁷⁸⁹ ")
    if any(f.startswith(c + " ") or f.startswith(c + ",") for c in TODOS_CONECTIVOS):
        return True
    # conectivo intercalado no início: "Os mineradores, por outro lado, enfrentam..."
    inicio = " ".join(f.split()[:8])
    return any(re.search(rf", {re.escape(c)},", inicio) for c in TODOS_CONECTIVOS if len(c) > 3)


def funcao_sugerida(paragrafo):
    """Infere a relação lógica do parágrafo para sugerir o conectivo."""
    p = paragrafo.lower()
    if re.search(r"\b(risco|porém|mas|no entanto|embora|queda|pior|limita|custo|contudo)\b", p):
        return "contraste ou ressalva", "Ainda assim, / No entanto, / Por outro lado,"
    if re.search(r"\b(porque|devido|já que|motivo|explica|razão)\b", p):
        return "causa", "Isso ocorre porque / Uma razão é que"
    if re.search(r"\b(por isso|portanto|resultado|implica|consequência|leva a)\b", p):
        return "consequência", "Com isso, / Como resultado, / Por isso,"
    if re.search(r"\b(exemplo|caso de|como em)\b", p):
        return "exemplo", "Por exemplo, / O caso de X mostra que"
    if re.search(r"\b(próximos|até 20\d\d|horizonte|futuro)\b", p):
        return "tempo ou projeção", "Nos próximos N anos, / Ao longo do horizonte,"
    return "adição ou retomada", "Além disso, / ou retome o termo anterior ('Esse aumento...')"


def ler_cabecalho(texto):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", texto, re.S)
    meta = {}
    if m:
        for linha in m.group(1).splitlines():
            if ":" in linha:
                k, v = linha.split(":", 1)
                meta[k.strip().lower()] = v.strip()
    return meta


# ----------------------------------------------------------------- revisão
def revisar(caminho, tema_forcado=None):
    texto = Path(caminho).read_text(encoding="utf-8")
    # comentários HTML viram linhas vazias (preserva a numeração)
    texto = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), texto, flags=re.S)
    meta = ler_cabecalho(texto)
    tema = tema_forcado or meta.get("tema")
    linhas = texto.splitlines()
    achados = []

    def add(nivel, cat, n, msg, trecho=""):
        achados.append((nivel, cat, n, msg, trecho.strip()[:100]))

    # ---- análise linha a linha
    em_codigo = em_meta = False
    total_palavras = 0
    travessoes = []
    for n, linha in enumerate(linhas, 1):
        if n == 1 and linha.strip() == "---":
            em_meta = True
            continue
        if em_meta:
            em_meta = linha.strip() != "---"
            continue
        if linha.strip().startswith("```"):
            em_codigo = not em_codigo
            continue
        if em_codigo or linha.strip().startswith(("|", "<!--", ">")) or "-->" in linha:
            continue
        baixa = linha.lower()
        corpo = not linha.startswith("#")
        total_palavras += len(palavras(linha))

        # [guia]
        for b in BANIDOS:
            if re.search(rf"(?<!\w){re.escape(b)}(?!\w)", baixa):
                add("ERRO", "guia", n, f"palavra banida: '{b}'", linha)
        for a in INFORMAL:
            if re.search(rf"(?<!\w){re.escape(a)}(?!\w)", baixa):
                add("ERRO", "guia", n, f"linguagem informal: '{a}'", linha)
        if "!" in re.sub(r"!\[|<!--", "", linha):
            add("ERRO", "guia", n, "ponto de exclamação", linha)
        if EMOJI.search(linha):
            add("ERRO", "guia", n, "emoji", linha)
        if corpo and re.search(r"\b[A-ZÁÉÍÓÚÃÕÇ]{6,}\b", linha):
            add("AVISO", "guia", n, "caixa alta para ênfase?", linha)
        if re.search(r"\b(bps|bp)\b", linha) or "pontos base" in baixa:
            add("ERRO", "guia", n, "use 'pontos-base' (1ª vez) e depois 'pb'", linha)
        if re.search(r"\d+\.\d+\s?%", linha):
            add("ERRO", "guia", n, "decimal com ponto; use vírgula (7,5%)", linha)
        if re.search(r"(?<!US)\$\s?\d", linha):
            add("ERRO", "guia", n, "moeda sem prefixo; use 'US$'", linha)
        if re.search(r"\b\d+(,\d+)?\s?(tri|bi|mi)\b", linha):
            add("AVISO", "guia", n, "escreva a unidade por extenso (trilhões, bilhões, milhões)", linha)
        if re.search(r"\b(eu|meu|minha|acho)\b", baixa):
            add("ERRO", "guia", n, "primeira pessoa do singular; use 'nós' institucional", linha)
        if re.search(r"\b(foi|foram) (revisad|elevad|reduzid|cortad)", baixa):
            add("AVISO", "guia", n, "voz passiva em revisão; prefira 'Elevamos/Reduzimos'", linha)
        for a in VAGOS:
            if re.search(rf"(?<!\w){re.escape(a)}(?!\w)", baixa):
                add("AVISO", "guia", n, f"intensificador vago '{a}': troque por número e comparação", linha)
        for a in ABSOLUTOS:
            if re.search(rf"\b{a}\b", baixa):
                add("AVISO", "guia", n, f"absoluto '{a}': confirme que é fato, não projeção", linha)
        if linha.startswith("## "):
            titulo = linha[3:].strip().rstrip(".").lower()
            if titulo not in SECOES_FIXAS and not re.search(r"[:,]|\.\.\.", titulo):
                add("AVISO", "guia", n, "título de seção sem tese em duas partes", linha)

        # [ia]
        if corpo:
            for m in re.finditer(r"—|\s–\s", linha):
                travessoes.append(n)
            if len(re.findall(r"—|\s–\s", linha)) >= 2:
                add("AVISO", "ia", n, "dois travessões na mesma linha (aposto entre travessões): use vírgulas ou divida a frase", linha)
            for c in CLICHES_IA:
                if re.search(rf"(?<!\w){re.escape(c)}(?!\w)", baixa):
                    add("AVISO", "ia", n, f"clichê de texto gerado: '{c}'", linha)
            if re.search(r"\bnão (é|são|se trata)( apenas| só| somente| de)?\b[^.;]{1,60}[,;]\s*(mas|e sim|é|são)\b", baixa) \
                    or re.search(r"\bmais do que [^.,]{1,40}, (é|são)\b", baixa):
                add("AVISO", "ia", n, "fórmula 'não é X, é Y' / 'mais do que X, é Y': afirme Y diretamente", linha)
            if "?" in linha and not linha.strip().startswith("-"):
                add("AVISO", "ia", n, "pergunta retórica: transforme em afirmação", linha)
            if re.search(r"[\"“]\w+[\"”]", linha):
                add("AVISO", "ia", n, "aspas em palavra solta (aspas de ênfase): tire ou atribua a fonte", linha)
            for a in ABERTURAS_GENERICAS:
                if baixa.lstrip("-*• ").startswith(a) and not linha.startswith("#"):
                    add("AVISO", "ia", n, f"abertura genérica '{a}': comece pela conclusão", linha)
            if not ROTULO.match(linha) and "Autores" not in linha:
                sem_rotulo = re.sub(r"^\s*[-*•]?\s*\*\*[^*]{1,120}\*\*", "", linha)  # título em negrito
                sem_rotulo = re.sub(r"\[[^\]]*\]", "", sem_rotulo)  # marcadores de modelo
                sem_rotulo = re.sub(r"https?://\S+|\d{1,2}:\d{2}", "", sem_rotulo)
                if sem_rotulo.count(":") >= 2:
                    add("AVISO", "ia", n, "vários dois-pontos na mesma linha: reescreva como frases", linha)
                elif re.search(r"^[^:]{3,45}:\s+\S", sem_rotulo.lstrip("-*• ")) and len(palavras(sem_rotulo)) > 8:
                    add("AVISO", "ia", n, "dois-pontos de efeito (frase curta + ':' + revelação): ligue com verbo ou conectivo", linha)
            if len(re.findall(r"\*\*[^*]+\*\*", linha)) >= 2 and "Autores" not in linha:
                add("AVISO", "ia", n, "negrito em excesso na mesma linha", linha)

    # densidade de travessões
    if travessoes:
        por_150 = len(travessoes) / max(total_palavras, 1) * 150
        nivel = "ERRO" if por_150 > 1 else "AVISO"
        add(nivel, "ia", travessoes[0],
            f"{len(travessoes)} travessão(ões) no texto ({por_150:.1f} a cada 150 palavras; máx. 1). "
            f"Use vírgula, ponto ou parênteses. Linhas: {sorted(set(travessoes))[:12]}")

    # repetição de palavras infladas e de tríades
    corpo_txt = "\n".join(l for l in linhas if not l.startswith(("#", "|", "<!--")))
    cont = Counter(w.lower() for w in palavras(corpo_txt))
    for w in INFLADOS:
        if cont[w] > 2:
            add("AVISO", "ia", 0, f"'{w}' aparece {cont[w]} vezes: varie ou troque por número")
    triades = re.findall(r"\b[\wÀ-ÿ]+, [\wÀ-ÿ]+ e [\wÀ-ÿ]+\b", corpo_txt)
    if len(triades) > max(3, total_palavras // 250):
        add("AVISO", "ia", 0, f"{len(triades)} listas de três itens ('X, Y e Z'): ritmo de texto gerado; varie")

    # ---- análise por parágrafo (conexão, tamanho, revisões)
    blocos, paragrafo, inicio, em_codigo, secao = [], [], 0, False, 0
    lista = False
    for n, linha in enumerate(linhas + [""], 1):
        if linha.strip().startswith("```"):
            em_codigo = not em_codigo
        if re.match(r"^[¹²³⁴⁵⁶⁷⁸⁹]", linha.strip()) and paragrafo:
            blocos.append((inicio, " ".join(paragrafo), secao, lista))
            paragrafo = []
        if linha.startswith("#"):
            secao += 1
        meta_linha = re.match(r"^\s*(Fonte|Nota|Notas|Retorno passado)\b", linha)
        if em_codigo or meta_linha or not linha.strip() or linha.startswith(("#", "|", ">", "---", "<!--")):
            if paragrafo:
                blocos.append((inicio, " ".join(paragrafo), secao, lista))
            paragrafo = []
            continue
        if not paragrafo:
            inicio = n
            lista = bool(re.match(r"^\s*[-*•]", linha))
        paragrafo.append(linha.strip().lstrip("-*• ").strip())

    uso_conectivos = Counter()
    anterior = None
    for n, p, sec, lista in blocos:
        fs = frases(p)
        limite = TEMAS.get(tema, {}).get("max_frase", 40)
        for f in fs:
            np_ = len(palavras(f))
            if np_ > limite + 10:
                add("ERRO", "guia", n, f"frase com {np_} palavras (máx. {limite})", f)
            elif np_ > limite:
                add("AVISO", "guia", n, f"frase com {np_} palavras (máx. {limite})", f)
            if re.search(VERBOS_REVISAO, f):
                tem_pb = re.search(r"pontos-base|\bpb\b", f)
                if not tem_pb and "%" in f:
                    add("ERRO", "guia", n, "revisão sem tamanho em pontos-base", f)
                if not tem_pb and not re.search(r"para \d+(,\d+)?%", f):
                    add("ERRO", "guia", n, "revisão sem tamanho e sem destino ('em N pb, para Y%')", f)
            fl = f.lower()
            for c in TODOS_CONECTIVOS:
                if len(c) > 4 and (fl.startswith(c + " ") or fl.startswith(c + ",")):
                    uso_conectivos[c] += 1
                    break
        if re.search(VERBOS_PROJECAO, p) and "%" in p and \
                not re.search(r"\banos?\b|horizonte|até 20\d\d|ao ano|em 20\d\d|meses|prazo", p):
            add("AVISO", "guia", n, "projeção com % sem horizonte explícito", p)

        # [conexão] frases picotadas e inícios repetidos
        curtas = 0
        for f in fs:
            curtas = curtas + 1 if len(palavras(f)) < 9 else 0
            if curtas == 3:
                add("AVISO", "conexão", n, "três frases curtas seguidas (texto picotado): una duas com 'porque', 'o que', 'mas' ou 'e'", p)
                break
        inicios = [palavras(f)[0].lower() for f in fs if palavras(f)]
        for i in range(len(inicios) - 2):
            if inicios[i] == inicios[i + 1] == inicios[i + 2]:
                add("AVISO", "conexão", n, f"três frases seguidas começam com '{inicios[i]}'", p)
                break

        # [conexão] transição abrupta entre parágrafos da mesma seção
        nota_ou_modelo = re.match(r"^[¹²³⁴⁵⁶⁷⁸⁹\[]", p)
        if anterior and anterior[2] == sec and not lista and not anterior[3] and fs and not nota_ou_modelo:
            primeira = fs[0]
            ligado = (comeca_com_conectivo(primeira) or RETOMADA.search(primeira)
                      or raizes(primeira) & raizes(anterior[1]))
            if not ligado:
                funcao, sugestao = funcao_sugerida(p)
                add("AVISO", "conexão", n,
                    f"transição abrupta: o parágrafo não retoma o anterior. Relação provável: {funcao}. "
                    f"Sugestões: {sugestao}", primeira)
        anterior = (n, p, sec, lista)

    for c, k in uso_conectivos.items():
        if k > 2:
            add("AVISO", "conexão", 0, f"conectivo '{c}' abre {k} frases: varie (ver GUIA §10)")
    total_frases = sum(len(frases(p)) for _, p, _, _ in blocos)
    if total_frases >= 12 and sum(uso_conectivos.values()) / total_frases > 0.4:
        add("AVISO", "conexão", 0, "mais de 40% das frases abrem com conectivo: o texto fica mecânico")

    # ---- documento
    if re.search(r"\d+(,\d+)?%", texto) and "Fonte:" not in texto:
        add("ERRO", "guia", 0, "documento com números e sem nenhuma linha 'Fonte:'")

    # [tema]
    if tema:
        regras = TEMAS.get(tema)
        if not regras:
            add("ERRO", "tema", 0, f"tema '{tema}' desconhecido. Use: {', '.join(TEMAS)}")
        else:
            for rx, msg in regras["obrigatorios"]:
                if not re.search(rx, texto, re.I | re.M):
                    add("ERRO", "tema", 0, f"[{tema}] {msg}")
            for rx, msg in regras["proibidos"]:
                for m in re.finditer(rx, texto, re.I | re.M):
                    add("ERRO", "tema", texto[:m.start()].count("\n") + 1, f"[{tema}] {msg}", m.group(0))
            for rx, msg in regras["avisos"]:
                for m in re.finditer(rx, texto, re.M):
                    n = texto[:m.start()].count("\n") + 1
                    linha = linhas[n - 1] if n - 1 < len(linhas) else ""
                    if not linha.startswith(("#", "|", "<!--")):
                        add("AVISO", "tema", n, f"[{tema}] {msg}", m.group(0))
            if regras["exige_em_resumo"] and "Em resumo" not in texto:
                add("ERRO", "tema", 0, f"[{tema}] falta o bloco 'Em resumo'")
    elif len(texto.split()) > 300:
        add("AVISO", "tema", 0, "sem tema declarado; adicione 'tema:' no cabeçalho para as regras específicas")
    return tema, achados


def main(args):
    if "--temas" in args:
        for k, v in TEMAS.items():
            print(f"  {k:<10} {v['descricao']}")
        return 0
    tema = None
    if "--tema" in args:
        i = args.index("--tema")
        tema = args[i + 1]
        args = args[:i] + args[i + 2:]
    total_erros = 0
    for a in args:
        t, achados = revisar(a, tema)
        erros = sum(1 for x in achados if x[0] == "ERRO")
        total_erros += erros
        print(f"\n{a}  (tema: {t or '—'}): {erros} erro(s), {len(achados) - erros} aviso(s)")
        for nivel, cat, n, msg, trecho in sorted(achados, key=lambda x: (x[2], x[1], x[0])):
            loc = f"L{n}" if n else "doc"
            print(f"  {nivel:<5} {loc:<5} [{cat}] {msg}" + (f"\n                └ {trecho}" if trecho else ""))
    return 1 if total_erros else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
