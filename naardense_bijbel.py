#!/usr/bin/env python3
"""
Naardense Bijbel Tekstophaler

Dit module haalt bijbelteksten op van naardensebijbel.nl en slaat ze op als txt-bestanden.
De teksten worden gebruikt voor exegese in de preekvoorbereiding.

URL-structuur: https://www.naardensebijbel.nl/[boek]/[hoofdstuk]/?hfst=[hoofdstuk]

W.M. Otte (w.m.otte@umcutrecht.nl)
"""

import re
import time
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("FOUT: requests en beautifulsoup4 zijn vereist.")
    print("Installeer met: pip install requests beautifulsoup4")
    raise


@dataclass
class BijbelReferentie:
    """Een bijbelreferentie met boek, hoofdstuk en optioneel verzen."""
    boek: str
    hoofdstuk: int
    vers_start: Optional[int] = None
    vers_eind: Optional[int] = None

    def __str__(self) -> str:
        if self.vers_start and self.vers_eind:
            return f"{self.boek} {self.hoofdstuk}:{self.vers_start}-{self.vers_eind}"
        elif self.vers_start:
            return f"{self.boek} {self.hoofdstuk}:{self.vers_start}"
        else:
            return f"{self.boek} {self.hoofdstuk}"


# Mapping van Nederlandse boeknamen naar URL-slugs
BOEK_NAAR_SLUG = {
    # Oude Testament
    "genesis": "genesis",
    "exodus": "exodus",
    "leviticus": "leviticus",
    "numeri": "numeri",
    "deuteronomium": "deuteronomium",
    "jozua": "jozua",
    "rechters": "rechters",
    "ruth": "ruth",
    "1 samuel": "1-samuel",
    "2 samuel": "2-samuel",
    "1 koningen": "1-koningen",
    "2 koningen": "2-koningen",
    "1 kronieken": "1-kronieken",
    "2 kronieken": "2-kronieken",
    "ezra": "ezra",
    "nehemia": "nehemia",
    "ester": "ester",
    "job": "job",
    "psalm": "psalm",
    "psalmen": "psalm",
    "spreuken": "spreuken",
    "prediker": "prediker",
    "hooglied": "hooglied",
    "jesaja": "jesaja",
    "jeremia": "jeremia",
    "klaagliederen": "klaagliederen",
    "ezechiel": "ezechiel",
    "ezechiël": "ezechiel",
    "daniel": "daniel",
    "daniël": "daniel",
    "hosea": "hosea",
    "joel": "joel",
    "joël": "joel",
    "amos": "amos",
    "obadja": "obadja",
    "jona": "jona",
    "micha": "micha",
    "nahum": "nahum",
    "habakuk": "habakuk",
    "sefanja": "sefanja",
    "haggai": "haggai",
    "haggaï": "haggai",
    "zacharia": "zacharia",
    "maleachi": "maleachi",
    # Nieuwe Testament
    "matteus": "matteus",
    "matteüs": "matteus",
    "mattheüs": "matteus",
    "mattheus": "matteus",
    "marcus": "marcus",
    "lucas": "lucas",
    "johannes": "johannes",
    "handelingen": "handelingen",
    "romeinen": "romeinen",
    "1 korintiërs": "1-korintiers",
    "1 korintiers": "1-korintiers",
    "1 korinthiërs": "1-korintiers",
    "2 korintiërs": "2-korintiers",
    "2 korintiers": "2-korintiers",
    "2 korinthiërs": "2-korintiers",
    "galaten": "galaten",
    "efeze": "efeze",
    "efeziërs": "efeze",
    "filippenzen": "filippenzen",
    "kolossenzen": "kolossenzen",
    "1 tessalonicenzen": "1-tessalonicenzen",
    "2 tessalonicenzen": "2-tessalonicenzen",
    "1 timoteüs": "1-timoteus",
    "1 timoteus": "1-timoteus",
    "2 timoteüs": "2-timoteus",
    "2 timoteus": "2-timoteus",
    "titus": "titus",
    "filemon": "filemon",
    "hebreeën": "hebreeen",
    "hebreeen": "hebreeen",
    "jakobus": "jakobus",
    "1 petrus": "1-petrus",
    "2 petrus": "2-petrus",
    "1 johannes": "1-johannes",
    "2 johannes": "2-johannes",
    "3 johannes": "3-johannes",
    "judas": "judas",
    "openbaring": "openbaring",
}


def parse_bijbelreferentie(tekst: str) -> Optional[BijbelReferentie]:
    """
    Parse een bijbelreferentie string naar een BijbelReferentie object.

    Voorbeelden:
        "Jesaja 9:1-6" -> BijbelReferentie(boek="jesaja", hoofdstuk=9, vers_start=1, vers_eind=6)
        "Lucas 2:1-14 (15-20)" -> BijbelReferentie(boek="lucas", hoofdstuk=2, vers_start=1, vers_eind=20)
        "Psalm 96" -> BijbelReferentie(boek="psalmen", hoofdstuk=96)
        "Titus 2:11-14" -> BijbelReferentie(boek="titus", hoofdstuk=2, vers_start=11, vers_eind=14)
    """
    tekst = tekst.strip()

    # Verwijder optionele verzen tussen haakjes en neem het hoogste versnummer
    # bijv. "Lucas 2:1-14 (15-20)" -> we willen 1-20
    haakjes_match = re.search(r'\((\d+)[-–]?(\d+)?\)', tekst)
    extra_eind = None
    if haakjes_match:
        if haakjes_match.group(2):
            extra_eind = int(haakjes_match.group(2))
        else:
            extra_eind = int(haakjes_match.group(1))
        tekst = re.sub(r'\s*\([^)]+\)', '', tekst)

    # Pattern: Boek Hoofdstuk:Vers-Vers of Boek Hoofdstuk:Vers of Boek Hoofdstuk
    # Ondersteunt ook "1 Samuel", "2 Koningen", etc.
    pattern = r'^(\d?\s*[A-Za-zëïüéèöä]+)\s+(\d+)(?::(\d+)(?:[-–](\d+))?)?'
    match = re.match(pattern, tekst, re.IGNORECASE)

    if not match:
        return None

    boek = match.group(1).strip().lower()
    hoofdstuk = int(match.group(2))
    vers_start = int(match.group(3)) if match.group(3) else None
    vers_eind = int(match.group(4)) if match.group(4) else vers_start

    # Als er extra verzen in haakjes waren, neem het maximum
    if extra_eind and (vers_eind is None or extra_eind > vers_eind):
        vers_eind = extra_eind

    return BijbelReferentie(
        boek=boek,
        hoofdstuk=hoofdstuk,
        vers_start=vers_start,
        vers_eind=vers_eind
    )


def get_boek_slug(boek: str) -> Optional[str]:
    """Converteer een boeknaam naar de URL-slug."""
    boek_lower = boek.lower().strip()
    return BOEK_NAAR_SLUG.get(boek_lower)


def haal_vers_op(boek_slug: str, hoofdstuk: int, vers: int) -> Optional[str]:
    """
    Haal een enkel vers op van de Naardense Bijbel website.

    URL: https://www.naardensebijbel.nl/vers/[boek]-[hoofdstuk]-[vers]/

    Returns:
        De bijbeltekst als string, of None bij een fout.
    """
    url = f"https://www.naardensebijbel.nl/vers/{boek_slug}-{hoofdstuk}-{vers}/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    max_retries = 3
    for poging in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 404:
                return None  # Vers bestaat niet
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Verwijder navigatie, scripts, etc.
            for tag in soup.find_all(['nav', 'script', 'style', 'header', 'footer', 'aside']):
                tag.decompose()

            body = soup.find('body')
            if not body:
                return None

            # Haal de tekst op
            tekst = body.get_text(separator='\n', strip=True)

            # Extraheer alleen de bijbeltekst (na de titel, voor de navigatie)
            lines = tekst.split('\n')
            bijbel_lines = []
            in_tekst = False
            titel_gevonden = False

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Skip header/titel regels
                if 'Naardense Bijbel' in line:
                    continue
                if 'literaire vertaling' in line.lower():
                    continue
                if line == '>':
                    continue

                # Herken de titel (bijv. "Johannes – 1 : 1")
                if re.match(r'^[A-Za-zëïüéèöä\s\d]+ – \d+ : \d+$', line):
                    titel_gevonden = True
                    in_tekst = True
                    continue

                # Stop bij navigatie links
                if line.startswith('Lees ') or line.startswith('Bekijk '):
                    break

                if in_tekst:
                    bijbel_lines.append(line)

            return ' '.join(bijbel_lines) if bijbel_lines else None

        except (requests.ConnectionError, requests.Timeout, requests.exceptions.ChunkedEncodingError) as e:
            if poging < max_retries - 1:
                wait_time = (poging + 1) * 2
                print(f"  Fout bij ophalen {url}: {e}. Opnieuw proberen in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"  Fout bij ophalen {url} na {max_retries} pogingen: {e}")
                return None
        except requests.RequestException as e:
            print(f"  Fout bij ophalen {url}: {e}")
            return None


# Mapping van boeknamen naar booknummers voor de zoek-URL
BOEK_NAAR_NUMMER = {
    "genesis": 1, "exodus": 2, "leviticus": 3, "numeri": 4, "deuteronomium": 5,
    "jozua": 6, "rechters": 7, "ruth": 8, "1 samuel": 9, "2 samuel": 10,
    "1 koningen": 11, "2 koningen": 12, "1 kronieken": 13, "2 kronieken": 14,
    "ezra": 15, "nehemia": 16, "ester": 17, "job": 18, "psalm": 19, "psalmen": 19,
    "spreuken": 20, "prediker": 21, "hooglied": 22, "jesaja": 23, "jeremia": 24,
    "klaagliederen": 25, "ezechiel": 26, "ezechiël": 26, "daniel": 27, "daniël": 27,
    "hosea": 28, "joel": 29, "joël": 29, "amos": 30, "obadja": 31, "jona": 32,
    "micha": 33, "nahum": 34, "habakuk": 35, "sefanja": 36, "haggai": 37, "haggaï": 37,
    "zacharia": 38, "maleachi": 39,
    # Nieuwe Testament
    "matteus": 40, "matteüs": 40, "mattheüs": 40, "mattheus": 40,
    "marcus": 41, "lucas": 42, "johannes": 43, "handelingen": 44,
    "romeinen": 45, "1 korintiërs": 46, "1 korintiers": 46, "1 korinthiërs": 46,
    "2 korintiërs": 47, "2 korintiers": 47, "2 korinthiërs": 47,
    "galaten": 48, "efeze": 49, "efeziërs": 49, "efeziers": 49,
    "filippenzen": 50, "kolossenzen": 51,
    "1 tessalonicenzen": 52, "2 tessalonicenzen": 53,
    "1 timoteüs": 54, "1 timoteus": 54, "2 timoteüs": 55, "2 timoteus": 55,
    "titus": 56, "filemon": 57, "hebreeën": 58, "hebreeen": 58,
    "jakobus": 59, "1 petrus": 60, "2 petrus": 61,
    "1 johannes": 62, "2 johannes": 63, "3 johannes": 64,
    "judas": 65, "openbaring": 66,
}


def haal_verzen_via_zoek(boek: str, hoofdstuk: int, vers_start: int, vers_eind: int) -> Optional[str]:
    """
    Haal verzen op via de zoek-URL (fallback voor boeken zonder directe vers-URLs).

    Returns:
        De bijbeltekst als string, of None bij een fout.
    """
    boek_lower = boek.lower().strip()
    boek_nr = BOEK_NAAR_NUMMER.get(boek_lower)

    if not boek_nr:
        return None

    # Bouw de zoek-URL
    vers_range = f"{vers_start}-{vers_eind}" if vers_start != vers_eind else str(vers_start)
    url = (
        f"https://www.naardensebijbel.nl/"
        f"?search-class=DB_CustomSearch_Widget-db_customsearch_widget"
        f"&widget_number=preset-default&-0=vers"
        f"&cs-booknr-1={boek_nr}"
        f"&cs-bijbelhoofdstuk-2={hoofdstuk}"
        f"&cs-versnummer-3={vers_range}"
        f"&cs-bijbelvers_v2-4="
        f"&search=Zoeken"
    )

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
    }

    max_retries = 3
    for poging in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # De resultaten staan in een table
            table = soup.find('table')
            if not table:
                return None

            # Parse de tabel rij voor rij
            verzen = []
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    # Eerste cel is het versnummer, tweede cel is de tekst
                    vers_nr = cells[0].get_text(strip=True)
                    vers_tekst = cells[1].get_text(strip=True)

                    if vers_nr.isdigit() and vers_tekst:
                        verzen.append(f"**{hoofdstuk}:{vers_nr}** {vers_tekst}")

            return '\n\n'.join(verzen) if verzen else None

        except (requests.ConnectionError, requests.Timeout, requests.exceptions.ChunkedEncodingError) as e:
            if poging < max_retries - 1:
                wait_time = (poging + 1) * 2
                print(f"  Fout bij zoeken: {e}. Opnieuw proberen in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"  Fout bij zoeken na {max_retries} pogingen: {e}")
                return None
        except requests.RequestException as e:
            print(f"  Fout bij zoeken: {e}")
            return None


def haal_verzen_op(boek_slug: str, hoofdstuk: int, vers_start: int, vers_eind: int) -> Optional[str]:
    """
    Haal meerdere verzen op en combineer ze.

    Returns:
        De gecombineerde bijbeltekst als string, of None bij een fout.
    """
    verzen = []

    for vers in range(vers_start, vers_eind + 1):
        tekst = haal_vers_op(boek_slug, hoofdstuk, vers)
        if tekst:
            verzen.append(f"**{hoofdstuk}:{vers}** {tekst}")
        else:
            # Stop als we een vers niet kunnen vinden (einde hoofdstuk?)
            if vers == vers_start:
                return None  # Eerste vers niet gevonden
            break

        # Kleine pauze tussen requests
        time.sleep(0.2)

    return '\n\n'.join(verzen) if verzen else None


def haal_heel_hoofdstuk_op(boek_slug: str, hoofdstuk: int, max_verzen: int = 100) -> Optional[str]:
    """
    Haal een heel hoofdstuk op door alle verzen te downloaden.

    Returns:
        De bijbeltekst als string, of None bij een fout.
    """
    verzen = []
    vers = 1

    while vers <= max_verzen:
        tekst = haal_vers_op(boek_slug, hoofdstuk, vers)
        if tekst:
            verzen.append(f"**{hoofdstuk}:{vers}** {tekst}")
            vers += 1
            time.sleep(0.2)
        else:
            break  # Einde van het hoofdstuk

    return '\n\n'.join(verzen) if verzen else None


def haal_bijbeltekst_op(referentie: BijbelReferentie) -> Optional[str]:
    """
    Haal de bijbeltekst op voor een gegeven referentie.

    Probeert eerst de directe vers-URL, en valt terug op de zoek-URL indien nodig.

    Args:
        referentie: Een BijbelReferentie object

    Returns:
        De bijbeltekst als string, of None bij een fout.
    """
    slug = get_boek_slug(referentie.boek)

    print(f"  Ophalen: {referentie} ...")

    # Bepaal vers range
    vers_start = referentie.vers_start or 1
    vers_eind = referentie.vers_eind or referentie.vers_start

    # Voor hele hoofdstukken (geen versnummers), bepaal de range
    if not referentie.vers_start:
        if referentie.boek.lower() in ('psalm', 'psalmen') and referentie.hoofdstuk in PSALM_LENGTES:
            vers_eind = PSALM_LENGTES[referentie.hoofdstuk]
        else:
            vers_eind = 200  # Max voor hele hoofdstukken (bv Psalm 119)

    # Probeer eerst de directe vers-URL (sneller, minder server load)
    if slug:
        tekst = haal_verzen_op(slug, referentie.hoofdstuk, vers_start, vers_eind)
        if tekst:
            return tekst

    # Fallback: gebruik de zoek-URL
    print(f"    -> Fallback naar zoek-URL...")
    tekst = haal_verzen_via_zoek(referentie.boek, referentie.hoofdstuk, vers_start, vers_eind)
    if tekst:
        return tekst

    # Laatste poging: haal heel hoofdstuk op via directe URLs
    if slug and not referentie.vers_start:
        return haal_heel_hoofdstuk_op(slug, referentie.hoofdstuk)

    print(f"  Onbekend bijbelboek of kon niet ophalen: {referentie.boek}")
    return None


def extract_lezingen_uit_liturgie(liturgie_tekst: str) -> list[str]:
    """
    Extraheer bijbelreferenties uit de liturgische context tekst.

    Zoekt naar patronen als:
    - "Eerste lezing: Jesaja 9:1-6"
    - "Evangelielezing: Lucas 2:1-14 (15-20)"
    - "Psalm 96"
    - "Titus 2:11-14"
    """
    referenties = []

    # Patronen voor verschillende typen lezingen
    patronen = [
        r'(?:Eerste|Tweede|Derde)?\s*(?:lezing|Lezing)[:\s]+([A-Za-zëïüéèöä\d\s]+\d+:\d+(?:[-–]\d+)?(?:\s*\([^)]+\))?)',
        r'(?:Evangelie|Epistel)(?:lezing)?[:\s]+([A-Za-zëïüéèöä\d\s]+\d+:\d+(?:[-–]\d+)?(?:\s*\([^)]+\))?)',
        r'Psalm(?:\s+van\s+de\s+\w+)?[:\s]+(?:Psalm\s+)?(\d+)',
        r'\*\*(?:Eerste|Evangelie|Epistel)lezing:\*\*\s+([A-Za-zëïüéèöä\d\s]+\d+:\d+(?:[-–]\d+)?)',
    ]

    for patroon in patronen:
        matches = re.findall(patroon, liturgie_tekst, re.IGNORECASE)
        for match in matches:
            ref = match.strip()
            # Voeg "Psalm" toe als het alleen een nummer is
            if re.match(r'^\d+$', ref):
                ref = f"Psalm {ref}"
            if ref and ref not in referenties:
                referenties.append(ref)

    # Zoek ook naar losse bijbelreferenties in bullet points
    bullet_pattern = r'[-*]\s*\*?\*?([A-Za-zëïüéèöä]+(?:\s+\d)?)\s+(\d+):(\d+)(?:[-–](\d+))?(?:\s*\([^)]+\))?'
    for match in re.finditer(bullet_pattern, liturgie_tekst):
        boek = match.group(1).strip()
        hoofdstuk = match.group(2)
        vers_start = match.group(3)
        vers_eind = match.group(4) or vers_start
        ref = f"{boek} {hoofdstuk}:{vers_start}-{vers_eind}"
        if ref not in referenties:
            referenties.append(ref)

    return referenties


# Bekende psalm lengtes (versnummers) - voor volledige psalmen
PSALM_LENGTES = {
    1: 6, 2: 12, 3: 9, 4: 9, 5: 13, 6: 11, 7: 18, 8: 10, 9: 21, 10: 18,
    23: 6, 24: 10, 25: 22, 27: 14, 42: 12, 51: 21, 91: 16, 96: 13, 100: 5,
    103: 22, 104: 35, 121: 8, 122: 9, 130: 8, 139: 24, 150: 6,
}


def download_lezingen(output_dir: Path, liturgie_tekst: str) -> dict[str, str]:
    """
    Download alle lezingen uit de liturgische context en sla ze op.

    Args:
        output_dir: De directory waar de teksten opgeslagen worden
        liturgie_tekst: De tekst van 00_zondag_kerkelijk_jaar.md

    Returns:
        Een dict met referentie -> bestandspad
    """
    print("\nBijbelteksten ophalen van naardensebijbel.nl...")

    # Maak een subdirectory voor de bijbelteksten
    bijbel_dir = output_dir / "bijbelteksten"
    bijbel_dir.mkdir(exist_ok=True)

    # Extraheer de referenties
    referenties_raw = extract_lezingen_uit_liturgie(liturgie_tekst)

    if not referenties_raw:
        print("  Geen bijbelreferenties gevonden in de liturgische context.")
        return {}

    print(f"  Gevonden referenties: {', '.join(referenties_raw)}")

    resultaten = {}

    for ref_str in referenties_raw:
        referentie = parse_bijbelreferentie(ref_str)
        if not referentie:
            print(f"  Kon niet parsen: {ref_str}")
            continue

        # Maak een veilige bestandsnaam
        safe_name = re.sub(r'[^\w\s-]', '', str(referentie)).replace(' ', '_')
        bestandspad = bijbel_dir / f"{safe_name}.txt"

        # Check of bestand al bestaat en niet leeg is
        if bestandspad.exists() and bestandspad.stat().st_size > 0:
            print(f"  ✓ Reeds gedownload: {bestandspad.name}")
            resultaten[str(referentie)] = str(bestandspad)
            continue

        tekst = haal_bijbeltekst_op(referentie)

        if tekst:
            # Voeg header toe en zorg voor goede Markdown spacing
            volledige_tekst = f"# {referentie}\n\n# Bron: Naardense Bijbel (Pieter Oussoren)\n\n{tekst}"

            # Zorg voor lege regel na de kopjes
            volledige_tekst = re.sub(r'^(#+ .*)\n+(?=[^\n])', r'\1\n\n', volledige_tekst, flags=re.MULTILINE)

            with open(bestandspad, 'w', encoding='utf-8') as f:
                f.write(volledige_tekst)

            print(f"  ✓ Opgeslagen: {bestandspad.name}")
            resultaten[str(referentie)] = str(bestandspad)
        else:
            print(f"  ✗ Kon niet ophalen: {referentie}")

        # Wacht even tussen requests om de server niet te overbelasten
        time.sleep(0.5)

    return resultaten


def laad_bijbelteksten(output_dir: Path) -> str:
    """
    Laad alle bijbelteksten uit de bijbelteksten directory.

    Returns:
        Een gecombineerde string met alle bijbelteksten.
    """
    bijbel_dir = output_dir / "bijbelteksten"

    if not bijbel_dir.exists():
        return ""

    teksten = []
    for txt_file in sorted(bijbel_dir.glob("*.txt")):
        with open(txt_file, 'r', encoding='utf-8') as f:
            teksten.append(f.read())

    return "\n\n---\n\n".join(teksten)


if __name__ == "__main__":
    # Test de module
    print("Test: Parse bijbelreferenties")
    test_refs = [
        "Jesaja 9:1-6",
        "Lucas 2:1-14 (15-20)",
        "Psalm 96",
        "Titus 2:11-14",
        "1 Koningen 19:9-13",
        "Johannes 1:1-18",
    ]

    for ref in test_refs:
        parsed = parse_bijbelreferentie(ref)
        print(f"  '{ref}' -> {parsed}")

    print("\nTest: Ophalen enkel vers (Johannes 1:1)")
    tekst = haal_vers_op("johannes", 1, 1)
    if tekst:
        print(f"  ✓ Opgehaald: {tekst[:100]}...")
    else:
        print("  ✗ Kon niet ophalen")

    print("\nTest: Ophalen verzen (Johannes 1:1-3)")
    ref = parse_bijbelreferentie("Johannes 1:1-3")
    if ref:
        tekst = haal_bijbeltekst_op(ref)
        if tekst:
            print(f"  ✓ Opgehaald ({len(tekst)} karakters):")
            print(tekst)
        else:
            print("  ✗ Kon niet ophalen")
