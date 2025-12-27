#!/usr/bin/env python3
"""
Batch Verdieping: Process alle bestaande output folders

Dit script doorloopt alle folders in de output directory en voert
01__verdieping.py uit voor elke folder.
"""

import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR / "output"
VERDIEPING_SCRIPT = SCRIPT_DIR / "01__verdieping.py"

def get_output_folders():
    """Haal alle output folders op, gesorteerd op naam."""
    if not OUTPUT_DIR.exists():
        return []

    folders = [f for f in OUTPUT_DIR.iterdir() if f.is_dir() and not f.name.startswith(".")]
    return sorted(folders, key=lambda x: x.name)

def main():
    print("\n" + "=" * 60)
    print("BATCH VERDIEPING - ALLE OUTPUT FOLDERS")
    print("=" * 60)

    folders = get_output_folders()

    if not folders:
        print("❌ Geen output folders gevonden.")
        sys.exit(1)

    print(f"\nGevonden folders: {len(folders)}")
    for i, folder in enumerate(folders, 1):
        print(f"  {i}. {folder.name}")

    print("\n" + "-" * 60)
    response = input("Wil je alle folders verwerken? [j/N]: ").strip().lower()

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
                [sys.executable, str(VERDIEPING_SCRIPT), "--folder", str(folder)],
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
