#!/usr/bin/env python3
"""
Start Traject: Preekvoorbereiding

Dit meta-script voert het volledige preekvoorbereidingstraject sequentieel uit:
1. 00__contextduiding.py (Basisanalyses & Liederen)
2. 01__verdieping.py (Exegese, Homiletiek, Gebeden, etc.)

Het detecteert automatisch de aangemaakte output folder en geeft deze door.
"""

import sys
import subprocess
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR / "output"

def get_latest_output_folder() -> Path:
    """Vind de laatst gewijzigde folder in de output directory."""
    if not OUTPUT_DIR.exists():
        return None
    
    folders = [f for f in OUTPUT_DIR.iterdir() if f.is_dir() and not f.name.startswith(".")]
    if not folders:
        return None
        
    return max(folders, key=lambda x: x.stat().st_mtime)

def main():
    print("\n" + "=" * 60)
    print("START PREOPTIEK TRAJECT")
    print("=" * 60)
    
    # STAP 1: CONTEXTDUIDING
    print("\n>>> STAP 1: Contextduiding starten...")
    context_script = SCRIPT_DIR / "00__contextduiding.py"
    
    # We draaien 00 interactief zodat de gebruiker data kan invullen
    try:
        subprocess.run([sys.executable, str(context_script)], check=True)
    except subprocess.CalledProcessError:
        print("\n❌ FOUT: Contextduiding afgebroken.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Traject afgebroken door gebruiker.")
        sys.exit(1)

    # STAP 2: VERDIEPING
    print("\n>>> STAP 2: Verdieping starten...")
    
    # Vind de folder die zojuist is gebruikt door 00__contextduiding.py
    session_file = SCRIPT_DIR / ".last_session_path"
    latest_folder = None
    
    if session_file.exists():
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                path_str = f.read().strip()
                if path_str:
                    latest_folder = Path(path_str)
        except Exception as e:
            print(f"Kon .last_session_path niet lezen: {e}")
            
    # Fallback (hoewel minder betrouwbaar)
    if not latest_folder or not latest_folder.exists():
        print("⚠️  Kon sessiepad niet lezen, probeer op basis van tijdstip...")
        latest_folder = get_latest_output_folder()
    
    if not latest_folder:
        print("❌ FOUT: Geen output folder gevonden na stap 1.")
        sys.exit(1)
        
    print(f"    Gedetecteerde folder: {latest_folder.name}")
    
    verdieping_script = SCRIPT_DIR / "01__verdieping.py"
    
    try:
        # We geven de folder expliciet mee via het nieuwe argument
        subprocess.run([sys.executable, str(verdieping_script), "--folder", str(latest_folder)], check=True)
    except subprocess.CalledProcessError:
        print("\n❌ FOUT: Verdieping afgebroken.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Traject afgebroken door gebruiker.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("TRAJECT VOLTOOID")
    print(f"Resultaten in: {latest_folder}")
    print("=" * 60)

if __name__ == "__main__":
    main()
