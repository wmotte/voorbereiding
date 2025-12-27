#!/usr/bin/env python3
"""
Final validation script to verify all song title updates.
"""

import os
import json
from pathlib import Path
from neo4j import GraphDatabase
import random

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

def load_title_map(bundel):
    """Load expected titles from JSON for a bundel."""
    title_map = {}

    if bundel == "Liedboek":
        json_file = SCRIPT_DIR / "song_titles" / "liedboek_2013_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        for song in data:
            title_map[song["number"]] = song["title"]

    elif bundel == "Hemelhoog":
        json_file = SCRIPT_DIR / "song_titles" / "hemelhoog_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        for song in data:
            title_map[str(song["number"])] = song["title"]

    elif bundel == "OpToonhoogte":
        json_file = SCRIPT_DIR / "song_titles" / "op_toonhoogte_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        for song in data:
            title_map[song["number"]] = song["title"]

    elif bundel == "Weerklank":
        json_file = SCRIPT_DIR / "song_titles" / "weerklank_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        for song in data:
            if song.get("category") != "Psalmen":
                title_map[str(song["number"])] = song["title"]

    elif bundel == "WeerklankPsalm":
        json_file = SCRIPT_DIR / "song_titles" / "weerklank_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        for song in data:
            if song.get("category") == "Psalmen":
                number = song["number"]
                if number.startswith("P"):
                    number_without_p = number[1:]
                    title_map[number_without_p] = song["title"]

    return title_map

def validate_bundel(session, bundel, sample_size=10):
    """Validate a sample of songs from a bundel."""
    print(f"\n{'='*80}")
    print(f"Validating {bundel}")
    print(f"{'='*80}\n")

    # Load expected titles
    title_map = load_title_map(bundel)

    # Get all songs from this bundel
    result = session.run(
        "MATCH (s:Song {bundel: $bundel}) RETURN s.nummer as nummer, s.titel as titel",
        bundel=bundel
    )
    songs = list(result)

    # Check all songs that should match
    correct = 0
    incorrect = 0
    missing_from_json = 0

    for record in songs:
        nummer = record["nummer"]
        current_title = record["titel"]
        expected_title = title_map.get(nummer)

        if expected_title is None:
            missing_from_json += 1
        elif current_title == expected_title:
            correct += 1
        else:
            incorrect += 1
            print(f"✗ MISMATCH at #{nummer}")
            print(f"  Expected: {expected_title}")
            print(f"  Got:      {current_title}\n")

    # Show random sample of correct matches
    correct_songs = [
        (r["nummer"], r["titel"])
        for r in songs
        if title_map.get(r["nummer"]) == r["titel"]
    ]

    if correct_songs:
        print(f"Sample of {min(sample_size, len(correct_songs))} correctly updated songs:")
        samples = random.sample(correct_songs, min(sample_size, len(correct_songs)))
        for num, title in sorted(samples, key=lambda x: int(''.join(filter(str.isdigit, x[0])) or 0)):
            print(f"  ✓ #{num}: {title}")

    # Print summary
    print(f"\n{'-'*80}")
    print(f"Summary for {bundel}:")
    print(f"  Total songs: {len(songs)}")
    print(f"  Correctly matched: {correct}")
    print(f"  Incorrect: {incorrect}")
    print(f"  Missing from JSON: {missing_from_json}")

    if incorrect == 0:
        print(f"  ✅ All matchable songs have correct titles!")
    else:
        print(f"  ❌ {incorrect} songs have incorrect titles!")

    print(f"{'-'*80}\n")

    return {
        "bundel": bundel,
        "total": len(songs),
        "correct": correct,
        "incorrect": incorrect,
        "missing": missing_from_json
    }


def main():
    """Main validation function."""
    print(f"\n{'='*80}")
    print(f"FINAL VALIDATION OF SONG TITLE UPDATES")
    print(f"{'='*80}")
    print(f"\nConnecting to {uri}, database={database}...\n")

    driver = GraphDatabase.driver(uri, auth=(username, password))

    bundels = ["Liedboek", "Hemelhoog", "OpToonhoogte", "Weerklank", "WeerklankPsalm"]
    all_stats = []

    try:
        with driver.session(database=database) as session:
            for bundel in bundels:
                stats = validate_bundel(session, bundel, sample_size=10)
                all_stats.append(stats)

            # Overall summary
            print(f"\n{'='*80}")
            print(f"OVERALL VALIDATION SUMMARY")
            print(f"{'='*80}\n")

            total_all = sum(s["total"] for s in all_stats)
            correct_all = sum(s["correct"] for s in all_stats)
            incorrect_all = sum(s["incorrect"] for s in all_stats)
            missing_all = sum(s["missing"] for s in all_stats)

            for stats in all_stats:
                status = "✅" if stats["incorrect"] == 0 else "❌"
                print(f"{status} {stats['bundel']:20} - Total: {stats['total']:4}, "
                      f"Correct: {stats['correct']:4}, Incorrect: {stats['incorrect']:4}, "
                      f"Missing: {stats['missing']:4}")

            print(f"\n{'TOTALS':23} - Total: {total_all:4}, "
                  f"Correct: {correct_all:4}, Incorrect: {incorrect_all:4}, "
                  f"Missing: {missing_all:4}")

            print(f"\n{'='*80}")
            if incorrect_all == 0:
                print("✅ VALIDATION SUCCESSFUL - All song titles are correct!")
            else:
                print(f"❌ VALIDATION FAILED - {incorrect_all} songs have incorrect titles")
            print(f"{'='*80}\n")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.close()


if __name__ == "__main__":
    main()
