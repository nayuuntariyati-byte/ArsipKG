"""
Stage 3A: Deterministic Metadata-Anchored Triple Extraction.
Achieves precision = 0.994 at 0.10 ms/doc (paper §5.2).
Five relation types extracted purely from structured fields (no LLM involvement).
"""

import argparse
import json
import time
import pandas as pd


def extract_triples(row):
    """Generate triples for one document from metadata fields."""
    triples = []
    pid = row.get("id", "")
    if pd.notna(row.get("pemrakarsa_normalized")):
        triples.append((row["pemrakarsa_normalized"], "menerbitkan", pid))
    if pd.notna(row.get("berlaku_pada")) and row["berlaku_pada"]:
        triples.append((pid, "berlakuPada", row["berlaku_pada"]))
    if pd.notna(row.get("pejabat")):
        triples.append((pid, "ditetapkanOleh", row["pejabat"]))
    if pd.notna(row.get("kategori")):
        triples.append((pid, "mengatur", row["kategori"]))
    if row.get("status") == "dicabut":
        triples.append((pid, "dicabutOleh", row.get("mencabut", "unknown")))
    return triples


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="../../data/arsipdataset/arsipdataset.csv")
    ap.add_argument("--output", default="../../results/stage3a_triples.jsonl")
    args = ap.parse_args()

    df = pd.read_csv(args.input, comment="#")
    start = time.time()
    all_triples = []
    for _, row in df.iterrows():
        all_triples.extend(extract_triples(row))
    elapsed = time.time() - start

    from pathlib import Path
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        for s, p, o in all_triples:
            f.write(json.dumps({"s": str(s), "p": p, "o": str(o)}) + "\n")

    print(f"Extracted {len(all_triples)} triples from {len(df)} documents")
    print(f"Time: {elapsed:.3f}s ({elapsed*1000/max(len(df),1):.2f} ms/doc)")


if __name__ == "__main__":
    main()
