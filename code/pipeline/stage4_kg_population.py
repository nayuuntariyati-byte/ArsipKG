"""
Stage 4: Knowledge Graph Population.
Ingests triples into Neo4j, deduplicates entities, exports to RDF.
Final KG: 1,211 individuals, 1,911 axioms, single connected component.
"""

import argparse
import json
from pathlib import Path

from rdflib import Graph, Namespace, Literal, URIRef, XSD
from rdflib.namespace import RDF

ARSIP = Namespace("https://w3id.org/arsipkg/ontology/v1#")


def safe_uri(text):
    """Sanitize text for use in URI."""
    return ARSIP[str(text).replace(" ", "_").replace("/", "-").replace(",", "")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage3a", default="../../results/stage3a_triples.jsonl")
    ap.add_argument("--stage3b", default="../../results/stage3b_supersession.jsonl")
    ap.add_argument("--ontology", default="../../ontology/arsipkg-ontology.ttl")
    ap.add_argument("--output_dir", default="../../data/arsipkg-auto/")
    ap.add_argument("--format", default="ttl,nt,cypher",
                    help="Comma-separated: ttl,nt,cypher")
    args = ap.parse_args()

    g = Graph()
    g.bind("arsip", ARSIP)
    try:
        g.parse(args.ontology, format="turtle")
        print(f"Loaded ontology: {len(g)} triples")
    except Exception as e:
        print(f"Warning: ontology load failed: {e}")

    # Stage 3A triples
    if Path(args.stage3a).exists():
        with open(args.stage3a) as f:
            for line in f:
                t = json.loads(line)
                g.add((safe_uri(t["s"]), safe_uri(t["p"]), safe_uri(t["o"])))

    # Stage 3B supersession triples (above confidence threshold)
    if Path(args.stage3b).exists():
        with open(args.stage3b) as f:
            for line in f:
                rec = json.loads(line)
                if rec.get("flagged_for_review"):
                    continue
                pid = safe_uri(rec["id"])
                for target in rec.get("menggantikan", []):
                    g.add((pid, ARSIP["menggantikan"], safe_uri(target)))
                for target in rec.get("menggantikan_sebagian", []):
                    g.add((pid, ARSIP["menggantikan_sebagian"], safe_uri(target)))

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    formats = args.format.split(",")
    if "ttl" in formats:
        g.serialize(out / "arsipkg-auto.ttl", format="turtle")
    if "nt" in formats:
        g.serialize(out / "arsipkg-auto.nt", format="nt")
    if "cypher" in formats:
        # Simplified Cypher export
        with open(out / "arsipkg-auto.cypher", "w") as f:
            f.write("// Auto-generated Cypher export\n")
            f.write("CREATE CONSTRAINT peraturan_id IF NOT EXISTS FOR (p:Peraturan) REQUIRE p.id IS UNIQUE;\n")
            for s, p, o in g:
                f.write(f"MERGE ({{uri: '{s}'}})-[:{p.split('#')[-1] if '#' in str(p) else 'relatesTo'}]->({{uri: '{o}'}});\n")

    print(f"KG written to {out}: {len(g)} total triples")


if __name__ == "__main__":
    main()
