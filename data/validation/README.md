# Inter-Annotator Validation Dataset

Independently re-annotated stratified sample of 26 documents from the ArsipDataset corpus, used to validate the rule-based weak supervision labels referenced throughout the paper. See Section 4.6 of the paper for the full protocol description.

## Files

| File | Description |
|---|---|
| `blind_template.csv` | 26-document blind template (no labels) — distributed to annotators |
| `annotator1_labels.csv` | Annotator 1's labels + reasoning notes |
| `annotator2_labels.csv` | Annotator 2's labels + reasoning notes |
| `consensus_labels.csv` | Final consensus labels with adjudication status |
| `disagreement_resolution.md` | Detailed record of the single disagreement case |

## Annotator Anonymization

Annotators are referenced only as "Annotator 1" and "Annotator 2" throughout this release. Both annotators are domain experts (archival science and Indonesian regulatory practice). Both provided **written informed consent** for their anonymized annotations and reasoning notes to be published as part of this open-source release.

No personally identifying information about the annotators is included in any file.

## Sampling Protocol

A stratified random sample of 26 documents was drawn from the full 614-document ArsipDataset corpus, balanced approximately by taxonomy category. This sample size was chosen to provide reliable κ estimation while remaining feasible for independent expert re-annotation.

| Category | Annotator 1 count | Annotator 2 count |
|---|---|---|
| KA | 6 | 5 |
| JRA | 6 | 6 |
| SKKAAD | 2 | 2 |
| PK | 8 | 9 |
| PA | 3 | 3 |
| PC | 1 | 1 |
| **Total** | **26** | **26** |

The slight difference between Annotators 1 and 2 (6 vs 5 for KA; 8 vs 9 for PK) reflects the single disagreement at Row 15, documented in `disagreement_resolution.md`.

## Inter-Annotator Agreement

| Metric | Value | Interpretation |
|---|---|---|
| Raw agreement | 25/26 (96.15%) | High |
| Cohen's κ | **0.9504** | Almost perfect (Landis & Koch 1977) |
| Rule-consensus agreement | 96.0% | Confirms validity of rule-based weak supervision |

This Cohen's κ value is reported in Section 4.6 of the paper as evidence supporting the use of rule-derived labels for supervised classifier training.

## Reproducing κ Computation

```python
import csv
from sklearn.metrics import cohen_kappa_score

with open('annotator1_labels.csv') as f:
    a1 = [r['label'] for r in csv.DictReader(f)]
with open('annotator2_labels.csv') as f:
    a2 = [r['label'] for r in csv.DictReader(f)]

kappa = cohen_kappa_score(a1, a2)
print(f"Cohen's kappa: {kappa:.4f}")  # Expected: 0.9504
```

## Citation

> Untariyati, N.A., Adi, K., Widodo, A.P., Uliniansyah, M.T. (2026). LLM-Driven Few-Shot Classification and Knowledge Graph Population from Indonesian Government Regulatory Archives. *International Journal of Data Science and Analytics*, Springer.

## License

CC BY 4.0 — Free for academic and commercial use with attribution.
