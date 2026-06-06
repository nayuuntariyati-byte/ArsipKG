"""
Triple extraction precision evaluation vs gold standard.
Expected: precision = 0.994 (Stage 3A), 0.391 (Stage 3B), 0.947 (combined).
"""

import argparse
import json
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions", required=True, help="JSONL with {s, p, o}")
    ap.add_argument("--gold", required=True, help="CSV with columns: s, p, o, label (Y/N)")
    args = ap.parse_args()

    with open(args.predictions) as f:
        preds = [json.loads(l) for l in f]
    pred_set = {(t["s"], t["p"], t["o"]) for t in preds}

    gold = pd.read_csv(args.gold, comment="#")
    gold_triples = set(zip(gold["s"], gold["p"], gold["o"]))
    gold_positive = set(zip(gold[gold["label"] == "Y"]["s"],
                            gold[gold["label"] == "Y"]["p"],
                            gold[gold["label"] == "Y"]["o"]))

    # Precision = validated triples in pred / total pred triples evaluated
    evaluated = pred_set & gold_triples
    validated = evaluated & gold_positive
    precision = len(validated) / len(evaluated) if evaluated else 0

    print(f"Predicted triples:    {len(pred_set)}")
    print(f"Gold-evaluated:       {len(evaluated)}")
    print(f"Validated as correct: {len(validated)}")
    print(f"Precision:            {precision:.4f}")


if __name__ == "__main__":
    main()
