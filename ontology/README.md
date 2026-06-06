# ArsipOnto: An Ontology for Indonesian Regulatory Archives

**Version**: 1.0.0
**License**: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
**Persistent identifier**: `https://w3id.org/arsipkg/ontology/v1`
**OWL profile**: OWL 2 DL

ArsipOnto is a domain ontology for representing Indonesian government regulatory archives. It models the core entities (`Peraturan`, `Lembaga`, `Pejabat`, `Tanggal`, `Kategori`) and their relations, with explicit alignment to internationally recognized vocabularies: **LKIF** (Legal Knowledge Interchange Format), **Dublin Core Terms**, **SKOS** (Simple Knowledge Organization System), and **FOAF** (Friend of a Friend).

The ontology underpins the **ArsipKG-Auto** knowledge graph (1,211 individuals, 1,911 axioms) populated from the **ArsipDataset** corpus of 614 regulations spanning 1961–2025.

## Quick Statistics

| Metric | Value |
|---|---|
| OWL classes | 16 (5 main + 11 subclasses) |
| Object properties | 9 (7 main + 2 inverses) |
| Datatype properties | 10 |
| Total axioms | 286 triples |
| Disjointness axioms | 2 explicit + AllDisjointClasses |
| Aligned vocabularies | LKIF, DCMI Terms, SKOS, FOAF |

## Files in This Repository

```
ArsipOnto/
├── arsipkg-ontology.ttl                 # Turtle format (canonical)
├── arsipkg-ontology.owl                 # RDF/XML format (Protégé-compatible)
├── arsipkg-ontology.rdf                 # XML serialization
├── ArsipOnto_Competency_Questions.docx  # 20 CQs with SPARQL queries
├── Paper_Integration_Patch.docx         # Paper update instructions
└── README.md                            # This file
```

## Class Hierarchy

```
owl:Thing
├── arsip:Peraturan (Regulation) — subClassOf lkif-norm:Legal_Document
│   ├── arsip:PeraturanAktif (Active)
│   └── arsip:PeraturanDicabut (Superseded) — disjointWith PeraturanAktif
├── arsip:Lembaga (Institution) — subClassOf lkif:Legal_Person, foaf:Organization
│   ├── arsip:Kementerian (Ministry)
│   ├── arsip:LPNK (Non-Ministerial Agency)
│   │   └── arsip:ANRI (National Archives of Indonesia)
├── arsip:Pejabat (Official) — subClassOf lkif:Natural_Person, foaf:Person
├── arsip:Tanggal (Date) — subClassOf lkif-time:Time_Point
└── arsip:Kategori (Category) — subClassOf skos:Concept
    ├── arsip:KA (Klasifikasi Arsip)
    ├── arsip:JRA (Jadwal Retensi Arsip)
    ├── arsip:SKKAAD (Sistem Klasifikasi Keamanan)
    ├── arsip:PK (Penyelenggaraan Kearsipan)
    ├── arsip:PA (Perubahan/Amendment) — disjointWith PC
    └── arsip:PC (Pencabutan/Revocation)
```

## Object Properties

| Property | Domain | Range | Type | DC Alignment |
|---|---|---|---|---|
| `menerbitkan` | Lembaga | Peraturan | — | subProperty of `dcterms:publisher` |
| `diterbitkanOleh` | Peraturan | Lembaga | inverse of `menerbitkan` | — |
| `mengatur` | Peraturan | Kategori | — | subProperty of `dcterms:subject` |
| `ditetapkanOleh` | Peraturan | Pejabat | — | subProperty of `dcterms:creator` |
| `berlakuPada` | Peraturan | Tanggal | — | subProperty of `dcterms:date` |
| `dicabutOleh` | Peraturan | Pejabat | — | — |
| `menggantikan` | Peraturan | Peraturan | **TransitiveProperty** | — |
| `digantikanOleh` | Peraturan | Peraturan | inverse of `menggantikan`, TransitiveProperty | — |
| `menggantikan_sebagian` | Peraturan | Peraturan | disjointWith `menggantikan` | — |

## Datatype Properties

| Property | Domain | Range | DC Alignment |
|---|---|---|---|
| `nomorPeraturan` | Peraturan | xsd:string | subProperty of `dcterms:identifier` |
| `tahunDitetapkan` | Peraturan | xsd:gYear | — |
| `tentang` | Peraturan | xsd:string | subProperty of `dcterms:title` |
| `jenisPeraturan` | Peraturan | xsd:string | subProperty of `dcterms:type` |
| `urlSumber` | Peraturan | xsd:anyURI | subProperty of `dcterms:source` |
| `status` | Peraturan | enum {aktif, dicabut} | — |
| `namaLembaga` | Lembaga | xsd:string | subProperty of `foaf:name`, `dcterms:title` |
| `namaPejabat` | Pejabat | xsd:string | subProperty of `foaf:name` |
| `jabatan` | Pejabat | xsd:string | subProperty of `foaf:title` |
| `tanggalISO` | Tanggal | xsd:date | — |

## Usage in Protégé

### Loading the ontology

1. Open **Protégé 5.6 or later**
2. File → Open → select `arsipkg-ontology.owl`
3. Wait for the ontology to load (should complete in <5 seconds)
4. Switch to the **Classes** tab to view the class hierarchy
5. Switch to the **OntoGraf** tab for visual exploration

### Running the reasoner

1. Reasoner → Configure → select **HermiT 1.4.3** or **Pellet** or **ELK**
2. Reasoner → Start reasoner
3. Confirm "Inferred ontology is consistent" appears in the status bar
4. Switch to **Object property hierarchy (inferred)** to see transitive closures

### Running SPARQL queries

1. Window → Tabs → SPARQL Query
2. Paste any competency question from `ArsipOnto_Competency_Questions.docx`
3. Click **Execute**
4. View results in the Results panel

## Usage in Apache Jena Fuseki

```bash
# Start Fuseki with the ontology loaded
fuseki-server --file=arsipkg-ontology.ttl /arsipkg

# Query via curl
curl -X POST http://localhost:3030/arsipkg/sparql \
  -H "Content-Type: application/sparql-query" \
  --data 'PREFIX arsip: <https://w3id.org/arsipkg/ontology/v1#>
          SELECT ?class WHERE { ?class a owl:Class } LIMIT 20'
```

## Usage in Python (rdflib)

```python
from rdflib import Graph, Namespace

ARSIP = Namespace("https://w3id.org/arsipkg/ontology/v1#")
g = Graph()
g.parse("arsipkg-ontology.ttl", format="turtle")

# Find all classes aligned with LKIF
results = g.query("""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX lkif: <http://www.estrellaproject.org/lkif-core/lkif-core.owl#>

SELECT ?class ?lkifClass
WHERE {
  ?class rdfs:subClassOf ?lkifClass .
  FILTER(STRSTARTS(STR(?lkifClass), STR(lkif:)))
}
""")
for row in results:
    print(row)
```

## Loading with the Instance Data (ArsipKG-Auto)

The ontology defines the *schema*. To load the actual *instance data* (1,211 individuals from 614 regulations), download `arsipkg-auto.nt` (or `.ttl`) from the companion dataset repository and load both files together:

```python
g = Graph()
g.parse("arsipkg-ontology.ttl", format="turtle")  # Schema
g.parse("arsipkg-auto.nt", format="nt")           # Instance data
```

## Validation

ArsipOnto has been validated through:

1. **Syntax validation**: Parsed successfully by rdflib 7.0+, OWLAPI 5.5+, and Protégé 5.6.4
2. **Logical consistency**: Confirmed consistent by HermiT 1.4.3 reasoner
3. **Competency questions**: All 20 CQs successfully answered (see `ArsipOnto_Competency_Questions.docx`)
4. **Standards compliance**: OWL 2 DL profile (validated via OWL 2 Profile Validator)

## Citation

If you use ArsipOnto in your research, please cite the accompanying paper:

```bibtex
@article{Untariyati2026ArsipKG,
  title={LLM-Driven Few-Shot Classification and Knowledge Graph Population
         from Indonesian Government Regulatory Archives},
  author={Untariyati, Nimas Ayu and Adi, Kusworo and
          Widodo, Aris Puji and Uliniansyah, M. Teduh},
  journal={International Journal of Data Science and Analytics},
  publisher={Springer},
  year={2026},
  doi={[TO BE ASSIGNED]}
}
```

For the ontology itself:

```bibtex
@misc{ArsipOnto2026,
  title={ArsipOnto: An Ontology for Indonesian Regulatory Archives},
  author={Untariyati, Nimas Ayu and Adi, Kusworo and
          Widodo, Aris Puji and Uliniansyah, M. Teduh},
  year={2026},
  publisher={Zenodo},
  version={1.0.0},
  doi={[TO BE ASSIGNED]},
  url={https://w3id.org/arsipkg/ontology/v1}
}
```

## Aligned External Vocabularies

| Vocabulary | URI | Purpose |
|---|---|---|
| **LKIF Core** | `http://www.estrellaproject.org/lkif-core/` | Legal document modeling |
| **LKIF Norm** | `http://www.estrellaproject.org/lkif-core/norm.owl#` | Norms and regulations |
| **LKIF Time** | `http://www.estrellaproject.org/lkif-core/time.owl#` | Temporal concepts |
| **Dublin Core Terms** | `http://purl.org/dc/terms/` | Metadata interoperability |
| **SKOS** | `http://www.w3.org/2004/02/skos/core#` | Taxonomy concepts |
| **FOAF** | `http://xmlns.com/foaf/0.1/` | Agent representation |

## Versioning

This is **version 1.0.0** of ArsipOnto. Future versions will follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (2.0.0): Backward-incompatible changes to class hierarchy or property domains/ranges
- **MINOR** (1.1.0): Backward-compatible additions of new classes or properties
- **PATCH** (1.0.1): Documentation fixes, annotation improvements, no schema changes

Version history is maintained in the `owl:versionInfo` annotation of the ontology header.

## Contact

For questions, bug reports, or suggestions for future versions, please contact:

**Nimas Ayu Untariyati** (corresponding author)
Doctoral Program in Information System
School of Postgraduate Studies, Universitas Diponegoro
Email: nayuuntariyati@students.undip.ac.id

## Acknowledgments

This ontology builds upon decades of work by the Semantic Web and Legal Informatics communities. Particular thanks to the LKIF Core development team (ESTRELLA Project), DCMI, the W3C SKOS working group, and the FOAF maintainers for their foundational vocabularies.
