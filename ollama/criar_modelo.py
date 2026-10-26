"""Cria (ou atualiza) o modelo `mercurius-escrita` no Ollama.

    python ollama/criar_modelo.py                 # usa qwen3.5:4b
    python ollama/criar_modelo.py --base qwen3:8b # outra base
    python ollama/criar_modelo.py --exemplos 6    # mais exemplos embutidos

O Modelfile é gerado a partir de:
  - ollama/prompt_sistema.txt   (regras fixas)
  - ollama/pares_base.jsonl     (exemplos antes/depois escritos à mão)
  - ollama/pares_aprendidos.jsonl, se existir (pares gerados pelo laço e aprovados pelo revisor)
Os exemplos mais curtos entram no Modelfile (poucos tokens, resposta rápida); todos ficam
no dataset para um futuro fine-tuning.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
NOME = "mercurius-escrita"


def instrucao(tema, texto):
    """Formato único de pedido. O escrever.py usa exatamente o mesmo."""
    return f"Reescreva no padrão Mercurius (tema: {tema}):\n{texto}"


def ler_pares():
    pares = []
    for arq in ("pares_base.jsonl", "pares_aprendidos.jsonl"):
        p = AQUI / arq
        if p.exists():
            pares += [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    return pares


def escolher(pares, n):
    """Escolhe n exemplos variados (um por tema primeiro), preferindo os mais curtos."""
    pares = sorted(pares, key=lambda p: len(p["antes"]) + len(p["depois"]))
    escolhidos, temas = [], set()
    for p in pares:
        if p["tema"] not in temas:
            escolhidos.append(p); temas.add(p["tema"])
    for p in pares:
        if len(escolhidos) >= n:
            break
        if p not in escolhidos:
            escolhidos.append(p)
    return escolhidos[:n]


def montar(base, n):
    sistema = (AQUI / "prompt_sistema.txt").read_text(encoding="utf-8").strip()
    linhas = [f"FROM {base}", "PARAMETER temperature 0.3", "PARAMETER top_p 0.9", "PARAMETER repeat_penalty 1.1",
              "PARAMETER num_ctx 4096", "PARAMETER num_predict 600", f'SYSTEM """{sistema}"""']
    for p in escolher(ler_pares(), n):
        linhas.append(f'MESSAGE user """{instrucao(p["tema"], p["antes"])}"""')
        linhas.append(f'MESSAGE assistant """{p["depois"]}"""')
    return "\n".join(linhas) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="qwen3.5:4b")
    ap.add_argument("--exemplos", type=int, default=5)
    a = ap.parse_args()
    mf = AQUI / "Modelfile"
    mf.write_text(montar(a.base, a.exemplos), encoding="utf-8")
    print(f"Modelfile escrito ({mf.stat().st_size} bytes). Criando '{NOME}' sobre {a.base}...")
    r = subprocess.run(["ollama", "create", NOME, "-f", str(mf)], capture_output=True, text=True, encoding="utf-8")
    print(r.stdout or r.stderr)
    sys.exit(r.returncode)
