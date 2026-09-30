# ArsipKG: Indonesian Government Regulatory Archives Knowledge Graph

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20569080.svg)](https://doi.org/10.5281/zenodo.20569080)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OWL 2 DL](https://img.shields.io/badge/OWL-2%20DL-blueviolet.svg)](https://w3id.org/arsipkg/ontology/v1)

Companion repository for the paper **"LLM-Driven Few-Shot Classification and Knowledge Graph Population from Indonesian Government Regulatory Archives"** (Untariyati et al., 2026, International Journal of Data Science and Analytics, Springer).

## 📋 Overview

This repository provides the complete experimental package for automated knowledge graph (KG) population from Indonesian government regulatory archives. It includes:

- **ArsipDataset**: A curated corpus of 614 Indonesian government regulations on archival administration (1961–2025, from 133 institutions)
- **ArsipOnto**: A formal OWL 2 DL ontology (16 classes, 9 object properties, 10 datatype properties, ~375 TBox axioms) aligned with LKIF, Dublin Core Terms, SKOS, and FOAF; validated via 20 SPARQL competency questions.
- **ArsipKG-Auto**: A populated knowledge graph with 1,211 nodes and 1,903 edges (single connected component); 1.09× graph expansion beyond source corpus via Stage 3B supersession discovery.
- **ArsipQA-v1**: A benchmark of 90 question-answer pairs across 7 question types
- **Three Inter-Annotator Validation Datasets**:
  - Classification IAA: 26 stratified documents, two annotators, Cohen's κ = **0.9504** (almost perfect)
  - Triple extraction gold standard: 339 triples across 99 documents, two annotators, Cohen's κ = **0.7482** (substantial)
  - QA benchmark quality validation: 100 QA pairs assessed by two annotators for factual correctness, natural language, and unambiguity
- **Experimental Code**: Four-stage pipeline implementation including baselines and evaluation scripts
- **Coverage Ablation Study**: Systematic 5-level sampling (0%, 25%, 50%, 75%, 100%; seed=42) evaluating KG completeness impact on downstream QA
- **Seven Parameterized Cypher Templates** (Appendix B): Structured query interface achieving 1.000 exact-match precision on the ArsipQA-v1 benchmark
- **3B vs 8B Robustness Analysis**: Comparative evaluation of LLaMA-3.1-8B and LLaMA-3.2-3B across k-shot configurations (k ∈ {0, 3, 5, 10})
- **Colab Notebooks**: Google Colab notebooks for end-to-end reproduction on free-tier GPU

## 🔑 Key Results (from the paper)

| Metric | Value | Notes |
|---|---|---|
| Best classification macro-F1 (LLaMA-3.1-8B 3-shot, N=62) | **0.9631** | Full held-out test set |
| Fair-subset F1 (N=25 manual-consensus subset) | **0.9717** | Apples-to-apples with baselines |
| Best baseline F1 (IndoBERT class-weighted, N=62) | 0.4187 | +0.54 ΔF1 vs LLM |
| Triple extraction precision (Stage 3A, metadata-anchored) | **0.994** | On 100-doc gold standard |
| Triple extraction precision (Stage 3B, LLM-based) | 0.391 | Supersession only |
| Combined pipeline precision | 0.947 | 339 triples annotated |
| Inter-annotator agreement (classification, 26 docs) | κ = **0.9504** | Almost perfect |
| Inter-annotator agreement (triples, 339 rows, 100 docs) | κ = **0.7482** | Substantial |
| KG structural | 1,211 nodes, 1,903 edges | 1 connected component |
| Graph expansion beyond source corpus | **1.09×** | 55 external Peraturan materialized |
| Cypher templates precision (Appendix B, ArsipQA-v1) | **1.000** | Exact match on 90/90 questions |
| Coverage ablation trend (Mann-Kendall, 5 levels) | S = −4, p = 0.462 | Not significant |
| Coverage ablation (Wilcoxon 100% vs 50%) | W = 1,148, p = 0.561 | Not significant |

## 📁 Repository Structure

```
ArsipKG/
├── README.md                          # This file
├── LICENSE                            # CC BY 4.0 (for data)
├── LICENSE-CODE                       # MIT License (for code)
├── CITATION.cff                       # Machine-readable citation
├── .zenodo.json                       # Zenodo metadata for auto-archiving
├── .gitignore
│
├── data/
│   ├── arsipdataset/                  # 614 regulations corpus
│   │   ├── arsipdataset.csv           # Main corpus (18 metadata fields)
│   │   ├── README.md                  # Field schema documentation
│   │   └── splits/                    # Train/val/test splits (seed=42)
│   │       ├── train.csv              # 490 documents
│   │       ├── val.csv                # 62 documents
│   │       └── test.csv               # 62 documents
│   │
│   ├── arsipqa-v1/                    # QA benchmark
│   │   ├── arsipqa_v1.jsonl           # 90 QA pairs across 7 types
│   │   ├── arsipqa_v1.csv             # Same data in CSV
│   │   └── README.md                  # Question type taxonomy
│   │
│   ├── validation/                    # Three inter-annotator validation exercises
│   │   ├── classification_iaa/        # Exercise 1: classification labels (26 docs)
│   │   │   ├── annotator1_labels.csv  # Annotator 1 (κ vs A2 = 0.9504)
│   │   │   ├── annotator2_labels.csv  # Annotator 2
│   │   │   ├── consensus_labels.csv   # Adjudicated final labels
│   │   │   └── blind_template.csv     # Blank template used
│   │   ├── triple_gold_standard/      # Exercise 2: triple validation (339 triples)
│   │   │   ├── annotator1_gold_standard.csv  # Annotator 1 (κ vs A2 = 0.7482)
│   │   │   └── annotator2_gold_standard.csv  # Annotator 2
│   │   ├── qa_benchmark_validation/   # Exercise 3: QA quality (100 QA pairs)
│   │   │   ├── annotation_annotator1.csv     # Annotator 1
│   │   │   └── annotation_annotator2.csv     # Annotator 2
│   │   └── README.md                  # Annotation protocol (all 3 exercises)
│   │
│   └── arsipkg-auto/                  # Populated knowledge graph
│       ├── arsipkg-auto.ttl           # Turtle serialization
│       ├── arsipkg-auto.nt            # N-Triples serialization
│       ├── arsipkg-auto.cypher        # Neo4j Cypher dump
│       └── README.md                  # Loading instructions
│
├── ontology/                          # ArsipOnto formal ontology
│   ├── arsipkg-ontology.ttl           # Canonical Turtle
│   ├── arsipkg-ontology.owl           # RDF/XML (Protégé-compatible)
│   ├── arsipkg-ontology.rdf           # Alternative XML serialization
│   ├── competency_questions.md        # 20 SPARQL competency questions
│   └── README.md                      # Ontology documentation
│
├── code/
│   ├── requirements.txt               # Python dependencies
│   ├── baselines/                     # Supervised baselines
│   │   ├── rule_based.py              # Rule-based keyword classifier
│   │   ├── tfidf_svm.py               # TF-IDF + LinearSVC
│   │   ├── indobert_finetune.py       # IndoBERT fine-tuning (2 variants)
│   │   └── README.md
│   │
│   ├── pipeline/                      # Four-stage pipeline
│   │   ├── stage1_ingestion.py        # Document ingestion + normalization
│   │   ├── stage2_classification.py   # Few-shot LLM classification
│   │   ├── stage3a_metadata.py        # Deterministic metadata extraction
│   │   ├── stage3b_llm_titles.py      # LLM-based title extraction
│   │   ├── stage4_kg_population.py    # Neo4j KG population
│   │   ├── coverage_ablation.py       # 5-level coverage ablation
│   │   ├── prompts/                   # Few-shot prompt templates
│   │   └── README.md
│   │
│   ├── notebooks/                     # Google Colab notebooks
│   │   ├── 01_stage3b_extraction_colab.ipynb   # LLM supersession extraction
│   │   ├── 02_coverage_ablation_colab.ipynb    # QA coverage ablation
│   │   └── 03_bertscore_recompute_colab.ipynb  # BERTScore recomputation
│   │
│   ├── cypher_templates/              # Appendix B — 7 parameterized templates
│   │   ├── T1_menerbitkan.cypher      # Issuing institution
│   │   ├── T2_berlakuPada.cypher      # Enactment date
│   │   ├── T3_mengatur.cypher         # Regulation category
│   │   ├── T4_ditetapkanOleh.cypher   # Enacting official
│   │   ├── T5_menggantikan.cypher     # Full supersession
│   │   ├── T6_menggantikan_sebagian.cypher  # Partial amendment
│   │   ├── T7_multi_hop.cypher        # Multi-hop aggregate
│   │   └── qa_dispatcher.py           # Python dispatcher (question → template)
│   │
│   └── evaluation/                    # Evaluation scripts
│       ├── compute_kappa.py           # Cohen's κ computation
│       ├── evaluate_classification.py # Macro-F1 per category
│       ├── evaluate_triples.py        # Triple extraction precision
│       ├── evaluate_qa.py             # BERTScore, ROUGE-L, Wilcoxon
│       └── README.md
│
├── appendices/                        # Supplementary material to paper
│   ├── Appendix_A_ArsipOnto_Specification.docx  # Ontology spec + 20 CQ summary
│   ├── Appendix_B_Cypher_Templates.docx         # 7 template documentation
│   └── ArsipOnto_Competency_Questions.docx      # Full 20 SPARQL queries with expected answers
│
├── results/                           # Reproducibility outputs
│   ├── classification/                # Per-document predictions
│   │   ├── results_detailed_0shot.csv         # LLaMA-3.1-8B, 62 docs
│   │   ├── results_detailed_3shot.csv
│   │   ├── results_detailed_5shot.csv
│   │   ├── results_detailed_10shot.csv
│   │   ├── paper_stats_summary_8B.json        # Aggregate stats 8B
│   │   └── paper_stats_summary_3B.json        # Aggregate stats 3B
│   │
│   └── coverage_ablation/             # Coverage ablation outputs (Section 5.5)
│       ├── qa_results_coverage_000.csv        # 0% (No-KG)
│       ├── qa_results_coverage_025.csv        # 25%
│       ├── qa_results_coverage_050.csv        # 50%
│       ├── qa_results_coverage_075.csv        # 75%
│       ├── qa_results_coverage_100.csv        # 100% (Full)
│       ├── coverage_ablation_summary.csv      # Aggregate table
│       ├── bertscore_recomputed.json          # BERTScore with mBERT
│       └── statistical_tests_fixed.json       # Wilcoxon + Mann-Kendall
│
└── docs/
    ├── INSTALLATION.md                # Setup guide
    ├── REPRODUCIBILITY.md             # Step-by-step reproduction
    ├── DATA_DICTIONARY.md             # Complete schema documentation
    └── ANNOTATION_GUIDELINES.md       # Validation study protocol
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- 16 GB RAM (32 GB recommended for IndoBERT fine-tuning)
- NVIDIA GPU with ≥ 8 GB VRAM (for LLM inference)
- Neo4j 5.x (for KG population, optional)

### Installation

```bash
git clone https://github.com/nayuuntariyati-byte/ArsipKG.git
cd ArsipKG
pip install -r code/requirements.txt
```

### Reproduce Classification Results

```bash
# Run the best few-shot configuration (LLaMA-3.1-8B 3-shot)
python code/pipeline/stage2_classification.py \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --k_shot 3 \
    --data data/arsipdataset/splits/test.csv \
    --output results/llama8b_3shot.json

# Expected: macro-F1 = 0.9631 (full N=62); 0.9717 on N=25 manual-consensus subset.
```

### Reproduce Coverage Ablation Study

Open `code/notebooks/02_coverage_ablation_colab.ipynb` in Google Colab, upload the required inputs (`all_triples_complete.csv` + `arsipqa_v1.jsonl`), and run all cells.

```bash
# Or via CLI (requires ArsipKG-Auto Neo4j instance)
python code/pipeline/coverage_ablation.py \
    --triples data/arsipkg-auto/all_triples_complete.csv \
    --qa data/arsipqa-v1/arsipqa_v1.jsonl \
    --seed 42 \
    --output results/coverage_ablation/

# Expected outputs (already included in results/coverage_ablation/):
#   • BERTScore (mBERT): 0.669 (0%), 0.636 (25%), 0.628 (50%), 0.628 (75%), 0.637 (100%)
#   • Wilcoxon 100% vs 50%: W = 1,148, p = 0.561 (not significant)
#   • Mann-Kendall trend: S = -4, Z = -0.735, p = 0.462 (not significant)
```

### Query with Cypher Templates (Appendix B)

```bash
# Load ArsipKG-Auto into Neo4j (see previous section), then:
python code/cypher_templates/qa_dispatcher.py \
    --benchmark data/arsipqa-v1/arsipqa_v1.jsonl \
    --neo4j-uri bolt://localhost:7687 \
    --neo4j-user neo4j \
    --neo4j-password YOUR_PASSWORD

# Expected: 90/90 exact-match precision (1.000) across all 7 template types
```

### Run Inter-Annotator Validation

```bash
# Classification IAA (26 documents, 6-class labels)
python code/evaluation/compute_kappa.py \
    --annotator1 data/validation/classification_iaa/annotator1_labels.csv \
    --annotator2 data/validation/classification_iaa/annotator2_labels.csv
# Expected: Cohen's κ = 0.9504

# Triple extraction gold standard (339 triples, Y/N labels)
python code/evaluation/compute_kappa.py \
    --annotator1 data/validation/triple_gold_standard/annotator1_gold_standard.csv \
    --annotator2 data/validation/triple_gold_standard/annotator2_gold_standard.csv \
    --label-col annotator1_correct
# Expected: Cohen's κ = 0.7482
```

### Load Knowledge Graph (Neo4j)

```bash
# Start Neo4j, then:
cypher-shell -u neo4j -p YOUR_PASSWORD < data/arsipkg-auto/arsipkg-auto.cypher

# Expected: 1,211 nodes, 1,903 edges, 1 connected component
```

### Query with SPARQL (using Apache Jena)

```bash
# Load ontology + instance data into Fuseki
fuseki-server --file=ontology/arsipkg-ontology.ttl \
              --file=data/arsipkg-auto/arsipkg-auto.ttl /arsipkg

# See ontology/competency_questions.md for 20 example queries
```

## 📊 Dataset Statistics

| Statistic | Value |
|---|---|
| Number of documents | 614 |
| Time span | 1961–2025 (64 years) |
| Issuing institutions | 133 distinct entities |
| Regulation types | 12 (PERATURAN BADAN/LEMBAGA, PERATURAN MENTERI, etc.) |
| Train / Val / Test split | 490 / 62 / 62 (80% / 10% / 10%, stratified) |

### Taxonomy Distribution

| Category | Description | Count | % |
|---|---|---|---|
| PK | Penyelenggaraan Kearsipan (general management) | 298 | 48.5% |
| JRA | Jadwal Retensi Arsip (retention schedule) | 156 | 25.4% |
| KA | Klasifikasi Arsip (classification scheme) | 56 | 9.1% |
| SKKAAD | Sistem Klasifikasi Keamanan Akses Arsip Dinamis | 55 | 9.0% |
| PA | Perubahan/Amendment | 40 | 6.5% |
| PC | Pencabutan/Revocation | 9 | 1.5% |

## 📜 License

- **Data** (corpus, KG, benchmark): [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- **Code**: [MIT License](https://opensource.org/licenses/MIT)
- **Ontology**: CC BY 4.0 (consistent with W3ID persistent identifier policy)

## 📝 Citation

If you use this work in your research, please cite:

```bibtex
@article{Untariyati2026ArsipKG,
  title={LLM-Driven Few-Shot Classification and Knowledge Graph Population
         from Indonesian Government Regulatory Archives},
  author={Untariyati, Nimas Ayu and Adi, Kusworo and
          Widodo, Aris Puji and Uliniansyah, M. Teduh},
  journal={International Journal of Data Science and Analytics},
  publisher={Springer},
  year={2026},
  doi={10.xxxx/xxxxxx}
}

@dataset{Untariyati2026ArsipKG_Bundle,
  title={ArsipKG: Reproducibility bundle for LLM-Driven Few-Shot Classification
         and Knowledge Graph Population from Indonesian Government Regulatory Archives},
  author={Untariyati, Nimas Ayu and Adi, Kusworo and
          Widodo, Aris Puji and Uliniansyah, M. Teduh},
  year={2026},
  publisher={Zenodo},
  version={1.0.0},
  doi={10.5281/zenodo.20569080},
  url={https://github.com/nayuuntariyati-byte/ArsipKG}
}
```

For the ontology specifically, see [ontology/README.md](ontology/README.md).

## 📧 Contact

**Nimas Ayu Untariyati** (corresponding author)
- Doctoral Program in Information Systems, Universitas Diponegoro
- Research Center for Data and Information Science, BRIN
- Email (primary): nayuuntariyati@students.undip.ac.id
- Email (institutional): nayuuntariyati@brin.go.id
- ORCID: [0009-0001-6466-9534](https://orcid.org/0009-0001-6466-9534)
