#!/usr/bin/env python3

import os
from pathlib import Path
from neo4j import GraphDatabase

# Load .env manually as done in the main script
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
        # Check if Song nodes exist
        result = session.run("MATCH (s:Song) RETURN count(s) as count")
        count = result.single()["count"]
        print(f"Found {count} Song nodes.")
        
        if count > 0:
            # Get a sample node and print its properties
            result = session.run("MATCH (s:Song) RETURN s LIMIT 1")
            record = result.single()
            node = record["s"]
            print("Sample Song Node Properties:")
            props = dict(node)
            for k, v in props.items():
                print(f"  {k}: {v}")
                
            if "eerste_regel" in props:
                print(f"\nCHECK: 'eerste_regel' found: {props['eerste_regel']}")
            else:
                print("\nCHECK: 'eerste_regel' NOT found on this node.")

            if "laatste_regel" in props:
                print(f"CHECK: 'laatste_regel' found: {props['laatste_regel']}")
            else:
                print("CHECK: 'laatste_regel' NOT found on this node.")
        else:
            print("No Song nodes found to check.")
            
    driver.close()
except Exception as e:
    print(f"Error: {e}")
