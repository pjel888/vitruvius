from vitruvius.kg.neo4j_client import Neo4jClient

client = Neo4jClient(uri='bolt://localhost:7687', user='neo4j', password='vitruvius')
result = client.run('MATCH ()-[r]->() RETURN type(r) AS rel_type, count(r) AS total ORDER BY total DESC')
for row in result:
    print(f"{row['rel_type']}: {row['total']}")
client.close()
