# Supervised Baselines

Three baselines for comparison with the few-shot LLM approach (paper §5.1, Table 4).

| Baseline | F1 (vs manual labels) | Description |
|---|---|---|
| Rule-based | 0.7815 | Keyword matching in `tentang` field |
| TF-IDF + LinearSVC | 0.7815 | Bag-of-words with class-weight balancing |
| IndoBERT (no weights) | 0.3838 | Fine-tuned indobert-base-p1 |
| IndoBERT (class-weighted) | 0.4187 | + inverse-frequency class weights |

## Running

```bash
python rule_based.py --data ../../data/arsipdataset/splits/test.csv
python tfidf_svm.py --train ../../data/arsipdataset/splits/train.csv \
                    --test ../../data/arsipdataset/splits/test.csv
python indobert_finetune.py --class_weighted  # use --no-weights for no-weight variant
```
