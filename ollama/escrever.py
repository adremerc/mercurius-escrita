"""Reescreve textos no padrão Mercurius com o Ollama, em laço com o revisor.

    python ollama/escrever.py reescrever texto.md --tema cripto            # imprime o resultado
    python ollama/escrever.py reescrever texto.md --tema cripto -o saida.md
    echo "parágrafo..." | python ollama/escrever.py reescrever - --tema macro
    python ollama/escrever.py rascunho --tema cripto --fatos "ETFs captaram US$ 38 bi em 2026; volatilidade de 48% a.a."

Como funciona, para cada parágrafo de prosa (títulos, tabelas, listas de código e notas passam direto):
  1. o modelo reescreve;
  2. uma limpeza mecânica tira travessões, "vale ressaltar" e afins;
  3. o revisor confere. Se houver problema, ele volta ao modelo como lista de correções;
  4. repete até zerar (máx. --rodadas), guardando a melhor versão;
  5. um guarda de números barra qualquer número que mude, suma ou seja inventado.
Os pares (antes, depois) aprovados vão para ollama/pares_aprendidos.jsonl e alimentam um futuro fine-tuning.
"""

import argparse
import json
import os
import re
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "ferramentas"))
sys.path.insert(0, str(AQUI))
import revisor  # noqa: E402
from criar_modelo import instrucao  # noqa: E402

URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
MODELO = os.environ.get("OLLAMA_MODELO", "mercurius-escrita")
APRENDIDOS = AQUI / "pares_aprendidos.jsonl"
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


# ------------------------------------------------------------------ Ollama
def chamar(mensagens, modelo=MODELO, max_tokens=500):
    corpo = {"model": modelo, "messages": mensagens, "stream": False, "think": False, "keep_alive": "30m",
             "options": {"temperature": 0.3, "num_predict": max_tokens}}
    req = urllib.request.Request(URL, json.dumps(corpo).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())["message"]["content"].strip()


# ------------------------------------------------------- limpeza mecânica
ABERTURAS = ["vale ressaltar que", "vale destacar que", "vale lembrar que", "vale notar que",
             "é importante destacar que", "é importante ressaltar que", "é importante notar que",
             "é fundamental destacar que", "em suma,", "em resumo,", "em conclusão,", "concluindo,",
             "no cenário atual,", "no atual cenário,", "nesse contexto,", "neste contexto,",
             "nesse sentido,", "neste sentido,", "ademais,", "outrossim,"]


def limpeza_mecanica(t):
    t = t.replace("**", "") if t.count("**") % 2 else t
    t = re.sub(r"\s+[—–]\s+", ", ", t)           # travessão de aposto vira vírgula
    t = re.sub(r"[—–]", ", ", t)
    t = t.replace("!", ".")
    t = EMOJI.sub("", t)
    for a in ABERTURAS:                            # no início de frase
        t = re.sub(rf"(^|(?<=[.?;] ))\s*{re.escape(a)}\s*([a-záéíóúâêôãõç])",
                   lambda m: (m.group(1) or "") + m.group(2).upper(), t, flags=re.I)
    return re.sub(r"\s{2,}", " ", re.sub(r"\s+,", ",", t)).strip()


# ---------------------------------------------------------- guarda de números
def numeros(t):
    t = re.sub(r"[¹²³⁴⁵⁶⁷⁸⁹⁰]", "", t)
    return sorted(m.rstrip(".,") for m in re.findall(r"\d[\d.,]*", t))


def checar_numeros(antes, depois):
    a, b = numeros(antes), numeros(depois)
    faltam = [n for n in set(a) if a.count(n) > b.count(n)]
    sobram = [n for n in set(b) if b.count(n) > a.count(n)]
    msgs = []
    if faltam:
        msgs.append(f"Faltam números do original: {', '.join(faltam)}. Mantenha todos.")
    if sobram:
        msgs.append(f"Há números que não existem no original: {', '.join(sobram)}. Remova.")
    return msgs



# ------------------------------------------------------- guarda de fidelidade
# Ideias que a IA costuma inventar ao reescrever. Se aparecem no texto novo e não no original, é acréscimo.
ALERTA = ["projeção", "projeções", "pontos-base", "recomend", "prazo", "anual", "anualmente", "trimestre",
          "cenário", "correlação", "saturação", "validação", "estimamos", "esperamos que", "devido à", "devido ao",
          "2025", "2026", "2027", "2028", "2029", "2030", "2035"]
PARADAS = set("""para com como mais menos muito pelo pela pelos pelas desde entre sobre ainda também porque mas
quando onde esse essa isso este esta estes estas seu sua seus suas nosso nossa são foi foram será serão está estão
ser ter tem têm pode podem deve devem uma uns umas dos das nos nas num numa aos até após cada todo toda todos todas
outro outra outros outras qual quais depois antes sempre nunca apenas""".split())


def radicais(t):
    return {w.lower()[:6] for w in re.findall(r"[A-Za-zÀ-ÿ]+", t) if len(w) >= 6 and w.lower() not in PARADAS}


def checar_fidelidade(antes, depois):
    """Barra conteúdo que o original não tem: ideias inventadas, texto muito maior, muito vocabulário novo."""
    depois = re.sub(r"\[DADO:[^\]]*\]", "", depois)     # o conteúdo do marcador não conta como informação nova
    msgs, a, d = [], antes.lower(), depois.lower()
    novos = [w for w in ALERTA if w in d and w not in a]
    if novos:
        msgs.append("Você acrescentou ideias que não estão no original (" + ", ".join(novos[:5]) +
                    "). Remova e use só o que o original diz.")
    na, nd = len(re.findall(r"\w+", antes)), len(re.findall(r"\w+", depois))
    if nd > 1.5 * na + 8:
        msgs.append(f"O texto novo tem {nd} palavras e o original {na}. Corte o que não está no original.")
    ra, rd = radicais(antes), radicais(depois)
    if rd and len(rd - ra) / len(rd) > 0.68 and nd > 16:
        msgs.append("O texto novo traz muita informação que o original não tem. Reescreva só o estilo, sem mudar o conteúdo.")
    return msgs

# ---------------------------------------------------------------- revisor
def apontamentos(texto, tema):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(texto + "\n\nFonte: interna.\n")
        caminho = f.name
    try:
        _, ach = revisor.revisar(caminho, tema)
    finally:
        os.unlink(caminho)
    saida = []
    for nivel, cat, n, msg, trecho in ach:
        if n == 0 and cat in ("tema", "guia", "conexão"):     # regras de documento inteiro
            continue
        if "transição abrupta" in msg:                         # exige o parágrafo anterior
            continue
        saida.append((nivel, cat, msg, trecho))
    return saida


def pontuar(ach):
    return sum(10 if n == "ERRO" else 1 for n, *_ in ach)


def feedback(ach, avisos_numericos):
    linhas = []
    for nivel, cat, msg, trecho in ach:
        linhas.append(f"- {msg}" + (f' (trecho: "{trecho[:70]}")' if trecho else ""))
    linhas += [f"- {m}" for m in avisos_numericos]
    return ("O texto ainda tem estes problemas:\n" + "\n".join(linhas) +
            "\nCorrija todos, mantendo os fatos e os números. Responda só com o texto corrigido.")


# ------------------------------------------------------------ um parágrafo
def reescrever_paragrafo(texto, tema, rodadas=3, verbose=True):
    msgs = [{"role": "user", "content": instrucao(tema, texto)}]
    melhor, melhor_pont, historico = None, 10**9, []
    for r in range(1, rodadas + 1):
        t0 = time.time()
        cand = limpeza_mecanica(chamar(msgs))
        ach = apontamentos(cand, tema)
        num = checar_numeros(texto, cand) + checar_fidelidade(texto, cand)
        pont = pontuar(ach) + 10 * len(num)
        historico.append((r, pont))
        if verbose:
            print(f"    rodada {r}: {len(ach)} apontamento(s), {len(num)} problema(s) de número/fidelidade, {time.time() - t0:.0f}s",
                  file=sys.stderr)
        if pont < melhor_pont:
            melhor, melhor_pont = cand, pont
        if pont == 0:
            break
        msgs += [{"role": "assistant", "content": cand}, {"role": "user", "content": feedback(ach, num)}]
    return melhor, melhor_pont, historico


# ----------------------------------------------------------------- arquivo
def eh_prosa(par):
    p = par.strip()
    if not p or p.startswith(("#", "|", ">", "<!--", "```", "---", "![", "Fonte:", "Nota:", "Fontes:")):
        return False
    if re.match(r"^[¹²³⁴⁵⁶⁷⁸⁹]", p) or len(re.findall(r"\w+", p)) < 8:
        return False
    return True


def guardar_par(antes, depois, tema):
    novo = {"tema": tema or "macro", "antes": antes.strip(), "depois": depois.strip()}
    if APRENDIDOS.exists() and any(json.loads(l)["antes"] == novo["antes"] for l in APRENDIDOS.read_text(encoding="utf-8").splitlines() if l.strip()):
        return
    with APRENDIDOS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(novo, ensure_ascii=False) + "\n")


def reescrever_texto(texto, tema, rodadas, aprender):
    blocos = re.split(r"\n\s*\n", texto)
    saida, n_ok, n_total = [], 0, 0
    for i, bloco in enumerate(blocos, 1):
        if not eh_prosa(bloco):
            saida.append(bloco)
            continue
        n_total += 1
        print(f"[{i}/{len(blocos)}] {bloco.strip()[:60]}...", file=sys.stderr)
        novo, pont, _ = reescrever_paragrafo(" ".join(bloco.split()), tema, rodadas)
        if pont == 0:
            n_ok += 1
            if aprender:
                guardar_par(" ".join(bloco.split()), novo, tema)
        else:
            print(f"    atenção: ficou com pontuação {pont}; revise à mão", file=sys.stderr)
        saida.append(novo if novo else bloco)
    print(f"\n{n_ok}/{n_total} parágrafos aprovados sem apontamentos.", file=sys.stderr)
    return "\n\n".join(saida)


def rascunho(tema, fatos, rodadas):
    pedido = (f"Escreva um parágrafo de análise no padrão Mercurius (tema: {tema}) usando SOMENTE estes fatos, "
              f"sem inventar nenhum número. Comece pela conclusão.\nFatos: {fatos}")
    msgs = [{"role": "user", "content": pedido}]
    melhor, melhor_pont = None, 10**9
    for r in range(rodadas):
        cand = limpeza_mecanica(chamar(msgs, max_tokens=400))
        ach = apontamentos(cand, tema)
        num = checar_numeros(fatos, cand)
        num = [m for m in num if m.startswith("Há números")]     # só barra números inventados
        pont = pontuar(ach) + 10 * len(num)
        if pont < melhor_pont:
            melhor, melhor_pont = cand, pont
        if pont == 0:
            break
        msgs += [{"role": "assistant", "content": cand}, {"role": "user", "content": feedback(ach, num)}]
    return melhor


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("reescrever"); r.add_argument("arquivo"); r.add_argument("--tema", default=None)
    r.add_argument("-o", "--saida"); r.add_argument("--rodadas", type=int, default=3)
    r.add_argument("--nao-aprender", action="store_true")
    d = sub.add_parser("rascunho"); d.add_argument("--tema", required=True); d.add_argument("--fatos", required=True)
    d.add_argument("--rodadas", type=int, default=3)
    a = ap.parse_args()
    if a.cmd == "reescrever":
        texto = sys.stdin.read() if a.arquivo == "-" else Path(a.arquivo).read_text(encoding="utf-8")
        tema = a.tema or revisor.ler_cabecalho(texto).get("tema")
        res = reescrever_texto(texto, tema, a.rodadas, not a.nao_aprender)
        if a.saida:
            Path(a.saida).write_text(res, encoding="utf-8"); print("salvo em", a.saida, file=sys.stderr)
        else:
            print(res)
    else:
        print(rascunho(a.tema, a.fatos, a.rodadas))
