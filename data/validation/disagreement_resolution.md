# Disagreement Resolution

## Overview

The inter-annotator validation involved 26 documents independently labeled by two domain-expert annotators using the six-category taxonomy (KA, JRA, SKKAAD, PK, PA, PC). This document records the single disagreement that occurred and how it was adjudicated.

## Summary Statistics

| Metric | Value |
|---|---|
| Total documents | 26 |
| Agreements | 25 (96.15%) |
| Disagreements | 1 (3.85%) |
| Cohen's κ | 0.9504 (almost perfect, per Landis & Koch 1977) |

## Disagreement Case

### Row 15 — "PEDOMAN KEARSIPAN DAN KODE KLASIFIKASI"

| Field | Value |
|---|---|
| Document title (tentang) | PEDOMAN KEARSIPAN DAN KODE KLASIFIKASI |
| Regulation type (jenis) | PERATURAN BADAN/LEMBAGA |
| Issuing institution | (See ArsipDataset for full attribution) |
| Annotator 1 label | **KA** (Klasifikasi Arsip) |
| Annotator 2 label | **PK** (Penyelenggaraan Kearsipan, residual) |

### Annotator 1 reasoning (label KA)

> The phrase "kode klasifikasi" (classification code) explicitly signals a classification scheme, which is the definitional core of the KA (Klasifikasi Arsip) category. While "PEDOMAN KEARSIPAN" is a generic framing, the presence of "KODE KLASIFIKASI" provides the specific terminological signal mapping to KA.

### Annotator 2 reasoning (label PK)

> The phrase "PEDOMAN KEARSIPAN" frames the document as general archival guidelines, not specifically a classification scheme. While "KODE KLASIFIKASI" can suggest KA, the dominant framing as a "PEDOMAN" (guideline) supports the residual PK (Penyelenggaraan Kearsipan) category. Following the rule "when in doubt between specific and residual category, prefer residual."

## Adjudication Decision

**Final consensus label: KA**

**Adjudicator:** Lead researcher (Nimas Ayu Untariyati, paper first author)

**Rationale:** The taxonomy definition for KA (Klasifikasi Arsip) explicitly covers "regulations establishing classification schemes for archival content" (§3.2 of the paper). The presence of "KODE KLASIFIKASI" in the title is a definitional match for the KA category, regardless of the surrounding "PEDOMAN" framing. The "prefer residual" heuristic invoked by Annotator 2 applies when neither specific nor residual category fits well; in this case, KA fits explicitly and should take precedence.

This adjudication is consistent with the rule-based labeling logic used throughout ArsipDataset, where documents containing classification-scheme terminology are systematically assigned to KA.

## Impact on Reported Results

This single disagreement does not affect the reported Cohen's κ value of 0.9504, which is computed from the raw annotator labels prior to adjudication. The consensus label (KA) is used in subsequent analyses (e.g., when this document appears in the test set, the consensus label serves as the gold standard).
