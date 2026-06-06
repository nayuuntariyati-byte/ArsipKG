"""
Stage 2: Few-Shot LLM Classification.
Classifies each document into one of 6 taxonomy categories using LLaMA-3.1-8B-Instruct.
Achieves macro-F1 = 0.963 with k=3 shots (paper §5.1).
"""

import argparse
import json
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

SYSTEM_PROMPT = """Anda adalah ahli klasifikasi peraturan kearsipan Indonesia.
Klasifikasikan setiap peraturan ke dalam satu dari enam kategori:
- KA (Klasifikasi Arsip): peraturan tentang skema klasifikasi arsip
- JRA (Jadwal Retensi Arsip): peraturan tentang jadwal retensi
- SKKAAD (Sistem Klasifikasi Keamanan dan Akses Arsip Dinamis): keamanan dan akses
- PK (Penyelenggaraan Kearsipan): manajemen kearsipan umum (residual)
- PA (Perubahan/Amendment): peraturan yang mengubah sebagian peraturan lain
- PC (Pencabutan/Revocation): peraturan yang mencabut peraturan lain

Hierarki: PC dan PA didahulukan. Output berupa JSON dengan field
{"kategori": "...", "confidence": 0.0-1.0, "alasan": "..."}.
"""


def build_prompt(tentang, jenis, few_shot_examples):
    """Construct the few-shot prompt with k exemplars per category."""
    parts = [SYSTEM_PROMPT, "\n\nContoh:\n"]
    for ex in few_shot_examples:
        parts.append(f'Tentang: "{ex["tentang"]}"\nJenis: {ex["jenis"]}\n'
                     f'Output: {{"kategori": "{ex["kategori"]}", "confidence": 1.0, '
                     f'"alasan": "{ex["alasan"]}"}}\n\n')
    parts.append(f'Tentang: "{tentang}"\nJenis: {jenis}\nOutput:')
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="meta-llama/Llama-3.1-8B-Instruct")
    ap.add_argument("--k", type=int, default=3, choices=[0, 3, 5, 10])
    ap.add_argument("--data", default="../../data/arsipdataset/splits/test.csv")
    ap.add_argument("--examples", default="prompts/few_shot_examples_k3.json")
    ap.add_argument("--output", default="../../results/llama_predictions.jsonl")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    torch.manual_seed(args.seed)

    print(f"Loading model {args.model} with 4-bit NF4 quantization...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True, bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, quantization_config=bnb_config, device_map="auto")
    model.eval()

    # Load few-shot examples (k per category, stratified)
    if args.k > 0:
        with open(args.examples) as f:
            examples = json.load(f)
    else:
        examples = []

    df = pd.read_csv(args.data, comment="#")
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    predictions = []
    for _, row in df.iterrows():
        prompt = build_prompt(row["tentang"], row.get("jenis_bentuk_peraturan", ""), examples)
        inputs = tok(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=256,
                                 temperature=0.1, top_p=0.9, do_sample=True,
                                 pad_token_id=tok.eos_token_id)
        raw = tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        try:
            parsed = json.loads(raw.split("\n")[0])
        except Exception:
            parsed = {"kategori": "PK", "confidence": 0.0, "alasan": "parse_error", "raw": raw}
        parsed["id"] = row.get("id", "")
        predictions.append(parsed)

    with open(args.output, "w") as f:
        for p in predictions:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    print(f"Predictions written to {args.output}")


if __name__ == "__main__":
    main()
