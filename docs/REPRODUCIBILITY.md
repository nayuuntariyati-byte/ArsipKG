# Reproducibility Guide

This document provides exact steps to reproduce the key results from the paper.

## Expected Results

| Result | Section | Expected Value |
|---|---|---|
| Best classification F1 | §5.1 | 0.963 (LLaMA-3.1-8B 3-shot) |
| Best baseline F1 | §5.1 | 0.4187 (IndoBERT class-weighted) |
| Stage 3A precision | §5.2 | 0.994 |
| Inter-annotator κ (classification) | §4.6 | 0.9504 |
| Inter-annotator κ (triples) | §5.2 | 0.748 |
| KG: nodes / edges | §5.3 | 1,211 / 1,911 |
| QA retention | §5.5 | 103.1% |
| Wilcoxon p (KG-Auto vs Semi-manual) | §5.5 | 0.027 |

## Step 1: Data Preparation

```bash
python code/pipeline/stage1_ingestion.py \
    --input data/arsipdataset/arsipdataset.csv \
    --output data/arsipdataset/normalized.jsonl
```

## Step 2: Run Baselines

```bash
# Rule-based (instant)
python code/baselines/rule_based.py --data data/arsipdataset/splits/test.csv
# Expected: macro-F1 ≈ 0.78

# TF-IDF + SVM
python code/baselines/tfidf_svm.py \
    --train data/arsipdataset/splits/train.csv \
    --test data/arsipdataset/splits/test.csv
# Expected: macro-F1 ≈ 0.78

# IndoBERT (no class weights)
python code/baselines/indobert_finetune.py
# Expected: macro-F1 ≈ 0.38 (after ~10 epochs with early stopping)

# IndoBERT (class-weighted)
python code/baselines/indobert_finetune.py --class_weighted
# Expected: macro-F1 ≈ 0.42
```

## Step 3: Run Best Configuration

```bash
python code/pipeline/stage2_classification.py \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --k 3 \
    --data data/arsipdataset/splits/test.csv \
    --output results/llama8b_3shot.jsonl
# Expected: macro-F1 = 0.963 (180.0 s on NVIDIA T4)

python code/evaluation/evaluate_classification.py \
    --predictions results/llama8b_3shot.jsonl \
    --gold data/arsipdataset/splits/test.csv
```

## Step 4: KG Construction

```bash
python code/pipeline/stage3a_metadata.py  # ~0.06 s for 614 docs
python code/pipeline/stage3b_llm_titles.py  # ~10 min on NVIDIA L4
python code/pipeline/stage4_kg_population.py --format ttl,nt,cypher
# Expected: 1,211 individuals, 1,911 axioms
```

## Step 5: Inter-Annotator Validation

```bash
python code/evaluation/compute_kappa.py \
    --annotator1 data/validation/annotator1_labels.csv \
    --annotator2 data/validation/annotator2_labels.csv
# Expected: κ = 0.9504, agreement = 96.15%
```

## Deterministic Seeds

All scripts use `seed=42` by default. LLM inference uses `temperature=0.1` for reproducibility.

## Hardware Notes

- Paper results from: NVIDIA T4 (Stage 2 classification) + NVIDIA L4 (Stages 3B, 4)
- Lower-VRAM GPUs (≥ 8 GB) can run with `--load_in_4bit` already enabled
- CPU-only execution works for baselines (Rule-based, TF-IDF) only
