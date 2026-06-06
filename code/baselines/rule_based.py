"""
Rule-based keyword classifier for the ArsipDataset taxonomy.
Achieves F1 = 0.7815 against independent manual labels (paper §5.1, Table 4).
"""

import argparse
import pandas as pd
from sklearn.metrics import classification_report, cohen_kappa_score

# Canonical keyword rules per category (priority order: PA/PC first, then content categories)
RULES = [
    ("PC",     ["pencabutan", "mencabut peraturan", "mencabut sebagian"]),
    ("PA",     ["perubahan atas", "mengubah peraturan"]),
    ("SKKAAD", ["sistem klasifikasi keamanan", "akses arsip dinamis",
                "klasifikasi keamanan arsip"]),
    ("KA",     ["klasifikasi arsip", "kode klasifikasi"]),
    ("JRA",    ["jadwal retensi arsip", "retensi arsip", "penyusutan arsip"]),
]
DEFAULT = "PK"  # Residual category


def classify(text: str) -> str:
    """Match keywords in priority order; fallback to PK."""
    t = text.lower()
    for label, keywords in RULES:
        if any(kw in t for kw in keywords):
            return label
    return DEFAULT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="CSV with columns: tentang, kategori")
    ap.add_argument("--output", default=None, help="Optional output CSV with predictions")
    args = ap.parse_args()

    df = pd.read_csv(args.data, comment="#")
    df["predicted"] = df["tentang"].apply(classify)

    if "kategori" in df.columns:
        print("=" * 60)
        print(classification_report(df["kategori"], df["predicted"], digits=4))
        print(f"Cohen's kappa: {cohen_kappa_score(df['kategori'], df['predicted']):.4f}")
        print("=" * 60)

    if args.output:
        df.to_csv(args.output, index=False)
        print(f"Predictions written to {args.output}")


if __name__ == "__main__":
    main()
