"""
Cohen's kappa inter-annotator agreement.
Expected for validation dataset: κ = 0.9504 (almost perfect, per Landis & Koch).
"""

import argparse
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--annotator1", default="../../data/validation/annotator1_labels.csv")
    ap.add_argument("--annotator2", default="../../data/validation/annotator2_labels.csv")
    args = ap.parse_args()

    a1 = pd.read_csv(args.annotator1, comment="#")
    a2 = pd.read_csv(args.annotator2, comment="#")

    # Join on id to ensure alignment
    merged = a1.merge(a2, on="id", suffixes=("_a1", "_a2"))
    kappa = cohen_kappa_score(merged["label_a1"], merged["label_a2"])
    raw_agreement = (merged["label_a1"] == merged["label_a2"]).mean()

    print("=" * 60)
    print(f"Documents compared:      {len(merged)}")
    print(f"Raw agreement:           {raw_agreement:.4f} ({(merged['label_a1'] == merged['label_a2']).sum()}/{len(merged)})")
    print(f"Cohen's kappa:           {kappa:.4f}")

    if kappa >= 0.81:
        interpretation = "Almost perfect (Landis & Koch 1977)"
    elif kappa >= 0.61:
        interpretation = "Substantial"
    elif kappa >= 0.41:
        interpretation = "Moderate"
    else:
        interpretation = "Fair to slight"
    print(f"Interpretation:          {interpretation}")
    print("=" * 60)

    # Confusion matrix
    print("\nConfusion matrix (rows=A1, cols=A2):")
    labels = sorted(set(merged["label_a1"]) | set(merged["label_a2"]))
    cm = confusion_matrix(merged["label_a1"], merged["label_a2"], labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print(cm_df)


if __name__ == "__main__":
    main()
