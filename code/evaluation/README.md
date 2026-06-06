# Evaluation Scripts

| Script | Purpose | Key Result |
|---|---|---|
| `compute_kappa.py` | Cohen's κ inter-annotator agreement | κ = 0.9504 |
| `evaluate_classification.py` | Macro-F1 per category | F1 = 0.963 (best) |
| `evaluate_triples.py` | Triple precision vs gold standard | P = 0.994 (Stage 3A) |
| `evaluate_qa.py` | BERTScore, ROUGE-L, Wilcoxon | retention = 103.1% |

## Quick Run

```bash
python compute_kappa.py
python evaluate_classification.py --predictions ../../results/llama_predictions.jsonl
python evaluate_triples.py --gold ../../data/validation/triple_gold_standard.csv
python evaluate_qa.py --benchmark ../../data/arsipqa-v1/arsipqa_v1.jsonl
```
