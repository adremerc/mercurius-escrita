"""Revisor do padrão de escrita Mercurius Research.

    python ferramentas/revisor.py texto.md [outro.md ...]

Aponta ERROS (quebram o padrão) e AVISOS (pedem revisão humana). Sai com código 1
se houver erro, para poder rodar em CI ou antes de publicar.
"""

import re
import sys
from pathlib import Path

BANIDOS = [
    "explosão", "explodir", "explodiu", "foguete", "to the moon", "bombar", "bombou", "disparou",
    "disparar", "imperdível", "oportunidade única", "revolucionário", "revolucionária",
    "incrível", "absurdo", "absurda", "garantido", "garantida", "certamente", "sem dúvida",
    "com certeza", "obviamente", "claramente", "game changer", "hype",
]
ABSOLUTOS = ["sempre", "nunca", "inevitavelmente", "jamais"]
INFORMAL = ["pra", "pro", "tá", "né", "tipo", "galera", "vai bombar"]
VAGOS = ["muito", "bastante", "enorme", "gigante", "forte alta", "forte queda"]
SECOES_FIXAS = {
    "principais conclusões", "sumário executivo", "em resumo", "autores", "conclusão", "notas",
    "metodologia", "apêndice", "prefácio", "riscos para a nossa perspectiva",
    "implicações para a carteira", "referências", "fontes", "o que mudou desde a última nota",
    "o que mudou desde a última edição", "papel na carteira",
}
VERBOS_REVISAO = r"\b(Elevamos|Reduzimos|Aumentamos|Cortamos|Revisamos|Rebaixamos)\b"
VERBOS_PROJECAO = r"\b(Esperamos|Projetamos|Prevemos|Estimamos)\b"
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


def frases(paragrafo):
    # separa em frases sem quebrar números como 7,5 ou abreviações comuns
    p = paragrafo.replace("**", "")
    p = re.sub(r"\b(Sr|Sra|Dr|Dra|ex|p\.ex|vs|aprox)\.", r"\1§", p)
    partes = re.split(r"(?<=[.?;])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ\"“(])", p)
    return [x.replace("§", ".").strip() for x in partes if x.strip()]


def revisar(caminho):
    texto = Path(caminho).read_text(encoding="utf-8")
    linhas = texto.splitlines()
    achados = []

    def add(nivel, n, msg, trecho=""):
        achados.append((nivel, n, msg, trecho.strip()[:90]))

    em_codigo = False
    for n, linha in enumerate(linhas, 1):
        if linha.strip().startswith("```"):
            em_codigo = not em_codigo
            continue
        if em_codigo or linha.strip().startswith(("|", "<!--", ">")):
            continue
        baixa = linha.lower()

        for b in BANIDOS:
            if re.search(rf"(?<!\w){re.escape(b)}(?!\w)", baixa):
                add("ERRO", n, f"palavra banida: '{b}'", linha)
        if "!" in re.sub(r"!\[|<!--", "", linha):
            add("ERRO", n, "ponto de exclamação", linha)
        if EMOJI.search(linha):
            add("ERRO", n, "emoji", linha)
        if re.search(r"\b[A-ZÁÉÍÓÚÃÕÇ]{6,}\b", linha) and not linha.startswith("#"):
            siglas = re.findall(r"\b[A-ZÁÉÍÓÚÃÕÇ]{6,}\b", linha)
            add("AVISO", n, f"caixa alta para ênfase? {siglas[:3]}", linha)
        if re.search(r"\b(bps|bp)\b", linha) or re.search(r"pontos base", baixa):
            add("ERRO", n, "use 'pontos-base' (1ª vez) e depois 'pb'", linha)
        if re.search(r"\d+\.\d+\s?%", linha):
            add("ERRO", n, "decimal com ponto; use vírgula (7,5%)", linha)
        if re.search(r"(?<!US)\$\s?\d", linha):
            add("ERRO", n, "moeda sem prefixo; use 'US$'", linha)
        if re.search(r"\b\d+(,\d+)?\s?(tri|bi|mi)\b", linha):
            add("AVISO", n, "escreva a unidade por extenso (trilhões, bilhões, milhões)", linha)
        if re.search(r"\b(eu|meu|minha|acho)\b", baixa):
            add("ERRO", n, "primeira pessoa do singular; use 'nós' institucional", linha)
        if re.search(r"\b(foi|foram) (revisad|elevad|reduzid|cortad)", baixa):
            add("AVISO", n, "voz passiva em revisão; prefira 'Elevamos/Reduzimos'", linha)
        for a in INFORMAL:
            if re.search(rf"(?<!\w){re.escape(a)}(?!\w)", baixa):
                add("ERRO", n, f"linguagem informal: '{a}'", linha)
        for a in VAGOS:
            if re.search(rf"(?<!\w){re.escape(a)}(?!\w)", baixa):
                add("AVISO", n, f"intensificador vago '{a}': troque por número e comparação", linha)
        for a in ABSOLUTOS:
            if re.search(rf"\b{a}\b", baixa):
                add("AVISO", n, f"absoluto '{a}': confirme que é fato, não projeção", linha)
        if linha.startswith("## "):
            titulo = linha[3:].strip().rstrip(".").lower()
            if titulo not in SECOES_FIXAS and ":" not in titulo and "..." not in titulo and "," not in titulo:
                add("AVISO", n, "título de seção sem tese em duas partes (use ':' ou '...')", linha)

    # análise por parágrafo
    paragrafo, inicio, em_codigo = [], 0, False
    blocos = []
    for n, linha in enumerate(linhas + [""], 1):
        if linha.strip().startswith("```"):
            em_codigo = not em_codigo
        if re.match(r"^[¹²³⁴⁵⁶⁷⁸⁹]", linha.strip()) and paragrafo:  # nota de rodapé = novo bloco
            blocos.append((inicio, " ".join(paragrafo)))
            paragrafo = []
        if em_codigo or not linha.strip() or linha.startswith(("#", "|", ">")):
            if paragrafo:
                blocos.append((inicio, " ".join(paragrafo)))
            paragrafo = []
            continue
        if not paragrafo:
            inicio = n
        paragrafo.append(linha.strip().lstrip("-*• ").strip())

    for n, p in blocos:
        for f in frases(p):
            palavras = len(re.findall(r"\w+", f))
            if palavras > 50:
                add("ERRO", n, f"frase com {palavras} palavras (máx. 40)", f)
            elif palavras > 40:
                add("AVISO", n, f"frase com {palavras} palavras (máx. 40)", f)
            if re.search(VERBOS_REVISAO, f):
                if not re.search(r"pontos-base|\bpb\b", f) and "%" in f:
                    add("ERRO", n, "revisão sem tamanho em pontos-base", f)
                if not re.search(r"para \d+(,\d+)?%", f) and not re.search(r"pontos-base|\bpb\b", f):
                    add("ERRO", n, "revisão sem tamanho e sem destino ('em N pb, para Y%')", f)
        if re.search(VERBOS_PROJECAO, p) and "%" in p:
            if not re.search(r"\banos?\b|horizonte|até 20\d\d|ao ano|em 20\d\d|meses|prazo", p):
                add("AVISO", n, "projeção com % sem horizonte explícito", p)

    if re.search(r"\d+(,\d+)?%", texto) and "Fonte:" not in texto:
        add("ERRO", 0, "documento com números e sem nenhuma linha 'Fonte:'")
    if re.search(r"^#{1,3} ", texto, re.M) and "Em resumo" not in texto and len(texto.split()) > 600:
        add("AVISO", 0, "documento longo sem bloco 'Em resumo'")
    return achados


def main(arqs):
    total_erros = 0
    for a in arqs:
        achados = revisar(a)
        erros = sum(1 for x in achados if x[0] == "ERRO")
        avisos = len(achados) - erros
        total_erros += erros
        print(f"\n{a}: {erros} erro(s), {avisos} aviso(s)")
        for nivel, n, msg, trecho in sorted(achados, key=lambda x: (x[1], x[0])):
            loc = f"L{n}" if n else "doc"
            print(f"  {nivel:<5} {loc:<5} {msg}" + (f"\n              └ {trecho}" if trecho else ""))
    return 1 if total_erros else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
