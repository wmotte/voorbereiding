#!/usr/bin/env python3
"""
Verdieping: Exegese, Kunst/Cultuur en Homiletiek voor Preekvoorbereiding

Dit script bouwt voort op de basisanalyse van contextduiding.py en voegt toe:
- 08a_exegese: Exegetische analyse van de Schriftlezingen
- 08c_commentaries: Exegetische diepgang via Neo4j Commentaren Database (MCP)
- 09_kunst_cultuur: Kunst, cultuur en film bij de lezingen
- 10_focus_en_functie: Focus en functie van de preek
- 11_kalender: Gedenkdagen en bijzondere momenten
- 12_representatieve_hoorders: Hoordersprofielen
- 13_homiletische_analyse: Homiletische analyse (Lowry's Plot)
- 13_homiletische_analyse_buttrick: Homiletische analyse (Buttrick's Moves & Structures)
- 13b_homiletische_illustraties: Illustraties generator (min. 20 illustraties)
- 14_klassieke_retorica: Klassiek-retorische analyse (Aristoteles)
- 14_gebeden: Gebeden voor de eredienst
- 15_kindermoment/bezinningsmoment: Optionele momenten
- 16-18_preken: Preekschetsen in stijlen van Sölle, Jüngel, Noordmans

Het leest de output van de vorige analyses (00-07) en gebruikt deze als context.
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
import asyncio
from pathlib import Path
from datetime import datetime

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("FOUT: De nieuwe 'google-genai' library is niet geïnstalleerd.")
    print("Installeer deze met: pip install google-genai")
    sys.exit(1)

# Probeer MCP client te importeren voor Neo4j integratie
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("WAARSCHUWING: 'mcp' library niet gevonden. Commentaar-analyse via database wordt overgeslagen.")
    print("Installeer met: pip install mcp")

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
    """Selecteer willekeurige fragmenten uit de Noordmans preken map."""
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
            if ((item / "01_zondag_kerkelijk_jaar.json").exists() or
                (item / "00_meta.json").exists() or
                (item / "00_zondag_kerkelijk_jaar.json").exists()):
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
        existing = []
        for num in range(20):
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

    files_to_read = [
        ("01_zondag_kerkelijk_jaar", "liturgische_context"),
        ("02_sociaal_maatschappelijke_context", "sociaal_maatschappelijk"),
        ("03_waardenorientatie", "waardenorientatie"),
        ("04_geloofsorientatie", "geloofsorientatie"),
        ("05_interpretatieve_synthese", "synthese"),
        ("06_actueel_wereldnieuws", "wereldnieuws"),
        ("07_politieke_orientatie", "politieke_orientatie"),
        ("08a_exegese", "exegese"),
        ("08c_commentaries", "commentaren"),
        ("09_kunst_cultuur", "kunst_cultuur"),
        ("10_focus_en_functie", "focus_en_functie"),
        ("11_kalender", "kalender"),
        ("12_representatieve_hoorders", "representatieve_hoorders"),
        ("13_homiletische_analyse", "homiletische_analyse"),
        ("13_homiletische_analyse_buttrick", "homiletische_analyse_buttrick"),
        ("13b_homiletische_illustraties", "homiletische_illustraties"),
        ("14_klassieke_retorica", "klassieke_retorica"),
        ("14_gebeden", "gebeden"),
        ("15_bezinningsmoment", "bezinningsmoment"),
        ("15_kindermoment", "kindermoment"),
    ]

    for basename, key in files_to_read:
        filepath_json = folder / f"{basename}.json"
        
        if filepath_json.exists():
            with open(filepath_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "_meta" in data:
                del data["_meta"]
            analyses[key] = json.dumps(data, ensure_ascii=False, indent=2)
            continue
            
    return analyses


def extract_user_input_from_folder(folder: Path) -> dict:
    """Probeer plaatsnaam, gemeente en datum te extraheren."""
    user_input = {"plaatsnaam": "", "gemeente": "", "datum": "", "adres": "", "website": ""}

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

    for json_path in sorted(folder.glob("*.json")):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            meta_input = data.get("_meta", {}).get("user_input")
            if meta_input:
                for key in user_input:
                    if meta_input.get(key):
                        user_input[key] = meta_input[key]
                if user_input["plaatsnaam"] and user_input["adres"]:
                    return user_input
        except (json.JSONDecodeError, KeyError):
            continue

    return user_input


def load_bible_context_as_json(folder: Path) -> str:
    """Lees alle gedownloade bijbelteksten."""
    bijbel_dir = folder / "bijbelteksten"
    if not bijbel_dir.exists():
        return ""

    context_data = {
        "naardense_bijbel": [],
        "nbv21": [],
        "grondtekst": []
    }

    # Lees bestanden
    for variant, suffix in [("naardense_bijbel", "_NB.json"), ("nbv21", "_NBV21.json"), ("grondtekst", "_Grondtekst.json")]:
        for json_file in sorted(bijbel_dir.glob(f"*{suffix}")):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    context_data[variant].append(data)
            except Exception as e:
                print(f"Fout bij lezen {json_file}: {e}")

    if not any(context_data.values()):
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
    """Bouw een context string van vorige analyses."""
    if excluded_sections is None:
        excluded_sections = []

    sections = []

    if previous_analyses.get("liturgische_context"):
        sections.append("## Liturgische Context en Schriftlezingen\n\n" + previous_analyses["liturgische_context"])

    if previous_analyses.get("sociaal_maatschappelijk"):
        sections.append("## Sociaal-Maatschappelijke Context\n\n" + previous_analyses["sociaal_maatschappelijk"])

    if previous_analyses.get("waardenorientatie"):
        sections.append("## Waardenoriëntatie\n\n" + previous_analyses["waardenorientatie"])

    if previous_analyses.get("geloofsorientatie"):
        sections.append("## Geloofsoriëntatie\n\n" + previous_analyses["geloofsorientatie"])

    if previous_analyses.get("synthese"):
        sections.append("## Interpretatieve Synthese\n\n" + previous_analyses["synthese"])

    if limited:
        return "\n\n---\n\n".join(sections)

    if previous_analyses.get("wereldnieuws") and "wereldnieuws" not in excluded_sections:
        sections.append("## Actueel Wereldnieuws\n\n" + previous_analyses["wereldnieuws"])

    if previous_analyses.get("politieke_orientatie") and "politieke_orientatie" not in excluded_sections:
        sections.append("## Politieke Oriëntatie\n\n" + previous_analyses["politieke_orientatie"])

    if previous_analyses.get("exegese") and "exegese" not in excluded_sections:
        sections.append("## Exegese\n\n" + previous_analyses["exegese"])

    if previous_analyses.get("commentaren") and "commentaren" not in excluded_sections:
        sections.append("## Commentaren (Onderzoek)\n\n" + previous_analyses["commentaren"])

    if previous_analyses.get("kunst_cultuur") and "kunst_cultuur" not in excluded_sections:
        sections.append("## Kunst & Cultuur\n\n" + previous_analyses["kunst_cultuur"])

    if previous_analyses.get("focus_en_functie") and "focus_en_functie" not in excluded_sections:
        sections.append("## Focus en Functie\n\n" + previous_analyses["focus_en_functie"])

    if previous_analyses.get("kalender") and "kalender" not in excluded_sections:
        sections.append("## Kalender\n\n" + previous_analyses["kalender"])

    if previous_analyses.get("representatieve_hoorders") and "representatieve_hoorders" not in excluded_sections:
        sections.append("## Representatieve Hoorders\n\n" + previous_analyses["representatieve_hoorders"])

    return "\n\n---\n\n".join(sections)


def extract_json(text: str) -> dict:
    """Extraheer JSON uit de response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    return {"error": "Kon geen valide JSON extraheren", "raw_response": text[:1000]}


def run_analysis(client: genai.Client, prompt: str, title: str, temperature: float = 0.2, model: str = None) -> dict:
    """Voer een analyse uit met Gemini en Google Search."""
    current_model = model or MODEL_NAME

    print(f"\n{'─' * 50}")
    print(f"Analyseren: {title}")
    print(f"{ '─' * 50}")

    max_retries = 2
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
                        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                    ]
                )
            )

            if response.text:
                result = extract_json(response.text)
                if "error" in result:
                    print(f"⚠ Analyse '{title}' voltooid maar JSON parsing mislukt")
                    if attempt < max_retries: continue
                else:
                    print(f"✓ Analyse '{title}' voltooid (valide JSON)")
                    return result
            else:
                print(f"✗ Geen tekst ontvangen voor '{title}'")
                if attempt < max_retries: continue

        except Exception as e:
            print(f"✗ Fout bij analyse '{title}': {str(e)}")
            if attempt < max_retries: continue

    if current_model == MODEL_NAME and MODEL_NAME_FALLBACK:
        print(f"\n⚠ Fallback naar {MODEL_NAME_FALLBACK}...")
        return run_analysis(client, prompt, title, temperature=temperature, model=MODEL_NAME_FALLBACK)

    return {"error": f"Analyse mislukt na herpogingen", "title": title}


def verify_kunst_cultuur(client: genai.Client, content: dict) -> dict:
    """Verifieer alle bronnen in de kunst/cultuur output."""
    print(f"\n{'─' * 50}")
    print("VERIFICATIE: Bronnen controleren...")
    print(f"{ '─' * 50}")

    content_str = json.dumps(content, ensure_ascii=False, indent=2)
    if len(content_str) > 100000:
        content_str = content_str[:100000] + "\n\n... [inhoud ingekort]"

    verification_prompt = """Je bent een strenge factchecker. Controleer de onderstaande JSON op niet-bestaande bronnen (films, boeken, kunst). Verwijder alles wat je niet kunt verifiëren via Search. Retourneer ALLEEN de geschoonde JSON."""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=verification_prompt + content_str,
            config=types.GenerateContentConfig(
                temperature=0.1,
                tools=[types.Tool(google_search=types.GoogleSearch())],
                response_mime_type="application/json"
            )
        )
        if response.text:
            verified = extract_json(response.text)
            if "error" not in verified:
                print("✓ Verificatie voltooid")
                return verified
    except Exception as e:
        print(f"✗ Verificatie fout: {e}")

    return content


def mcp_tool_to_gemini_function(tool) -> types.FunctionDeclaration:
    """Converteer MCP tool naar Gemini FunctionDeclaration."""
    def clean_schema(schema):
        if not isinstance(schema, dict): return schema
        cleaned = {}
        for key, value in schema.items():
            if key in ['additionalProperties', '$schema', '$id']: continue
            if isinstance(value, dict): cleaned[key] = clean_schema(value)
            elif isinstance(value, list): cleaned[key] = [clean_schema(item) if isinstance(item, dict) else item for item in value]
            else: cleaned[key] = value
        return cleaned

    parameters = tool.inputSchema if tool.inputSchema else {"type": "object", "properties": {}}
    cleaned_parameters = clean_schema(parameters)
    if "type" not in cleaned_parameters: cleaned_parameters["type"] = "object"
    if "properties" not in cleaned_parameters: cleaned_parameters["properties"] = {}

    return types.FunctionDeclaration(
        name=tool.name,
        description=tool.description or f"Tool: {tool.name}",
        parameters=cleaned_parameters
    )


async def find_commentaries_via_mcp(client: genai.Client, context: str) -> dict:
    """Gebruik MCP om exegetische informatie te zoeken in de 'commentaries' database."""
    if not MCP_AVAILABLE:
        return {"error": "MCP niet beschikbaar"}

    print(f"\n{'─' * 50}")
    print("MCP: Gemini zoekt in commentaren database...")
    print(f"{ '─' * 50}")

    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    username = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password")
    database = "commentaries"

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@nibronix/mcp-neo4j-server"],
        env={
            "NEO4J_URI": uri,
            "NEO4J_USERNAME": username,
            "NEO4J_PASSWORD": password,
            "NEO4J_DATABASE": database,
            "PATH": os.environ.get("PATH", ""),
        }
    )

    try:
        prompt_path = PROMPTS_DIR / "08c_commentaries.md"
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_instruction = f.read()
    except Exception as e:
        print(f"⚠ Fout bij laden prompt: {e}")
        return {"error": str(e)}

    user_query = f"Hier is de context voor de exegese (lezingen en achtergrond):\n\n{context}\n\nVoer nu het onderzoek uit in de database en schrijf de exegese zoals gevraagd."

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                gemini_tools = [types.Tool(function_declarations=[mcp_tool_to_gemini_function(tool)]) for tool in tools_result.tools]
                
                messages = [types.Content(role="user", parts=[types.Part(text=user_query)])]
                max_iterations = 15
                iteration = 0
                final_response = ""

                while iteration < max_iterations:
                    iteration += 1
                    print(f"  Iteratie {iteration}/{max_iterations}...")
                    config_params = {"tools": gemini_tools, "system_instruction": system_instruction, "temperature": 0.2, "max_output_tokens": 8192}
                    if iteration > 5: config_params["response_mime_type"] = "application/json"

                    response = client.models.generate_content(model=MODEL_NAME, contents=messages, config=types.GenerateContentConfig(**config_params))
                    if not response.candidates: break
                    parts = response.candidates[0].content.parts
                    has_function_call = False

                    for part in parts:
                        if hasattr(part, 'text') and part.text:
                            final_response = part.text
                        if hasattr(part, 'function_call') and part.function_call:
                            has_function_call = True
                            func_call = part.function_call
                            tool_name = func_call.name
                            tool_args = dict(func_call.args) if func_call.args else {}

                            print(f"  → Tool: {tool_name}")
                            try:
                                result = await asyncio.wait_for(session.call_tool(tool_name, tool_args), timeout=60.0)
                                tool_result = result.content[0].text if result.content else "Geen resultaat"
                                
                                # Performance logging en Truncation
                                result_len = len(tool_result)
                                print(f"    ✓ Resultaat: {result_len} chars")
                                
                                if result_len > 150000:
                                    print(f"    ⚠ WAARSCHUWING: Response te groot ({result_len} chars). Wordt ingekort tot 150.000.")
                                    tool_result = tool_result[:150000] + "\n... [DATA INGEKORT WEGENS LENGTE. VERFIJN JE QUERY.]"
                                    
                            except Exception as e:
                                tool_result = f"Error: {e}"
                                print(f"    ✗ Tool error: {e}")

                            messages.append(types.Content(role="model", parts=parts))
                            messages.append(types.Content(role="user", parts=[types.Part(function_response=types.FunctionResponse(name=tool_name, response={"result": tool_result}))]))
                            break
                    if not has_function_call: break

                try: return {**json.loads(final_response), "_meta": {"iterations": iteration}}
                except:
                    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', final_response, re.DOTALL)
                    if json_match: return {**json.loads(json_match.group(1)), "_meta": {"iterations": iteration}}
                    return {"error": "Geen valide JSON", "markdown_output": final_response}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


def save_analysis(output_dir: Path, filename: str, content: dict, title: str, user_input: dict = None):
    """Sla een analyse op naar een JSON bestand."""
    filepath = output_dir / f"{filename}.json"
    meta = {"title": title, "filename": filename, "generated_at": datetime.now().isoformat()}
    if user_input: meta["user_input"] = user_input
    content_with_meta = {"_meta": meta, **content}
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
    overzicht_json_path = output_dir / "00_overzicht.json"
    if overzicht_json_path.exists():
        try:
            with open(overzicht_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            new_analyses = [
                ("08a_exegese", "Exegese van de Schriftlezingen"),
                ("08c_commentaries", "Exegetische Diepgang (Commentaren)"),
                ("09_kunst_cultuur", "Kunst, Cultuur en Film"),
                ("10_focus_en_functie", "Focus en Functie"),
                ("11_kalender", "Kalender"),
                ("12_representatieve_hoorders", "Representatieve Hoorders"),
                ("13_homiletische_analyse", "Homiletische Analyse (Lowry's Plot)"),
                ("13_homiletische_analyse_buttrick", "Homiletische Analyse (Buttrick's Moves & Structures)"),
                ("13b_homiletische_illustraties", "Homiletische Illustraties Generator"),
                ("14_klassieke_retorica", "Klassiek-Retorische Analyse (Aristoteles)"),
                ("14_gebeden", "Gebeden voor de Eredienst"),
                ("14_gebeden_profetisch", "Profetische Gebeden (Brueggemann)"),
                ("14_gebeden_dialogisch", "Dialogische Gebeden (Dumas)"),
                ("14_gebeden_eenvoudig", "Eenvoudige Gebeden (B1-niveau)"),
                ("15_bezinningsmoment", "Moment van Bezinning"),
                ("15_kindermoment", "Kindermoment"),
                ("16_preek_solle", "Preek in de stijl van Sölle"),
                ("17_preek_jungel", "Preek in de stijl van Jüngel"),
                ("18_preek_noordmans", "Preekschets in de stijl van Noordmans"),
            ]

            existing_names = [a.get("name") for a in data.get("analyses", [])]
            for name, title in new_analyses:
                if (output_dir / f"{name}.json").exists() and name not in existing_names:
                    data.setdefault("analyses", []).append({"name": name, "title": title, "file": f"{name}.json"})

            with open(overzicht_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass

    overzicht_md_path = output_dir / "00_overzicht.md"
    if overzicht_md_path.exists():
        with open(overzicht_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        for name, title in new_analyses:
            if ((output_dir / f"{name}.json").exists() or (output_dir / f"{name}.md").exists()) and f"[{title}]" not in content:
                if "## Analyses" in content:
                    content = content.rstrip() + f"\n- [{title}]({name}.json)\n"
        with open(overzicht_md_path, "w", encoding="utf-8") as f:
            f.write(content)


def combine_all_json(folder: Path):
    """Combineer alle genummerde JSON-bestanden (00-15) tot één bestand, met ontdubbeling van metadata."""
    print("\nAlle JSON-outputs combineren...")
    combined_data = {}
    
    meta_file = folder / "00_meta.json"
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                combined_data["00_meta"] = json.load(f)
        except Exception as e:
            print(f"  Fout bij lezen 00_meta.json: {e}")

    json_files = sorted([f for f in folder.glob("*.json") if re.match(r"^\d{2}[a-z]?_.*\.json$", f.name)])
    for json_file in json_files:
        key = json_file.stem
        if key in ["00_meta", "combined_output"]: continue
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "_meta" in data: del data["_meta"]
                combined_data[key] = data
        except Exception as e:
            print(f"  Fout bij lezen {json_file.name}: {e}")

    bijbel_dir = folder / "bijbelteksten"
    if bijbel_dir.exists():
        bijbel_data = {"naardense_bijbel": [], "nbv21": [], "grondtekst": []}
        for variant, suffix in [("naardense_bijbel", "_NB.json"), ("nbv21", "_NBV21.json"), ("grondtekst", "_Grondtekst.json")]:
            for json_file in sorted(bijbel_dir.glob(f"*{suffix}")):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        if isinstance(content, list): bijbel_data[variant].extend(content)
                        else: bijbel_data[variant].append(content)
                except: pass
        if any(bijbel_data.values()): combined_data["Bijbelteksten"] = bijbel_data
            
    output_path = folder / "combined_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    print(f"  Gecombineerde output opgeslagen: {output_path.name}")
    
    try:
        script_path = SCRIPT_DIR / "technical/count_tokens.py"
        print(f"\nTokens tellen voor {output_path.name}...")
        subprocess.run([sys.executable, str(script_path), "--file", str(output_path)], check=False)
    except:
        pass


def main():
    """Hoofdfunctie."""
    parser = argparse.ArgumentParser(description="Verdieping: Exegese, Kunst/Cultuur en Homiletiek")
    parser.add_argument("--exegese", action="store_true", help="Voer alleen de exegese analyse uit")
    args = parser.parse_args()

    env_file = SCRIPT_DIR / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"\'')

    folder = select_folder()
    print(f"\nGeselecteerd: {folder.name}")
    previous_analyses = read_previous_analyses(folder)
    user_input = extract_user_input_from_folder(folder)

    if not previous_analyses.get("liturgische_context"):
        print("\nFOUT: Geen liturgische context gevonden.")
        sys.exit(1)

    print("\n" + "─" * 50 + "\nBIJBELTEKSTEN OPHALEN\n" + "─" * 50)
    bijbel_dir = folder / "bijbelteksten"
    if not (bijbel_dir.exists() and list(bijbel_dir.glob("*_NB.json"))):
        download_lezingen(folder, previous_analyses["liturgische_context"])
    if not (bijbel_dir.exists() and list(bijbel_dir.glob("*_NBV21.json"))):
        save_nbv21_lezingen(folder, previous_analyses["liturgische_context"])
    if not (bijbel_dir.exists() and list(bijbel_dir.glob("*_Grondtekst.json"))):
        save_grondtekst_lezingen(folder, previous_analyses["liturgische_context"])

    client = get_gemini_client()
    LOGS_DIR = folder / "logs"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    context_string = build_context_string(previous_analyses)
    bible_json_context = load_bible_context_as_json(folder)
    if bible_json_context:
        context_string += f"\n\n---\n## Bijbelteksten\n```json\n{bible_json_context}\n```\n"

    base_prompt = load_prompt("base_prompt_verdieping.md", user_input)

    print("\nOPTIONELE ONDERDELEN:")
    wil_kindermoment = input("  Wil je een Kindermoment genereren? (j/n): ").strip().lower() == 'j'
    wil_bezinningsmoment = input("  Wil je een Moment van Bezinning genereren? (j/n): ").strip().lower() == 'j'

    print("\n" + "=" * 60 + f"\nVERDIEPING STARTEN MET MODEL: {MODEL_NAME}\n" + "=" * 60)

    analysis_definitions = [
        ("08a_exegese", "Exegese van de Schriftlezingen"),
        ("08c_commentaries", "Exegetische Diepgang (Commentaren)"),
        ("09_kunst_cultuur", "Kunst, Cultuur en Film"),
        ("10_focus_en_functie", "Focus en Functie"),
        ("11_kalender", "Kalender: Gedenkdagen en Bijzondere Momenten"),
        ("12_representatieve_hoorders", "Representatieve Hoorders"),
        ("13_homiletische_analyse", "Homiletische Analyse (Lowry's Plot)"),
        ("13_homiletische_analyse_buttrick", "Homiletische Analyse (Buttrick's Moves & Structures)"),
        ("13b_homiletische_illustraties", "Homiletische Illustraties Generator"),
        ("14_klassieke_retorica", "Klassiek-Retorische Analyse (Aristoteles)"),
        ("14_gebeden", "Gebeden voor de Eredienst"),
        ("14_gebeden_profetisch", "Profetische Gebeden (Brueggemann)"),
        ("14_gebeden_dialogisch", "Dialogische Gebeden (Dumas)"),
        ("14_gebeden_eenvoudig", "Eenvoudige Gebeden (B1-niveau)"),
    ]
    if wil_kindermoment: analysis_definitions.append(("15_kindermoment", "Kindermoment"))
    if wil_bezinningsmoment: analysis_definitions.append(("15_bezinningsmoment", "Moment van Bezinning"))
    analysis_definitions.extend([("16_preek_solle", "Preek in de stijl van Sölle"), ("17_preek_jungel", "Preek in de stijl van Jüngel"), ("18_preek_noordmans", "Preekschets in de stijl van Noordmans")])

    if args.exegese:
        analysis_definitions = [x for x in analysis_definitions if x[0].startswith("08")]

    for name, title in analysis_definitions:
        if (folder / f"{name}.json").exists():
            if input(f"\n{name}.json bestaat al. Overschrijven? (j/n): ").strip().lower() != 'j': continue

        if name == "08c_commentaries":
            if MCP_AVAILABLE:
                try:
                    result = asyncio.run(find_commentaries_via_mcp(client, context_string))
                    save_analysis(folder, name, result, title, user_input)
                except Exception as e: print(f"✗ Fout bij commentaren: {e}")
            continue

        extra_replacements = {}
        if name == "14_gebeden_profetisch": extra_replacements["voorbeeld_gebeden"] = sample_profetische_gebeden()
        elif name == "14_gebeden_dialogisch": extra_replacements["voorbeeld_gebeden"] = sample_dialogische_gebeden()
        elif name == "16_preek_solle": extra_replacements["voorbeeld_gebeden"] = sample_solle_preken()
        elif name == "17_preek_jungel": extra_replacements["voorbeeld_gebeden"] = sample_jungel_preken()
        elif name == "18_preek_noordmans": extra_replacements["voorbeeld_gebeden"] = sample_noordmans_preken()

        task_prompt = load_prompt(f"{name}.md", user_input, extra_replacements)
        analysis_context = build_context_string(previous_analyses, limited=(name == "12_representatieve_hoorders"), excluded_sections=["kunst_cultuur", "kalender", "representatieve_hoorders"] if name.startswith("14_gebeden") else [])

        full_prompt = f"{base_prompt}\n# Preekgegevens\n- **Plaatsnaam:** {user_input.get('plaatsnaam')}\n- **Gemeente:** {user_input.get('gemeente')}\n- **Adres:** {'N.v.t.' if name.startswith('14_gebeden') else user_input.get('adres')}\n- **Website:** {user_input.get('website') or 'Geen'}\n- **Datum:** {user_input.get('datum')}\n\n# Dossier\n{analysis_context}\n\n---\n# Opdracht: {title}\n{task_prompt}"
        save_log(LOGS_DIR, name, full_prompt)

        temp = 0.8 if name in ["13b_homiletische_illustraties", "14_gebeden", "16_preek_solle"] else 0.2
        result = run_analysis(client, full_prompt, title, temperature=temp)
        if name == "09_kunst_cultuur": result = verify_kunst_cultuur(client, result)
        save_analysis(folder, name, result, title, user_input)

    update_summary(folder)
    combine_all_json(folder)
    print("\n" + "=" * 60 + f"\nKLAAR\nLocatie: {folder}\n" + "=" * 60)


if __name__ == "__main__":
    main()
