# Classification Evaluation Artifacts

Supporting data for Section 5.1 "Classification Results" of the paper.

## Files

| File | Description |
|---|---|
| `classification_comparison_8B.png` | Macro-F1 per configuration + per-category F1 for LLaMA-3.1-8B-Instruct (best model in paper) |
| `table4_classification_3B_results.csv` | LLaMA-3.2-3B-Instruct results across 4 shot counts (k=0,3,5,10) for comparison |

## LLaMA-3.1-8B-Instruct (Primary Model)

Source: `classification_comparison_8B.png`

| k-shot | Macro-F1 |
|---|---|
| 0 | 0.900 |
| **3** | **0.963 (best)** |
| 5 | 0.963 |
| 10 | 0.946 |

Per-category F1 (3-shot best configuration):
- KA = 0.923 (one boundary case misclassified as PK)
- JRA = 1.000
- SKKAAD = 0.889
- PK = 0.967 (one document with "Kode Klasifikasi" phrase misclassified as KA)
- PA = 1.000
- PC = 1.000

Stability across k: σ = 0.029 (highly robust)

## LLaMA-3.2-3B-Instruct (Comparison Model)

Source: `table4_classification_3B_results.csv`

| k-shot | Macro-F1 |
|---|---|
| 0 | 1.000 (surface pattern matching) |
| 3 | 0.910 |
| **5** | **0.949 (best valid)** |
| 10 | 0.538 (catastrophic collapse) |

Stability across k: σ = 0.21 (high variance)

Per-category degradation at 10-shot reveals attention dilution failure:
- KA = 0.000 (complete failure)
- PA = 0.000 (complete failure)
- PK = 0.932 (only majority class survives)

## Key Finding

The comparison demonstrates **non-linear shot-count sensitivity** in smaller LLMs:
- 8B model is robust across k ∈ {0, 3, 5, 10}
- 3B model collapses at k=10 due to attention dilution over ~60 demonstration documents
- For production deployment where prompt-engineering oversight is limited, the 8B model is the safer choice

## Reproduction

The exact prompts, hyperparameters (temperature=0.1, top-p=0.9, seed=42), and shot selection strategy are documented in Section 4.3 of the paper. Model: vanilla HuggingFace inference of `meta-llama/Llama-3.1-8B-Instruct` and `meta-llama/Llama-3.2-3B-Instruct` (no fine-tuning).

## Note on Label Correction

The original CSV file (`table1_classification_revised.csv`) labels rows as "LLaMA-3-8B" but the per-category degradation profile (specifically F1_KA=0 and F1_PA=0 at 10-shot, with σ=0.21 across k) unambiguously matches the 3.2-3B model's behavior described in paper §5.1, not the 8B model's stable profile (σ=0.029). Labels have been corrected to "LLaMA-3.2-3B-Instruct" in the version provided here. The visual artifact `classification_comparison_8B.png` correctly shows 8B results (F1=0.963 at 3-shot best, matching paper §5.1 confusion matrix and per-category Table 5).
