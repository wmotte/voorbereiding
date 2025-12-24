#!/usr/bin/env python3
"""
Verdieping: Exegese, Kunst/Cultuur en Homiletiek voor Preekvoorbereiding

Dit script bouwt voort op de basisanalyse van contextduiding.py en voegt toe:
- 07_exegese: Exegetische analyse van de Schriftlezingen
- 08_kunst_cultuur: Kunst, cultuur en film bij de lezingen
- 09_focus_en_functie: Focus en functie van de preek
- 10_kalender: Gedenkdagen en bijzondere momenten
- 11_representatieve_hoorders: Hoordersprofielen
- 12_homiletische_analyse: Homiletische analyse (Lowry's Plot)
- 13_gebeden: Gebeden voor de eredienst

Het leest de output van de vorige analyses (00-06) en gebruikt deze als context.
Voor de exegese worden de bijbelteksten opgehaald van naardensebijbel.nl.

W.M. Otte (w.m.otte@umcutrecht.nl)
"""

import os
import sys
import re
import json
import random
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("FOUT: De nieuwe 'google-genai' library is niet geïnstalleerd.")
    print("Installeer deze met: pip install google-genai")
    sys.exit(1)

try:
    from naardense_bijbel import download_lezingen, laad_bijbelteksten
except ImportError:
    print("FOUT: naardense_bijbel module niet gevonden.")
    print("Zorg dat naardense_bijbel.py in dezelfde directory staat.")
    sys.exit(1)

try:
    from nbv21_bijbel import get_nbv21_lezingen_text, save_nbv21_lezingen
except ImportError:
    print("WAARSCHUWING: nbv21_bijbel module niet gevonden. NBV21 teksten worden niet meegenomen.")
    def get_nbv21_lezingen_text(text): return ""
    def save_nbv21_lezingen(d, t): return {}

try:
    from grondtekst_bijbel import save_grondtekst_lezingen
except ImportError:
    print("WAARSCHUWING: grondtekst_bijbel module niet gevonden.")
    def save_grondtekst_lezingen(f, c): return []

# Configuratie
SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR / "output"
PROMPTS_DIR = SCRIPT_DIR / "prompts"

# Solle constanten
SERMON_MAGIC = b'SOLLE01'
SERMON_VERSION = 1
SERMON_XOR_KEY = b'DorotheeS\xc3\xb6lle1929-2003MystiekEnVerzet'
SERMON_DATA_FILE = SCRIPT_DIR / "solle_sermons.dat"

# Model keuze: Gemini 3 flash als primair, pro als fallback
MODEL_NAME = "gemini-3-flash-preview"
#MODEL_NAME = "gemini-3-pro-preview"
MODEL_NAME_FALLBACK = "gemini-3-pro-preview"


def sample_profetische_gebeden(n: int = 10) -> str:
    """Selecteer willekeurige gebeden uit de voorbeeldmap."""
    examples_dir = SCRIPT_DIR / "gebeden_voorbeeld_profetisch"
    if not examples_dir.exists():
        return "Geen voorbeeldgebeden gevonden."

    files = list(examples_dir.glob("*.json"))
    if not files:
        return "Geen voorbeeldgebeden gevonden."

    selected_files = random.sample(files, min(n, len(files)))
    
    output_parts = []
    for i, file_path in enumerate(selected_files, 1):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                title = data.get("title_nl", "Naamloos")
                text = data.get("text_nl", "")
                if text:
                    output_parts.append(f"### Voorbeeld {i}: {title}\n\n{text}")
        except Exception as e:
            print(f"Fout bij lezen voorbeeld {file_path.name}: {e}")

    return "\n\n".join(output_parts)


def sample_dialogische_gebeden(n: int = 10) -> str:
    """Selecteer willekeurige gebeden uit de voorbeeldmap voor dialogische gebeden."""
    examples_dir = SCRIPT_DIR / "gebeden_voorbeeld_dialogisch"
    if not examples_dir.exists():
        return "Geen voorbeeldgebeden gevonden."

    files = list(examples_dir.glob("*.json"))
    if not files:
        return "Geen voorbeeldgebeden gevonden."

    selected_files = random.sample(files, min(n, len(files)))
    
    output_parts = []
    for i, file_path in enumerate(selected_files, 1):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                title = data.get("title_nl", "Naamloos")
                text = data.get("text_nl", "")
                if text:
                    output_parts.append(f"### Voorbeeld {i}: {title}\n\n{text}")
        except Exception as e:
            print(f"Fout bij lezen voorbeeld {file_path.name}: {e}")

    return "\n\n".join(output_parts)


def sample_jungel_preken(n: int = 5) -> str:
    """Selecteer willekeurige preken uit de Jüngel preken map."""
    jungel_dir = SCRIPT_DIR / "preken_jungel"
    if not jungel_dir.exists():
        return "Geen voorbeeldpreken van Jüngel gevonden."

    files = list(jungel_dir.glob("*.json"))
    if not files:
        return "Geen voorbeeldpreken van Jüngel gevonden."

    selected_files = random.sample(files, min(n, len(files)))

    output_parts = []
    for i, file_path in enumerate(selected_files, 1):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                title = data.get("schriftgedeelte", "Naamloos")
                text = data.get("tekst", "")
                if text:
                    output_parts.append(f"### Voorbeeld {i}: {title}\n\n{text}")
        except Exception as e:
            print(f"Fout bij lezen Jüngel voorbeeld {file_path.name}: {e}")

    return "\n\n".join(output_parts)


def sample_noordmans_preken(n: int = 15) -> str:
    """Selecteer willekeurige fragmenten uit de Noordmans preken map.

    Let op: Dit zijn fragmenten uit Verzamelde Werken deel 8, geen complete preken.
    Ze dienen als inspiratie voor toon, stijl en theologische denkwijze.
    """
    noordmans_dir = SCRIPT_DIR / "preken_noordmans"
    if not noordmans_dir.exists():
        return "Geen voorbeeldfragmenten van Noordmans gevonden."

    files = list(noordmans_dir.glob("*.txt"))
    if not files:
        return "Geen voorbeeldfragmenten van Noordmans gevonden."

    selected_files = random.sample(files, min(n, len(files)))

    output_parts = [
        "**Let op:** De onderstaande teksten zijn fragmenten uit Noordmans' Verzamelde Werken deel 8. "
        "Ze zijn niet compleet maar tonen wel zijn karakteristieke stijl, toon en theologische denkwijze. "
        "Gebruik ze als inspiratie voor de cadans en het taalveld.\n"
    ]

    for i, file_path in enumerate(selected_files, 1):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                # Haal titel uit eerste regels
                lines = text.strip().split("\n")
                title = lines[1] if len(lines) > 1 else file_path.stem
                if text:
                    output_parts.append(f"### Fragment {i}: {title}\n\n{text}")
        except Exception as e:
            print(f"Fout bij lezen Noordmans fragment {file_path.name}: {e}")

    return "\n\n".join(output_parts)


def _xor_bytes(data: bytes, key: bytes) -> bytes:
    """Apply XOR operation to data with key."""
    key_len = len(key)
    return bytes(b ^ key[i % key_len] for i, b in enumerate(data))


def _load_sermons_from_binary(binary_file: Path) -> list[dict]:
    """Load all sermons from the binary data file."""
    import struct
    import zlib
    sermons = []

    if not binary_file.exists():
        return sermons

    try:
        with open(binary_file, 'rb') as f:
            # Read and verify header
            magic = f.read(len(SERMON_MAGIC))
            if magic != SERMON_MAGIC:
                return sermons

            version = struct.unpack('<B', f.read(1))[0]
            if version != SERMON_VERSION:
                return sermons

            count = struct.unpack('<H', f.read(2))[0]

            # Read each sermon
            for _ in range(count):
                length = struct.unpack('<I', f.read(4))[0]
                obfuscated = f.read(length)
                compressed = _xor_bytes(obfuscated, SERMON_XOR_KEY)
                json_bytes = zlib.decompress(compressed)
                sermon = json.loads(json_bytes.decode('utf-8'))
                sermons.append(sermon)
    except Exception as e:
        print(f"Fout bij inladen Sölle preken: {e}")

    return sermons


def sample_solle_preken(n: int = 5) -> str:
    """Selecteer willekeurige preken uit het binaire bestand."""
    all_sermons = _load_sermons_from_binary(SERMON_DATA_FILE)
    if not all_sermons:
        return "Geen voorbeeldpreken van Sölle gevonden."

    selected = random.sample(all_sermons, min(n, len(all_sermons)))
    
    output_parts = []
    for i, data in enumerate(selected, 1):
        title = data.get("title", "Naamloos")
        scripture = data.get("scripture", "")
        text = data.get("text", "")
        if text:
            output_parts.append(f"### Voorbeeld {i}: {title} ({scripture})\n\n{text}")

    return "\n\n".join(output_parts)


def load_prompt(filename: str, user_input: dict, extra_replacements: dict = None) -> str:
    """Laad een prompt uit een markdown bestand en vervang placeholders."""
    filepath = PROMPTS_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Prompt bestand niet gevonden: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Huidige datum in Nederlands formaat
    huidige_datum = datetime.now().strftime("%d %B %Y")
    # Vertaal Engelse maandnamen naar Nederlands
    maanden_nl = {
        'January': 'januari', 'February': 'februari', 'March': 'maart',
        'April': 'april', 'May': 'mei', 'June': 'juni',
        'July': 'juli', 'August': 'augustus', 'September': 'september',
        'October': 'oktober', 'November': 'november', 'December': 'december'
    }
    for en, nl in maanden_nl.items():
        huidige_datum = huidige_datum.replace(en, nl)

    content = content.replace("{{plaatsnaam}}", user_input.get("plaatsnaam", ""))
    content = content.replace("{{gemeente}}", user_input.get("gemeente", ""))
    content = content.replace("{{datum}}", user_input.get("datum", ""))
    content = content.replace("{{huidige_datum}}", huidige_datum)

    if extra_replacements:
        for key, value in extra_replacements.items():
            content = content.replace(f"{{{{{key}}}}}", value)

    return content


def list_output_folders() -> list[Path]:
    """Lijst alle beschikbare output folders."""
    if not OUTPUT_DIR.exists():
        return []

    folders = []
    for item in OUTPUT_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            # Controleer of er een geldige analyse folder is
            if ((item / "01_zondag_kerkelijk_jaar.json").exists() or
                (item / "00_meta.json").exists() or
                (item / "00_zondag_kerkelijk_jaar.json").exists()): # Backwards compat
                folders.append(item)

    return sorted(folders, key=lambda x: x.stat().st_mtime, reverse=True)


def select_folder() -> Path:
    """Laat de gebruiker een output folder kiezen."""
    folders = list_output_folders()

    if not folders:
        print("\nFOUT: Geen output folders gevonden met basisanalyses.")
        print("Voer eerst contextduiding.py uit om basisanalyses te genereren.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("VERDIEPING: EXEGESE EN KUNST/CULTUUR (JSON OUTPUT)")
    print("=" * 60)
    print("\nBeschikbare analyses:\n")

    for i, folder in enumerate(folders, 1):
        # Tel bestaande analyses (check both JSON and MD)
        existing = []
        for num in range(15):
            json_pattern = f"{num:02d}_*.json"
            md_pattern = f"{num:02d}_*.md"
            if list(folder.glob(json_pattern)):
                existing.append(f"{num:02d}")
            elif list(folder.glob(md_pattern)):
                existing.append(f"{num:02d}(md)")

        print(f"  {i}. {folder.name}")
        print(f"     Analyses: {', '.join(existing)}")

    print()
    while True:
        try:
            choice = input("Kies een nummer (of 'q' om te stoppen): ").strip()
            if choice.lower() == 'q':
                sys.exit(0)
            idx = int(choice) - 1
            if 0 <= idx < len(folders):
                return folders[idx]
            print("Ongeldig nummer, probeer opnieuw.")
        except ValueError:
            print("Voer een geldig nummer in.")


def read_previous_analyses(folder: Path) -> dict:
    """Lees alle vorige analyses uit de folder (JSON of MD) en stript de _meta data."""
    analyses = {}

    # Bestanden die we willen lezen (basis naam zonder extensie)
    # Mapping van nieuwe structuur (01-07) en oude structuur (00-06)
    files_to_read = [
        ("01_zondag_kerkelijk_jaar", "liturgische_context"),
        ("02_sociaal_maatschappelijke_context", "sociaal_maatschappelijk"),
        ("03_waardenorientatie", "waardenorientatie"),
        ("04_geloofsorientatie", "geloofsorientatie"),
        ("05_interpretatieve_synthese", "synthese"),
        ("06_actueel_wereldnieuws", "wereldnieuws"),
        ("07_politieke_orientatie", "politieke_orientatie"),
        ("08_exegese", "exegese"),
        ("09_kunst_cultuur", "kunst_cultuur"),
        ("10_focus_en_functie", "focus_en_functie"),
        ("11_kalender", "kalender"),
        ("12_representatieve_hoorders", "representatieve_hoorders"),
        ("13_homiletische_analyse", "homiletische_analyse"),
        ("13_homiletische_analyse_buttrick", "homiletische_analyse_buttrick"),
        ("14_gebeden", "gebeden"),
        ("15_kindermoment", "kindermoment"),
    ]

    # Backwards compatibility check
    old_files_to_read = [
        ("00_zondag_kerkelijk_jaar", "liturgische_context"),
        ("01_sociaal_maatschappelijke_context", "sociaal_maatschappelijk"),
        ("02_waardenorientatie", "waardenorientatie"),
        ("03_geloofsorientatie", "geloofsorientatie"),
        ("04_interpretatieve_synthese", "synthese"),
        ("05_actueel_wereldnieuws", "wereldnieuws"),
        ("06_politieke_orientatie", "politieke_orientatie"),
        ("07_exegese", "exegese"),
        ("08_kunst_cultuur", "kunst_cultuur"),
        ("09_focus_en_functie", "focus_en_functie"),
        ("10_kalender", "kalender"),
        ("11_representatieve_hoorders", "representatieve_hoorders"),
        ("12_homiletische_analyse", "homiletische_analyse"),
        ("13_gebeden", "gebeden"),
    ]

    for basename, key in files_to_read:
        filepath_json = folder / f"{basename}.json"
        
        # Probeer nieuwe naam
        if filepath_json.exists():
            with open(filepath_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Verwijder de _meta key om tokens te besparen
            if "_meta" in data:
                del data["_meta"]
            analyses[key] = json.dumps(data, ensure_ascii=False, indent=2)
            continue
            
        # Probeer oude naam (backwards compat)
        old_basename = next((old for old, k in old_files_to_read if k == key), None)
        if old_basename:
             old_json = folder / f"{old_basename}.json"
             old_md = folder / f"{old_basename}.md"
             if old_json.exists():
                with open(old_json, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Verwijder de _meta key om tokens te besparen
                if "_meta" in data:
                    del data["_meta"]
                analyses[key] = json.dumps(data, ensure_ascii=False, indent=2)
             elif old_md.exists():
                with open(old_md, "r", encoding="utf-8") as f:
                    analyses[key] = f.read()
             else:
                analyses[key] = ""
        else:
            analyses[key] = ""

    return analyses


def extract_user_input_from_folder(folder: Path) -> dict:
    """Probeer plaatsnaam, gemeente en datum te extraheren uit bestanden of foldernaam."""
    user_input = {"plaatsnaam": "", "gemeente": "", "datum": "", "adres": "", "website": ""}

    # 1. Check specifieke meta file (Nieuwste standaard)
    meta_file = folder / "00_meta.json"
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for key in user_input:
                    if data.get(key):
                        user_input[key] = data[key]
                return user_input
        except (json.JSONDecodeError, KeyError):
            pass

    # 2. Zoek in alle JSON bestanden naar _meta.user_input (meest betrouwbaar)
    for json_path in sorted(folder.glob("*.json")):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            meta_input = data.get("_meta", {}).get("user_input")
            if meta_input:
                # Update onze dict met gevonden waarden, maar behoud wat we al hebben als het leger is
                for key in user_input:
                    if meta_input.get(key):
                        user_input[key] = meta_input[key]
                
                # Als we de belangrijkste velden hebben, kunnen we stoppen
                if user_input["plaatsnaam"] and user_input["adres"]:
                    return user_input
        except (json.JSONDecodeError, KeyError):
            continue

    # 2. Fallback: probeer uit 00_overzicht.json (Oud formaat)
    overzicht_json = folder / "00_overzicht.json"
    if overzicht_json.exists():
        try:
            with open(overzicht_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            gegevens = data.get("gegevens", {})
            user_input["plaatsnaam"] = gegevens.get("plaatsnaam", "")
            user_input["gemeente"] = gegevens.get("gemeente", "")
            user_input["datum"] = gegevens.get("datum_preek", "")
            if user_input["plaatsnaam"]:
                return user_input
        except (json.JSONDecodeError, KeyError):
            pass

    # 3. Fallback: probeer uit MD overzicht
    overzicht_md = folder / "00_overzicht.md"
    if overzicht_md.exists():
        with open(overzicht_md, "r", encoding="utf-8") as f:
            content = f.read()

        for line in content.split("\n"):
            if "**Plaatsnaam:**" in line:
                user_input["plaatsnaam"] = line.split("**Plaatsnaam:**")[-1].strip()
            elif "**Gemeente:**" in line:
                user_input["gemeente"] = line.split("**Gemeente:**")[-1].strip()
            elif "**Datum" in line:
                parts = line.split(":**")
                if len(parts) > 1:
                    user_input["datum"] = parts[-1].strip()

    # 4. Fallback: gebruik foldernaam
    if not user_input["plaatsnaam"]:
        # Split op underscores en filter lege strings
        parts = [p for p in folder.name.split("_") if p]
        
        if len(parts) >= 6:
            content_parts = parts[:-2] 
            datum_parts = content_parts[-3:]
            user_input["datum"] = " ".join(datum_parts)
            plaats_parts = content_parts[:-3]
            user_input["plaatsnaam"] = " ".join(plaats_parts)
        elif len(parts) > 0:
            user_input["plaatsnaam"] = parts[0]

    return user_input


def load_bible_context_as_json(folder: Path) -> str:
    """
    Lees alle gedownloade bijbelteksten (NB en NBV21) uit de bijbelteksten map
    en retourneer deze als een geformatteerde JSON string.
    """
    bijbel_dir = folder / "bijbelteksten"
    if not bijbel_dir.exists():
        return ""

    context_data = {
        "naardense_bijbel": [],
        "nbv21": []
    }

    # Lees Naardense Bijbel bestanden
    for json_file in sorted(bijbel_dir.glob("*_NB.json")):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                context_data["naardense_bijbel"].append(data)
        except Exception as e:
            print(f"Fout bij lezen {json_file}: {e}")

    # Lees NBV21 bestanden
    for json_file in sorted(bijbel_dir.glob("*_NBV21.json")):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                context_data["nbv21"].append(data)
        except Exception as e:
            print(f"Fout bij lezen {json_file}: {e}")

    # Lees Grondtekst bestanden
    context_data["grondtekst"] = []
    for json_file in sorted(bijbel_dir.glob("*_Grondtekst.json")):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                context_data["grondtekst"].append(data)
        except Exception as e:
            print(f"Fout bij lezen {json_file}: {e}")

    # Als alles leeg is, retourneer lege string
    if not context_data["naardense_bijbel"] and not context_data["nbv21"] and not context_data["grondtekst"]:
        return ""

    return json.dumps(context_data, ensure_ascii=False, indent=2)


def get_gemini_client() -> genai.Client:
    """Initialiseer de Gemini Client."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        print("\nFOUT: Geen API key gevonden.")
        print("Stel de GEMINI_API_KEY environment variable in.")
        sys.exit(1)

    return genai.Client(api_key=api_key)


def build_context_string(previous_analyses: dict, limited: bool = False, excluded_sections: list = None) -> str:
    """Bouw een context string van vorige analyses.

    Args:
        previous_analyses: Dictionary met alle analyses
        limited: Als True, alleen sociaal-maatschappelijke context voor hoordersprofielen
        excluded_sections: Lijst met sleutels die uitgesloten moeten worden (bv. 'kunst_cultuur')
    """
    if excluded_sections is None:
        excluded_sections = []

    sections = []

    if previous_analyses.get("liturgische_context"):
        sections.append("## Liturgische Context en Schriftlezingen\n\n" +
                       previous_analyses["liturgische_context"])

    if previous_analyses.get("sociaal_maatschappelijk"):
        sections.append("## Sociaal-Maatschappelijke Context\n\n" +
                       previous_analyses["sociaal_maatschappelijk"])

    if previous_analyses.get("waardenorientatie"):
        sections.append("## Waardenoriëntatie\n\n" +
                       previous_analyses["waardenorientatie"])

    if previous_analyses.get("geloofsorientatie"):
        sections.append("## Geloofsoriëntatie\n\n" +
                       previous_analyses["geloofsorientatie"])

    if previous_analyses.get("synthese"):
        sections.append("## Interpretatieve Synthese\n\n" +
                       previous_analyses["synthese"])

    # Voor hoordersprofielen stoppen we hier - exegese, kunst, kalender etc. niet nodig
    if limited:
        return "\n\n---\n\n".join(sections)

    if previous_analyses.get("wereldnieuws") and "wereldnieuws" not in excluded_sections:
        sections.append("## Actueel Wereldnieuws\n\n" +
                       previous_analyses["wereldnieuws"])

    if previous_analyses.get("politieke_orientatie") and "politieke_orientatie" not in excluded_sections:
        sections.append("## Politieke Oriëntatie\n\n" +
                       previous_analyses["politieke_orientatie"])

    if previous_analyses.get("exegese") and "exegese" not in excluded_sections:
        sections.append("## Exegese\n\n" +
                       previous_analyses["exegese"])

    if previous_analyses.get("kunst_cultuur") and "kunst_cultuur" not in excluded_sections:
        sections.append("## Kunst & Cultuur\n\n" +
                       previous_analyses["kunst_cultuur"])

    if previous_analyses.get("focus_en_functie") and "focus_en_functie" not in excluded_sections:
        sections.append("## Focus en Functie\n\n" +
                       previous_analyses["focus_en_functie"])

    if previous_analyses.get("kalender") and "kalender" not in excluded_sections:
        sections.append("## Kalender\n\n" +
                       previous_analyses["kalender"])

    if previous_analyses.get("representatieve_hoorders") and "representatieve_hoorders" not in excluded_sections:
        sections.append("## Representatieve Hoorders\n\n" +
                       previous_analyses["representatieve_hoorders"])

    if previous_analyses.get("homiletische_analyse") and "homiletische_analyse" not in excluded_sections:
        sections.append("## Homiletische Analyse (Lowry)\n\n" +
                       previous_analyses["homiletische_analyse"])

    if previous_analyses.get("homiletische_analyse_buttrick") and "homiletische_analyse_buttrick" not in excluded_sections:
        sections.append("## Homiletische Analyse (Buttrick)\n\n" +
                       previous_analyses["homiletische_analyse_buttrick"])

    if previous_analyses.get("gebeden") and "gebeden" not in excluded_sections:
        sections.append("## Gebeden\n\n" +
                       previous_analyses["gebeden"])

    return "\n\n---\n\n".join(sections)


def extract_json(text: str) -> dict:
    """Extraheer JSON uit de response, ook als deze in markdown is gewrapt."""
    # Probeer eerst direct te parsen
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Probeer JSON uit markdown code block te halen
    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Probeer JSON te vinden tussen { en }
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    # Als niets werkt, return error object
    return {"error": "Kon geen valide JSON extraheren", "raw_response": text[:1000]}


def run_analysis(client: genai.Client, prompt: str, title: str, temperature: float = 0.2, model: str = None) -> dict:
    """Voer een analyse uit met Gemini en Google Search. Retourneert JSON dict.

    Args:
        client: De Gemini client
        prompt: De prompt voor het model
        title: Titel van de analyse (voor logging)
        temperature: Temperatuur voor het model
        model: Model om te gebruiken (default: MODEL_NAME, fallback naar MODEL_NAME_FALLBACK)
    """
    current_model = model or MODEL_NAME

    print(f"\n{'─' * 50}")
    print(f"Analyseren: {title}")
    print(f"{'─' * 50}")

    max_retries = 2  # 3 pogingen totaal met flash
    for attempt in range(max_retries + 1):
        if attempt > 0:
            print(f"Poging {attempt + 1}/{max_retries + 1} ({current_model})...")
        else:
            print(f"Bezig met redeneren en zoeken ({current_model})...")

        try:
            response = client.models.generate_content(
                model=current_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    top_p=0.90,
                    top_k=30,
                    max_output_tokens=32768,
                    tools=[types.Tool(
                        google_search=types.GoogleSearch()
                    )],
                    safety_settings=[
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                    ]
                )
            )

            if response.text:
                result = extract_json(response.text)
                if "error" in result:
                    print(f"⚠ Analyse '{title}' voltooid maar JSON parsing mislukt (poging {attempt + 1})")
                    if attempt < max_retries:
                        continue
                else:
                    print(f"✓ Analyse '{title}' voltooid (valide JSON)")
                    return result
            else:
                print(f"✗ Geen tekst ontvangen voor '{title}' (poging {attempt + 1})")
                if attempt < max_retries:
                    continue

        except Exception as e:
            error_msg = f"Fout bij analyse '{title}': {str(e)}"
            print(f"✗ {error_msg}")
            if attempt < max_retries:
                continue

    # Als alle retries met huidige model mislukt zijn, probeer fallback model
    if current_model == MODEL_NAME and MODEL_NAME_FALLBACK:
        print(f"\n⚠ Alle pogingen met {MODEL_NAME} mislukt. Fallback naar {MODEL_NAME_FALLBACK}...")
        return run_analysis(client, prompt, title, temperature=temperature, model=MODEL_NAME_FALLBACK)

    # Als ook fallback mislukt, return error
    return {"error": f"Analyse mislukt na herpogingen (inclusief fallback)", "title": title}


def verify_kunst_cultuur(client: genai.Client, content: dict) -> dict:
    """Verificeer alle bronnen in de kunst/cultuur output en verwijder niet-verifieerbare items."""
    print(f"\n{'─' * 50}")
    print("VERIFICATIE: Bronnen controleren...")
    print(f"{'─' * 50}")
    print("Bezig met verifiëren van films, boeken en kunstwerken...")

    content_str = json.dumps(content, ensure_ascii=False, indent=2)

    # Voeg een limiet toe aan de grootte van de content om timeouts te voorkomen
    if len(content_str) > 100000:  # ~100KB limiet
        print("⚠ Content te groot voor verificatie - limiteren tot 100KB")
        content_str = content_str[:100000] + "\n\n... [inhoud ingekort voor verificatie]"

    verification_prompt = """Je bent een strenge factchecker. Je taak is om de onderstaande JSON te controleren op duidelijk niet-bestaande bronnen.

## Instructies

1. Doorloop ELKE genoemde film, boek, kunstwerk, muziekstuk en andere culturele verwijzing
2. Verifieer via Google Search of deze ECHT BESTAAT:
   - Bij films: controleer of de film bestaat met die titel, regisseur en jaar
   - Bij boeken: controleer of het boek bestaat met die auteur en titel
   - Bij kunstwerken: controleer of het kunstwerk bestaat van die kunstenaar
   - Bij muziek: controleer of het stuk bestaat van die componist/artiest

3. Als je een item duidelijk NIET kunt verifiëren (duidelijk verzonnen, niet gevonden):
   - Verwijder het HELE object uit de array
   - Laat geen lege arrays achter als alle items verwijderd zijn

4. Als je een item WEL kunt verifiëren maar details kloppen niet:
   - Corrigeer de details (bijv. verkeerd jaar, verkeerde regisseur)

5. Behoud de originele JSON structuur

## BELANGRIJK
- Wees STRENG: bij twijfel, verwijderen (liever 3 geverifieerde items dan 6 waarvan er 2 niet bestaan)
- Concentreer je op duidelijke hallucinaties (compleet verzonnen items)
- Retourneer ALLEEN valide JSON, geen markdown of toelichting
- Begin DIRECT met de JSON, geen inleiding

## Te controleren JSON:

"""

    max_retries = 3
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=verification_prompt + content_str,
                config=types.GenerateContentConfig(
                    temperature=0.1,  # Zeer laag voor maximale precisie
                    top_p=0.85,
                    top_k=20,
                    max_output_tokens=32768,
                    # Verlaag de timeout parameters om te voorkomen dat het proces te lang duurt
                    response_mime_type="application/json",
                    tools=[types.Tool(
                        google_search=types.GoogleSearch()
                    )],
                    safety_settings=[
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                    ]
                )
            )

            if response.text:
                verified = extract_json(response.text)
                if "error" not in verified:
                    print("✓ Verificatie voltooid - niet-verifieerbare items verwijderd")
                    return verified
                else:
                    print(f"⚠ Verificatie parsing mislukt (poging {attempt + 1})")
                    if attempt < max_retries:
                        continue
            else:
                print(f"✗ Verificatie mislukt (geen text) (poging {attempt + 1})")
                if attempt < max_retries:
                    continue

        except Exception as e:
            print(f"✗ Verificatie fout: {str(e)} (poging {attempt + 1})")
            import traceback
            print(f"  Volledige foutstack: {traceback.format_exc()}")
            if attempt < max_retries:
                print(f"  Wachten 5 seconden voor volgende poging...")
                import time
                time.sleep(5)  # Wacht 5 seconden tussen pogingen
                continue

    # Als alles mislukt, retourneer originele content
    print("⚠ Verificatie volledig mislukt - originele data behouden")
    return content


def save_analysis(output_dir: Path, filename: str, content: dict, title: str, user_input: dict = None):
    """Sla een analyse op naar een JSON bestand."""
    filepath = output_dir / f"{filename}.json"

    # Voeg metadata toe
    meta = {
        "title": title,
        "filename": filename,
        "generated_at": datetime.now().isoformat()
    }

    if user_input:
        meta["user_input"] = user_input

    content_with_meta = {
        "_meta": meta,
        **content
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(content_with_meta, f, ensure_ascii=False, indent=2)

    print(f"  Opgeslagen: {filepath.name}")


def save_log(logs_dir: Path, filename: str, content: str):
    """Sla de volledige prompt op in een logbestand."""
    filepath = logs_dir / f"{filename}.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Log opgeslagen: logs/{filepath.name}")


def update_summary(output_dir: Path):
    """Update het overzichtsbestand met de nieuwe analyses."""
    # Update JSON overzicht
    overzicht_json_path = output_dir / "00_overzicht.json"
    if overzicht_json_path.exists():
        try:
            with open(overzicht_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            new_analyses = [
                ("08_exegese", "Exegese van de Schriftlezingen"),
                ("09_kunst_cultuur", "Kunst, Cultuur en Film"),
                ("10_focus_en_functie", "Focus en Functie"),
                ("11_kalender", "Kalender"),
                ("12_representatieve_hoorders", "Representatieve Hoorders"),
                ("13_homiletische_analyse", "Homiletische Analyse (Lowry's Plot)"),
                ("13_homiletische_analyse_buttrick", "Homiletische Analyse (Buttrick's Moves & Structures)"),
                ("14_gebeden", "Gebeden voor de Eredienst"),
                ("14_gebeden_profetisch", "Profetische Gebeden (Brueggemann)"),
                ("14_gebeden_dialogisch", "Dialogische Gebeden (Dumas)"),
                ("14_gebeden_eenvoudig", "Eenvoudige Gebeden (B1-niveau)"),
                ("15_kindermoment", "Kindermoment"),
                ("16_preek_solle", "Preek in de stijl van Sölle"),
                ("17_preek_jungel", "Preek in de stijl van Jüngel"),
                ("18_preek_noordmans", "Preekschets in de stijl van Noordmans"),
            ]

            existing_names = [a.get("name") for a in data.get("analyses", [])]
            for name, title in new_analyses:
                if (output_dir / f"{name}.json").exists() and name not in existing_names:
                    data.setdefault("analyses", []).append({
                        "name": name,
                        "title": title,
                        "file": f"{name}.json"
                    })

            with open(overzicht_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except (json.JSONDecodeError, KeyError):
            pass

    # Update MD overzicht
    overzicht_md_path = output_dir / "00_overzicht.md"
    if overzicht_md_path.exists():
        with open(overzicht_md_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_analyses = [
            ("08_exegese", "Exegese van de Schriftlezingen"),
            ("09_kunst_cultuur", "Kunst, Cultuur en Film"),
            ("10_focus_en_functie", "Focus en Functie"),
            ("11_kalender", "Kalender"),
            ("12_representatieve_hoorders", "Representatieve Hoorders"),
            ("13_homiletische_analyse", "Homiletische Analyse (Lowry's Plot)"),
            ("13_homiletische_analyse_buttrick", "Homiletische Analyse (Buttrick's Moves & Structures)"),
                            ("14_gebeden", "Gebeden voor de Eredienst"),
                            ("14_gebeden_profetisch", "Profetische Gebeden (Brueggemann)"),
                            ("14_gebeden_dialogisch", "Dialogische Gebeden (Dumas)"),
                            ("14_gebeden_eenvoudig", "Eenvoudige Gebeden (B1-niveau)"),
                            ("15_kindermoment", "Kindermoment"),            ("16_preek_solle", "Preek in de stijl van Sölle"),
            ("17_preek_jungel", "Preek in de stijl van Jüngel"),
            ("18_preek_noordmans", "Preekschets in de stijl van Noordmans"),
        ]

        for name, title in new_analyses:
            # Check for JSON file first, then MD
            if (output_dir / f"{name}.json").exists() and f"[{title}]" not in content:
                if "## Analyses" in content:
                    content = content.rstrip()
                    content += f"\n- [{title}]({name}.json)\n"
            elif (output_dir / f"{name}.md").exists() and f"[{title}]" not in content:
                if "## Analyses" in content:
                    content = content.rstrip()
                    content += f"\n- [{title}]({name}.md)\n"

        with open(overzicht_md_path, "w", encoding="utf-8") as f:
            f.write(content)


def main():
    """Hoofdfunctie."""
    parser = argparse.ArgumentParser(description="Verdieping: Exegese, Kunst/Cultuur en Homiletiek")
    parser.add_argument("--exegese", action="store_true", help="Voer alleen de exegese analyse uit")
    args = parser.parse_args()

    # Laad environment variables uit .env
    env_file = SCRIPT_DIR / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"\'')

    # Selecteer folder
    folder = select_folder()
    print(f"\nGeselecteerd: {folder.name}")

    # Lees vorige analyses
    print("\nVorige analyses laden...")
    previous_analyses = read_previous_analyses(folder)
    user_input = extract_user_input_from_folder(folder)

    print(f"  Plaatsnaam: {user_input['plaatsnaam']}")
    print(f"  Gemeente: {user_input['gemeente']}")
    print(f"  Datum: {user_input['datum']}")

    # Controleer of liturgische context aanwezig is
    if not previous_analyses.get("liturgische_context"):
        print("\nFOUT: Geen liturgische context gevonden (00_zondag_kerkelijk_jaar.md)")
        print("Deze is nodig voor de exegese en kunst/cultuur analyse.")
        sys.exit(1)

    # Download bijbelteksten van de Naardense Bijbel
    print("\n" + "─" * 50)
    print("BIJBELTEKSTEN OPHALEN")
    print("─" * 50)

    # Controleer eerst of er al bijbelteksten bestaan
    bijbel_dir = folder / "bijbelteksten"
    nb_files = list(bijbel_dir.glob("*_NB.json")) if bijbel_dir.exists() else []
    nbv21_files = list(bijbel_dir.glob("*_NBV21.json")) if bijbel_dir.exists() else []
    grondtekst_files = list(bijbel_dir.glob("*_Grondtekst.json")) if bijbel_dir.exists() else []

    if nb_files:
        print(f"\n! {len(nb_files)} Naardense Bijbel bestanden gevonden, overslaan download")
        bijbelteksten_map = {str(f): str(f) for f in nb_files}  # Simulate result
    else:
        bijbelteksten_map = download_lezingen(folder, previous_analyses["liturgische_context"])
        if bijbelteksten_map:
            print(f"✓ {len(bijbelteksten_map)} bijbeltekst(en) opgehaald en opgeslagen")
        else:
            print("\n! Geen bijbelteksten kunnen ophalen (exegese gaat door zonder grondtekst)")

    # Controleer of NBV21 bestanden al bestaan
    if nbv21_files:
        print(f"! {len(nbv21_files)} NBV21 bestanden gevonden, overslaan download")
    else:
        # Haal NBV21 teksten op en sla ze op
        # We hoeven de return value (tekst) niet te gebruiken, want we lezen straks de JSONs
        nbv21_files = save_nbv21_lezingen(folder, previous_analyses["liturgische_context"])

        if nbv21_files:
            print(f"✓ NBV21 teksten opgehaald en opgeslagen ({len(nbv21_files)} bestanden)")

    # Controleer of Grondtekst bestanden al bestaan
    if grondtekst_files:
        print(f"! {len(grondtekst_files)} Grondtekst bestanden gevonden, overslaan download")
    else:
        # Haal Grondtekst (BHS/NA28) op en sla ze op
        grondtekst_files = save_grondtekst_lezingen(folder, previous_analyses["liturgische_context"])

        if grondtekst_files:
            print(f"✓ Grondteksten (BHS/NA28) opgehaald en opgeslagen ({len(grondtekst_files)} bestanden)")

    # Initialiseer client
    print("\nGoogle GenAI Client initialiseren...")
    client = get_gemini_client()

    # LOGS DIRECTORY AANMAKEN
    LOGS_DIR = folder / "logs"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Bouw context (inclusief bijbelteksten)
    context_string = build_context_string(previous_analyses)

    # Laad bijbelteksten als JSON en voeg toe aan context
    bible_json_context = load_bible_context_as_json(folder)
    
    if bible_json_context:
        context_string += f"""

---

## Bijbelteksten (Bronmateriaal)

De volgende bijbelteksten zijn beschikbaar voor exegese (in JSON formaat):

```json
{bible_json_context}
```
"""

    # Laad prompts
    base_prompt = load_prompt("base_prompt_verdieping.md", user_input)

    # Analyses uitvoeren
    print("\n" + "=" * 60)
    print(f"VERDIEPING STARTEN MET MODEL: {MODEL_NAME}")
    print("=" * 60)

    analysis_definitions = [
        ("08_exegese", "Exegese van de Schriftlezingen"),
        ("09_kunst_cultuur", "Kunst, Cultuur en Film"),
        ("10_focus_en_functie", "Focus en Functie"),
        ("11_kalender", "Kalender: Gedenkdagen en Bijzondere Momenten"),
        ("12_representatieve_hoorders", "Representatieve Hoorders"),
        ("13_homiletische_analyse", "Homiletische Analyse (Lowry's Plot)"),
        ("13_homiletische_analyse_buttrick", "Homiletische Analyse (Buttrick's Moves & Structures)"),
        ("14_gebeden", "Gebeden voor de Eredienst"),
        ("14_gebeden_profetisch", "Profetische Gebeden (Brueggemann)"),
        ("14_gebeden_dialogisch", "Dialogische Gebeden (Dumas)"),
        ("14_gebeden_eenvoudig", "Eenvoudige Gebeden (B1-niveau)"),
        ("15_kindermoment", "Kindermoment"),
        ("16_preek_solle", "Preek in de stijl van Sölle"),
        ("17_preek_jungel", "Preek in de stijl van Jüngel"),
        ("18_preek_noordmans", "Preekschets in de stijl van Noordmans"),
    ]

    if args.exegese:
        print("\nINFO: Alleen exegese wordt uitgevoerd (--exegese)")
        analysis_definitions = [x for x in analysis_definitions if x[0] == "08_exegese"]

    # Mapping van oude naar nieuwe bestandsnamen (voor backwards compatibility)
    old_to_new = {
        "08_exegese": "07_exegese",
        "09_kunst_cultuur": "08_kunst_cultuur",
        "10_focus_en_functie": "09_focus_en_functie",
        "11_kalender": "10_kalender",
        "12_representatieve_hoorders": "11_representatieve_hoorders",
        "13_homiletische_analyse": "12_homiletische_analyse",
        "14_gebeden": "13_gebeden",
    }

    for name, title in analysis_definitions:
        # Controleer of analyse al bestaat (JSON of MD, nieuwe of oude nummering)
        existing_file = None
        if (folder / f"{name}.json").exists():
            existing_file = f"{name}.json"
        elif (folder / f"{name}.md").exists():
            existing_file = f"{name}.md (oud formaat)"
        # Check ook oude naam (bijv. 07_exegese.json)
        elif name in old_to_new:
             old_name = old_to_new[name]
             if (folder / f"{old_name}.json").exists():
                 existing_file = f"{old_name}.json (oud nummer)"
             elif (folder / f"{old_name}.md").exists():
                 existing_file = f"{old_name}.md (oud formaat)"

        if existing_file:
            overwrite = input(f"\n{existing_file} bestaat al. Overschrijven als JSON met nieuwe naam? (j/n): ").strip().lower()
            if overwrite != 'j':
                print(f"  Overgeslagen: {name}")
                continue

        # Bereid extra replacements voor
        extra_replacements = {}
        if name == "14_gebeden_profetisch":
            print("  Willekeurige voorbeeldgebeden selecteren...")
            extra_replacements["voorbeeld_gebeden"] = sample_profetische_gebeden()
        elif name == "14_gebeden_dialogisch":
            print("  Willekeurige dialogische voorbeeldgebeden selecteren...")
            extra_replacements["voorbeeld_gebeden"] = sample_dialogische_gebeden()
        elif name == "16_preek_solle":
            print("  Willekeurige voorbeeldpreken van Sölle selecteren...")
            extra_replacements["voorbeeld_gebeden"] = sample_solle_preken()
        elif name == "17_preek_jungel":
            print("  Willekeurige voorbeeldpreken van Jüngel selecteren...")
            extra_replacements["voorbeeld_gebeden"] = sample_jungel_preken()
        elif name == "18_preek_noordmans":
            print("  Willekeurige voorbeeldpreken van Noordmans selecteren...")
            extra_replacements["voorbeeld_gebeden"] = sample_noordmans_preken()

        # Bouw prompt
        task_prompt = load_prompt(f"{name}.md", user_input, extra_replacements)

        # Context bepalen
        if name == "12_representatieve_hoorders":
            analysis_context = build_context_string(previous_analyses, limited=True)
        elif name.startswith("14_gebeden"):
            # Voor gebeden: geen kunst/cultuur, kalender, hoorders
            analysis_context = build_context_string(
                previous_analyses, 
                excluded_sections=["kunst_cultuur", "kalender", "representatieve_hoorders"]
            )
        else:
            analysis_context = context_string

        # Voor gebeden: maskeer adres om letterlijk gebruik te voorkomen
        display_adres = user_input.get('adres') or 'Onbekend'
        if name in ["14_gebeden", "14_gebeden_profetisch", "14_gebeden_dialogisch", "14_gebeden_eenvoudig"]:
            display_adres = "N.v.t. voor deze taak (niet letterlijk noemen)"

        full_prompt = f"""{base_prompt}

# Preekgegevens
- **Plaatsnaam:** {user_input.get('plaatsnaam')}
- **Gemeente:** {user_input.get('gemeente')}
- **Adres:** {display_adres}
- **Website:** {user_input.get('website') or 'Geen'}
- **Datum:** {user_input.get('datum')}

# Dossier: Eerdere Analyses & Context
Hieronder vind je de output van eerdere stappen in het proces. Gebruik deze informatie als fundament voor je huidige taak.

{analysis_context}

---

# Huidige Opdracht: {title}

{task_prompt}
"""

        # LOG DE PROMPT
        save_log(LOGS_DIR, name, full_prompt)

        # Voer analyse uit
        if name == "11_kalender":
            temp = 0.1 # Laag voor feitelijke precisie
        elif name in ["14_gebeden", "14_gebeden_profetisch", "14_gebeden_dialogisch", "14_gebeden_eenvoudig", "15_kindermoment"]:
            temp = 0.7 # Hoger voor poëtische creativiteit
        else:
            temp = 0.2 # Standaard

        result = run_analysis(client, full_prompt, title, temperature=temp)

        # Extra verificatiestap voor kunst_cultuur om hallucinaties te verwijderen
        if name == "09_kunst_cultuur":
            result = verify_kunst_cultuur(client, result)

        save_analysis(folder, name, result, title, user_input)

    # Update overzicht
    update_summary(folder)
    
    # Combineer alle JSONs
    combine_all_json(folder)

    print("\n" + "=" * 60)
    print("KLAAR")
    print(f"Locatie: {folder}")
    print("=" * 60)


def combine_all_json(folder: Path):
    """Combineer alle genummerde JSON-bestanden (00-15) tot één bestand, met ontdubbeling van metadata."""
    print("\nAlle JSON-outputs combineren...")
    combined_data = {}
    
    # 1. Laad 00_meta.json (Basis metadata)
    meta_file = folder / "00_meta.json"
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                combined_data["00_meta"] = json.load(f)
        except Exception as e:
            print(f"  Fout bij lezen 00_meta.json: {e}")

    # 2. Laad alle andere genummerde bestanden
    # We sorteren ze zodat de volgorde logisch is
    json_files = sorted([f for f in folder.glob("*.json") if re.match(r"^\d{2}_.*\.json$", f.name)])
    
    for json_file in json_files:
        key = json_file.stem # bestandsnaam zonder extensie
        
        # Sla 00_meta over (al gedaan) en combined_output zelf
        if key == "00_meta" or key == "combined_output":
            continue
            
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # Ontdubbeling: Verwijder _meta object als het bestaat
                # (Dit bevat vaak redundante info zoals adres, datum, etc.)
                if "_meta" in data:
                    del data["_meta"]
                
                combined_data[key] = data
        except Exception as e:
            print(f"  Fout bij lezen {json_file.name}: {e}")

    # 3. Voeg bijbelteksten toe
    bijbel_dir = folder / "bijbelteksten"
    if bijbel_dir.exists():
        bijbel_data = {
            "naardense_bijbel": [],
            "nbv21": [],
            "grondtekst": []
        }
        
        # Lees Naardense Bijbel
        for json_file in sorted(bijbel_dir.glob("*_NB.json")):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    if isinstance(content, list):
                        bijbel_data["naardense_bijbel"].extend(content)
                    else:
                        bijbel_data["naardense_bijbel"].append(content)
            except Exception as e:
                print(f"  Fout bij lezen NB tekst {json_file.name}: {e}")

        # Lees NBV21
        for json_file in sorted(bijbel_dir.glob("*_NBV21.json")):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    if isinstance(content, list):
                        bijbel_data["nbv21"].extend(content)
                    else:
                        bijbel_data["nbv21"].append(content)
            except Exception as e:
                print(f"  Fout bij lezen NBV21 tekst {json_file.name}: {e}")

        # Lees Grondtekst
        for json_file in sorted(bijbel_dir.glob("*_Grondtekst.json")):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    if isinstance(content, list):
                        bijbel_data["grondtekst"].extend(content)
                    else:
                        bijbel_data["grondtekst"].append(content)
            except Exception as e:
                print(f"  Fout bij lezen Grondtekst {json_file.name}: {e}")
        
        if any(bijbel_data.values()):
            combined_data["Bijbelteksten"] = bijbel_data
            
    output_path = folder / "combined_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
        
    print(f"  Gecombineerde output opgeslagen: {output_path.name}")
    
    # Draai count_tokens.py op het gecombineerde bestand
    try:
        script_path = SCRIPT_DIR / "count_tokens.py"
        print(f"\nTokens tellen voor {output_path.name}...")
        subprocess.run([sys.executable, str(script_path), "--file", str(output_path)], check=False)
    except Exception as e:
        print(f"  Kon count_tokens.py niet uitvoeren: {e}")


if __name__ == "__main__":
    main()
