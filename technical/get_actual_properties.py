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
        # Get actual properties of Song nodes
        print("=== All Properties of Sample Song Nodes ===\n")

        result = session.run("MATCH (s:Song) RETURN s LIMIT 5")

        for i, record in enumerate(result, 1):
            node = record["s"]
            props = dict(node)
            print(f"Song #{i}:")
            for k, v in sorted(props.items()):
                # Truncate long values
                v_str = str(v)
                if len(v_str) > 100:
                    v_str = v_str[:100] + "..."
                print(f"  {k}: {v_str}")
            print("-" * 80)

    driver.close()
except Exception as e:
    print(f"Error: {e}")
