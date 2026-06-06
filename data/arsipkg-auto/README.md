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


## 📜 License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
