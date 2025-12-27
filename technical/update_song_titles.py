#!/usr/bin/env python3
"""
Script to update song titles in the hymns database from the official title JSON files.
"""

import os
import json
from pathlib import Path
from neo4j import GraphDatabase
from typing import Dict, List

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


def load_titles(bundel_name: str) -> Dict:
    """Load titles from JSON files and return a mapping of number -> title."""
    title_map = {}

    if bundel_name == "Liedboek":
        json_file = SCRIPT_DIR / "song_titles" / "liedboek_2013_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        for song in data:
            # Numbers can be strings like "1", "1a", "1b", etc.
            title_map[song["number"]] = song["title"]

    elif bundel_name == "Hemelhoog":
        json_file = SCRIPT_DIR / "song_titles" / "hemelhoog_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        for song in data:
            # Numbers are integers in this file
            title_map[str(song["number"])] = song["title"]

    elif bundel_name == "OpToonhoogte":
        json_file = SCRIPT_DIR / "song_titles" / "op_toonhoogte_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        for song in data:
            title_map[song["number"]] = song["title"]

    elif bundel_name == "Weerklank":
        json_file = SCRIPT_DIR / "song_titles" / "weerklank_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        # Non-Psalmen songs
        for song in data:
            if song.get("category") != "Psalmen":
                title_map[song["number"]] = song["title"]

    elif bundel_name == "WeerklankPsalm":
        json_file = SCRIPT_DIR / "song_titles" / "weerklank_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        # Psalmen songs - strip the "P" prefix for matching
        for song in data:
            if song.get("category") == "Psalmen":
                # Song numbers in JSON are like "P1", "P2", etc.
                # Database stores them as 1, 2, etc.
                number = song["number"]
                if number.startswith("P"):
                    # Store both with and without "P" for flexibility
                    number_without_p = number[1:]
                    title_map[number_without_p] = song["title"]
                    title_map[number] = song["title"]

    return title_map


def update_titles_for_bundel(session, bundel: str, limit: int = None, dry_run: bool = True):
    """Update titles for a specific bundel."""
    print(f"\n{'='*80}")
    print(f"Processing bundel: {bundel}")
    print(f"{'='*80}\n")

    # Load title mappings
    title_map = load_titles(bundel)
    print(f"Loaded {len(title_map)} titles from JSON for {bundel}")

    # Get songs from database
    query = "MATCH (s:Song {bundel: $bundel}) RETURN s.nummer as nummer, s.titel as titel, s.id as id"
    if limit:
        query += f" LIMIT {limit}"

    result = session.run(query, bundel=bundel)
    songs = list(result)
    print(f"Found {len(songs)} songs in database for {bundel}\n")

    # Track statistics
    matched = 0
    unmatched = 0
    updated = 0
    unchanged = 0

    for record in songs:
        nummer = record["nummer"]
        current_title = record["titel"]
        song_id = record["id"]

        # Convert nummer to string for matching
        nummer_str = str(nummer)

        # Try to find the correct title
        correct_title = title_map.get(nummer_str)

        if correct_title is None:
            # For Liedboek, also try converting int to string with letter suffixes
            # This handles cases where database has 1 but JSON has "1a", "1b", etc.
            unmatched += 1
            print(f"⚠️  UNMATCHED: {bundel} #{nummer} - No title found in JSON")
            print(f"   Current title: {current_title}")
            continue

        matched += 1

        # Check if title needs updating
        if current_title == correct_title:
            unchanged += 1
            if not dry_run:
                print(f"✓ UNCHANGED: {bundel} #{nummer} - '{correct_title}'")
        else:
            updated += 1
            print(f"{'[DRY RUN] ' if dry_run else ''}UPDATE: {bundel} #{nummer}")
            print(f"  OLD: {current_title}")
            print(f"  NEW: {correct_title}")

            if not dry_run:
                # Actually update the database
                update_query = """
                    MATCH (s:Song {id: $id})
                    SET s.titel = $new_title
                    RETURN s.titel as updated_title
                """
                update_result = session.run(update_query, id=song_id, new_title=correct_title)
                updated_title = update_result.single()["updated_title"]
                print(f"  ✓ Updated to: {updated_title}")
            print()

    # Print summary
    print(f"\n{'-'*80}")
    print(f"Summary for {bundel}:")
    print(f"  Total songs processed: {len(songs)}")
    print(f"  Matched: {matched}")
    print(f"  Unmatched: {unmatched}")
    print(f"  Updated: {updated}")
    print(f"  Unchanged: {unchanged}")
    print(f"{'-'*80}\n")

    return {
        "bundel": bundel,
        "total": len(songs),
        "matched": matched,
        "unmatched": unmatched,
        "updated": updated,
        "unchanged": unchanged
    }


def main():
    """Main function to update song titles."""
    print(f"Connecting to {uri}, database={database}...\n")

    driver = GraphDatabase.driver(uri, auth=(username, password))

    try:
        with driver.session(database=database) as session:
            # Start with a small test: 5 songs from Liedboek
            stats = update_titles_for_bundel(
                session,
                bundel="Liedboek",
                limit=5,  # Only process 5 songs for testing
                dry_run=False  # Actually update the database
            )

            print("\n" + "="*80)
            print("TEST COMPLETED")
            print("="*80)
            print(f"\nTo actually update the database, set dry_run=False in the code.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.close()


if __name__ == "__main__":
    main()
