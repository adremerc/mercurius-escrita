# Ollama: redator local da Mercurius

Um modelo local (`mercurius-escrita`) que reescreve textos no padrão do [GUIA](../GUIA.md), tira os
vícios de IA e escreve rascunhos de relatório. Roda no seu computador, sem enviar nada para a nuvem.

## Uso rápido

```bash
# 1. criar o modelo (uma vez, e de novo sempre que mudar o prompt ou os pares)
python ollama/criar_modelo.py

# 2. reescrever um texto, parágrafo por parágrafo, com o revisor conferindo
python ollama/escrever.py reescrever meu-texto.md --tema cripto -o meu-texto-novo.md

# 3. rascunho a partir de fatos que você fornece (ele não inventa número)
python ollama/escrever.py rascunho --tema cripto --fatos "ETFs captaram US$ 38 bi em 2026; volatilidade de 48% ao ano"
```

O Ollama precisa estar aberto (ícone na bandeja ou `ollama serve`).

## O que acontece por baixo

| Etapa | O que faz |
|---|---|
| Modelo treinado por prompt | `prompt_sistema.txt` (regras e vícios proibidos) mais 5 exemplos antes/depois embutidos |
| Limpeza mecânica | tira travessões, "vale ressaltar", "em suma", exclamação e emoji |
| Revisor em laço | confere o texto e devolve a lista de problemas ao modelo, até 3 rodadas |
| Guarda de números | barra qualquer número que mude, suma ou seja inventado |
| Aprendizado | parágrafos aprovados sem apontamentos viram pares em `pares_aprendidos.jsonl` |

## Medindo se melhorou

```bash
python ollama/avaliar.py
```

Roda 6 parágrafos que o modelo nunca viu e compara o modelo cru, o treinado e o treinado com o
laço. O resultado fica em [`RESULTADOS.md`](RESULTADOS.md).

## Limites desta máquina

13 GB de RAM e sem placa de vídeo dedicada. O modelo gera cerca de 6 palavras por segundo, então
um parágrafo leva de 15 a 40 segundos. O modo de raciocínio do Qwen fica desligado, porque
consome todo o limite de resposta e devolve texto vazio. Um modelo de 4 bilhões de parâmetros
às vezes muda o sentido de uma frase: **sempre leia o resultado antes de publicar**.

## Treino de verdade

Veja [`treinar_lora.md`](treinar_lora.md). Só vale a pena com 200 a 500 pares aprovados.
