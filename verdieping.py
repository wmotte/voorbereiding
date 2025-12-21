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

# Configuratie
SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR / "output"
PROMPTS_DIR = SCRIPT_DIR / "prompts"

MODEL_NAME = "gemini-3-flash-preview"


def load_prompt(filename: str, user_input: dict) -> str:
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

    return content


def list_output_folders() -> list[Path]:
    """Lijst alle beschikbare output folders."""
    if not OUTPUT_DIR.exists():
        return []

    folders = []
    for item in OUTPUT_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            # Controleer of er een 00_zondag_kerkelijk_jaar.md bestaat
            if (item / "00_zondag_kerkelijk_jaar.md").exists():
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
    print("VERDIEPING: EXEGESE EN KUNST/CULTUUR")
    print("=" * 60)
    print("\nBeschikbare analyses:\n")

    for i, folder in enumerate(folders, 1):
        # Tel bestaande analyses
        existing = []
        for num in range(14):
            pattern = f"{num:02d}_*.md"
            if list(folder.glob(pattern)):
                existing.append(f"{num:02d}")

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
    """Lees alle vorige analyses uit de folder."""
    analyses = {}

    # Bestanden die we willen lezen
    files_to_read = [
        ("00_zondag_kerkelijk_jaar.md", "liturgische_context"),
        ("01_sociaal_maatschappelijke_context.md", "sociaal_maatschappelijk"),
        ("02_waardenorientatie.md", "waardenorientatie"),
        ("03_geloofsorientatie.md", "geloofsorientatie"),
        ("04_interpretatieve_synthese.md", "synthese"),
        ("05_actueel_wereldnieuws.md", "wereldnieuws"),
        ("06_politieke_orientatie.md", "politieke_orientatie"),
        ("07_exegese.md", "exegese"),
        ("08_kunst_cultuur.md", "kunst_cultuur"),
        ("09_focus_en_functie.md", "focus_en_functie"),
        ("10_kalender.md", "kalender"),
        ("11_representatieve_hoorders.md", "representatieve_hoorders"),
        ("12_homiletische_analyse.md", "homiletische_analyse"),
        ("13_gebeden.md", "gebeden"),
    ]

    for filename, key in files_to_read:
        filepath = folder / filename
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                analyses[key] = f.read()
        else:
            analyses[key] = ""

    return analyses


def extract_user_input_from_folder(folder: Path) -> dict:
    """Probeer plaatsnaam, gemeente en datum te extraheren uit de foldernaam of overzicht."""
    # Probeer uit overzicht.md
    overzicht = folder / "00_overzicht.md"
    user_input = {"plaatsnaam": "", "gemeente": "", "datum": ""}

    if overzicht.exists():
        with open(overzicht, "r", encoding="utf-8") as f:
            content = f.read()

        for line in content.split("\n"):
            if "**Plaatsnaam:**" in line:
                user_input["plaatsnaam"] = line.split("**Plaatsnaam:**")[-1].strip()
            elif "**Gemeente:**" in line:
                user_input["gemeente"] = line.split("**Gemeente:**")[-1].strip()
            elif "**Datum" in line:
                # Datum preek: of Datum:
                parts = line.split(":**")
                if len(parts) > 1:
                    user_input["datum"] = parts[-1].strip()

    # Fallback: gebruik foldernaam
    if not user_input["plaatsnaam"]:
        parts = folder.name.split("_")
        if parts:
            user_input["plaatsnaam"] = parts[0]

    return user_input


def get_gemini_client() -> genai.Client:
    """Initialiseer de Gemini Client."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        print("\nFOUT: Geen API key gevonden.")
        print("Stel de GEMINI_API_KEY environment variable in.")
        sys.exit(1)

    return genai.Client(api_key=api_key)


def build_context_string(previous_analyses: dict, limited: bool = False) -> str:
    """Bouw een context string van vorige analyses.

    Args:
        previous_analyses: Dictionary met alle analyses
        limited: Als True, alleen sociaal-maatschappelijke context voor hoordersprofielen
    """
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

    if previous_analyses.get("wereldnieuws"):
        sections.append("## Actueel Wereldnieuws\n\n" +
                       previous_analyses["wereldnieuws"])

    if previous_analyses.get("politieke_orientatie"):
        sections.append("## Politieke Oriëntatie\n\n" +
                       previous_analyses["politieke_orientatie"])

    if previous_analyses.get("exegese"):
        sections.append("## Exegese\n\n" +
                       previous_analyses["exegese"])

    if previous_analyses.get("kunst_cultuur"):
        sections.append("## Kunst en Cultuur\n\n" +
                       previous_analyses["kunst_cultuur"])

    if previous_analyses.get("focus_en_functie"):
        sections.append("## Focus en Functie\n\n" +
                       previous_analyses["focus_en_functie"])

    if previous_analyses.get("kalender"):
        sections.append("## Kalender\n\n" +
                       previous_analyses["kalender"])

    if previous_analyses.get("representatieve_hoorders"):
        sections.append("## Representatieve Hoorders\n\n" +
                       previous_analyses["representatieve_hoorders"])

    if previous_analyses.get("homiletische_analyse"):
        sections.append("## Homiletische Analyse\n\n" +
                       previous_analyses["homiletische_analyse"])

    if previous_analyses.get("gebeden"):
        sections.append("## Gebeden\n\n" +
                       previous_analyses["gebeden"])

    return "\n\n---\n\n".join(sections)


def run_analysis(client: genai.Client, prompt: str, title: str, temperature: float = 0.2) -> str:
    """Voer een analyse uit met Gemini en Google Search."""
    print(f"\n{'─' * 50}")
    print(f"Analyseren: {title}")
    print(f"{'─' * 50}")
    print("Bezig met redeneren en zoeken...")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
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
            print(f"✓ Analyse '{title}' voltooid")
            return response.text
        else:
            print(f"✗ Geen tekst ontvangen voor '{title}'")
            return f"# {title}\n\nGeen analyse beschikbaar."

    except Exception as e:
        error_msg = f"Fout bij analyse '{title}': {str(e)}"
        print(f"✗ {error_msg}")
        return f"# {title}\n\n**Fout:** {error_msg}"


def verify_kunst_cultuur(client: genai.Client, content: str) -> str:
    """Verificeer alle bronnen in de kunst/cultuur output en verwijder niet-verifieerbare items."""
    print(f"\n{'─' * 50}")
    print("VERIFICATIE: Bronnen controleren...")
    print(f"{'─' * 50}")
    print("Bezig met verifiëren van films, boeken en kunstwerken...")

    verification_prompt = """Je bent een strenge factchecker. Je taak is om de onderstaande tekst te controleren op niet-bestaande bronnen.

## Instructies

1. Doorloop ELKE genoemde film, boek, kunstwerk, muziekstuk en andere culturele verwijzing
2. Verifieer via Google Search of deze ECHT BESTAAT:
   - Bij films: controleer of de film bestaat met die titel, regisseur en jaar
   - Bij boeken: controleer of het boek bestaat met die auteur en titel
   - Bij kunstwerken: controleer of het kunstwerk bestaat van die kunstenaar
   - Bij muziek: controleer of het stuk bestaat van die componist/artiest

3. Als je een item NIET kunt verifiëren of als de details niet kloppen:
   - Verwijder het HELE item inclusief de beschrijving
   - Laat geen lege secties achter

4. Als je een item WEL kunt verifiëren maar details kloppen niet:
   - Corrigeer de details (bijv. verkeerd jaar, verkeerde regisseur)

5. Behoud de originele structuur en opmaak van de tekst

## BELANGRIJK
- Wees STRENG: bij twijfel, verwijderen
- Liever 3 geverifieerde items dan 6 waarvan 2 niet bestaan
- Verwijder GEEN zoektermen, die mogen blijven staan
- Geef de VOLLEDIGE gecorrigeerde tekst terug, niet alleen de wijzigingen
- Voeg GEEN meta-tekst toe zoals "Ik heb de tekst gecontroleerd..." of "Hieronder volgt de tekst..."
- Begin DIRECT met de inhoud (de titel van het document), zonder inleiding

## Te controleren tekst:

"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=verification_prompt + content,
            config=types.GenerateContentConfig(
                temperature=0.1,  # Zeer laag voor maximale precisie
                top_p=0.85,
                top_k=20,
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
            print("✓ Verificatie voltooid - niet-verifieerbare items verwijderd")
            return response.text
        else:
            print("✗ Verificatie mislukt - originele tekst behouden")
            return content

    except Exception as e:
        print(f"✗ Verificatie fout: {str(e)} - originele tekst behouden")
        return content


def save_analysis(output_dir: Path, filename: str, content: str, title: str):
    """Sla een analyse op naar een markdown bestand."""
    filepath = output_dir / f"{filename}.md"

    if not content.strip().startswith("#"):
        content = f"# {title}\n\n{content}"

    # 1. Zorg voor een lege regel VÓÓR elke kop (behalve de allereerste regel)
    content = re.sub(r'([^\n])\n(#+ .*)', r'\1\n\n\2', content)
    
    # 2. Zorg voor een lege regel NA elke kop
    content = re.sub(r'^(#+ .*)\n+(?=[^\n])', r'\1\n\n', content, flags=re.MULTILINE)
    
    # 3. Zorg voor een lege regel rondom scheidingslijnen (---)
    content = re.sub(r'([^\n])\n(---)', r'\1\n\n\2', content)
    content = re.sub(r'(---)\n+(?=[^\n])', r'\1\n\n', content)

    # 4. Zorg dat bullet points op een nieuwe regel staan als ze direct na een dubbele punt of zin komen
    content = re.sub(r'([:.:])\s*(\n*)\s*([\*\-] )', r'\1\n\n\3', content)

    # 5. Zorg voor een lege regel NA bold koppen (bijv. **Titel**) als er bullet points volgen
    content = re.sub(r'(\*\*[^*]+\*\*)\n([\*\-] )', r'\1\n\n\2', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Opgeslagen: {filepath.name}")


def update_summary(output_dir: Path):
    """Update het overzichtsbestand met de nieuwe analyses."""
    overzicht_path = output_dir / "00_overzicht.md"

    if not overzicht_path.exists():
        return

    with open(overzicht_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Voeg nieuwe analyses toe als ze nog niet in het overzicht staan
    new_analyses = [
        ("07_exegese", "Exegese van de Schriftlezingen"),
        ("08_kunst_cultuur", "Kunst, Cultuur en Film"),
        ("09_focus_en_functie", "Focus en Functie"),
        ("10_kalender", "Kalender"),
        ("11_representatieve_hoorders", "Representatieve Hoorders"),
        ("12_homiletische_analyse", "Homiletische Analyse (Lowry's Plot)"),
        ("13_gebeden", "Gebeden voor de Eredienst"),
    ]

    for name, title in new_analyses:
        if (output_dir / f"{name}.md").exists() and f"[{title}]" not in content:
            # Zoek het einde van de analyses sectie
            if "## Analyses" in content:
                # Voeg toe aan het einde van de analyses lijst
                content = content.rstrip()
                content += f"\n- [{title}]({name}.md)\n"

    with open(overzicht_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    """Hoofdfunctie."""
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

    bijbelteksten_map = download_lezingen(folder, previous_analyses["liturgische_context"])

    if bijbelteksten_map:
        print(f"\n✓ {len(bijbelteksten_map)} bijbeltekst(en) opgehaald en opgeslagen")
    else:
        print("\n! Geen bijbelteksten kunnen ophalen (exegese gaat door zonder grondtekst)")

    # Laad de bijbelteksten voor de context
    bijbelteksten = laad_bijbelteksten(folder)

    # Initialiseer client
    print("\nGoogle GenAI Client initialiseren...")
    client = get_gemini_client()

    # Bouw context (inclusief bijbelteksten)
    context_string = build_context_string(previous_analyses)

    # Voeg bijbelteksten toe aan de context
    if bijbelteksten:
        context_string += f"""

---

## Bijbelteksten (Naardense Bijbel - Pieter Oussoren)

{bijbelteksten}
"""

    # Laad prompts
    base_prompt = load_prompt("base_prompt.md", user_input)

    # Analyses uitvoeren
    print("\n" + "=" * 60)
    print(f"VERDIEPING STARTEN MET MODEL: {MODEL_NAME}")
    print("=" * 60)

    analysis_definitions = [
        ("07_exegese", "Exegese van de Schriftlezingen"),
        ("08_kunst_cultuur", "Kunst, Cultuur en Film"),
        ("09_focus_en_functie", "Focus en Functie"),
        ("10_kalender", "Kalender: Gedenkdagen en Bijzondere Momenten"),
        ("11_representatieve_hoorders", "Representatieve Hoorders"),
        ("12_homiletische_analyse", "Homiletische Analyse (Lowry's Plot)"),
        ("13_gebeden", "Gebeden voor de Eredienst"),
    ]

    # Mapping van oude naar nieuwe bestandsnamen (voor backwards compatibility)
    old_to_new = {
        "07_exegese": "06_exegese",
        "08_kunst_cultuur": "07_kunst_cultuur",
        "09_focus_en_functie": "08_focus_en_functie",
    }

    for name, title in analysis_definitions:
        # Controleer of analyse al bestaat (nieuwe of oude nummering)
        existing_file = None
        if (folder / f"{name}.md").exists():
            existing_file = f"{name}.md"
        elif name in old_to_new and (folder / f"{old_to_new[name]}.md").exists():
            existing_file = f"{old_to_new[name]}.md"

        if existing_file:
            overwrite = input(f"\n{existing_file} bestaat al. Overschrijven? (j/n): ").strip().lower()
            if overwrite != 'j':
                print(f"  Overgeslagen: {name}")
                continue

        # Bouw prompt
        task_prompt = load_prompt(f"{name}.md", user_input)

        # Voor representatieve hoorders: beperkte context (geen exegese, kunst, kalender)
        if name == "11_representatieve_hoorders":
            analysis_context = build_context_string(previous_analyses, limited=True)
        else:
            analysis_context = context_string

        full_prompt = f"""{base_prompt}

# Eerdere Analyses (Context)

{analysis_context}

---

# Huidige Opdracht

{task_prompt}
"""

        # Voer analyse uit (lage temperature voor kalender om hallucinaties te voorkomen)
        temp = 0.1 if name == "10_kalender" else 0.2
        result = run_analysis(client, full_prompt, title, temperature=temp)

        # Extra verificatiestap voor kunst_cultuur om hallucinaties te verwijderen
        if name == "08_kunst_cultuur":
            result = verify_kunst_cultuur(client, result)

        save_analysis(folder, name, result, title)

    # Update overzicht
    update_summary(folder)

    print("\n" + "=" * 60)
    print("KLAAR")
    print(f"Locatie: {folder}")
    print("=" * 60)


if __name__ == "__main__":
    main()
