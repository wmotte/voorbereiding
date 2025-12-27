#!/usr/bin/env python3

import os
import json
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

# Check database Weerklank numbers
print("=== Database Weerklank Songs (first 10) ===")
result = session.run('MATCH (s:Song {bundel: "Weerklank"}) RETURN s.nummer as nummer, s.titel as titel ORDER BY toInteger(s.nummer) LIMIT 10')
db_songs = list(result)
for r in db_songs:
    print(f"  DB: {r['nummer']} (type: {type(r['nummer'])}) - {r['titel']}")

# Check JSON Weerklank data
print("\n=== JSON Weerklank Songs (non-Psalmen, first 10) ===")
json_file = SCRIPT_DIR / "song_titles" / "weerklank_titles.json"
with open(json_file) as f:
    data = json.load(f)

non_psalmen = [x for x in data if x.get('category') != 'Psalmen'][:10]
for song in non_psalmen:
    print(f"  JSON: {song['number']} (type: {type(song['number'])}) - {song['title']}")

# Try to match
print("\n=== Matching Test ===")
json_map = {song["number"]: song["title"] for song in data if song.get("category") != "Psalmen"}
print(f"Total JSON non-Psalmen songs: {len(json_map)}")
print(f"Keys in JSON map (first 10): {list(json_map.keys())[:10]}")

for r in db_songs[:5]:
    nummer = r["nummer"]
    match = json_map.get(nummer)
    print(f"  DB nummer '{nummer}' -> JSON match: {match}")

driver.close()
