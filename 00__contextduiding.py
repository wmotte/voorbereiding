#!/usr/bin/env python3
"""
Contextduiding voor Protestantse Preekvoorbereiding

Dit script voert een uitgebreide hoordersanalyse uit voor preekvoorbereiding,
gebaseerd op de homiletische methodiek van De Leede & Stark.

Het gebruikt de NIEUWE Google GenAI SDK (v1.0+) met Gemini 3.0 en Google Search
grounding om actuele informatie te verzamelen.

W.M. Otte (w.m.otte@umcutrecht.nl)
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime

# Importeer de nieuwe SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("FOUT: De nieuwe 'google-genai' library is niet geïnstalleerd.")
    print("Installeer deze met: pip install google-genai")
    sys.exit(1)

# Configuratie
SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR / "output"
PROMPTS_DIR = SCRIPT_DIR / "prompts"

# Model keuze: Gemini 3 flash (i.p.v. pro)
MODEL_NAME = "gemini-3-flash-preview"


def load_prompt(filename: str, user_input: dict) -> str:
    """Laad een prompt uit een markdown bestand en vervang placeholders.

    Placeholders:
        {{plaatsnaam}}     - wordt vervangen door user_input['plaatsnaam']
        {{gemeente}}       - wordt vervangen door user_input['gemeente']
        {{datum}}          - wordt vervangen door user_input['datum']
        {{huidige_datum}}  - wordt vervangen door de huidige datum
    """
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

    # Vervang placeholders
    content = content.replace("{{plaatsnaam}}", user_input.get("plaatsnaam", ""))
    content = content.replace("{{gemeente}}", user_input.get("gemeente", ""))
    content = content.replace("{{datum}}", user_input.get("datum", ""))
    content = content.replace("{{huidige_datum}}", huidige_datum)

    return content


def get_user_input() -> dict:
    """Vraag de gebruiker om de benodigde informatie."""
    print("\n" + "=" * 60)
    print("CONTEXTDUIDING VOOR PREEKVOORBEREIDING")
    print("Gebaseerd op de homiletische methodiek van De Leede & Stark")
    print("=" * 60 + "\n")

    print("Dit programma voert een uitgebreide hoordersanalyse uit voor uw preek.")
    print("Vul de volgende gegevens in:\n")

    plaatsnaam = input("1. Plaatsnaam waar de preek gehouden wordt: ").strip()
    if not plaatsnaam:
        print("FOUT: Plaatsnaam is verplicht.")
        sys.exit(1)

    gemeente = input("2. Naam van de kerkelijke gemeente: ").strip()
    if not gemeente:
        print("FOUT: Gemeente is verplicht.")
        sys.exit(1)

    datum_str = input("3. Datum van de preek (bijv. 25 december 2025): ").strip()
    if not datum_str:
        print("FOUT: Datum is verplicht.")
        sys.exit(1)

    # Optionele extra context
    print("\n4. Eventuele extra context (optioneel, druk Enter om over te slaan):")
    print("   (bijv. bijzondere dienst, thema, doelgroep)")
    extra_context = input("   Extra context: ").strip()

    return {
        "plaatsnaam": plaatsnaam,
        "gemeente": gemeente,
        "datum": datum_str,
        "extra_context": extra_context
    }


def create_output_directory(plaatsnaam: str, datum: str) -> Path:
    """Maak een output directory aan voor de analyses."""
    safe_name = "".join(c if c.isalnum() or c in "- " else "_" for c in plaatsnaam)
    safe_date = "".join(c if c.isalnum() else "_" for c in datum)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_name = f"{safe_name}_{safe_date}_{timestamp}"

    output_path = OUTPUT_DIR / dir_name
    output_path.mkdir(parents=True, exist_ok=True)

    return output_path


def get_gemini_client() -> genai.Client:
    """Initialiseer de Gemini Client met de nieuwe SDK."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        print("\nFOUT: Geen API key gevonden.")
        print("Stel de GEMINI_API_KEY environment variable in.")
        sys.exit(1)

    return genai.Client(api_key=api_key)


def build_first_analysis(user_input: dict) -> dict:
    """Bouw de eerste analyse: Zondag van het Kerkelijk Jaar.

    Deze wordt eerst uitgevoerd zodat de lezingen en liturgische context
    beschikbaar zijn voor de andere analyses.
    """
    base_prompt = load_prompt("base_prompt.md", user_input)

    context_info = f"""
## Preekgegevens
- **Plaatsnaam:** {user_input['plaatsnaam']}
- **Gemeente:** {user_input['gemeente']}
- **Datum:** {user_input['datum']}
"""
    if user_input.get('extra_context'):
        context_info += f"- **Extra context:** {user_input['extra_context']}\n"

    task_prompt = load_prompt("00_zondag_kerkelijk_jaar.md", user_input)
    full_prompt = f"{base_prompt}\n\n{context_info}\n\n{task_prompt}"

    return {
        "name": "00_zondag_kerkelijk_jaar",
        "title": "Zondag van het Kerkelijk Jaar",
        "prompt": full_prompt
    }


def build_remaining_analyses(user_input: dict, kerkelijk_jaar_context: str) -> list[dict]:
    """Bouw de overige analyses, inclusief de liturgische context.

    Args:
        user_input: De gebruikersinvoer (plaatsnaam, gemeente, datum)
        kerkelijk_jaar_context: De output van de eerste analyse (lezingen, etc.)
    """
    base_prompt = load_prompt("base_prompt.md", user_input)

    # Context info nu inclusief de liturgische informatie
    context_info = f"""
## Preekgegevens
- **Plaatsnaam:** {user_input['plaatsnaam']}
- **Gemeente:** {user_input['gemeente']}
- **Datum:** {user_input['datum']}
"""
    if user_input.get('extra_context'):
        context_info += f"- **Extra context:** {user_input['extra_context']}\n"

    # Voeg de liturgische context toe
    context_info += f"""
## Liturgische Context (uit eerder onderzoek)

{kerkelijk_jaar_context}
"""

    # De overige analyses (01-06)
    analysis_definitions = [
        ("01_sociaal_maatschappelijke_context", "Sociaal-Maatschappelijke Context"),
        ("02_waardenorientatie", "Waardenoriëntatie"),
        ("03_geloofsorientatie", "Geloofsoriëntatie"),
        ("04_interpretatieve_synthese", "Interpretatieve Synthese"),
        ("05_actueel_wereldnieuws", "Actueel Wereldnieuws"),
        ("06_politieke_orientatie", "Politieke Oriëntatie"),
    ]

    analyses = []
    for name, title in analysis_definitions:
        task_prompt = load_prompt(f"{name}.md", user_input)
        full_prompt = f"{base_prompt}\n\n{context_info}\n\n{task_prompt}"

        analyses.append({
            "name": name,
            "title": title,
            "prompt": full_prompt
        })

    return analyses


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


def run_analysis(client: genai.Client, prompt: str, title: str) -> dict:
    """Voer een analyse uit met Taalmodel en Search. Retourneert JSON dict."""
    print(f"\n{'─' * 50}")
    print(f"Analyseren: {title}")
    print(f"{'─' * 50}")
    print("Bezig met redeneren en zoeken...")

    try:
        # Configuratie voor de generatie
        # We zetten safety filters UIT (BLOCK_NONE) omdat preekvoorbereiding
        # moet kunnen gaan over zonde, lijden, dood en religieus extremisme.
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,  # Lager dan normaal om minder hallucinaties te krijgen
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
                # Nieuwe syntax voor Google Search Tool
                tools=[types.Tool(
                    google_search=types.GoogleSearch()
                )],
                # Nieuwe syntax voor Safety Settings
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
                print(f"⚠ Analyse '{title}' voltooid maar JSON parsing mislukt")
            else:
                print(f"✓ Analyse '{title}' voltooid (valide JSON)")
            return result
        else:
            print(f"✗ Geen tekst ontvangen voor '{title}'")
            return {"error": "Geen response ontvangen", "title": title}

    except Exception as e:
        error_msg = f"Fout bij analyse '{title}': {str(e)}"
        print(f"✗ {error_msg}")
        return {"error": error_msg, "title": title}


def verify_liedboek(client: genai.Client, content: dict) -> dict:
    """Verifieer alle liedsuggesties met Google Search."""
    print(f"\n{'─' * 50}")
    print("VERIFICATIE: Liedboek 2013 suggesties controleren...")
    print(f"{'─' * 50}")
    print("Bezig met verifiëren van liednummers en titels...")

    content_str = json.dumps(content, ensure_ascii=False, indent=2)

    verification_prompt = """Je bent een strenge factchecker voor het 'Liedboek - Zingen en bidden in huis en kerk' (2013).

## Instructies

1. Controleer ELKE liedsuggestie in de onderstaande JSON.
2. Gebruik Google Search om te verifiëren of het lied met dat nummer en die titel BESTAAT in Liedboek 2013.
   - Zoektermen: "Liedboek 2013 [nummer]", "Liedboek 2013 [titel]", "Kerkliedwiki [nummer]"
3. Verwijder liederen die:
   - NIET in Liedboek 2013 staan.
   - Uit andere bundels komen (zoals Weerklank, Opwekking, Evangelische Liedbundel), tenzij ze OOK in Liedboek 2013 staan.
   - Niet bestaan.
4. Als het nummer niet klopt bij de titel, corrigeer het dan op basis van Kerkliedwiki.
5. Behoud de originele JSON structuur.
6. Retourneer ALLEEN valide JSON.

## Te controleren JSON:

"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=verification_prompt + content_str,
            config=types.GenerateContentConfig(
                temperature=0.1,  # Zeer laag voor maximale precisie
                top_p=0.85,
                top_k=20,
                max_output_tokens=8192,
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
                print("✓ Verificatie voltooid - foute liedsuggesties verwijderd")
                return verified
            else:
                print("⚠ Verificatie parsing mislukt - originele data behouden")
                return content
        else:
            print("✗ Verificatie mislukt (geen text) - originele data behouden")
            return content

    except Exception as e:
        print(f"✗ Verificatie fout: {str(e)} - originele data behouden")
        return content


def save_analysis(output_dir: Path, filename: str, content: dict, title: str):
    """Sla een analyse op naar een JSON bestand."""
    filepath = output_dir / f"{filename}.json"

    # Voeg metadata toe
    content_with_meta = {
        "_meta": {
            "title": title,
            "filename": filename,
            "generated_at": datetime.now().isoformat()
        },
        **content
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(content_with_meta, f, ensure_ascii=False, indent=2)

    print(f"  Opgeslagen: {filepath.name}")


def list_output_folders() -> list[Path]:
    """Lijst alle beschikbare output folders."""
    if not OUTPUT_DIR.exists():
        return []

    folders = []
    for item in OUTPUT_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            # Controleer of er een 00_zondag_kerkelijk_jaar bestand bestaat (JSON of MD)
            # OF dat het een geldige output folder lijkt
            if ((item / "00_zondag_kerkelijk_jaar.json").exists() or
                (item / "00_zondag_kerkelijk_jaar.md").exists() or
                (item / "00_overzicht.json").exists() or
                (item / "00_overzicht.md").exists()):
                folders.append(item)

    return sorted(folders, key=lambda x: x.stat().st_mtime, reverse=True)


def extract_user_input_from_folder(folder: Path) -> dict:
    """Probeer plaatsnaam, gemeente en datum te extraheren uit de foldernaam of overzicht."""
    user_input = {"plaatsnaam": "", "gemeente": "", "datum": "", "extra_context": ""}

    # Probeer eerst uit JSON overzicht
    overzicht_json = folder / "00_overzicht.json"
    if overzicht_json.exists():
        try:
            with open(overzicht_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            gegevens = data.get("gegevens", {})
            user_input["plaatsnaam"] = gegevens.get("plaatsnaam", "")
            user_input["gemeente"] = gegevens.get("gemeente", "")
            user_input["datum"] = gegevens.get("datum_preek", "")
            user_input["extra_context"] = gegevens.get("extra_context", "")
            if user_input["plaatsnaam"]:
                return user_input
        except (json.JSONDecodeError, KeyError):
            pass

    # Fallback: probeer uit MD overzicht
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
            elif "**Extra context:**" in line:
                user_input["extra_context"] = line.split("**Extra context:**")[-1].strip()

    # Fallback: gebruik foldernaam
    if not user_input["plaatsnaam"]:
        parts = folder.name.split("_")
        if parts:
            user_input["plaatsnaam"] = parts[0]

    return user_input


def select_startup_mode() -> tuple[str, Path | None]:
    """
    Laat de gebruiker kiezen: Nieuwe analyse of bestaande folder.
    Returns: ('new', None) or ('existing', folder_path)
    """
    folders = list_output_folders()

    print("\n" + "=" * 60)
    print("CONTEXTDUIDING: START (JSON OUTPUT)")
    print("=" * 60)
    print("\nWat wilt u doen?\n")
    print("  1. Nieuwe analyse starten")

    if folders:
        print("\n  Bestaande analyses:")
        for i, folder in enumerate(folders, 1):
            # Tel bestaande analyses (check both JSON and MD)
            existing = []
            for num in range(7):  # 00-06
                json_pattern = f"{num:02d}_*.json"
                md_pattern = f"{num:02d}_*.md"
                if list(folder.glob(json_pattern)):
                    existing.append(f"{num:02d}")
                elif list(folder.glob(md_pattern)):
                    existing.append(f"{num:02d}(md)")

            print(f"  {i+1}. {folder.name}")
            print(f"     Beschikbaar: {', '.join(existing)}")
    else:
        print("\n  (Geen eerdere analyses gevonden)")

    print()
    while True:
        try:
            choice = input("Kies een nummer (of 'q' om te stoppen): ").strip()
            if choice.lower() == 'q':
                sys.exit(0)

            idx = int(choice)

            if idx == 1:
                return 'new', None

            if folders and 1 < idx <= len(folders) + 1:
                return 'existing', folders[idx - 2]

            print("Ongeldig nummer, probeer opnieuw.")
        except ValueError:
            print("Voer een geldig nummer in.")


def main():
    """Hoofdfunctie."""
    # Laad environment variables uit .env (optioneel)
    env_file = SCRIPT_DIR / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"\'')

    # Keuze: Nieuw of Bestaand
    mode, folder = select_startup_mode()

    if mode == 'new':
        user_input = get_user_input()
        output_dir = create_output_directory(user_input['plaatsnaam'], user_input['datum'])
    else:
        output_dir = folder
        user_input = extract_user_input_from_folder(output_dir)
        print(f"\nGegevens geladen uit: {output_dir.name}")
        print(f"  Plaatsnaam: {user_input['plaatsnaam']}")
        print(f"  Gemeente:   {user_input['gemeente']}")
        print(f"  Datum:      {user_input['datum']}")
        if user_input.get('extra_context'):
             print(f"  Context:    {user_input['extra_context']}")

    print("\nGoogle GenAI Client (v1.0+) initialiseren...")
    client = get_gemini_client()

    print(f"Output directory: {output_dir}")

    print("\n" + "=" * 60)
    print(f"STARTEN MET MODEL: {MODEL_NAME}")
    print("=" * 60)

    # FASE 1: Eerst de liturgische context ophalen
    print("\n" + "─" * 60)
    print("FASE 1: Liturgische context verzamelen")
    print("─" * 60)

    first_analysis = build_first_analysis(user_input)

    # Check of bestand bestaat (JSON of MD)
    file_path_json = output_dir / f"{first_analysis['name']}.json"
    file_path_md = output_dir / f"{first_analysis['name']}.md"
    run_this = True
    kerkelijk_jaar_result = None

    if file_path_json.exists():
        overwrite = input(f"  {first_analysis['name']}.json bestaat al. Overschrijven? (j/n): ").strip().lower()
        if overwrite != 'j':
            run_this = False
            print(f"  Gebruik bestaande: {first_analysis['name']}.json")
            with open(file_path_json, "r", encoding="utf-8") as f:
                kerkelijk_jaar_result = json.load(f)
    elif file_path_md.exists():
        overwrite = input(f"  {first_analysis['name']}.md bestaat al (oud formaat). Opnieuw genereren als JSON? (j/n): ").strip().lower()
        if overwrite != 'j':
            run_this = False
            print(f"  Gebruik bestaande: {first_analysis['name']}.md (let op: oud formaat)")
            with open(file_path_md, "r", encoding="utf-8") as f:
                kerkelijk_jaar_result = {"_legacy_markdown": f.read()}

    if run_this:
        kerkelijk_jaar_result = run_analysis(
            client,
            first_analysis['prompt'],
            first_analysis['title']
        )
        
        # VERIFICATIE SLAG
        kerkelijk_jaar_result = verify_liedboek(client, kerkelijk_jaar_result)

        save_analysis(
            output_dir,
            first_analysis['name'],
            kerkelijk_jaar_result,
            first_analysis['title']
        )

    # Converteer JSON naar leesbare context string voor volgende analyses
    kerkelijk_jaar_context = json.dumps(kerkelijk_jaar_result, ensure_ascii=False, indent=2)

    # FASE 2: De overige analyses met de liturgische context
    print("\n" + "─" * 60)
    print("FASE 2: Contextanalyses met liturgische informatie")
    print("─" * 60)

    remaining_analyses = build_remaining_analyses(user_input, kerkelijk_jaar_context)
    all_analyses = [first_analysis] + remaining_analyses

    for analysis in remaining_analyses:
        file_path_json = output_dir / f"{analysis['name']}.json"
        file_path_md = output_dir / f"{analysis['name']}.md"

        if file_path_json.exists():
            overwrite = input(f"  {analysis['name']}.json bestaat al. Overschrijven? (j/n): ").strip().lower()
            if overwrite != 'j':
                print(f"  Overgeslagen: {analysis['name']}")
                continue
        elif file_path_md.exists():
            overwrite = input(f"  {analysis['name']}.md bestaat al (oud formaat). Opnieuw als JSON? (j/n): ").strip().lower()
            if overwrite != 'j':
                print(f"  Overgeslagen: {analysis['name']}")
                continue

        result = run_analysis(client, analysis['prompt'], analysis['title'])
        save_analysis(output_dir, analysis['name'], result, analysis['title'])

    print("\n" + "=" * 60)
    print("KLAAR")
    print(f"Locatie: {output_dir}")


if __name__ == "__main__":
    main()

