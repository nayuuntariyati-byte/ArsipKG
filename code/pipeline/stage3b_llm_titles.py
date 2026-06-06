"""
Stage 3B: LLM-Based Supersession Extraction.
Extracts menggantikan / menggantikan_sebagian relations from regulation titles.
Uses LLaMA-3.2-3B-Instruct on the 49-document PA/PC subset.
Precision = 0.391 (paper §5.2, Table 6).
"""

import argparse
import json
import re
from pathlib import Path
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

PROMPT_TEMPLATE = """Ekstrak relasi supersesi dari judul peraturan Indonesia.
Output JSON: {"menggantikan": [...], "menggantikan_sebagian": [...], "confidence": 0.0-1.0}

Contoh:
Judul: "Pencabutan Peraturan Menteri Kesehatan Nomor 12 Tahun 2018"
Output: {"menggantikan": ["PERMENKES 12/2018"], "menggantikan_sebagian": [], "confidence": 0.95}

Judul: "Perubahan atas Peraturan Menteri Nomor 5 Tahun 2019"
Output: {"menggantikan": [], "menggantikan_sebagian": ["PERMEN 5/2019"], "confidence": 0.90}

Judul: "{title}"
Output:"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="meta-llama/Llama-3.2-3B-Instruct")
    ap.add_argument("--data", default="../../data/arsipdataset/arsipdataset.csv")
    ap.add_argument("--output", default="../../results/stage3b_supersession.jsonl")
    ap.add_argument("--confidence_threshold", type=float, default=0.70)
    args = ap.parse_args()

    bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                    bnb_4bit_compute_dtype=torch.float16)
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, quantization_config=bnb_config, device_map="auto")
    model.eval()

    df = pd.read_csv(args.data, comment="#")
    # Filter to PA/PC subset only (49 documents in production)
    subset = df[df["kategori"].isin(["PA", "PC"])]
    print(f"Processing {len(subset)} PA/PC documents")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        for _, row in subset.iterrows():
            prompt = PROMPT_TEMPLATE.format(title=row["tentang"])
            inputs = tok(prompt, return_tensors="pt").to(model.device)
            with torch.no_grad():
                out = model.generate(**inputs, max_new_tokens=256, temperature=0.1,
                                     pad_token_id=tok.eos_token_id)
            raw = tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
            try:
                result = json.loads(raw.split("\n")[0])
            except Exception:
                result = {"menggantikan": [], "menggantikan_sebagian": [],
                          "confidence": 0.0, "raw": raw}
            result["id"] = row["id"]
            result["flagged_for_review"] = result.get("confidence", 0) < args.confidence_threshold
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
    print(f"Done. Output: {args.output}")


if __name__ == "__main__":
    main()
