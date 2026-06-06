"""
Classification evaluation: macro-F1 across 6 taxonomy categories.
"""

import argparse
import json
import pandas as pd
from sklearn.metrics import classification_report, f1_score, accuracy_score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions", required=True, help="JSONL with {id, kategori}")
    ap.add_argument("--gold", default="../../data/arsipdataset/splits/test.csv")
    args = ap.parse_args()

    gold = pd.read_csv(args.gold, comment="#")[["id", "kategori"]]
    with open(args.predictions) as f:
        preds = [json.loads(l) for l in f]
    pred_df = pd.DataFrame(preds)[["id", "kategori"]].rename(columns={"kategori": "predicted"})

    merged = gold.merge(pred_df, on="id")
    f1 = f1_score(merged["kategori"], merged["predicted"], average="macro")
    acc = accuracy_score(merged["kategori"], merged["predicted"])

    print("=" * 60)
    print(f"Documents:    {len(merged)}")
    print(f"Accuracy:     {acc:.4f}")
    print(f"Macro-F1:     {f1:.4f}")
    print("=" * 60)
    print(classification_report(merged["kategori"], merged["predicted"], digits=4))


if __name__ == "__main__":
    main()
