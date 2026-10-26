"""Exporta os pares (antes, depois) para o formato de fine-tuning (conversas JSONL).

    python ollama/exportar_finetune.py            # gera ollama/finetune/treino.jsonl e validacao.jsonl

Junta pares_base.jsonl (escritos à mão) e pares_aprendidos.jsonl (aprovados pelo revisor), tira
duplicatas, exclui o teste cego e separa 10% para validação. Cada linha é uma conversa completa
(sistema, pedido, resposta), pronta para Unsloth, Axolotl ou TRL.
"""

import json
import random
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from criar_modelo import instrucao  # noqa: E402


def ler(arq):
    p = AQUI / arq
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def main():
    sistema = (AQUI / "prompt_sistema.txt").read_text(encoding="utf-8").strip()
    cego = {d["antes"] for d in ler("teste_cego.jsonl")}
    vistos, pares = set(), []
    for p in ler("pares_base.jsonl") + ler("pares_aprendidos.jsonl"):
        if p["antes"] in vistos or p["antes"] in cego:
            continue
        vistos.add(p["antes"]); pares.append(p)
    random.Random(7).shuffle(pares)
    corte = max(1, len(pares) // 10)
    val, treino = pares[:corte], pares[corte:]
    saida = AQUI / "finetune"; saida.mkdir(exist_ok=True)

    def linha(p):
        return json.dumps({"messages": [{"role": "system", "content": sistema},
                                         {"role": "user", "content": instrucao(p["tema"], p["antes"])},
                                         {"role": "assistant", "content": p["depois"]}]}, ensure_ascii=False)
    (saida / "treino.jsonl").write_text("\n".join(linha(p) for p in treino) + "\n", encoding="utf-8")
    (saida / "validacao.jsonl").write_text("\n".join(linha(p) for p in val) + "\n", encoding="utf-8")
    print(f"{len(treino)} pares de treino, {len(val)} de validação em {saida}")
    if len(pares) < 150:
        print(f"Aviso: {len(pares)} pares ainda é pouco. O ideal para LoRA é de 200 a 500. "
              "Continue usando o escrever.py para juntar mais.")


if __name__ == "__main__":
    main()
