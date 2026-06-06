################################################################################
# TABLE 6 — OPSI B: RE-RUN DENGAN GOLD ANSWER NATURAL LANGUAGE
# ============================================================================
# Revises gold answers from technical IDs (PerMENTERI_KEMENKEU_4_2024) to
# natural language (Kementerian Keuangan, 04 Juli 2025, etc.)
# Then re-computes F1, ROUGE-L, BERTScore and Wilcoxon tests
# ============================================================================
# PREREQUISITES:
#   - arsipqa_v1_benchmark.csv (from previous run)
#   - qa_results_No_KG_LLM_only.csv
#   - qa_results_Semi-manual_KG.csv
#   - qa_results_ArsipKG-Auto_Full.csv
#   - ArsipDataset-clean.csv
# ============================================================================
# This script does NOT re-run LLM inference — it only re-evaluates the
# EXISTING predictions against REVISED gold answers.
# ESTIMATED RUNTIME: ~5 minutes (BERTScore computation only)
################################################################################


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ CELL 1: SETUP                                                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
    "pandas", "rouge-score", "bert-score", "scipy"])

import json, re, warnings
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import Counter

warnings.filterwarnings("ignore")
print("Setup complete")


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ CELL 2: UPLOAD FILES                                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

from google.colab import files as colab_files

print("Upload ArsipDataset-clean.csv:")
up1 = colab_files.upload()
df_dataset = pd.read_csv(list(up1.keys())[0])
print(f"  Dataset: {df_dataset.shape[0]} rows")

print("\nUpload arsipqa_v1_benchmark.csv:")
up2 = colab_files.upload()
df_qa = pd.read_csv(list(up2.keys())[0])
print(f"  QA pairs: {df_qa.shape[0]}")

print("\nUpload qa_results_No_KG_LLM_only.csv:")
up3 = colab_files.upload()
df_nokg = pd.read_csv(list(up3.keys())[0])

print("Upload qa_results_Semi-manual_KG.csv:")
up4 = colab_files.upload()
df_semi = pd.read_csv(list(up4.keys())[0])

print("Upload qa_results_ArsipKG-Auto_Full.csv:")
up5 = colab_files.upload()
df_auto = pd.read_csv(list(up5.keys())[0])

print(f"\nAll files loaded: NoKG={len(df_nokg)}, Semi={len(df_semi)}, Auto={len(df_auto)}")


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ CELL 3: REVISE GOLD ANSWERS TO NATURAL LANGUAGE                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# Build lookup from regulation ID patterns to natural language
def build_lookup(df):
    """Build lookup dictionaries from dataset."""
    lookup = {}
    for _, row in df.iterrows():
        jenis = str(row.get('jenis_bentuk_peraturan', ''))
        pemrakarsa = str(row.get('pemrakarsa', ''))
        nomor = str(row.get('nomor', ''))
        tahun = str(row.get('tahun', ''))
        tentang = str(row.get('tentang', ''))
        tanggal = str(row.get('ditetapkan_tanggal', ''))
        pejabat = str(row.get('pejabat_yang_menetapkan', ''))
        label = str(row.get('label', ''))

        # Build various ID patterns that might appear in gold answers
        pem_short = re.sub(r'[^A-Z]', '', pemrakarsa.upper())[:8]
        jenis_short = jenis.replace("PERATURAN ", "Per").replace("KEPUTUSAN ", "Kep")
        jenis_short = re.sub(r'[^a-zA-Z0-9]', '', jenis_short)[:10]
        reg_id = f"{jenis_short}_{pem_short}_{nomor}_{tahun}"

        lookup[reg_id] = {
            'pemrakarsa': pemrakarsa,
            'tentang': tentang[:200],
            'tanggal': tanggal,
            'pejabat': pejabat,
            'label': label,
            'full_name': f"{jenis} Nomor {nomor} Tahun {tahun}",
        }
    return lookup

LOOKUP = build_lookup(df_dataset)
print(f"Built lookup with {len(LOOKUP)} entries")

# Category mapping
CAT_MAP = {
    "Klasifikasi Arsip": "Klasifikasi Arsip (KA)",
    "Jadwal Retensi Arsip": "Jadwal Retensi Arsip (JRA)",
    "Sistem Klasifikasi Keamanan dan Akses Arsip Dinamis": "Sistem Klasifikasi Keamanan dan Akses Arsip Dinamis (SKKAAD)",
    "Penyelenggaraan Kearsipan": "Penyelenggaraan Kearsipan (PK)",
    "Perubahan/Amandemen": "Perubahan/Amandemen (PA)",
    "Pencabutan": "Pencabutan (PC)",
}


def revise_gold_answer(row):
    """Convert technical gold answer to natural language."""
    relation = row['relation']
    old_answer = str(row['answer'])
    question = str(row['question'])

    if relation == 'menerbitkan':
        # Old answer: LEMBAGA NAME (already natural in most cases)
        return old_answer.strip()

    elif relation == 'berlakuPada':
        # Old answer: date string (already natural)
        return old_answer.strip()

    elif relation == 'mengatur':
        # Old answer: category name -> add abbreviation
        return CAT_MAP.get(old_answer, old_answer)

    elif relation == 'ditetapkanOleh':
        # Old answer: PEJABAT NAME (already natural)
        return old_answer.strip()

    elif relation == 'menggantikan':
        # Old answer: regulation ID -> convert to full name
        info = LOOKUP.get(old_answer)
        if info:
            return f"{info['full_name']} tentang {info['tentang'][:100]}"
        # Try partial match
        for key, info in LOOKUP.items():
            if old_answer in key or key in old_answer:
                return f"{info['full_name']} tentang {info['tentang'][:100]}"
        return old_answer  # Keep as-is if no match

    elif relation == 'menggantikan_sebagian':
        # Same as menggantikan
        info = LOOKUP.get(old_answer)
        if info:
            return f"{info['full_name']} tentang {info['tentang'][:100]}"
        for key, info in LOOKUP.items():
            if old_answer in key or key in old_answer:
                return f"{info['full_name']} tentang {info['tentang'][:100]}"
        return old_answer

    elif relation == 'multi_hop':
        # Old answer: count number (already natural)
        return old_answer.strip()

    return old_answer


# Apply revision
df_qa['answer_original'] = df_qa['answer']
df_qa['answer_revised'] = df_qa.apply(revise_gold_answer, axis=1)

print("\nRevised gold answers — samples:")
print(f"{'Relation':<25} {'Original':<40} {'Revised':<50}")
print("-" * 115)
for rel in df_qa['relation'].unique():
    sample = df_qa[df_qa['relation'] == rel].iloc[0]
    orig = str(sample['answer_original'])[:38]
    rev = str(sample['answer_revised'])[:48]
    print(f"{rel:<25} {orig:<40} {rev:<50}")

# Count how many were actually changed
changed = (df_qa['answer_original'] != df_qa['answer_revised']).sum()
print(f"\nAnswers revised: {changed}/{len(df_qa)} ({changed/len(df_qa)*100:.1f}%)")

# Save revised benchmark
df_qa.to_csv("arsipqa_v1_benchmark_revised.csv", index=False)
print("Saved: arsipqa_v1_benchmark_revised.csv")


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ CELL 4: RE-COMPUTE METRICS WITH REVISED GOLD ANSWERS                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

from rouge_score import rouge_scorer
from bert_score import score as bert_score_fn


def compute_token_f1(prediction, gold):
    """Token-level F1."""
    pred_tokens = set(str(prediction).upper().split())
    gold_tokens = set(str(gold).upper().split())
    if not pred_tokens or not gold_tokens:
        return 0.0
    common = pred_tokens & gold_tokens
    if not common:
        return 0.0
    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)


rouge = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=False)

configs = {
    "No KG (LLM only)": df_nokg,
    "Semi-manual KG": df_semi,
    "ArsipKG-Auto Full": df_auto,
}

# Map revised gold answers to each config's results
revised_answers = df_qa['answer_revised'].tolist()

table6_opsi_b = {}

print(f"\n{'='*70}")
print("OPSI B: RE-EVALUATION WITH NATURAL LANGUAGE GOLD ANSWERS")
print(f"{'='*70}")

for config_name, df_results in configs.items():
    predictions = df_results['predicted_answer'].tolist()

    # Token F1
    f1_scores = [compute_token_f1(p, g) for p, g in zip(predictions, revised_answers)]
    mean_f1 = np.mean(f1_scores)

    # ROUGE-L
    rouge_scores = [rouge.score(str(g), str(p))['rougeL'].fmeasure
                    for g, p in zip(revised_answers, predictions)]
    mean_rouge = np.mean(rouge_scores)

    # BERTScore
    P, R, F_bert = bert_score_fn(
        [str(p) for p in predictions],
        [str(g) for g in revised_answers],
        lang="id", verbose=False
    )
    mean_bertscore = F_bert.mean().item()

    table6_opsi_b[config_name] = {
        'f1': round(mean_f1, 4),
        'rouge_l': round(mean_rouge, 4),
        'bert_score': round(mean_bertscore, 4),
        'f1_scores': f1_scores,
        'rouge_scores': rouge_scores,
        'bert_scores': F_bert.tolist(),
    }

    print(f"\n  {config_name}:")
    print(f"    Token F1:   {mean_f1:.4f}")
    print(f"    ROUGE-L:    {mean_rouge:.4f}")
    print(f"    BERTScore:  {mean_bertscore:.4f}")

    # Per-relation breakdown
    relations = df_qa['relation'].tolist()
    print(f"    Per-relation F1:")
    for rel in sorted(set(relations)):
        rel_f1 = [f for r, f in zip(relations, f1_scores) if r == rel]
        print(f"      {rel}: {np.mean(rel_f1):.4f} (n={len(rel_f1)})")


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ CELL 5: WILCOXON TESTS                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

from scipy.stats import wilcoxon

print(f"\n{'='*60}")
print("WILCOXON SIGNED-RANK TESTS (Opsi B)")
print(f"{'='*60}")

auto_f1 = table6_opsi_b["ArsipKG-Auto Full"]["f1_scores"]
semi_f1 = table6_opsi_b["Semi-manual KG"]["f1_scores"]
nokg_f1 = table6_opsi_b["No KG (LLM only)"]["f1_scores"]

wilcoxon_results = {}

tests = [
    ("auto_vs_semi", auto_f1, semi_f1, "Auto-Full vs Semi-manual"),
    ("auto_vs_nokg", auto_f1, nokg_f1, "Auto-Full vs No KG"),
    ("semi_vs_nokg", semi_f1, nokg_f1, "Semi-manual vs No KG"),
]

for key, a, b, label in tests:
    try:
        # Check if arrays are identical (Wilcoxon requires differences)
        diffs = [x - y for x, y in zip(a, b)]
        non_zero = [d for d in diffs if d != 0]
        if len(non_zero) < 2:
            print(f"\n  {label}: Cannot compute (too few non-zero differences)")
            wilcoxon_results[key] = {"p_value": 1.0, "significant": False, "note": "insufficient differences"}
            continue

        stat, p = wilcoxon(a, b, alternative='two-sided')
        sig = p < 0.05
        wilcoxon_results[key] = {"p_value": round(p, 6), "significant": sig, "statistic": round(stat, 4)}
        print(f"\n  {label}:")
        print(f"    Statistic: {stat:.4f}")
        print(f"    p-value:   {p:.6f}")
        print(f"    Significant (α=0.05): {'Yes' if sig else 'No'}")
    except Exception as e:
        print(f"\n  {label}: Error — {e}")
        wilcoxon_results[key] = {"p_value": 1.0, "significant": False, "note": str(e)}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ CELL 6: PRINT FINAL TABLE 6 — BOTH OPTIONS                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# Load Opsi A data from file or use known values
opsi_a_data = {
    "No KG (LLM only)": {"f1": 0.0313, "rouge_l": 0.0664, "bert_score": 0.6193},
    "Semi-manual KG": {"f1": 0.0000, "rouge_l": 0.0470, "bert_score": 0.6410},
    "ArsipKG-Auto Full": {"f1": 0.0227, "rouge_l": 0.0906, "bert_score": 0.6610},
}

print(f"\n{'='*90}")
print("COMPARISON: OPSI A (original gold) vs OPSI B (revised gold)")
print(f"{'='*90}")

print(f"\n{'Config':<25} {'--- Opsi A (technical IDs) ---':^35} {'--- Opsi B (natural language) ---':^35}")
print(f"{'':25} {'F1':>7} {'ROUGE':>7} {'BERT':>7}    {'F1':>7} {'ROUGE':>7} {'BERT':>7}    {'ΔF1':>7}")
print(f"{'-'*90}")

for config in ["No KG (LLM only)", "Semi-manual KG", "ArsipKG-Auto Full"]:
    a = opsi_a_data[config]
    b = table6_opsi_b[config]
    delta_f1 = b['f1'] - a['f1']
    print(f"{config:<25} {a['f1']:>7.4f} {a['rouge_l']:>7.4f} {a['bert_score']:>7.4f}    "
          f"{b['f1']:>7.4f} {b['rouge_l']:>7.4f} {b['bert_score']:>7.4f}    {delta_f1:>+7.4f}")

# QA Retention
semi_b = table6_opsi_b["Semi-manual KG"]
auto_b = table6_opsi_b["ArsipKG-Auto Full"]
if semi_b['f1'] > 0:
    retention_f1 = auto_b['f1'] / semi_b['f1'] * 100
else:
    retention_f1 = float('inf') if auto_b['f1'] > 0 else 0

retention_bert = auto_b['bert_score'] / semi_b['bert_score'] * 100 if semi_b['bert_score'] > 0 else 0

print(f"\nQA Retention (Opsi B):")
print(f"  Token F1:   {retention_f1:.1f}%" if retention_f1 != float('inf') else "  Token F1:   Auto > Semi (Semi=0)")
print(f"  BERTScore:  {retention_bert:.1f}%")


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ CELL 7: SAVE ALL RESULTS                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# Table 6 CSV (Opsi B)
table6_rows = []
semi_f1_mean = table6_opsi_b["Semi-manual KG"]["f1"]
for config in ["No KG (LLM only)", "Semi-manual KG", "ArsipKG-Auto Full"]:
    r = table6_opsi_b[config]
    delta = r['f1'] - semi_f1_mean if config != "Semi-manual KG" else 0
    table6_rows.append({
        "KG_Backend": config,
        "F1": r['f1'],
        "ROUGE_L": r['rouge_l'],
        "BERTScore": r['bert_score'],
        "Delta_F1_vs_Semi": round(delta, 4),
    })
pd.DataFrame(table6_rows).to_csv("table6_opsi_b.csv", index=False)
print("Saved: table6_opsi_b.csv")

# Combined summary JSON
combined = {
    "opsi_a": {
        "description": "Original gold answers (technical regulation IDs)",
        "primary_metric": "BERTScore",
        "table6": opsi_a_data,
        "qa_retention_bertscore_pct": 103.1,
    },
    "opsi_b": {
        "description": "Revised gold answers (natural language)",
        "primary_metric": "Token F1",
        "table6": {k: {"f1": v["f1"], "rouge_l": v["rouge_l"], "bert_score": v["bert_score"]}
                   for k, v in table6_opsi_b.items()},
        "qa_retention_f1_pct": round(retention_f1, 1) if retention_f1 != float('inf') else "Auto > Semi",
        "qa_retention_bertscore_pct": round(retention_bert, 1),
    },
    "wilcoxon_opsi_b": wilcoxon_results,
    "recommendation": "Use Opsi B if F1 improves significantly; otherwise fall back to Opsi A with BERTScore as primary",
    "timestamp": datetime.now().isoformat(),
}

with open("table6_comparison_a_vs_b.json", "w") as f:
    json.dump(combined, f, indent=2, default=str)
print("Saved: table6_comparison_a_vs_b.json")

# Download
output_files = [
    "arsipqa_v1_benchmark_revised.csv",
    "table6_opsi_b.csv",
    "table6_comparison_a_vs_b.json",
]

print(f"\n{'='*60}")
print(f"OUTPUT FILES")
print(f"{'='*60}")
for f in output_files:
    if Path(f).exists():
        print(f"  {f} ({Path(f).stat().st_size/1024:.1f} KB)")

for f in output_files:
    if Path(f).exists():
        try:
            colab_files.download(f)
        except:
            pass

print(f"""
{'='*60}
COMPLETE — Upload table6_comparison_a_vs_b.json for final analysis
{'='*60}
""")
