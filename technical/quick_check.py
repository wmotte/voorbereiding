#!/usr/bin/env python3

import os
from pathlib import Path
from neo4j import GraphDatabase

SCRIPT_DIR = Path(".").resolve()
env_file = SCRIPT_DIR / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"\'')

uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
username = os.environ.get("NEO4J_USER", "neo4j")
password = os.environ.get("NEO4J_PASSWORD", "password")
database = os.environ.get("NEO4J_DATABASE", "hymns")

driver = GraphDatabase.driver(uri, auth=(username, password))
session = driver.session(database=database)

# First check if the songs exist
result1 = session.run('MATCH (s:Song {bundel: "Liedboek"}) RETURN count(s) as count')
count = result1.single()["count"]
print(f"Total Liedboek songs: {count}")

# Check first 5
result2 = session.run('MATCH (s:Song {bundel: "Liedboek"}) RETURN s.nummer as nummer, s.titel as titel ORDER BY s.nummer LIMIT 5')
print("\nFirst 5 songs:")
for r in result2:
    print(f"  {r['nummer']}: {r['titel']}")

# Check WHERE IN query
result3 = session.run('MATCH (s:Song {bundel: "Liedboek"}) WHERE s.nummer IN [1, 2, 3, 4, 5] RETURN s.nummer as nummer, s.titel as titel ORDER BY s.nummer')
songs = list(result3)
print(f"\nUsing WHERE IN [1,2,3,4,5]: Found {len(songs)} songs")
for r in songs:
    print(f"  {r['nummer']}: {r['titel']}")

# Check specific songs
for i in [1, 2, 3, 4, 5]:
    result = session.run('MATCH (s:Song {bundel: "Liedboek", nummer: $num}) RETURN s.titel as titel', num=i)
    rec = result.single()
    if rec:
        print(f"\nDirect lookup #{i}: {rec['titel']}")
    else:
        print(f"\nDirect lookup #{i}: NOT FOUND")

driver.close()
