#!/usr/bin/env python3
"""
Script to validate that song titles were updated correctly in the database.
"""

import os
import json
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
        print("=== Validating Updated Songs ===\n")

        # Check the 5 test songs from Liedboek
        result = session.run("""
            MATCH (s:Song {bundel: 'Liedboek'})
            WHERE s.nummer IN ['1', '2', '3', '4', '5']
            RETURN s.nummer as nummer, s.titel as titel
            ORDER BY toInteger(s.nummer)
        """)

        songs = list(result)
        print(f"Found {len(songs)} songs to validate\n")

        # Load expected titles from JSON
        json_file = SCRIPT_DIR / "song_titles" / "liedboek_2013_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        title_map = {song["number"]: song["title"] for song in data}

        all_correct = True
        for record in songs:
            nummer = record["nummer"]  # This is already a string
            current_title = record["titel"]
            expected_title = title_map.get(nummer)  # Use nummer directly (it's a string)

            if current_title == expected_title:
                print(f"✓ Song #{nummer}: CORRECT")
                print(f"  Title: {current_title}")
            else:
                all_correct = False
                print(f"✗ Song #{nummer}: MISMATCH")
                print(f"  Expected: {expected_title}")
                print(f"  Got:      {current_title}")
            print()

        if all_correct:
            print("="*80)
            print("✓ VALIDATION SUCCESSFUL - All titles are correct!")
            print("="*80)
        else:
            print("="*80)
            print("✗ VALIDATION FAILED - Some titles don't match")
            print("="*80)

    driver.close()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
