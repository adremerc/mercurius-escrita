# Fine-tuning (LoRA) do mercurius-escrita

Só vale a pena depois de juntar **200 a 500 pares** aprovados. Antes disso, o prompt de sistema
mais o laço do revisor rendem quase o mesmo. Esta máquina (13 GB de RAM, sem placa NVIDIA) não
treina modelo, então o treino roda na nuvem e o resultado volta para o Ollama.

## 1. Juntar os pares

Cada vez que você rodar `escrever.py reescrever`, os parágrafos aprovados sem nenhum apontamento
viram um par novo em `ollama/pares_aprendidos.jsonl`. Antes de treinar, **leia os pares**: um par
ruim ensina o modelo a errar. Apague os que estiverem estranhos.

```bash
python ollama/exportar_finetune.py
```

Isso gera `ollama/finetune/treino.jsonl` e `validacao.jsonl`.

## 2. Treinar no Google Colab (GPU T4 gratuita, ou L4 por poucos dólares)

Abra um notebook novo em colab.research.google.com com GPU, suba os dois arquivos e rode:

```python
!pip install -q unsloth
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

modelo, tok = FastLanguageModel.from_pretrained("unsloth/Qwen3-4B-Instruct-2507", max_seq_length=2048, load_in_4bit=True)
modelo = FastLanguageModel.get_peft_model(modelo, r=16, lora_alpha=32, target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"])
dados = load_dataset("json", data_files={"train": "treino.jsonl", "validation": "validacao.jsonl"})
dados = dados.map(lambda ex: {"text": tok.apply_chat_template(ex["messages"], tokenize=False)})

SFTTrainer(model=modelo, tokenizer=tok, train_dataset=dados["train"], eval_dataset=dados["validation"],
           args=SFTConfig(per_device_train_batch_size=2, gradient_accumulation_steps=4, num_train_epochs=3,
                          learning_rate=2e-4, output_dir="saida", dataset_text_field="text", report_to="none")).train()

modelo.save_pretrained_gguf("mercurius-escrita-gguf", tok, quantization_method="q4_k_m")
```

Baixe o arquivo `.gguf` gerado.

## 3. Voltar para o Ollama

Crie um arquivo `Modelfile.ft` ao lado do `.gguf`:

```
FROM ./mercurius-escrita-q4_k_m.gguf
PARAMETER temperature 0.3
PARAMETER num_ctx 4096
```

```bash
ollama create mercurius-escrita-v2 -f Modelfile.ft
OLLAMA_MODELO=mercurius-escrita-v2 python ollama/avaliar.py
```

Compare o resultado novo com o `RESULTADOS.md` anterior. Só troque de modelo se a média baixar.

## Cuidados

- Nunca inclua no treino textos com números reais de clientes ou informação confidencial.
- Mantenha o teste cego (`teste_cego.jsonl`) fora do treino. O exportador já faz isso.
- Treinar demais com poucos pares faz o modelo decorar frases. Três épocas bastam.
