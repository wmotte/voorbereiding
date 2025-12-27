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

print(f"Connecting to {uri}, database={database}...\n")

try:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session(database=database) as session:
        # Get all unique bundel values
        print("=== All Hymn Books (bundel) in Database ===\n")

        result = session.run("""
            MATCH (s:Song)
            RETURN DISTINCT s.bundel as bundel, count(*) as count
            ORDER BY bundel
        """)

        for record in result:
            print(f"{record['bundel']}: {record['count']} songs")

        # Get sample songs from each bundel
        print("\n=== Sample Song from Each Bundel ===\n")

        result = session.run("""
            MATCH (s:Song)
            WITH s.bundel as bundel, collect(s)[0] as sample
            RETURN bundel, sample.nummer as nummer, sample.titel as titel
            ORDER BY bundel
        """)

        for record in result:
            print(f"Bundel: {record['bundel']}")
            print(f"  Sample nummer: {record['nummer']}")
            print(f"  Sample titel: {record['titel']}")
            print()

    driver.close()
except Exception as e:
    print(f"Error: {e}")
