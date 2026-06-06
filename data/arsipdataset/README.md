# ArsipDataset

The ArsipDataset corpus contains **614 Indonesian government regulations** related to archival administration, spanning **1961–2025**, collected from the official portal [peraturan.go.id](https://peraturan.go.id).

## Files

| File | Rows | Description |
|---|---|---|
| `arsipdataset.csv` | 614 | Complete corpus |
| `splits/train.csv` | 490 | Training split (80%, stratified, seed=42) |
| `splits/val.csv` | 62 | Validation split (10%, stratified) |
| `splits/test.csv` | 62 | Held-out test split (10%, stratified) |

All files share the same schema and use UTF-8 encoding.

## Schema (20 columns)

| Column | Type | Description |
|---|---|---|
| `doc_id` | string | Stable identifier (`ARS-0001` to `ARS-0614`) |
| `title` | string | Full official regulation title |
| `jenis_bentuk_peraturan` | string | Regulation type (e.g., PERATURAN MENTERI, PERATURAN BADAN/LEMBAGA) |
| `pemrakarsa` | string | Issuing institution name |
| `nomor` | string | Regulation number |
| `tahun` | int | Year of enactment |
| `tentang` | string | Regulation subject/topic |
| `tempat_penetapan` | string | Place of enactment (typically "Jakarta") |
| `ditetapkan_tanggal` | string | Enactment date (mixed format) |
| `pejabat_yang_menetapkan` | string | Enacting official (public capacity) |
| `status` | string | "Berlaku" (active) or "Tidak Berlaku Dicabut Oleh: ..." (superseded by ...) |
| `dokumen_peraturan` | string | URL to original PDF on peraturan.go.id |
| `jumlah_dilihat` | int | View count on portal |
| `jumlah_didownload` | int | Download count on portal |
| `tahun_pengundangan` | int | Gazette publication year |
| `nomor_pengundangan` | string | Gazette publication number |
| `nomor_tambahan` | string | Supplementary gazette number |
| `tanggal_pengundangan` | string | Gazette publication date |
| `pejabat_pengundangan` | string | Gazette-signing official (public capacity) |
| `label` | string | Taxonomy category — one of: KA, JRA, SKKAAD, PK, PA, PC |

## Taxonomy Distribution

| Category | Full name | Count | % |
|---|---|---|---|
| KA | Klasifikasi Arsip (Archival Classification Scheme) | 56 | 9.1% |
| JRA | Jadwal Retensi Arsip (Archival Retention Schedule) | 156 | 25.4% |
| SKKAAD | Sistem Klasifikasi Keamanan dan Akses Arsip Dinamis | 55 | 9.0% |
| PK | Penyelenggaraan Kearsipan (residual category) | 298 | 48.5% |
| PA | Perubahan/Amendment | 40 | 6.5% |
| PC | Pencabutan/Revocation | 9 | 1.5% |
| **Total** | | **614** | **100%** |

See paper §3.2 for taxonomy definitions and §5.1 for classification results.

## Corpus Statistics

- **Time span**: 1961–2025 (65 years)
- **Issuing institutions**: 133 unique entities
- **Active regulations** (`Berlaku`): 557 (90.7%)
- **Superseded** (`Tidak Berlaku`): 48 (7.8%)
- **Unspecified status**: 9 (1.5%)

## Splits

Train/Val/Test splits are stratified by `label` to preserve the taxonomy distribution. Using `random_state=42` ensures reproducibility:

```python
from sklearn.model_selection import train_test_split

train_val_idx, test_idx = train_test_split(
    indices, test_size=62, stratify=labels, random_state=42)
train_idx, val_idx = train_test_split(
    train_val_idx, test_size=62, stratify=[labels[i] for i in train_val_idx], random_state=42)
```

## Privacy Note

This dataset contains only **publicly available** Indonesian government regulations from peraturan.go.id. The `pejabat_yang_menetapkan` and `pejabat_pengundangan` fields contain names of public officials who signed the regulations in their **official capacity**; these names already appear on the publicly accessible regulation documents and do not constitute private information.

No private PII (NIK, NIP, personal email, phone numbers, home addresses) is present.

## Provenance

Documents were retrieved between **March 2024 and April 2025** from `peraturan.go.id`. Each document was deduplicated by `(jenis_bentuk_peraturan, pemrakarsa, nomor, tahun)` tuple and validated against the original PDF. Institution names in `pemrakarsa` were semi-manually normalized to 133 canonical forms (e.g., "Arsip Nasional RI", "Arsip Nasional Republik Indonesia", "ANRI" → "ARSIP NASIONAL").

## Citation

> Untariyati, N.A., Adi, K., Widodo, A.P., Uliniansyah, M.T. (2026). LLM-Driven Few-Shot Classification and Knowledge Graph Population from Indonesian Government Regulatory Archives. *International Journal of Data Science and Analytics*, Springer.

## License

CC BY 4.0 — Free for academic and commercial use with attribution.
