# ArsipKG-Auto: Populated Knowledge Graph

The automatically populated knowledge graph produced by the four-stage pipeline described in the paper.

## 📊 Statistics

| Metric | Value |
|---|---|
| Total individuals (nodes) | **1,211** |
| Total axioms (edges) | **1,911** |
| Connected components | **1** (fully connected) |
| Corpus coverage | **109%** |
| Graph density | 0.00131 |

## 🧮 Decomposition

**Individuals (1,211 total)**:
- Peraturan (Regulations): 669
- Tanggal (Dates): 361
- Lembaga (Institutions): 133
- Pejabat (Officials): 42
- Kategori (Categories): 6

**Axioms (1,911 total)**:
- menerbitkan: 609
- mengatur: 598
- berlakuPada: 539
- ditetapkanOleh: 62
- dicabutOleh: 47
- menggantikan: 39
- menggantikan_sebagian: 17

## 📁 Files

| File | Format | Use Case |
|---|---|---|
| `arsipkg-auto.ttl` | Turtle (W3C RDF) | Apache Jena, GraphDB, Stardog, rdflib |
| `arsipkg-auto.nt` | N-Triples | Streaming load, line-by-line parsing |
| `arsipkg-auto.cypher` | Neo4j Cypher | Neo4j Desktop, Neo4j Browser |

## 🚀 Quick Load

### Apache Jena Fuseki

```bash
fuseki-server --file=../../ontology/arsipkg-ontology.ttl \
              --file=arsipkg-auto.ttl /arsipkg
```

### Python (rdflib)

```python
from rdflib import Graph
g = Graph()
g.parse("../../ontology/arsipkg-ontology.ttl", format="turtle")
g.parse("arsipkg-auto.ttl", format="turtle")
print(f"Loaded {len(g)} triples")  # Expected: 1,911 + ontology axioms
```

### Neo4j

```bash
cypher-shell -u neo4j -p YOUR_PASSWORD < arsipkg-auto.cypher
```

Then in Neo4j Browser:

```cypher
MATCH (n) RETURN count(n) AS nodes;  // Expected: 1211
MATCH ()-[r]->() RETURN count(r) AS edges;  // Expected: 1911
CALL gds.wcc.stats('arsipkg')          // Expected: 1 component
YIELD componentCount;
```

## ⚠️ Status

This is a **PLACEHOLDER** package. To generate the actual ArsipKG-Auto from your ArsipDataset:

```bash
# Run the four-stage pipeline (requires ArsipDataset to be populated)
python ../../code/pipeline/stage1_ingestion.py
python ../../code/pipeline/stage2_classification.py
python ../../code/pipeline/stage3a_metadata.py
python ../../code/pipeline/stage3b_llm_titles.py
python ../../code/pipeline/stage4_kg_population.py --export ttl,nt,cypher
```

Expected runtime: ~11 minutes total (~10 min Stage 3B on NVIDIA L4, rest negligible).

## 📜 License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
