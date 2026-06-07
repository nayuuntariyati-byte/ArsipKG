# Complete Data Dictionary

This document provides comprehensive schema documentation for all datasets in this repository.

## ArsipDataset (data/arsipdataset/)

See `data/arsipdataset/README.md` for the 18-field schema.

**Source**: peraturan.go.id (Indonesian government regulation portal)
**Validation**: cross-referenced against ANRI (National Archives of Indonesia) registry
**Time span**: 1961–2025
**Total**: 614 documents

## ArsipQA-v1 (data/arsipqa-v1/)

JSONL format with fields: `id`, `question_type`, `question`, `regulation_id`, `gold_answer`, `gold_answer_alternatives`, `notes`.

**Total**: 90 QA pairs across 7 question types (see data/arsipqa-v1/README.md).

## Validation Dataset (data/validation/)

5 files for the 26-document stratified inter-annotator study.
Schema documented in data/validation/README.md.

## ArsipKG-Auto (data/arsipkg-auto/)

Three serialization formats (TTL, NT, Cypher) of the populated knowledge graph.

**Entity types** (5):
- Peraturan (669 individuals)
- Lembaga (133 individuals)
- Pejabat (42 individuals)
- Tanggal (361 individuals)
- Kategori (6 individuals)

**Relation types** (7):
- menerbitkan (609 edges): Lembaga → Peraturan
- mengatur (598 edges): Peraturan → Kategori
- berlakuPada (539 edges): Peraturan → Tanggal
- ditetapkanOleh (62 edges): Peraturan → Pejabat
- dicabutOleh (47 edges): Peraturan → Pejabat
- menggantikan (39 edges): Peraturan → Peraturan (transitive)
- menggantikan_sebagian (17 edges): Peraturan → Peraturan

## ArsipOnto (ontology/)

OWL 2 DL ontology with 16 classes, 9 object properties, 10 datatype properties, 286 axioms total.
Full documentation: `ontology/README.md`
