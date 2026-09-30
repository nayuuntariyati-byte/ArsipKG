# ArsipKG: Indonesian Government Regulatory Archives Knowledge Graph

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Companion repository for the paper **"LLM-Driven Few-Shot Classification and Knowledge Graph Population from Indonesian Government Regulatory Archives"** (Untariyati et al., 2026, International Journal of Data Science and Analytics, Springer).

## 📋 Overview

This repository provides the complete experimental package for automated knowledge graph (KG) population from Indonesian government regulatory archives. It includes:

- **ArsipDataset**: A curated corpus of 614 Indonesian government regulations on archival administration (1961–2025, from 133 institutions)
- **ArsipOnto**: A formal OWL 2 DL ontology aligned with LKIF, Dublin Core Terms, SKOS, and FOAF
- **ArsipKG-Auto**: A populated knowledge graph with 1,211 individuals and 1,911 axioms 
- **ArsipQA-v1**: A benchmark of 90 question-answer pairs across 7 question types
- **Validation Dataset**: 26 stratified documents independently annotated by two domain experts (Cohen's κ = 0.9504)
- **Experimental Code**: Four-stage pipeline implementation including baselines and evaluation scripts

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
│   ├── validation/                    # Inter-annotator validation
│   │   ├── blind_template.csv         # Blank annotation template
│   │   ├── annotator1_labels.csv      # Annotator 1 labels
│   │   ├── annotator2_labels.csv      # Annotator 2 labels
│   │   ├── consensus_labels.csv       # Adjudicated final labels
│   │   └── README.md                  # Annotation protocol
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
│   │   ├── stage4_kg_population.py    # Neo4j KG construction
│   │   ├── prompts/                   # Few-shot prompt templates
│   │   └── README.md
│   │
│   └── evaluation/                    # Evaluation scripts
│       ├── compute_kappa.py           # Cohen's κ computation
│       ├── evaluate_classification.py # Macro-F1 per category
│       ├── evaluate_triples.py        # Triple extraction precision
│       ├── evaluate_qa.py             # BERTScore, ROUGE-L, Wilcoxon
│       └── README.md
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

# Expected: macro-F1 = 0.963
```

### Run Inter-Annotator Validation

```bash
python code/evaluation/compute_kappa.py \
    --annotator1 data/validation/annotator1_labels.csv \
    --annotator2 data/validation/annotator2_labels.csv

# Expected: Cohen's κ = 0.9504
```

### Load Knowledge Graph (Neo4j)

```bash
# Start Neo4j, then:
cypher-shell -u neo4j -p YOUR_PASSWORD < data/arsipkg-auto/arsipkg-auto.cypher

# Expected: 1,211 nodes, 1,911 edges, 1 connected component
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

@dataset{ArsipKG2026,
  title={ArsipKG: Indonesian Government Regulatory Archives Knowledge Graph},
  author={Untariyati, Nimas Ayu and Adi, Kusworo and
          Widodo, Aris Puji and Uliniansyah, M. Teduh},
  year={2026},
  publisher={Zenodo},
  version={1.0.0},
  doi={10.5281/zenodo.20569079},
  url={https://github.com/nayuuntariyati-byte/ArsipKG}
}
```

For the ontology specifically, see [ontology/README.md](ontology/README.md).

## 📧 Contact

**Nimas Ayu Untariyati** (corresponding author)
- Doctoral Program in Information Systems, Universitas Diponegoro
- Research Center for Data and Information Science, BRIN
- Email: nayuuntariyati@students.undip.ac.id | nima004@brin.go.id
- ORCID: [0009-0001-6466-9534](https://orcid.org/0009-0001-6466-9534)

