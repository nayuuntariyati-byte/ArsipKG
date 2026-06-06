"""
Downstream QA evaluation on ArsipQA-v1.
Primary metric: BERTScore. Secondary: Token F1, ROUGE-L.
Statistical test: Wilcoxon signed-rank.
"""

import argparse
import json
import pandas as pd
from scipy.stats import wilcoxon


def compute_token_f1(pred, gold):
    p_tokens, g_tokens = set(pred.lower().split()), set(gold.lower().split())
    if not g_tokens:
        return 0.0
    common = p_tokens & g_tokens
    if not common:
        return 0.0
    precision = len(common) / len(p_tokens)
    recall = len(common) / len(g_tokens)
    return 2 * precision * recall / (precision + recall)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", default="../../data/arsipqa-v1/arsipqa_v1.jsonl")
    ap.add_argument("--predictions", required=True, help="JSONL with {id, answer}")
    ap.add_argument("--compare_baseline", default=None,
                    help="Optional second predictions file for Wilcoxon test")
    args = ap.parse_args()

    benchmark = {}
    with open(args.benchmark) as f:
        for line in f:
            rec = json.loads(line)
            benchmark[rec["id"]] = rec

    with open(args.predictions) as f:
        preds = [json.loads(l) for l in f]

    # Token F1 + (optionally) BERTScore + ROUGE-L if libraries installed
    f1_scores = []
    for p in preds:
        gold = benchmark.get(p["id"], {}).get("gold_answer", "")
        f1_scores.append(compute_token_f1(p.get("answer", ""), gold))

    print(f"Token F1 (mean):  {sum(f1_scores)/len(f1_scores):.4f}")

    try:
        from bert_score import score as bertscore_fn
        candidates = [p.get("answer", "") for p in preds]
        references = [benchmark.get(p["id"], {}).get("gold_answer", "") for p in preds]
        _, _, F1_bert = bertscore_fn(candidates, references, lang="id", verbose=False)
        print(f"BERTScore (mean): {F1_bert.mean().item():.4f}")
    except ImportError:
        print("BERTScore: install bert-score for this metric")

    try:
        from rouge_score import rouge_scorer
        scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
        rl = [scorer.score(benchmark.get(p["id"], {}).get("gold_answer", ""),
                           p.get("answer", ""))["rougeL"].fmeasure for p in preds]
        print(f"ROUGE-L (mean):   {sum(rl)/len(rl):.4f}")
    except ImportError:
        print("ROUGE-L: install rouge-score for this metric")

    # Wilcoxon vs baseline
    if args.compare_baseline:
        with open(args.compare_baseline) as f:
            baseline = [json.loads(l) for l in f]
        b_scores = []
        for p in baseline:
            gold = benchmark.get(p["id"], {}).get("gold_answer", "")
            b_scores.append(compute_token_f1(p.get("answer", ""), gold))
        stat, pval = wilcoxon(f1_scores, b_scores)
        print(f"\nWilcoxon vs baseline: statistic={stat:.2f}, p-value={pval:.4f}")


if __name__ == "__main__":
    main()
