# ArsipQA-v1 Benchmark

**90 question-answer pairs** for evaluating KG-grounded question answering on Indonesian government regulatory archives. This is the benchmark used in Section 5.5 of Untariyati et al. (2026) to compare ArsipKG-Auto against semi-manual KG and no-KG (LLM-only) baselines.

## Files

| File | Description |
|---|---|
| **`arsipqa_v1.csv`** | **PRIMARY** benchmark (6 cols) — used to generate paper §5.5 numbers |
| **`arsipqa_v1.jsonl`** | **PRIMARY** in JSON Lines format (programmatic access) |
| `arsipqa_v1_revised.csv` | Supplementary version with `answer_revised` natural-language alternatives for Token F1 / ROUGE-L compatibility |

## Schema (Primary)

### CSV columns
```
id              - Unique question identifier (e.g., Q_menerbitkan_0)
question        - Indonesian natural language question
answer          - Gold standard answer (technical regulation IDs / institution names)
relation        - One of 7 question types (see below)
source_triple   - KG triple supporting the answer
question_format - factoid (80) or count (10)
```

### JSONL format
```json
{
  "id": "Q_menerbitkan_0",
  "question_type": "menerbitkan",
  "question_format": "factoid",
  "question": "Lembaga apa yang menerbitkan peraturan tentang \"PerMENTERI_KEMENTER_5_2015\"?",
  "gold_answer": "KEMENTERIAN PERENCANAAN PEMBANGUNAN NASIONAL/BADAN PERENCANAAN PEMBANGUNAN NASIONAL",
  "source_triple": "KEMENTERIAN PERENCANAAN PEMBANGUNAN NASIONAL/BADAN PERENCANAAN PEMBANGUNAN NASIONAL -> menerbitkan -> PerMENTERI_KEMENTER_5_2015"
}
```

## Distribution by Relation Type (7 types)

| Relation | N | Description |
|---|---|---|
| menerbitkan | 20 | Which institution issued regulation X? |
| berlakuPada | 15 | When did regulation X take effect? |
| mengatur | 15 | What category does regulation X govern? |
| ditetapkanOleh | 10 | Who enacted regulation X? |
| menggantikan | 10 | What regulation was revoked by X? |
| menggantikan_sebagian | 10 | What regulation was partially amended by X? |
| multi_hop | 10 | Aggregation queries (counting, listing across regulations) |
| **TOTAL** | **90** | |

Generation seed: 42 (reproducible).

## Evaluation Results (Paper §5.5, Table 6)

| System | Token F1 | ROUGE-L | BERTScore |
|---|---|---|---|
| No KG (LLM only) | 0.0313 | 0.0664 | 0.6193 |
| Semi-manual KG | 0.0000 | 0.0470 | 0.6410 |
| **ArsipKG-Auto Full** | **0.0227** | **0.0906** | **0.6610** |

**Wilcoxon signed-rank test (BERTScore)**:
- ArsipKG-Auto vs Semi-manual: p = 0.0269 ✓ significant
- Semi-manual vs No-KG: p = 0.0002 ✓ significant
- ArsipKG-Auto vs No-KG: p = 0.5662 (not significant — KG-grounding effect already captured)

**Primary metric: BERTScore** (semantic similarity, robust to format mismatch between technical IDs and natural language).

**Model used**: meta-llama/Llama-3.1-8B-Instruct

Reproduction artifacts available in `../code/evaluation/qa_eval_artifacts/`:
- `predictions/qa_results_*.csv` — per-question predictions for each system
- `table6_qa_evaluation.csv` — aggregated Table 6 (CSV format)
- `table6_qa_summary.json` — complete results with Wilcoxon tests
- `ArsipQA_OpsiB_Reeval_Colab.py` — Colab re-evaluation script
- `table6_comparison_a_vs_b.json` — comparison of two answer-format framings

## About the "revised" version

`arsipqa_v1_revised.csv` was generated during exploratory analysis to test whether using natural-language gold answers (instead of technical regulation IDs) would yield higher Token F1 scores. After comparison, the original technical-ID format was retained as primary because:
1. It is closer to the underlying KG structure (preserves source triples)
2. BERTScore (the primary metric) is robust to format choice
3. The original framing matches what was reported in the paper

The revised version is preserved for transparency and to support users who prefer lexical-overlap metrics. See `table6_comparison_a_vs_b.json` for details.

## Citation

> Untariyati, N.A., Adi, K., Widodo, A.P., Uliniansyah, M.T. (2026). LLM-Driven Few-Shot Classification and Knowledge Graph Population from Indonesian Government Regulatory Archives. *International Journal of Data Science and Analytics*, Springer.

## License

CC BY 4.0
