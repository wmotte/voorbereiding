#!/usr/bin/env python3

import os
from pathlib import Path
from neo4j import GraphDatabase

# Load .env manually
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

print(f"Connecting to {uri}, database={database}...")

try:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session(database=database) as session:
        print("\n--- Labels ---")
        result = session.run("CALL db.labels()")
        for record in result:
            print(f"Label: {record['label']}")
            
        print("\n--- Relationship Types ---")
        result = session.run("CALL db.relationshipTypes()")
        for record in result:
            print(f"Type: {record['relationshipType']}")

        print("\n--- Sample BiblicalReference ---")
        result = session.run("MATCH (br:BiblicalReference) RETURN br.reference as ref LIMIT 5")
        for record in result:
            print(f"Ref: {record['ref']}")

        print("\n--- Sample Keyword ---")
        result = session.run("MATCH (k:Keyword) RETURN k.name as name LIMIT 5")
        for record in result:
            print(f"Keyword: {record['name']}")

    driver.close()
except Exception as e:
    print(f"Error: {e}")
