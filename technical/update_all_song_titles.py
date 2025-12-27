#!/usr/bin/env python3
"""
Script to update ALL song titles in the hymns database from the official title JSON files.
Run with --dry-run to preview changes without updating (default).
Run with --execute to actually update the database.
"""

import os
import json
import argparse
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
        # Non-Psalmen songs - numbers are integers in JSON but strings in DB
        for song in data:
            if song.get("category") != "Psalmen":
                # Convert to string for matching with database
                title_map[str(song["number"])] = song["title"]

    elif bundel_name == "WeerklankPsalm":
        json_file = SCRIPT_DIR / "song_titles" / "weerklank_titles.json"
        with open(json_file) as f:
            data = json.load(f)
        # Psalmen songs - strip the "P" prefix for matching
        for song in data:
            if song.get("category") == "Psalmen":
                # Song numbers in JSON are like "P1", "P2", etc.
                # Database stores them as "1", "2", etc. (strings)
                number = song["number"]
                if number.startswith("P"):
                    # Store without "P" for matching with database
                    number_without_p = number[1:]
                    title_map[number_without_p] = song["title"]

    return title_map


def update_titles_for_bundel(session, bundel: str, dry_run: bool = True, verbose: bool = True):
    """Update titles for a specific bundel."""
    if verbose:
        print(f"\n{'='*80}")
        print(f"Processing bundel: {bundel}")
        print(f"{'='*80}\n")

    # Load title mappings
    title_map = load_titles(bundel)
    if verbose:
        print(f"Loaded {len(title_map)} titles from JSON for {bundel}")

    # Get songs from database
    query = "MATCH (s:Song {bundel: $bundel}) RETURN s.nummer as nummer, s.titel as titel, s.id as id"
    result = session.run(query, bundel=bundel)
    songs = list(result)

    if verbose:
        print(f"Found {len(songs)} songs in database for {bundel}\n")

    # Track statistics
    matched = 0
    unmatched = 0
    updated = 0
    unchanged = 0
    unmatched_songs = []

    for record in songs:
        nummer = record["nummer"]  # This is a string
        current_title = record["titel"]
        song_id = record["id"]

        # Try to find the correct title
        correct_title = title_map.get(nummer)

        if correct_title is None:
            unmatched += 1
            unmatched_songs.append((nummer, current_title))
            if verbose:
                print(f"⚠️  UNMATCHED: {bundel} #{nummer} - No title found in JSON")
                print(f"   Current title: {current_title}")
            continue

        matched += 1

        # Check if title needs updating
        if current_title == correct_title:
            unchanged += 1
            if verbose and not dry_run:
                print(f"✓ UNCHANGED: {bundel} #{nummer} - '{correct_title}'")
        else:
            updated += 1
            if verbose:
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
                if verbose:
                    print(f"  ✓ Updated to: {updated_title}")

            if verbose:
                print()

    # Print summary
    if verbose:
        print(f"\n{'-'*80}")
        print(f"Summary for {bundel}:")
        print(f"  Total songs processed: {len(songs)}")
        print(f"  Matched: {matched}")
        print(f"  Unmatched: {unmatched}")
        print(f"  Updated: {updated}")
        print(f"  Unchanged: {unchanged}")

        if unmatched_songs and unmatched <= 10:
            print(f"\n  Unmatched songs:")
            for num, title in unmatched_songs:
                print(f"    #{num}: {title}")

        print(f"{'-'*80}\n")

    return {
        "bundel": bundel,
        "total": len(songs),
        "matched": matched,
        "unmatched": unmatched,
        "updated": updated,
        "unchanged": unchanged,
        "unmatched_songs": unmatched_songs
    }


def main():
    """Main function to update song titles."""
    parser = argparse.ArgumentParser(
        description='Update song titles in the hymns database'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually update the database (default is dry-run mode)'
    )
    parser.add_argument(
        '--bundel',
        type=str,
        help='Process only a specific bundel (default: all)',
        choices=['Liedboek', 'Hemelhoog', 'OpToonhoogte', 'Weerklank', 'WeerklankPsalm']
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress detailed output, only show summaries'
    )

    args = parser.parse_args()

    dry_run = not args.execute
    verbose = not args.quiet

    mode = "DRY RUN" if dry_run else "EXECUTE"
    print(f"\n{'='*80}")
    print(f"MODE: {mode}")
    print(f"{'='*80}")

    if dry_run and verbose:
        print("\nRunning in DRY RUN mode - no changes will be made.")
        print("Use --execute to actually update the database.\n")

    print(f"Connecting to {uri}, database={database}...\n")

    driver = GraphDatabase.driver(uri, auth=(username, password))

    # Determine which bundels to process
    bundels = [args.bundel] if args.bundel else [
        "Liedboek",
        "Hemelhoog",
        "OpToonhoogte",
        "Weerklank",
        "WeerklankPsalm"
    ]

    try:
        with driver.session(database=database) as session:
            all_stats = []

            for bundel in bundels:
                stats = update_titles_for_bundel(
                    session,
                    bundel=bundel,
                    dry_run=dry_run,
                    verbose=verbose
                )
                all_stats.append(stats)

            # Print overall summary
            print("\n" + "="*80)
            print("OVERALL SUMMARY")
            print("="*80 + "\n")

            total_all = sum(s["total"] for s in all_stats)
            matched_all = sum(s["matched"] for s in all_stats)
            unmatched_all = sum(s["unmatched"] for s in all_stats)
            updated_all = sum(s["updated"] for s in all_stats)
            unchanged_all = sum(s["unchanged"] for s in all_stats)

            for stats in all_stats:
                print(f"{stats['bundel']:20} - Total: {stats['total']:4}, "
                      f"Matched: {stats['matched']:4}, Unmatched: {stats['unmatched']:4}, "
                      f"Updated: {stats['updated']:4}, Unchanged: {stats['unchanged']:4}")

            print(f"\n{'TOTALS':20} - Total: {total_all:4}, "
                  f"Matched: {matched_all:4}, Unmatched: {unmatched_all:4}, "
                  f"Updated: {updated_all:4}, Unchanged: {unchanged_all:4}")

            print("\n" + "="*80)
            if dry_run:
                print("DRY RUN COMPLETED - No changes were made")
                print("Run with --execute to apply these changes")
            else:
                print("✓ UPDATE COMPLETED")
            print("="*80 + "\n")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.close()


if __name__ == "__main__":
    main()
