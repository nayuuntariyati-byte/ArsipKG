# Annotation Guidelines (Inter-Annotator Validation Study)

This document describes the protocol followed by the two annotators in the 26-document validation study (§4.6 of the paper).

## Annotator Profile

Two domain experts in Indonesian archival regulations, recruited via professional network. Both have:
- Working knowledge of ANRI archival doctrine
- Familiarity with the 6-category taxonomy
- No prior involvement in the rule-based labeling system

## Materials Provided

For each document, annotators received:
- `id`: document identifier (anonymized)
- `tentang`: regulation title
- `jenis_bentuk_peraturan`: regulation type (e.g., PERATURAN MENTERI)

Annotators were **NOT** shown:
- Rule-based labels
- LLM predictions
- Other annotator's labels (until adjudication)
- Document body text (judgment based on title only)

## Taxonomy Definitions

### KA (Klasifikasi Arsip)
Regulations establishing classification schemes for archival content.

**Canonical signals**: "Klasifikasi Arsip", "Kode Klasifikasi", "Skema Klasifikasi"

### JRA (Jadwal Retensi Arsip)
Regulations setting retention schedules and disposition rules.

**Canonical signals**: "Jadwal Retensi Arsip", "Retensi", "Penyusutan Arsip", "Pemusnahan"

### SKKAAD (Sistem Klasifikasi Keamanan dan Akses Arsip Dinamis)
Regulations governing security classification and access control of dynamic archives.

**Canonical signals**: "Sistem Klasifikasi Keamanan", "Akses Arsip Dinamis", "Klasifikasi Keamanan Arsip"

### PK (Penyelenggaraan Kearsipan)
Residual category for general archival management not falling into KA, JRA, or SKKAAD.

**Examples**: "Pedoman Kearsipan", "Tata Naskah Dinas", "Pengelolaan Arsip"

### PA (Perubahan/Amendment)
Regulations that partially amend prior regulations. Takes priority over content categories.

**Canonical signals**: "Perubahan atas", "Perubahan Kedua atas"

### PC (Pencabutan/Revocation)
Regulations that fully supersede prior regulations. Takes priority over content categories.

**Canonical signals**: "Pencabutan", "Mencabut"

## Decision Procedure

1. Read `tentang` and `jenis_bentuk_peraturan`
2. Check for PC signals → assign PC if present
3. Check for PA signals → assign PA if present
4. Check for content category signals (SKKAAD > KA > JRA, in priority order)
5. Fallback: assign PK
6. Record confidence (low / medium / high) and optional rationale

## Disagreement Resolution

In the validation study, **1 of 26 documents** triggered disagreement:
- Annotator 1: SKKAAD (medium confidence)
- Annotator 2: PK (high confidence)
- Lead researcher adjudication: PK (multi-topic regulation with classification codes as one component, but dominant content is general management)

See `data/validation/disagreement_resolution.md` for full case details.

## Statistical Results

- Raw agreement: 25/26 = 96.15%
- Cohen's κ: 0.9504 (almost perfect, per Landis & Koch 1977)
- Post-adjudication rule-consensus: 96.0%
