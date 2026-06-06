# Four-Stage Pipeline

The taxonomy-guided LLM pipeline described in paper §4.

| Stage | Script | Purpose | Runtime (614 docs) |
|---|---|---|---|
| 1 | `stage1_ingestion.py` | CSV ingestion + metadata normalization | <1 s |
| 2 | `stage2_classification.py` | Few-shot LLM classification (LLaMA-3.1-8B) | ~3 min |
| 3A | `stage3a_metadata.py` | Deterministic triple extraction | 0.061 s |
| 3B | `stage3b_llm_titles.py` | LLM supersession extraction (49 PA/PC docs) | ~10 min |
| 4 | `stage4_kg_population.py` | Neo4j KG construction + RDF export | <30 s |
| **Total** | | | **~11 min** |

## Prompts

Few-shot prompts and example selections are in `prompts/`:
- `system_prompt.md` — 6-category taxonomy definitions
- `few_shot_examples_k3.json` — 3-shot exemplars (best config)
- `few_shot_examples_k5.json` — 5-shot exemplars
- `stage3b_supersession_prompt.md` — Supersession extraction template

## Reproducing Best Result

```bash
python stage1_ingestion.py
python stage2_classification.py --model meta-llama/Llama-3.1-8B-Instruct --k 3
# Expected: macro-F1 = 0.963 on test set
```
