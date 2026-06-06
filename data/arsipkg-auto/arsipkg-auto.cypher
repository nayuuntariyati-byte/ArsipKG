// === PLACEHOLDER: Neo4j Cypher export ===
// === Generate with: python code/pipeline/stage4_kg_population.py --format cypher ===

// Schema
CREATE CONSTRAINT peraturan_id IF NOT EXISTS FOR (p:Peraturan) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT lembaga_name IF NOT EXISTS FOR (l:Lembaga) REQUIRE l.name IS UNIQUE;
CREATE CONSTRAINT pejabat_name IF NOT EXISTS FOR (p:Pejabat) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT tanggal_iso IF NOT EXISTS FOR (t:Tanggal) REQUIRE t.iso IS UNIQUE;
CREATE CONSTRAINT kategori_code IF NOT EXISTS FOR (k:Kategori) REQUIRE k.code IS UNIQUE;

// Example node + relations (replace with your full 1,211 nodes / 1,911 edges)
MERGE (p:Peraturan {id: "PER-EXAMPLE-001", tentang: "Jadwal Retensi Arsip Substantif", tahun: 2020})
MERGE (l:Lembaga {name: "KEMENTERIAN KESEHATAN"})
MERGE (k:Kategori {code: "JRA"})
MERGE (d:Tanggal {iso: date("2020-04-01")})
MERGE (l)-[:menerbitkan]->(p)
MERGE (p)-[:mengatur]->(k)
MERGE (p)-[:berlakuPada]->(d);
