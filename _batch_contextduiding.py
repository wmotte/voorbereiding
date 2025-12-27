#!/usr/bin/env python3
"""
Batch Contextduiding: Process alle bestaande output folders

Dit script doorloopt alle folders in de output directory en voert
00__contextduiding.py uit voor elke folder (update/aanvullen van analyses).
"""

import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR / "output"
CONTEXTDUIDING_SCRIPT = SCRIPT_DIR / "00__contextduiding.py"

def get_output_folders():
    """Haal alle output folders op, gesorteerd op naam."""
    if not OUTPUT_DIR.exists():
        return []

    folders = [f for f in OUTPUT_DIR.iterdir() if f.is_dir() and not f.name.startswith(".")]
    return sorted(folders, key=lambda x: x.name)

def count_analyses(folder: Path) -> dict:
    """Tel welke analyses al aanwezig zijn in een folder."""
    counts = {"total": 0, "json": 0, "missing": []}

    # Check meta file
    if (folder / "00_meta.json").exists():
        counts["total"] += 1
        counts["json"] += 1

    # Check analyses 01-07
    for num in range(1, 8):
        json_files = list(folder.glob(f"{num:02d}_*.json"))
        if json_files:
            counts["total"] += 1
            counts["json"] += 1
        else:
            counts["missing"].append(f"{num:02d}")

    # Check liedsuggesties
    if list(folder.glob("08b_*.json")):
        counts["total"] += 1
        counts["json"] += 1
    else:
        counts["missing"].append("08b")

    return counts

def main():
    print("\n" + "=" * 60)
    print("BATCH CONTEXTDUIDING - ALLE OUTPUT FOLDERS")
    print("=" * 60)

    folders = get_output_folders()

    if not folders:
        print("❌ Geen output folders gevonden.")
        sys.exit(1)

    print(f"\nGevonden folders: {len(folders)}")
    for i, folder in enumerate(folders, 1):
        stats = count_analyses(folder)
        status = f"{stats['json']} analyses"
        if stats['missing']:
            status += f" (missend: {', '.join(stats['missing'])})"
        print(f"  {i}. {folder.name}")
        print(f"     Status: {status}")

    print("\n" + "-" * 60)
    print("WAARSCHUWING: Dit script voert contextduiding uit op bestaande folders.")
    print("Bestaande analyses worden OVERGESLAGEN, missende worden aangevuld.")
    print("-" * 60)

    response = input("\nWil je alle folders verwerken? [j/N]: ").strip().lower()

    if response not in ['j', 'ja', 'y', 'yes']:
        print("Afgebroken door gebruiker.")
        sys.exit(0)

    print("\n" + "=" * 60)
    print("START BATCH VERWERKING")
    print("=" * 60)

    success_count = 0
    failed_folders = []

    for i, folder in enumerate(folders, 1):
        print(f"\n>>> [{i}/{len(folders)}] Verwerken: {folder.name}")
        print("-" * 60)

        try:
            subprocess.run(
                [sys.executable, str(CONTEXTDUIDING_SCRIPT), "--folder", str(folder)],
                check=True
            )
            success_count += 1
            print(f"✓ Voltooid: {folder.name}")
        except subprocess.CalledProcessError:
            print(f"❌ FOUT bij: {folder.name}")
            failed_folders.append(folder.name)
        except KeyboardInterrupt:
            print("\n\n❌ Batch verwerking afgebroken door gebruiker.")
            print(f"\nVoortgang: {success_count}/{len(folders)} voltooid")
            if failed_folders:
                print(f"Mislukt: {', '.join(failed_folders)}")
            sys.exit(1)

    print("\n" + "=" * 60)
    print("BATCH VERWERKING VOLTOOID")
    print("=" * 60)
    print(f"Succesvol: {success_count}/{len(folders)}")

    if failed_folders:
        print(f"\nMislukte folders:")
        for folder_name in failed_folders:
            print(f"  - {folder_name}")

    print()

if __name__ == "__main__":
    main()
