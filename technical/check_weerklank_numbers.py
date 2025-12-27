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
        print("=== WeerklankPsalm Songs ===\n")

        result = session.run("""
            MATCH (s:Song {bundel: 'WeerklankPsalm'})
            RETURN s.nummer as nummer, s.titel as titel
            ORDER BY s.nummer
            LIMIT 10
        """)

        for record in result:
            print(f"Nummer: {record['nummer']} - Titel: {record['titel']}")

        print("\n=== Weerklank Songs ===\n")

        result = session.run("""
            MATCH (s:Song {bundel: 'Weerklank'})
            RETURN s.nummer as nummer, s.titel as titel
            ORDER BY s.nummer
            LIMIT 10
        """)

        for record in result:
            print(f"Nummer: {record['nummer']} - Titel: {record['titel']}")

    driver.close()
except Exception as e:
    print(f"Error: {e}")
