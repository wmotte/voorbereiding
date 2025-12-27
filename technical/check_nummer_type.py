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

result = session.run('MATCH (s:Song {bundel: "Liedboek"}) RETURN s.nummer as nummer LIMIT 10')
print("Number types and values:")
for r in result:
    num = r['nummer']
    print(f"  Value: {num}, Type: {type(num)}, Repr: {repr(num)}")

driver.close()
