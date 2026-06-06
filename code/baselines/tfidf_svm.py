"""
TF-IDF + LinearSVC baseline with class-weight balancing.
Achieves F1 = 0.7815 against independent manual labels.
Hyperparameters from paper Table 3: unigram, max_features=1000, C=10.0.
"""

import argparse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, cohen_kappa_score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=True)
    ap.add_argument("--test", required=True)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    df_train = pd.read_csv(args.train, comment="#")
    df_test = pd.read_csv(args.test, comment="#")

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 1),
            max_features=1000,
            sublinear_tf=True,
            lowercase=True,
        )),
        ("svm", LinearSVC(
            C=10.0,
            class_weight="balanced",
            random_state=args.seed,
            max_iter=10000,
        )),
    ])

    pipe.fit(df_train["tentang"], df_train["kategori"])
    pred = pipe.predict(df_test["tentang"])

    print("=" * 60)
    print(classification_report(df_test["kategori"], pred, digits=4))
    print(f"Cohen's kappa: {cohen_kappa_score(df_test['kategori'], pred):.4f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
