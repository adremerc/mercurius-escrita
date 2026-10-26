"""Mede o quanto o treino melhora o modelo, com parágrafos que ele nunca viu (teste cego).

    python ollama/avaliar.py

Compara três configurações nos mesmos parágrafos:
  A) modelo cru (qwen3.5:4b) com um pedido simples de reescrita
  B) mercurius-escrita, uma tentativa (prompt de sistema + exemplos)
  C) mercurius-escrita com o laço do revisor (até 3 rodadas)
Pontuação de cada texto = 10 por erro + 1 por aviso do revisor + 10 por número alterado. Menor é melhor.
Resultado em ollama/RESULTADOS.md. Rode de novo depois de adicionar pares ou trocar a base.
"""

import json
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import escrever as E  # noqa: E402

BASE = "qwen3.5:4b"
TESTE = [json.loads(l) for l in (AQUI / "teste_cego.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]


def pontos(texto, original, tema):
    """Devolve (estilo, fidelidade). Estilo = pontos do revisor. Fidelidade = nº de problemas de número/conteúdo."""
    ach = E.apontamentos(texto, tema)
    fid = E.checar_numeros(original, texto) + E.checar_fidelidade(original, texto)
    return E.pontuar(ach), len(fid)


def main():
    linhas, est, fid, comb = [], {"A": 0, "B": 0, "C": 0}, {"A": 0, "B": 0, "C": 0}, {"A": 0, "B": 0, "C": 0}
    fieis = {"A": 0, "B": 0, "C": 0}
    detalhes = []
    for i, d in enumerate(TESTE, 1):
        orig, tema = d["antes"], d["tema"]
        e0, _ = pontos(orig, orig, tema)
        t0 = time.time()
        a = E.limpeza_mecanica(E.chamar([{"role": "user", "content": "Reescreva o texto abaixo em português, de forma mais natural e humana, mantendo os fatos:\n" + orig}], modelo=BASE))
        b = E.limpeza_mecanica(E.chamar([{"role": "user", "content": E.instrucao(tema, orig)}]))
        c, _, hist = E.reescrever_paragrafo(orig, tema, rodadas=3, verbose=False)
        celulas = {}
        for k, t in (("A", a), ("B", b), ("C", c)):
            e, f = pontos(t, orig, tema)
            est[k] += e; fid[k] += f; comb[k] += e + 10 * f; fieis[k] += (f == 0)
            celulas[k] = f"{e} / {f}"
        linhas.append(f"| {i} | {tema} | {e0} | {celulas['A']} | {celulas['B']} | {celulas['C']} | {len(hist)} |")
        detalhes.append((i, orig, a, b, c))
        print(f"[{i}/{len(TESTE)}] original={e0}  A={celulas['A']}  B={celulas['B']}  C={celulas['C']}  ({time.time() - t0:.0f}s)", file=sys.stderr, flush=True)
    n = len(TESTE)
    md = ["# Resultado do teste cego", "",
          f"Modelo base: `{BASE}`. {n} parágrafos nunca vistos no treino. Cada célula mostra **estilo / fidelidade**.",
          "Estilo é a pontuação do revisor (10 por erro, 1 por aviso). Fidelidade conta problemas de número alterado, ideia acrescentada ou texto inflado. Menor é melhor nos dois.", "",
          "| # | tema | original | A: cru | B: treinado | C: treinado + laço | rodadas |", "|---|---|---|---|---|---|---|", *linhas,
          f"| | **média estilo** | | **{est['A'] / n:.1f}** | **{est['B'] / n:.1f}** | **{est['C'] / n:.1f}** | |",
          f"| | **problemas de fidelidade** | | **{fid['A']}** | **{fid['B']}** | **{fid['C']}** | |",
          f"| | **parágrafos fiéis** | | **{fieis['A']}/{n}** | **{fieis['B']}/{n}** | **{fieis['C']}/{n}** | |",
          f"| | **nota combinada** | | **{comb['A'] / n:.1f}** | **{comb['B'] / n:.1f}** | **{comb['C'] / n:.1f}** | |", ""]
    for i, orig, a, b, c in detalhes:
        md += [f"## Parágrafo {i}", "**Original**", f"> {orig}", "", "**A (modelo cru)**", f"> {a}", "", "**B (treinado, 1 tentativa)**", f"> {b}", "",
               "**C (treinado + laço)**", f"> {c}", ""]
    (AQUI / "RESULTADOS.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\nnota combinada  A={comb['A'] / n:.1f}  B={comb['B'] / n:.1f}  C={comb['C'] / n:.1f}   fiéis A={fieis['A']} B={fieis['B']} C={fieis['C']}", file=sys.stderr)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
