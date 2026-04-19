#!/usr/bin/env python3
"""Introspect the Neo4j schema for the Phase 1 foundation audit."""
import neo4j
from collections import Counter

driver = neo4j.GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'vitruvius'))

def run(q):
    with driver.session() as s:
        return list(s.run(q))

# Node labels
print('=== NODE LABELS ===')
for r in run('CALL db.labels() YIELD label RETURN label ORDER BY label'):
    print(r['label'])

# Relationship types
print('\n=== RELATIONSHIP TYPES ===')
for r in run('CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType ORDER BY relationshipType'):
    print(r['relationshipType'])

# Node count by label
print('\n=== NODE COUNTS BY LABEL ===')
for r in run('MATCH (n) RETURN labels(n)[0] AS label, count(*) AS cnt ORDER BY cnt DESC'):
    print(f"  {r['label']}: {r['cnt']}")

# Property keys
print('\n=== PROPERTY KEYS ===')
for r in run('CALL db.propertyKeys() YIELD propertyKey RETURN propertyKey ORDER BY propertyKey'):
    print(r['propertyKey'])

# Sample taxonomy roots
print('\n=== TAXONOMY ROOTS ===')
for r in run("MATCH (t:Taxonomy) RETURN t.id AS id, t.label AS label ORDER BY label LIMIT 20"):
    print(f"  {r['id']}: {r['label']}")

# CanonicalNode types
print('\n=== CANONICAL NODE TYPES ===')
for r in run('MATCH (c:CanonicalNode) RETURN c.type AS type, count(*) AS cnt ORDER BY cnt DESC'):
    print(f"  {r['type']}: {r['cnt']}")

# Relationship stats
print('\n=== RELATIONSHIP STATS ===')
for r in run('MATCH ()-[r]->() RETURN type(r) AS t, count(*) AS cnt ORDER BY cnt DESC'):
    print(f"  {r['t']}: {r['cnt']}")

# EvidenceSpan properties sample
print('\n=== EVIDENCE SPAN SAMPLE PROPERTIES ===')
for r in run("MATCH (e:EvidenceSpan) RETURN e LIMIT 1"):
    node = r['e']
    for k, v in sorted(node.items()):
        print(f"  {k}: {v!r}")

# CanonicalNode sample properties
print('\n=== CANONICAL NODE SAMPLE PROPERTIES ===')
for r in run("MATCH (c:CanonicalNode) RETURN c LIMIT 1"):
    node = r['c']
    for k, v in sorted(node.items()):
        print(f"  {k}: {v!r}")

# Check for any node without expected labels
print('\n=== UNLABELLED / OTHER NODE IDS ===')
for r in run("MATCH (n) WHERE NOT n:Taxonomy AND NOT n:Topic AND NOT n:Subtopic AND NOT n:CanonicalNode AND NOT n:EvidenceSpan RETURN labels(n) AS labs, n.id AS id LIMIT 10"):
    print(f"  {r['labs']}: {r['id']}")

driver.close()
