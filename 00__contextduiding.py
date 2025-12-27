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
import asyncio
from typing import Optional
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

# Probeer MCP client te importeren voor Neo4j integratie
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("WAARSCHUWING: 'mcp' library niet gevonden. MCP-gebaseerde liedsuggesties worden overgeslagen.")
    print("Installeer met: pip install mcp")

# Neo4j driver is niet meer nodig (we gebruiken MCP)
# Deze import check blijft alleen voor backward compatibility
NEO4J_AVAILABLE = False

# Configuratie
SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR / "output"
PROMPTS_DIR = SCRIPT_DIR / "prompts"

# Model keuze: Gemini 3 flash als primair, pro als fallback
#MODEL_NAME = "gemini-3-flash-preview"
MODEL_NAME = "gemini-3-pro-preview"
MODEL_NAME_FALLBACK = "gemini-3-pro-preview"


def normalize_scripture_reference(reference: str) -> str:
    """Normaliseer schriftverwijzingen door 'a'/'b' suffixen te verwijderen en
    cross-hoofdstuk referenties te splitsen.

    Voorbeelden:
        "Jesaja 8:23b-9:3" -> "Jesaja 8:23 en Jesaja 9:1-3"
        "Marcus 1:14a-15" -> "Marcus 1:14-15"
        "Genesis 2:4b" -> "Genesis 2:4"
    """
    if not reference or not isinstance(reference, str):
        return reference

    # Verwijder 'a' of 'b' achter versnummers
    # Pattern: cijfer gevolgd door 'a' of 'b'
    normalized = re.sub(r'(\d+)[ab]\b', r'\1', reference)

    # Detecteer cross-hoofdstuk referenties (bijv. "Jesaja 8:23-9:3")
    # Pattern: Boeknaam Hoofdstuk1:Vers1-Hoofdstuk2:Vers2
    cross_chapter_pattern = r'^((?:\d\s+)?[A-Za-zëïüéèöä]+(?:\s+[A-Za-zëïüéèöä]+)*)\s+(\d+):(\d+)[-–](\d+):(\d+)$'
    match = re.match(cross_chapter_pattern, normalized)

    if match:
        book = match.group(1)
        chapter1 = match.group(2)
        verse1 = match.group(3)
        chapter2 = match.group(4)
        verse2 = match.group(5)

        # Split in twee referenties
        # Eerste deel: van vers1 tot einde van hoofdstuk (we nemen aan dat hoofdstukken niet langer zijn dan 200 verzen)
        # Tweede deel: van begin van hoofdstuk2 tot vers2
        normalized = f"{book} {chapter1}:{verse1} en {book} {chapter2}:1-{verse2}"

    return normalized


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

    # Vervang voorbeeld placeholders (als er geen voorbeelden zijn, verwijder de placeholder)
    content = content.replace("{{voorbeeld_gebeden}}", "")
    content = content.replace("{{voorbeeld_preken}}", "")

    return content


def get_user_input() -> dict:
    """Vraag de gebruiker om de benodigde informatie."""
    print("\n" + "=" * 60)
    print("CONTEXTDUIDING VOOR PREEKVOORBEREIDING")
    print("Gebaseerd op de homiletische methodiek van De Leede & Stark")
    print("=" * 60 + "\n")

    print("Dit programma voert een uitgebreide hoordersanalyse uit voor uw preek.")
    print("Vul de volgende gegevens in:\n")

    plaatsnaam = input("1. Plaatsnaam: ").strip()
    if not plaatsnaam:
        print("FOUT: Plaatsnaam is verplicht.")
        sys.exit(1)

    gemeente = input("2. Naam van de kerk of het gebouw: ").strip()
    if not gemeente:
        print("FOUT: Naam is verplicht.")
        sys.exit(1)

    datum_str = input("3. Datum van de preek (bijv. 25 december 2025): ").strip()
    if not datum_str:
        print("FOUT: Datum is verplicht.")
        sys.exit(1)

    website = input("4. Website URL van de kerk (optioneel): ").strip()

    # Optionele extra context
    print("\n5. Eventuele extra context (optioneel, druk Enter om over te slaan):")
    print("   (bijv. bijzondere dienst, thema, doelgroep)")
    extra_context = input("   Extra context: ").strip()

    return {
        "plaatsnaam": plaatsnaam,
        "gemeente": gemeente,
        "datum": datum_str,
        "website": website,
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


def get_liturgical_calendar_data(datum_str: str) -> Optional[dict]:
    """Zoek de lezingen op in de lokale liturgische kalender JSON."""
    calendar_path = SCRIPT_DIR / "misc" / "liturgische_kalender_2025_2026.json"
    if not calendar_path.exists():
        print(f"WAARSCHUWING: Kalender niet gevonden op {calendar_path}")
        return None

    try:
        with open(calendar_path, "r", encoding="utf-8") as f:
            calendar_data = json.load(f)
        
        rooster = calendar_data.get("rooster", [])
        
        # Maanden mapping voor matching
        maanden = {
            'januari': 'jan', 'februari': 'feb', 'maart': 'mrt', 'april': 'apr',
            'mei': 'mei', 'juni': 'jun', 'juli': 'jul', 'augustus': 'aug',
            'september': 'sep', 'oktober': 'okt', 'november': 'nov', 'december': 'dec'
        }
        
        # Normalizeer gebruikersdatum (bijv. "4 januari 2026" -> "4 jan")
        datum_lower = datum_str.lower()
        search_day = ""
        search_month = ""
        
        parts = datum_lower.split()
        if len(parts) >= 2:
            search_day = parts[0]
            month_full = parts[1]
            search_month = maanden.get(month_full, month_full[:3])
        
        for entry in rooster:
            entry_date = entry.get("datum", "").lower()
            # Match dag en maand (simpele check)
            if search_day in entry_date and search_month in entry_date:
                # Extra check voor jaartal als dat in de kalender staat (bijv. '25 of '26)
                if "'26" in entry_date or "26" in entry_date:
                    if "2026" in datum_str or "26" in datum_str:
                        return entry
                elif "25" in entry_date:
                    if "2025" in datum_str or "25" in datum_str:
                        return entry
                else:
                    # Geen jaar in entry, match op dag/maand is genoeg
                    return entry
                    
    except Exception as e:
        print(f"Fout bij lezen kalender: {e}")
    
    return None


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
- **Adres:** {user_input.get('adres', 'Onbekend')}
- **Website:** {user_input.get('website', 'Geen')}
- **Datum:** {user_input['datum']}
"""
    if user_input.get('extra_context'):
        context_info += f"- **Extra context:** {user_input['extra_context']}\n"

    # Haal data uit de kalender
    kalender_data = get_liturgical_calendar_data(user_input['datum'])
    if kalender_data:
        context_info += f"""
## Vastgestelde Lezingen (uit liturgische kalender)
De volgende lezingen staan vast voor deze datum en MOETEN worden gebruikt:
- **Gelegenheid:** {kalender_data.get('gelegenheid')}
- **Eerste lezing:** {kalender_data.get('eerste_lezing')}
- **Tweede lezing (Epistel):** {kalender_data.get('tweede_lezing') or 'geen'}
- **Evangelie:** {kalender_data.get('evangelie')}
- **Psalm:** {kalender_data.get('psalm')}
- **Periode:** {kalender_data.get('periode')}
"""
        print(f"✓ Liturgische gegevens gevonden voor {user_input['datum']}: {kalender_data.get('gelegenheid')}")
    else:
        print(f"! Geen exacte match gevonden in liturgische kalender voor {user_input['datum']}. Model zal zelf zoeken.")

    task_prompt = load_prompt("01_zondag_kerkelijk_jaar.md", user_input)
    full_prompt = f"{base_prompt}\n\n{context_info}\n\n{task_prompt}"

    return {
        "name": "01_zondag_kerkelijk_jaar",
        "title": "Zondag van het Kerkelijk Jaar",
        "prompt": full_prompt
    }


def build_liedsuggesties_analysis(user_input: dict, kerkelijk_jaar_result: dict, context_samenvatting: str = "") -> dict:
    """Bouw de analyse voor liedsuggesties - MCP of legacy Neo4j.

    Deze functie bereidt de data voor maar voert GEEN queries meer uit.
    De queries worden uitgevoerd door Gemini via MCP in find_hymns_via_mcp().
    """
    if not MCP_AVAILABLE:
        return None

    # Haal lezingen en thema op
    lezingen_dict = {}
    if "lezingen" in kerkelijk_jaar_result:
        for k, v in kerkelijk_jaar_result["lezingen"].items():
            if isinstance(v, dict) and "referentie" in v:
                lezingen_dict[k] = v["referentie"]
            elif isinstance(v, str):
                lezingen_dict[k] = v

    thematiek = kerkelijk_jaar_result.get("thematiek")
    liturgische_periode = kerkelijk_jaar_result.get("positie_kerkelijk_jaar", {}).get("liturgische_periode")
    zondag_naam = kerkelijk_jaar_result.get("positie_kerkelijk_jaar", {}).get("zondag_naam", "Onbekend")

    return {
        "name": "08b_liedsuggesties_database",
        "title": "Passende Liederen",
        "lezingen": lezingen_dict,
        "thematiek": thematiek,
        "liturgische_periode": liturgische_periode,
        "zondag_naam": zondag_naam,
        "context_samenvatting": context_samenvatting,
        "use_mcp": MCP_AVAILABLE  # Flag om te bepalen welke methode te gebruiken
    }


def verify_church_location(client: genai.Client, user_input: dict) -> dict:
    """Zoek en verifieer het adres en website van de kerk."""
    print("\n" + "─" * 50)
    print("VERIFICATIE: Kerklocatie controleren...")
    print(f"{'─' * 50}")
    
    extra_info = ""
    if user_input.get('website'):
        extra_info = f"\nWebsite van de kerk: {user_input['website']}"
        print(f"Bezig met zoeken naar het adres van {user_input['gemeente']} in {user_input['plaatsnaam']} (gebruikmakend van {user_input['website']})...")
    else:
        print(f"Bezig met zoeken naar het adres van {user_input['gemeente']} in {user_input['plaatsnaam']}...")

    prompt = f"""
Zoek het exacte adres van de volgende kerk:
Kerk: {user_input['gemeente']}
Plaats: {user_input['plaatsnaam']}{extra_info}

Geef het antwoord als JSON:
{{
  "adres": "straat huisnummer, postcode plaats",
  "gebouw_naam": "naam van het kerkgebouw (indien van toepassing)",
  "website": "url van de kerk (indien gevonden)"
}}
"""

    max_retries = 1
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    response_mime_type="application/json"
                )
            )

            found_data = {"adres": "Onbekend", "website": "", "gebouw": ""}
            
            if response.text:
                data = extract_json(response.text)
                # Als extract_json een fout geeft, is het geen geldige JSON
                if "error" in data:
                    print(f"⚠ Locatie zoeken mislukt: ongeldige JSON (poging {attempt + 1})")
                    if attempt < max_retries:
                        continue
                else:
                    found_data["adres"] = data.get("adres", "Onbekend")
                    found_data["gebouw"] = data.get("gebouw_naam", "")
                    found_data["website"] = data.get("website", "")
                    
                    print(f"\nGevonden locatie:")
                    if found_data["gebouw"]:
                        print(f"  Gebouw:  {found_data['gebouw']}")
                    print(f"  Adres:   \033[1m{found_data['adres']}\033[0m")
                    if found_data["website"]:
                        print(f"  Website: {found_data['website']}")
                    
                    choice = input("\nIs dit het correcte adres? (j/n): ").strip().lower()
                    if choice in ('j', 'ja', 'y', 'yes'):
                        return found_data
                    
                    # Als gebruiker 'nee' zegt, heeft retrying geen zin, we vallen door naar handmatige input
                    break 
                
            else:
                print(f"⚠ Geen adres gevonden via Google Search (poging {attempt + 1})")
                if attempt < max_retries:
                    continue

        except Exception as e:
            print(f"⚠ Fout bij zoeken adres: {e} (poging {attempt + 1})")
            if attempt < max_retries:
                continue

    # Als niet gevonden, retries op, of niet correct bevonden door gebruiker
    correct_address = input("\nVoer het correcte adres in (Straat Huisnummer, Postcode Plaats): ").strip()
    correct_website = input("Voer de website in (optioneel): ").strip()
    return {"adres": correct_address, "website": correct_website, "gebouw": ""}


def build_remaining_analyses(user_input: dict, kerkelijk_jaar_context: str, church_address: str = "") -> list[dict]:
    """Bouw de overige analyses, inclusief de liturgische context.

    Args:
        user_input: De gebruikersinvoer (plaatsnaam, gemeente, datum)
        kerkelijk_jaar_context: De output van de eerste analyse (lezingen, etc.)
        church_address: Het geverifieerde adres van de kerk
    """
    base_prompt = load_prompt("base_prompt.md", user_input)

    # Context info nu inclusief de liturgische informatie
    context_info = f"""
## Preekgegevens
- **Plaatsnaam:** {user_input['plaatsnaam']}
- **Gemeente:** {user_input['gemeente']}
- **Adres:** {church_address}
- **Datum:** {user_input['datum']}
"""
    if user_input.get('extra_context'):
        context_info += f"- **Extra context:** {user_input['extra_context']}\n"

    # Voeg de liturgische context toe
    context_info += f"""
## Liturgische Context (uit eerder onderzoek)

{kerkelijk_jaar_context}
"""

    # De overige analyses (02-07)
    analysis_definitions = [
        ("02_sociaal_maatschappelijke_context", "Sociaal-Maatschappelijke Context"),
        ("03_waardenorientatie", "Waardenoriëntatie"),
        ("04_geloofsorientatie", "Geloofsoriëntatie"),
        ("05_interpretatieve_synthese", "Interpretatieve Synthese"),
        ("06_actueel_wereldnieuws", "Actueel Wereldnieuws"),
        ("07_politieke_orientatie", "Politieke Oriëntatie"),
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


def run_analysis(client: genai.Client, prompt: str, title: str, model: str = None) -> dict:
    """Voer een analyse uit met Taalmodel en Search. Retourneert JSON dict.

    Args:
        client: De Gemini client
        prompt: De prompt voor het model
        title: Titel van de analyse (voor logging)
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
            # Configuratie voor de generatie
            # We zetten safety filters UIT (BLOCK_NONE) omdat preekvoorbereiding
            # moet kunnen gaan over zonde, lijden, dood en religieus extremisme.
            response = client.models.generate_content(
                model=current_model,
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
        return run_analysis(client, prompt, title, model=MODEL_NAME_FALLBACK)

    # Als ook fallback mislukt, return error
    return {"error": f"Analyse mislukt na herpogingen (inclusief fallback)", "title": title}


def mcp_tool_to_gemini_function(tool) -> types.FunctionDeclaration:
    """Converteer MCP tool naar Gemini FunctionDeclaration.

    Verwijdert velden die Gemini API niet accepteert (zoals additionalProperties).
    """
    def clean_schema(schema):
        """Recursief cleanen van JSON Schema voor Gemini compatibiliteit."""
        if not isinstance(schema, dict):
            return schema

        # Maak een kopie om het origineel niet te wijzigen
        cleaned = {}

        for key, value in schema.items():
            # Skip velden die Gemini niet accepteert
            if key in ['additionalProperties', 'additional_properties', '$schema', '$id']:
                continue

            # Recursief cleanen van geneste objecten
            if isinstance(value, dict):
                cleaned[key] = clean_schema(value)
            elif isinstance(value, list):
                cleaned[key] = [clean_schema(item) if isinstance(item, dict) else item for item in value]
            else:
                cleaned[key] = value

        return cleaned

    # Haal input schema op en clean het
    parameters = tool.inputSchema if tool.inputSchema else {"type": "object", "properties": {}}
    cleaned_parameters = clean_schema(parameters)

    # Zorg dat minimaal vereiste velden aanwezig zijn
    if "type" not in cleaned_parameters:
        cleaned_parameters["type"] = "object"
    if "properties" not in cleaned_parameters:
        cleaned_parameters["properties"] = {}

    return types.FunctionDeclaration(
        name=tool.name,
        description=tool.description or f"Tool: {tool.name}",
        parameters=cleaned_parameters
    )


async def verify_hymn_numbers(session: ClientSession, hymn_data: dict) -> dict:
    """
    Verifieer alle liedbundelnummers in de gegenereerde JSON tegen de database.
    Retourneert een dict met:
    - verified_data: De geschoonde JSON (alleen correcte liederen)
    - errors: Lijst van fouten/hallucinaties
    """
    errors = []
    verified_data = {}

    # Kopieer de analyse sectie
    if "analyse" in hymn_data:
        verified_data["analyse"] = hymn_data["analyse"].copy()

    # Voor elke bundel
    for bundel_key in ["liedboek_2013", "hemelhoog", "op_toonhoogte", "weerklank", "weerklank_psalmen"]:
        if bundel_key not in hymn_data:
            continue

        verified_songs = []
        songs = hymn_data[bundel_key]

        for song in songs:
            nummer = song.get("nummer", "")
            titel = song.get("titel", "")

            if not nummer or not titel:
                errors.append(f"{bundel_key}: Lied zonder nummer of titel overgeslagen")
                continue

            # Query de database voor dit specifieke nummer
            # Gebruik de Song node properties die we kennen
            query = f"""
            MATCH (s:Song {{nummer: '{nummer}'}})
            RETURN s.nummer as nummer, s.titel as titel
            LIMIT 1
            """

            try:
                result = await session.call_tool("query", {"query": query})
                result_text = result.content[0].text if result.content else ""

                # Parse het resultaat (meestal JSON of text met de data)
                if result_text and titel in result_text:
                    # Nummer + titel combo klopt!
                    verified_songs.append(song)
                else:
                    # HALLUCINATIE GEDETECTEERD
                    errors.append(f"❌ HALLUCINATIE: {bundel_key} {nummer} '{titel}' bestaat niet in database")

            except Exception as e:
                errors.append(f"⚠ Verificatie fout voor {bundel_key} {nummer}: {str(e)}")
                # Bij twijfel: behoud het lied (voorzichtig)
                verified_songs.append(song)

        if verified_songs:
            verified_data[bundel_key] = verified_songs

    return {
        "verified_data": verified_data,
        "errors": errors
    }


async def find_hymns_via_mcp(
    client: genai.Client,
    lezingen: dict,
    thematiek: dict = None,
    liturgische_periode: str = None,
    zondag_naam: str = "Onbekend",
    context_samenvatting: str = ""
) -> dict:
    """
    Gebruik MCP om Gemini zelfstandig liederen te laten zoeken in de Neo4j database.

    Returns:
        dict met 'markdown_output' (string) en 'raw_response' (string)
    """
    if not MCP_AVAILABLE:
        return {
            "error": "MCP niet beschikbaar",
            "markdown_output": "MCP library niet geïnstalleerd. Installeer met: pip install mcp"
        }

    print(f"\n{'─' * 50}")
    print("MCP: Gemini zoekt zelfstandig liederen via Neo4j...")
    print(f"{'─' * 50}")

    # Neo4j configuratie
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    username = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password")
    database = os.environ.get("NEO4J_DATABASE", "hymns")

    # MCP server parameters
    # Gebruik @nibronix/mcp-neo4j-server - meest recente versie met auto-fix voor Cypher syntax
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

    # Bouw lezingen samenvatting
    lezingen_text = []
    for key, val in lezingen.items():
        if val and isinstance(val, dict) and "referentie" in val:
            lezingen_text.append(f"- {key}: {val['referentie']}")
        elif val and isinstance(val, str):
            lezingen_text.append(f"- {key}: {val}")
    lezingen_str = "\n".join(lezingen_text) if lezingen_text else "Geen lezingen beschikbaar"

    # Thematiek
    thema_str = ""
    if thematiek:
        centraal = thematiek.get("centraal_thema", "")
        stemming = thematiek.get("stemming", "")
        if centraal:
            thema_str += f"\n- Centraal thema: {centraal}"
        if stemming:
            thema_str += f"\n- Stemming: {stemming}"

    # Laad system instruction uit de prompt file
    try:
        prompt_path = PROMPTS_DIR / "01a_liedsuggesties.md"
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_instruction = f.read()
    except Exception as e:
        print(f"⚠ Fout bij laden prompt 01a_liedsuggesties.md: {e}")
        # Fallback naar een minimale instructie als bestand niet bestaat
        system_instruction = """Je bent een expert in kerkliederen. Gebruik MCP tools om liederen te zoeken in Neo4j.
        Gebruik expliciete velden in Cypher (s.nummer, s.titel). Geef JSON output."""

    # Gebruikersvraag - Alleen de feitelijke data, de instructies staan in de system_instruction (MD file)
    user_query = f"""Hieronder volgt de specifieke liturgische en maatschappelijke context voor de liedselectie:

**Zondag/Gelegenheid:** {zondag_naam}
**Liturgische periode:** {liturgische_periode or 'Onbekend'}

**Schriftlezingen:**
{lezingen_str}

**Thematiek:**{thema_str if thema_str else " Geen specifieke thematiek gegeven"}

**Context uit de hoordersanalyse (Maatschappij/Actualiteit):**
{context_samenvatting if context_samenvatting else 'Geen aanvullende context'}

Voer nu de zoektocht uit in de database zoals beschreven in je instructies."""

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialiseer MCP sessie
                await session.initialize()
                print("✓ MCP sessie geïnitialiseerd")

                # Haal tools op
                tools_result = await session.list_tools()
                mcp_tools = {tool.name: tool for tool in tools_result.tools}
                print(f"✓ Beschikbare tools: {list(mcp_tools.keys())}")

                # Converteer naar Gemini format
                print(f"  Converteren van {len(tools_result.tools)} MCP tools naar Gemini format...")
                gemini_tools = [
                    types.Tool(function_declarations=[mcp_tool_to_gemini_function(tool)])
                    for tool in tools_result.tools
                ]
                print(f"✓ Tools geconverteerd en klaar voor gebruik")

                # Conversation history
                messages = [
                    types.Content(role="user", parts=[types.Part(text=user_query)])
                ]

                # Agentic loop
                max_iterations = 15
                iteration = 0
                final_response = ""

                while iteration < max_iterations:
                    iteration += 1
                    print(f"  Iteratie {iteration}/{max_iterations}...")

                    try:
                        # Roep Gemini aan
                        # Voor de laatste iteratie (zonder function calls) forceren we JSON output
                        config_params = {
                            "tools": gemini_tools,
                            "system_instruction": system_instruction,
                            "temperature": 0.3,
                            "max_output_tokens": 8192,
                        }

                        # Als we al wat iteraties hebben gedaan, probeer JSON mode
                        if iteration > 3:
                            config_params["response_mime_type"] = "application/json"

                        response = client.models.generate_content(
                            model=MODEL_NAME,
                            contents=messages,
                            config=types.GenerateContentConfig(**config_params)
                        )

                        # Check response
                        if not response.candidates:
                            print("⚠ Geen candidates in response")
                            break

                        candidate = response.candidates[0]
                        if not candidate.content or not candidate.content.parts:
                            print("⚠ Geen content.parts in response")
                            break

                        parts = candidate.content.parts
                        has_function_call = False

                        for part in parts:
                            # Check voor tekst
                            if hasattr(part, 'text') and part.text:
                                final_response = part.text
                                print(f"  ✓ Gemini response ontvangen ({len(part.text)} chars)")

                            # Check voor function call
                            if hasattr(part, 'function_call') and part.function_call:
                                has_function_call = True
                                func_call = part.function_call
                                tool_name = func_call.name
                                tool_args = dict(func_call.args) if func_call.args else {}

                                print(f"  → Tool: {tool_name}")
                                if tool_args and 'query' in tool_args:
                                    # Toon query preview (eerste 100 chars)
                                    query_preview = str(tool_args['query'])[:100]
                                    print(f"    Query: {query_preview}...")

                                # Voer tool uit via MCP
                                try:
                                    result = await session.call_tool(tool_name, tool_args)
                                    tool_result = result.content[0].text if result.content else "Geen resultaat"
                                    print(f"    ✓ Resultaat: {len(tool_result)} chars")

                                except Exception as e:
                                    tool_result = f"Error: {str(e)}"
                                    print(f"    ✗ Tool error: {e}")

                                # Voeg model response en tool result toe aan messages
                                messages.append(types.Content(role="model", parts=parts))
                                messages.append(types.Content(
                                    role="user",
                                    parts=[types.Part(
                                        function_response=types.FunctionResponse(
                                            name=tool_name,
                                            response={"result": tool_result}
                                        )
                                    )]
                                ))
                                break  # Verwerk één tool call per iteratie

                        if not has_function_call:
                            # Geen tool calls meer, we zijn klaar
                            print("✓ Gemini heeft zoektocht afgerond")
                            break

                    except Exception as iter_error:
                        print(f"  ✗ Error in iteratie {iteration}: {iter_error}")
                        import traceback
                        traceback.print_exc()
                        # Als het een kritieke error is, stop dan
                        if iteration == 1:
                            raise
                        break

                # Probeer JSON te parsen uit de response
                try:
                    # Als het al valid JSON is
                    result_json = json.loads(final_response)
                    print(f"✓ Valide JSON ontvangen met {result_json.get('analyse', {}).get('aantal_gevonden_totaal', 0)} liederen")

                    # 🔍 VERIFICATIE STAP: Controleer alle liedbundelnummers
                    print(f"\n{'─' * 50}")
                    print("🔍 VERIFICATIE: Controleren van liedbundelnummers...")
                    print(f"{'─' * 50}")
                    verification = await verify_hymn_numbers(session, result_json)

                    if verification["errors"]:
                        print("\n⚠️  HALLUCINATIES GEDETECTEERD:")
                        for error in verification["errors"]:
                            print(f"  {error}")
                        print(f"\n✓ Geschoonde data bevat nu alleen geverifieerde liederen")
                    else:
                        print("✓ Alle liederen geverifieerd - geen hallucinaties gevonden!")

                    return {
                        **verification["verified_data"],
                        "_meta": {
                            "iterations": iteration,
                            "raw_response": final_response,
                            "verification_errors": verification["errors"],
                            "original_data": result_json  # Bewaar origineel voor debugging
                        }
                    }
                except json.JSONDecodeError:
                    # Probeer JSON uit markdown code block te halen
                    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', final_response, re.DOTALL)
                    if json_match:
                        try:
                            result_json = json.loads(json_match.group(1))
                            print(f"✓ JSON geëxtraheerd uit markdown")

                            # 🔍 VERIFICATIE STAP: Controleer alle liedbundelnummers
                            print(f"\n{'─' * 50}")
                            print("🔍 VERIFICATIE: Controleren van liedbundelnummers...")
                            print(f"{'─' * 50}")
                            verification = await verify_hymn_numbers(session, result_json)

                            if verification["errors"]:
                                print("\n⚠️  HALLUCINATIES GEDETECTEERD:")
                                for error in verification["errors"]:
                                    print(f"  {error}")
                                print(f"\n✓ Geschoonde data bevat nu alleen geverifieerde liederen")
                            else:
                                print("✓ Alle liederen geverifieerd - geen hallucinaties gevonden!")

                            return {
                                **verification["verified_data"],
                                "_meta": {
                                    "iterations": iteration,
                                    "raw_response": final_response,
                                    "verification_errors": verification["errors"],
                                    "original_data": result_json  # Bewaar origineel voor debugging
                                }
                            }
                        except json.JSONDecodeError:
                            pass

                    # Als JSON parsing mislukt, return als markdown met error
                    print(f"⚠ Kon geen JSON parsen, return als markdown")
                    return {
                        "error": "Geen valide JSON ontvangen",
                        "markdown_output": final_response,
                        "iterations": iteration
                    }

    except Exception as e:
        error_msg = f"MCP fout: {str(e)}"
        print(f"✗ {error_msg}")
        return {
            "error": error_msg,
            "markdown_output": f"Fout bij MCP zoektocht: {error_msg}"
        }


def choice_is_yes(choice: str) -> bool:
    """Helper om ja/nee input te parsen."""
    return choice.lower() in ('j', 'ja', 'y', 'yes')


def print_liturgy_summary(data: dict):
    """Print een samenvatting van de gevonden liturgie voor verificatie."""
    print("\n" + "═" * 60)
    print("VERIFICATIE LITURGISCH ROOSTER")
    print("═" * 60)
    
    # Zondag naam
    zondag = data.get("traditionele_naam", {}).get("nederlandse_vertaling", "Onbekend")
    if data.get("bijzondere_zondag_pkn", {}).get("is_bijzonder"):
        zondag += f" ({data['bijzondere_zondag_pkn']['naam']})"
    print(f"Zondag:   \033[1m{zondag}\033[0m")
    
    # Lezingen
    lezingen = data.get("lezingen", {})
    evangelie = lezingen.get("evangelie", {}).get("referentie", "-")
    oud_test = lezingen.get("eerste_lezing", {}).get("referentie", "-")
    epistel = lezingen.get("epistel", {}).get("referentie", "-")
    psalm = lezingen.get("psalm", {}).get("referentie", "-")
    
    print(f"Evangelie:\033[1m {evangelie} \033[0m")
    print(f"1e Lezing: {oud_test}")
    print(f"Epistel:   {epistel}")
    print(f"Psalm:     {psalm}")
    print("─" * 60)


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


def list_output_folders() -> list[Path]:
    """Lijst alle beschikbare output folders."""
    if not OUTPUT_DIR.exists():
        return []

    folders = []
    for item in OUTPUT_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            # Controleer of er een geldig bestand bestaat
            # Nieuwe structuur: 00_meta.json of 01_zondag...
            # Oude structuur: 00_zondag...
            if ((item / "00_meta.json").exists() or
                (item / "01_zondag_kerkelijk_jaar.json").exists() or
                (item / "00_zondag_kerkelijk_jaar.json").exists() or
                (item / "00_zondag_kerkelijk_jaar.md").exists() or
                (item / "00_overzicht.json").exists() or
                (item / "00_overzicht.md").exists()):
                folders.append(item)

    return sorted(folders, key=lambda x: x.stat().st_mtime, reverse=True)


def extract_user_input_from_folder(folder: Path) -> dict:
    """Probeer alle gebruikersinvoer te extraheren uit bestaande analyses in de folder."""
    user_input = {"plaatsnaam": "", "gemeente": "", "datum": "", "extra_context": "", "adres": "", "website": ""}

    # 1. Check specifieke meta file (Nieuwste standaard)
    meta_file = folder / "00_meta.json"
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 00_meta.json bevat direct de user_input velden
                for key in user_input:
                    if data.get(key):
                        user_input[key] = data[key]
                return user_input
        except (json.JSONDecodeError, KeyError):
            pass

    # 2. Zoek in alle JSON bestanden naar _meta.user_input (meest betrouwbare bron voor legacy)
    for json_path in sorted(folder.glob("*.json")):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            meta_input = data.get("_meta", {}).get("user_input")
            if meta_input:
                # Update onze dict met gevonden waarden
                for key in user_input:
                    if meta_input.get(key):
                        user_input[key] = meta_input[key]
                
                # Als we de belangrijkste velden hebben, kunnen we stoppen
                if user_input["plaatsnaam"] and user_input["adres"]:
                    return user_input
        except (json.JSONDecodeError, KeyError):
            continue

    # 2. Fallback: Probeer uit JSON overzicht (oud formaat)
    overzicht_json = folder / "00_overzicht.json"
    if overzicht_json.exists():
        try:
            with open(overzicht_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            gegevens = data.get("gegevens", {})
            user_input["plaatsnaam"] = gegevens.get("plaatsnaam", user_input["plaatsnaam"])
            user_input["gemeente"] = gegevens.get("gemeente", user_input["gemeente"])
            user_input["datum"] = gegevens.get("datum_preek", user_input["datum"])
            user_input["extra_context"] = gegevens.get("extra_context", user_input["extra_context"])
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
            elif "**Extra context:**" in line:
                user_input["extra_context"] = line.split("**Extra context:**")[-1].strip()

    # 4. Fallback: gebruik foldernaam voor plaatsnaam
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
            if (folder / "00_meta.json").exists():
                existing.append("00(meta)")

            for num in range(1, 8):  # 01-07
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

    # LOGS DIRECTORY AANMAKEN
    LOGS_DIR = output_dir / "logs"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    print("\nGoogle GenAI Client (v1.0+) initialiseren...")
    client = get_gemini_client()

    print(f"Output directory: {output_dir}")
    
    # VERIFICATIE KERKLOCATIE (DIRECT BIJ START)
    # We doen dit altijd als we in 'new' mode zijn, of als het adres nog niet bekend is.
    if mode == 'new' or not user_input.get("adres"):
        location_data = verify_church_location(client, user_input)
        user_input.update(location_data)
    else:
        print(f"  Adres:      {user_input.get('adres')}")
        if user_input.get('website'):
            print(f"  Website:    {user_input.get('website')}")

    # SLA META DATA OP (00_meta.json)
    meta_path = output_dir / "00_meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(user_input, f, ensure_ascii=False, indent=2)
    print(f"  Metadata opgeslagen: 00_meta.json")

    print("\n" + "=" * 60)
    print(f"STARTEN MET MODEL: {MODEL_NAME}")
    print("=" * 60)

    # FASE 1: Liturgische context verzamelen
    print("\n" + "─" * 60)
    print("FASE 1: Liturgische context verzamelen")
    print("─" * 60)

    first_analysis = build_first_analysis(user_input)

    # Check of bestand bestaat (JSON of MD)
    file_path_json = output_dir / f"{first_analysis['name']}.json"
    run_this = True
    kerkelijk_jaar_result = None

    if file_path_json.exists():
        overwrite = input(f"  {first_analysis['name']}.json bestaat al. Overschrijven? (j/n): ").strip().lower()
        if overwrite != 'j':
            run_this = False
            print(f"  Gebruik bestaande: {first_analysis['name']}.json")
            with open(file_path_json, "r", encoding="utf-8") as f:
                kerkelijk_jaar_result = json.load(f)

    if run_this:
        # LOG DE PROMPT
        save_log(LOGS_DIR, first_analysis['name'], first_analysis['prompt'])

        kerkelijk_jaar_result = run_analysis(
            client,
            first_analysis['prompt'],
            first_analysis['title']
        )
        
        save_analysis(
            output_dir,
            first_analysis['name'],
            kerkelijk_jaar_result,
            first_analysis['title'],
            user_input
        )

    # Converteer JSON naar leesbare context string voor volgende analyses

    # FASE 2: De overige analyses met de liturgische context
    print("\n" + "─" * 60)
    print("FASE 2: Contextanalyses met liturgische informatie")
    print("─" * 60)
    
    # We moeten de context opnieuw opbouwen als we een bestaand resultaat hebben ingeladen
    if not kerkelijk_jaar_result:
         # Fallback, zou niet moeten gebeuren als run_this=False correct werkt met laden
         print("FOUT: Geen liturgische context beschikbaar.")
         sys.exit(1)
         
    # Converteer JSON resultaat naar string voor context
    kerkelijk_jaar_context = json.dumps(kerkelijk_jaar_result, ensure_ascii=False, indent=2)

    remaining_analyses = build_remaining_analyses(user_input, kerkelijk_jaar_context, user_input.get("adres", ""))
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

        # LOG DE PROMPT
        save_log(LOGS_DIR, analysis['name'], analysis['prompt'])

        result = run_analysis(client, analysis['prompt'], analysis['title'])
        save_analysis(output_dir, analysis['name'], result, analysis['title'], user_input)

    # FASE 3: Liedsuggesties uit Database (met volledige context)
    print("\n" + "─" * 60)
    print("FASE 3: Liedsuggesties uit Database (MCP)")
    print("─" * 60)

    if MCP_AVAILABLE:
        # Verzamel context uit alle gegenereerde bestanden
        context_parts = []
        for analysis in remaining_analyses:
            json_path = output_dir / f"{analysis['name']}.json"
            if json_path.exists():
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # We pakken de samenvatting of relevante secties als die bestaan
                        # Dit is afhankelijk van de JSON structuur per analyse
                        if "samenvatting" in data:
                            context_parts.append(f"### {analysis['title']}\n{data['samenvatting']}")
                        elif "kernpunten" in data:
                            context_parts.append(f"### {analysis['title']}\n" + "\n".join(f"- {p}" for p in data['kernpunten']))
                        # Fallback: dump de hele content (beperkt)
                        else:
                            # Filter meta keys
                            clean_data = {k:v for k,v in data.items() if not k.startswith("_")}
                            context_parts.append(f"### {analysis['title']}\n{str(clean_data)[:500]}...")
                except Exception as e:
                    print(f"⚠ Fout bij lezen context {analysis['name']}: {e}")

        context_samenvatting = "\n\n".join(context_parts)

        lied_analysis = build_liedsuggesties_analysis(user_input, kerkelijk_jaar_result, context_samenvatting)
        if lied_analysis:
            # Check of bestand al bestaat
            file_path_json = output_dir / f"{lied_analysis['name']}.json"
            run_lied_analysis = True

            if file_path_json.exists():
                overwrite = input(f"  {lied_analysis['name']}.json bestaat al. Overschrijven? (j/n): ").strip().lower()
                if overwrite != 'j':
                    print(f"  Overgeslagen: {lied_analysis['name']}")
                    run_lied_analysis = False

            if run_lied_analysis:
                if lied_analysis.get('use_mcp'):
                    # MCP-based agentic search - Gemini zoekt zelfstandig
                    print(f"  Gebruikt MCP voor zelfstandige database exploratie...")
                    try:
                        lied_result = asyncio.run(
                            find_hymns_via_mcp(
                                client=client,
                                lezingen=lied_analysis['lezingen'],
                                thematiek=lied_analysis['thematiek'],
                                liturgische_periode=lied_analysis['liturgische_periode'],
                                zondag_naam=lied_analysis['zondag_naam'],
                                context_samenvatting=lied_analysis['context_samenvatting']
                            )
                        )

                        # Sla resultaat op
                        save_analysis(
                            output_dir,
                            lied_analysis['name'],
                            lied_result,
                            lied_analysis['title'],
                            user_input
                        )
                    except Exception as e:
                        print(f"✗ MCP zoektocht gefaald: {e}")
                        print(f"  Liedsuggesties worden overgeslagen.")
                        # Sla error op
                        error_result = {"error": str(e), "message": "MCP zoektocht mislukt"}
                        save_analysis(output_dir, lied_analysis['name'], error_result, lied_analysis['title'], user_input)

                else:
                    # MCP niet beschikbaar
                    print(f"  MCP niet beschikbaar. Installeer met: pip install mcp")
                    error_result = {"error": "MCP niet geïnstalleerd", "message": "Installeer met: pip install mcp"}
                    save_analysis(output_dir, lied_analysis['name'], error_result, lied_analysis['title'], user_input)

    print("\n" + "=" * 60)
    print("KLAAR")
    print(f"Locatie: {output_dir}")


if __name__ == "__main__":
    main()

