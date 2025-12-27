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
        # Get sample songs from each hymn book
        print("=== Sample Songs from Each Hymn Book ===\n")

        result = session.run("""
            MATCH (s:Song)
            RETURN s.source as source, s.number as number, s.title as title,
                   s.eerste_regel as eerste_regel
            LIMIT 20
        """)

        for record in result:
            print(f"Source: {record['source']}")
            print(f"Number: {record['number']}")
            print(f"Title: {record['title']}")
            print(f"Eerste regel: {record['eerste_regel']}")
            print("-" * 60)

        # Get counts per source
        print("\n=== Song Counts by Source ===\n")
        result = session.run("""
            MATCH (s:Song)
            RETURN s.source as source, count(s) as count
            ORDER BY source
        """)

        for record in result:
            print(f"{record['source']}: {record['count']} songs")

    driver.close()
except Exception as e:
    print(f"Error: {e}")
