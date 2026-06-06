"""
IndoBERT fine-tuning baseline (indobenchmark/indobert-base-p1).

Two configurations (paper §4.3, §5.1):
- Standard cross-entropy: F1 = 0.3838
- Class-weighted (inverse-frequency): F1 = 0.4187

Hyperparameters (paper Table 3):
- Max epochs: 20
- Batch size: 16
- LR: 1e-5
- Weight decay: 0.01
- Early stopping: patience=4 on val macro-F1
"""

import argparse
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          TrainingArguments, Trainer, EarlyStoppingCallback)
from sklearn.metrics import f1_score, classification_report
from sklearn.utils.class_weight import compute_class_weight

LABEL_LIST = ["KA", "JRA", "SKKAAD", "PK", "PA", "PC"]
LABEL2ID = {l: i for i, l in enumerate(LABEL_LIST)}
ID2LABEL = {i: l for l, i in LABEL2ID.items()}


class ArsipDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.texts, self.labels = list(texts), list(labels)
        self.tokenizer, self.max_len = tokenizer, max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        enc = self.tokenizer(self.texts[idx], truncation=True, padding="max_length",
                             max_length=self.max_len, return_tensors="pt")
        return {"input_ids": enc["input_ids"].squeeze(),
                "attention_mask": enc["attention_mask"].squeeze(),
                "labels": torch.tensor(LABEL2ID[self.labels[idx]])}


def compute_metrics(eval_pred):
    preds = np.argmax(eval_pred.predictions, axis=1)
    return {"macro_f1": f1_score(eval_pred.label_ids, preds, average="macro")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="../../data/arsipdataset/splits/train.csv")
    ap.add_argument("--val", default="../../data/arsipdataset/splits/val.csv")
    ap.add_argument("--test", default="../../data/arsipdataset/splits/test.csv")
    ap.add_argument("--model", default="indobenchmark/indobert-base-p1")
    ap.add_argument("--class_weighted", action="store_true",
                    help="Apply inverse-frequency class weights (improves F1 from 0.384 to 0.419)")
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--batch_size", type=int, default=16)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    torch.manual_seed(args.seed)

    df_train = pd.read_csv(args.train, comment="#")
    df_val = pd.read_csv(args.val, comment="#")
    df_test = pd.read_csv(args.test, comment="#")

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model, num_labels=6, id2label=ID2LABEL, label2id=LABEL2ID)

    train_ds = ArsipDataset(df_train["tentang"], df_train["kategori"], tok)
    val_ds = ArsipDataset(df_val["tentang"], df_val["kategori"], tok)
    test_ds = ArsipDataset(df_test["tentang"], df_test["kategori"], tok)

    # Compute class weights if requested (inverse frequency, normalized to len)
    class_weights = None
    if args.class_weighted:
        labels_int = [LABEL2ID[l] for l in df_train["kategori"]]
        cw = compute_class_weight("balanced", classes=np.arange(6), y=labels_int)
        class_weights = torch.tensor(cw, dtype=torch.float32)
        print(f"Class weights: {dict(zip(LABEL_LIST, cw))}")

    class WeightedTrainer(Trainer):
        def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
            labels = inputs.pop("labels")
            outputs = model(**inputs)
            loss_fn = torch.nn.CrossEntropyLoss(
                weight=class_weights.to(model.device) if class_weights is not None else None)
            loss = loss_fn(outputs.logits, labels)
            return (loss, outputs) if return_outputs else loss

    args_train = TrainingArguments(
        output_dir="./indobert_output",
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.lr,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        logging_steps=10,
        seed=args.seed,
    )

    trainer_cls = WeightedTrainer if args.class_weighted else Trainer
    trainer = trainer_cls(
        model=model, args=args_train,
        train_dataset=train_ds, eval_dataset=val_ds,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=4)],
    )
    trainer.train()

    # Test evaluation
    test_pred = trainer.predict(test_ds)
    test_pred_labels = [ID2LABEL[i] for i in np.argmax(test_pred.predictions, axis=1)]
    print("=" * 60)
    print(classification_report(df_test["kategori"], test_pred_labels, digits=4))
    print("=" * 60)


if __name__ == "__main__":
    main()
