#!/usr/bin/env python3
"""
Naardense Bijbel Tekstophaler

Dit module haalt bijbelteksten op van naardensebijbel.nl en slaat ze op als txt- en json-bestanden.
De teksten worden gebruikt voor exegese in de preekvoorbereiding.

URL-structuur: https://www.naardensebijbel.nl/[boek]/[hoofdstuk]/?hfst=[hoofdstuk]

W.M. Otte (w.m.otte@umcutrecht.nl)
"""

import re
import time
import json
from pathlib import Path
from typing import Optional, List, Dict, Tuple
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
    "genesis": "genesis", "exodus": "exodus", "leviticus": "leviticus",
    "numeri": "numeri", "deuteronomium": "deuteronomium", "jozua": "jozua",
    "rechters": "rechters", "ruth": "ruth", "1 samuel": "1-samuel", "1 samuël": "1-samuel", "1-samuël": "1-samuel",
    "2 samuel": "2-samuel", "2 samuël": "2-samuel", "2-samuël": "2-samuel", "1 koningen": "1-koningen", "2 koningen": "2-koningen",
    "1 kronieken": "1-kronieken", "2 kronieken": "2-kronieken", "ezra": "ezra",
    "nehemia": "nehemia", "ester": "ester", "job": "job", "psalm": "psalm",
    "psalmen": "psalm", "spreuken": "spreuken", "prediker": "prediker",
    "hooglied": "hooglied", "jesaja": "jesaja", "jeremia": "jeremia",
    "klaagliederen": "klaagliederen", "ezechiel": "ezechiel", "ezechiël": "ezechiel",
    "daniel": "daniel", "daniël": "daniel", "hosea": "hosea", "joel": "joel",
    "joël": "joel", "amos": "amos", "obadja": "obadja", "jona": "jona",
    "micha": "micha", "nahum": "nahum", "habakuk": "habakuk", "sefanja": "sefanja",
    "haggai": "haggai", "haggaï": "haggai", "zacharia": "zacharia",
    "maleachi": "maleachi",
    # Nieuwe Testament
    "matteus": "matteus", "matteüs": "matteus", "mattheüs": "matteus",
    "mattheus": "matteus", "marcus": "marcus", "lucas": "lucas",
    "johannes": "johannes", "handelingen": "handelingen", "romeinen": "romeinen",
    "1 korintiërs": "1-korintiers", "1 korintiers": "1-korintiers",
    "1 korinthiërs": "1-korintiers", "2 korintiërs": "2-korintiers",
    "2 korintiers": "2-korintiers", "2 korinthiërs": "2-korintiers",
    "galaten": "galaten", "efeze": "efeze", "efeziërs": "efeze", "efeziers": "efeze", "efesiërs": "efeze", "efesiers": "efeze",
    "filippenzen": "filippenzen", "kolossenzen": "kolossenzen",
    "1 tessalonicenzen": "1-tessalonicenzen", "2 tessalonicenzen": "2-tessalonicenzen",
    "1 timoteüs": "1-timoteus", "1 timoteus": "1-timoteus",
    "2 timoteüs": "2-timoteus", "2 timoteus": "2-timoteus", "titus": "titus",
    "filemon": "filemon", "hebreeën": "hebreeen", "hebreeen": "hebreeen",
    "jakobus": "jakobus", "1 petrus": "1-petrus", "2 petrus": "2-petrus",
    "1 johannes": "1-johannes", "2 johannes": "2-johannes",
    "3 johannes": "3-johannes", "judas": "judas", "openbaring": "openbaring",
    # Deuterocanoniek
    "sirach": "sirach", "jezus sirach": "sirach", "ecclesiasticus": "sirach",
    "wijsheid": "wijsheid", "wijsheid van salomo": "wijsheid",
    "tobit": "tobit", "judit": "judith", "judith": "judith",
    "baruch": "baruch", "1 makkabeeën": "1-makkabeeen", "2 makkabeeën": "2-makkabeeen",
}

# Mapping voor NBV21 codes
MAPPINGS_SOURCE = {
  "GEN": ["GEN", "Genesis", "1 Mozes", "1Mozes"],
  "EXO": ["EXO", "Exodus", "2 Mozes", "2Mozes"],
  "LEV": ["LEV", "Leviticus", "3 Mozes", "3Mozes"],
  "NUM": ["NUM", "Numeri", "4 Mozes", "4Mozes"],
  "DEU": ["DEU", "Deuteronomium", "5 Mozes", "5Mozes"],
  "JOS": ["JOS", "Jozua", "Joshua"],
  "JDG": ["JDG", "Rechters", "Judges"],
  "RUT": ["RUT", "Ruth"],
  "1SA": ["1SA", "1 Samuel", "1Samuel", "1 Sam", "1Sam"],
  "2SA": ["2SA", "2 Samuel", "2Samuel", "2 Sam", "2Sam"],
  "1KI": ["1KI", "1 Koningen", "1Koningen", "1 Kings", "1Kings"],
  "2KI": ["2KI", "2 Koningen", "2Koningen", "2 Kings", "2Kings"],
  "1CH": ["1CH", "1 Kronieken", "1Kronieken", "1 Chronicles", "1Chronicles"],
  "2CH": ["2CH", "2 Kronieken", "2Kronieken", "2 Chronicles", "2Chronicles"],
  "EZR": ["EZR", "Ezra"],
  "NEH": ["NEH", "Nehemia", "Nehemiah"],
  "EST": ["EST", "Esther"],
  "JOB": ["JOB", "Job"],
  "PSA": ["PSA", "Psalmen", "Psalms", "Psalm"],
  "PRO": ["PRO", "Spreuken", "Proverbs"],
  "ECC": ["ECC", "Prediker", "Ecclesiastes"],
  "SNG": ["SNG", "Hooglied", "Song of Songs", "Song of Solomon"],
  "ISA": ["ISA", "Jesaja", "Isaiah"],
  "JER": ["JER", "Jeremia", "Jeremiah"],
  "LAM": ["LAM", "Klaagliederen", "Lamentations"],
  "EZK": ["EZK", "Ezechiël", "Ezekiel", "Ezechiel"],
  "DAN": ["DAN", "Daniël", "Daniel", "Daniel"],
  "HOS": ["HOS", "Hosea"],
  "JOL": ["JOL", "Joël", "Joel", "Joel"],
  "AMO": ["AMO", "Amos"],
  "OBA": ["OBA", "Obadja", "Obadiah"],
  "JON": ["JON", "Jona", "Jonah"],
  "MIC": ["MIC", "Micha", "Micah"],
  "NAM": ["NAM", "Nahum"],
  "HAB": ["HAB", "Habakuk", "Habakkuk"],
  "ZEP": ["ZEP", "Sefanja", "Zephaniah"],
  "HAG": ["HAG", "Haggai"],
  "ZEC": ["ZEC", "Zacharia", "Zechariah"],
  "MAL": ["MAL", "Maleachi", "Malachi"],
  "MAT": ["MAT", "Matteüs", "Matthew", "Matt", "Matteus"],
  "MRK": ["MRK", "Marcus", "Mark", "Markus"],
  "LUK": ["LUK", "Lucas", "Luke"],
  "JHN": ["JHN", "Johannes", "John"],
  "ACT": ["ACT", "Handelingen", "Acts"],
  "ROM": ["ROM", "Romeinen", "Romans"],
  "1CO": ["1CO", "1 Korinthiërs", "1Korinthiërs", "1 Korintiërs", "1Korintiërs", "1 Corinthians", "1Corinthians", "1 Kor", "1Kor", "1 Korintiers"],
  "2CO": ["2CO", "2 Korinthiërs", "2Korinthiërs", "2 Korintiërs", "2Korintiërs", "2 Corinthians", "2Corinthians", "2 Kor", "2Kor", "2 Korintiers"],
  "GAL": ["GAL", "Galaten", "Galatians"],
  "EPH": ["EPH", "Efeziërs", "Ephesians", "Efeze"],
  "PHP": ["PHP", "Filippenzen", "Philippians"],
  "COL": ["COL", "Kolossenzen", "Colossians"],
  "1TH": ["1TH", "1 Tessalonicenzen", "1Tessalonicenzen", "1 Thessalonians", "1Thessalonians", "1 Thess", "1Thess"],
  "2TH": ["2TH", "2 Tessalonicenzen", "2Tessalonicenzen", "2 Thessalonians", "2Thessalonians", "2 Thess", "2Thess"],
  "1TI": ["1TI", "1 Timoteüs", "1Timoteüs", "1 Timotheüs", "1Timotheüs", "1 Timothy", "1Timothy", "1 Tim", "1Tim", "1 Timoteus"],
  "2TI": ["2TI", "2 Timoteüs", "2Timoteüs", "2 Timotheüs", "2Timotheüs", "2 Timothy", "2Timothy", "2 Tim", "2Tim", "2 Timoteus"],
  "TIT": ["TIT", "Titus"],
  "PHM": ["PHM", "Filemon", "Philemon"],
  "HEB": ["HEB", "Hebreeën", "Hebrews", "Hebreeen"],
  "JAS": ["JAS", "Jakobus", "Jacobus", "James"],
  "1PE": ["1PE", "1 Petrus", "1Petrus", "1 Peter", "1Peter", "1 Pet", "1Pet"],
  "2PE": ["2PE", "2 Petrus", "2Petrus", "2 Peter", "2Peter", "2 Pet", "2Pet"],
  "1JN": ["1JN", "1 Johannes", "1Johannes", "1 John", "1John"],
  "2JN": ["2JN", "2 Johannes", "2Johannes", "2 John", "2John"],
  "3JN": ["3JN", "3 Johannes", "3Johannes", "3 John", "3John"],
  "JUD": ["JUD", "Judas", "Jude"],
  "REV": ["REV", "Openbaring", "Revelation"]
}

NAME_TO_CODE = {}
for code, names in MAPPINGS_SOURCE.items():
    for name in names:
        NAME_TO_CODE[name.upper()] = code


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

        # Split in twee referenties met " en " als separator
        # Eerste deel: van vers1 tot einde van hoofdstuk
        # Tweede deel: van begin van hoofdstuk2 tot vers2
        normalized = f"{book} {chapter1}:{verse1} en {book} {chapter2}:1-{verse2}"

    return normalized


def parse_bijbelreferentie(tekst: str) -> Optional[BijbelReferentie]:
    """Parse een bijbelreferentie string naar een BijbelReferentie object.
    Handles verse suffixes like 'a' or 'b' (e.g., "3a") by ignoring them.
    """
    tekst = tekst.strip()
    haakjes_match = re.search(r'\((\d+)[-–]?(\d+)?\)', tekst)
    extra_eind = None
    if haakjes_match:
        if haakjes_match.group(2):
            extra_eind = int(haakjes_match.group(2))
        else:
            extra_eind = int(haakjes_match.group(1))
        tekst = re.sub(r'\s*\([^)]+\)', '', tekst)

    # Regex aangepast om boeknamen met meerdere woorden (en spaties) toe te staan
    # bijv. "Jezus Sirach 24" of "1 Koningen 12"
    # Allow optional letter suffix (a, b, etc.) after verse numbers
    pattern = r'^(\d?\s*[A-Za-zëïüéèöä]+(?:\s+[A-Za-zëïüéèöä]+)*)\s+(\d+)(?::(\d+)[a-z]?(?:[-–](\d+)[a-z]?)?)?'
    match = re.match(pattern, tekst, re.IGNORECASE)

    if not match:
        return None

    boek = match.group(1).strip().lower()
    hoofdstuk = int(match.group(2))
    vers_start = int(match.group(3)) if match.group(3) else None
    vers_eind = int(match.group(4)) if match.group(4) else vers_start

    if extra_eind and (vers_eind is None or extra_eind > vers_eind):
        vers_eind = extra_eind

    return BijbelReferentie(boek=boek, hoofdstuk=hoofdstuk, vers_start=vers_start, vers_eind=vers_eind)


def get_boek_slug(boek: str) -> Optional[str]:
    """Converteer een boeknaam naar de URL-slug."""
    boek_lower = boek.lower().strip()
    return BOEK_NAAR_SLUG.get(boek_lower)

def get_boek_code(boek: str) -> str:
    """Converteer boeknaam naar NBV21 code (of fallback naar slug/naam)."""
    code = NAME_TO_CODE.get(boek.upper().strip())
    return code if code else boek.upper()

def haal_vers_op(boek_slug: str, hoofdstuk: int, vers: int) -> Optional[str]:
    """Haal een enkel vers op als string."""
    url = f"https://www.naardensebijbel.nl/vers/{boek_slug}-{hoofdstuk}-{vers}/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    max_retries = 3
    for poging in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 404:
                return None
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            for tag in soup.find_all(['nav', 'script', 'style', 'header', 'footer', 'aside']):
                tag.decompose()

            body = soup.find('body')
            if not body: return None

            # Behoud de poëtische structuur door naar specifieke span elementen te zoeken
            # Zoek naar de lead paragraph met de bijbeltekst
            lead_para = body.find('p', class_='lead')
            if lead_para:
                # Zoek naar de span elementen met class 'q' (poëtische regels)
                poeze_regels = lead_para.find_all('span', class_='q')
                if poeze_regels:
                    regels = []
                    for regel in poeze_regels:
                        regel_tekst = regel.get_text(separator=' ', strip=True)
                        if regel_tekst:
                            regels.append(regel_tekst)
                    return '\n'.join(regels) if regels else None

            # Fallback: oude methode
            tekst = body.get_text(separator='\n', strip=True)
            lines = tekst.split('\n')
            bijbel_lines = []
            in_tekst = False

            for line in lines:
                line = line.strip()
                if not line or 'Naardense Bijbel' in line or 'literaire vertaling' in line.lower() or line == '>':
                    continue
                if re.match(r'^[A-Za-zëïüéèöä\s\d]+ – \d+ : \d+$', line):
                    in_tekst = True
                    continue
                if line.startswith('Lees ') or line.startswith('Bekijk '):
                    break
                if in_tekst:
                    bijbel_lines.append(line)

            return '\n'.join(bijbel_lines) if bijbel_lines else None
        except Exception as e:
            if poging < max_retries - 1:
                time.sleep((poging + 1) * 2)
            else:
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
    "galaten": 48, "efeze": 49, "efeziërs": 49, "efeziers": 49, "efesiërs": 49, "efesiers": 49,
    "filippenzen": 50, "kolossenzen": 51,
    "1 tessalonicenzen": 52, "2 tessalonicenzen": 53,
    "1 timoteüs": 54, "1 timoteus": 54, "2 timoteüs": 55, "2 timoteus": 55,
    "titus": 56, "filemon": 57, "hebreeën": 58, "hebreeen": 58,
    "jakobus": 59, "1 petrus": 60, "2 petrus": 61,
    "1 johannes": 62, "2 johannes": 63, "3 johannes": 64,
    "judas": 65, "openbaring": 66,
}


def haal_verzen_via_zoek(boek: str, hoofdstuk: int, vers_start: int, vers_eind: int) -> List[Dict]:
    """Haal verzen op via zoek-URL en retourneer structured data."""
    boek_lower = boek.lower().strip()
    boek_nr = BOEK_NAAR_NUMMER.get(boek_lower)
    if not boek_nr: return []

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

    headers = {'User-Agent': 'Mozilla/5.0'}
    verzen = []

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if table:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 2:
                    vers_nr = cells[0].get_text(strip=True)
                    # Behoud de poëtische structuur in de vers-tekst
                    cell_content = cells[1]
                    # Zoek naar poëtische elementen (span class="q") binnen de cel
                    poeze_regels = cell_content.find_all('span', class_='q')
                    if poeze_regels:
                        regels = []
                        for regel in poeze_regels:
                            regel_tekst = regel.get_text(separator=' ', strip=True)
                            if regel_tekst:
                                regels.append(regel_tekst)
                        vers_tekst = '\n'.join(regels)
                    else:
                        # Fallback naar normale tekst
                        vers_tekst = cells[1].get_text(strip=True)

                    if vers_nr.isdigit() and vers_tekst:
                        verzen.append({"verse": int(vers_nr), "text": vers_tekst})
    except Exception as e:
        print(f"  Fout bij zoeken: {e}")

    return verzen

def haal_verzen_data(boek_slug: str, hoofdstuk: int, vers_start: int, vers_eind: int) -> List[Dict]:
    """Haal verzen op en retourneer structured data."""
    data = []
    for vers in range(vers_start, vers_eind + 1):
        tekst = haal_vers_op(boek_slug, hoofdstuk, vers)
        if tekst:
            data.append({"verse": vers, "text": tekst})
        else:
            if vers == vers_start: return []
            break
        time.sleep(0.2)
    return data

def haal_heel_hoofdstuk_data(boek_slug: str, hoofdstuk: int, max_verzen: int = 200) -> List[Dict]:
    """Haal heel hoofdstuk op als structured data."""
    data = []
    vers = 1
    while vers <= max_verzen:
        tekst = haal_vers_op(boek_slug, hoofdstuk, vers)
        if tekst:
            data.append({"verse": vers, "text": tekst})
            vers += 1
            time.sleep(0.2)
        else:
            break
    return data

def haal_bijbeltekst_op(referentie: BijbelReferentie) -> Tuple[Optional[str], Optional[List[Dict]]]:
    """
    Haal de bijbeltekst op. Retourneert (Markdown string, Verses List).
    """
    slug = get_boek_slug(referentie.boek)
    print(f"  Ophalen: {referentie} ...")

    vers_start = referentie.vers_start or 1
    vers_eind = referentie.vers_eind or referentie.vers_start
    if not referentie.vers_start:
        if referentie.boek.lower() in ('psalm', 'psalmen') and referentie.hoofdstuk in PSALM_LENGTES:
            vers_eind = PSALM_LENGTES[referentie.hoofdstuk]
        else:
            vers_eind = 200

    data = []

    # Speciale afhandeling voor 1 Samuel en 2 Samuel - de zoek-URL werkt daar verkeerd
    if slug and referentie.boek.lower() in ('1 samuel', '1 samuël', '2 samuel', '2 samuël'):
        # Speciale handmatige correctie voor 1 Samuel 1 - dit hoofdstuk wordt verkeerd geleverd via de zoekfunctie
        if referentie.boek.lower() in ('1 samuel', '1 samuël') and referentie.hoofdstuk == 1:
            print(f"    -> Waarschuwing: 1 Samuel 1 kan niet automatisch worden opgehaald vanwege website beperkingen")
            print(f"  Onbekend bijbelboek of kon niet ophalen: {referentie.boek}")
            return None, None

        # Probeer eerst directe toegang via slug
        data = haal_verzen_data(slug, referentie.hoofdstuk, vers_start, vers_eind)
        if not data and not referentie.vers_start:
             data = haal_heel_hoofdstuk_data(slug, referentie.hoofdstuk)

        # Als dat ook niet werkt, probeer dan een alternatieve aanpak
        if not data:
            print(f"    -> Fallback naar zoek-URL (speciaal voor Samuel boeken)...")
            data = haal_verzen_via_zoek(referentie.boek, referentie.hoofdstuk, vers_start, vers_eind)

            # Extra controle voor Samuel boeken: soms geeft de zoekfunctie verkeerde resultaten
            if data and referentie.boek.lower() in ('1 samuel', '1 samuël'):
                # Controleer of de verzen overeenkomen met het verwachte hoofdstuk
                # Als eerste vers begint met "En het geschiedt na Sauls dooden" dan is het 2 Samuel i.p.v. 1 Samuel
                if data and len(data) > 0 and "Saul" in data[0].get('text', '') and "dooden" in data[0].get('text', ''):
                    print(f"    -> Waarschuwing: mogelijk verkeerd hoofdstuk ontvangen voor {referentie.boek}")
                    # Probeer dan met een alternatieve methode of geef foutmelding
                    data = []  # Reset data zodat het als niet gevonden wordt gemarkeerd
            elif data and referentie.boek.lower() in ('2 samuel', '2 samuël'):
                # Voor 2 Samuel controleren we of het met de juiste tekst begint
                pass  # Geen specifieke controle nodig voor 2 Samuel
    else:
        # Standaardafhandeling voor andere boeken
        if slug:
            data = haal_verzen_data(slug, referentie.hoofdstuk, vers_start, vers_eind)
            if not data and not referentie.vers_start:
                 data = haal_heel_hoofdstuk_data(slug, referentie.hoofdstuk)

        if not data:
            print(f"    -> Fallback naar zoek-URL...")
            data = haal_verzen_via_zoek(referentie.boek, referentie.hoofdstuk, vers_start, vers_eind)

    if not data:
        print(f"  Onbekend bijbelboek of kon niet ophalen: {referentie.boek}")
        return None, None

    # Format to markdown
    md_lines = []
    for item in data:
        md_lines.append(f"**{referentie.hoofdstuk}:{item['verse']}** {item['text']}")

    return '\n\n'.join(md_lines), data

def extract_lezingen_uit_liturgie(liturgie_tekst: str) -> list[tuple[str, str]]:
    """Extraheer bijbelreferenties uit de liturgische context tekst.

    Haalt alleen de officiële lezingen uit de 'lezingen' key van de JSON.

    Returns:
        List of tuples (original_reference, normalized_reference)
    """
    referenties = []  # List of (original, normalized) tuples
    seen_originals = set()

    # Probeer eerst de liturgie_tekst te parsen als JSON
    try:
        data = json.loads(liturgie_tekst)

        # Haal alleen referenties uit de 'lezingen' key
        if 'lezingen' in data:
            lezingen_obj = data['lezingen']

            # Haal referenties uit de standaard lezingen
            for key in ['eerste_lezing', 'tweede_lezing', 'derde_lezing', 'epistel', 'evangelie', 'psalm']:
                if key in lezingen_obj and isinstance(lezingen_obj[key], dict):
                    ref = lezingen_obj[key].get('referentie', '')
                    if ref and ref not in seen_originals:
                        # Speciale behandeling voor psalm nummers
                        if key == 'psalm' and re.match(r'^\d+$', ref):
                            ref = f"Psalm {ref}"
                        normalized = normalize_scripture_reference(ref)
                        referenties.append((ref, normalized))
                        seen_originals.add(ref)

            # Haal referenties uit alternatieve lezingen
            if 'alternatieve_lezingen' in lezingen_obj and isinstance(lezingen_obj['alternatieve_lezingen'], list):
                for alt in lezingen_obj['alternatieve_lezingen']:
                    if isinstance(alt, dict):
                        ref = alt.get('referentie', '')
                        if ref and ref not in seen_originals:
                            normalized = normalize_scripture_reference(ref)
                            referenties.append((ref, normalized))
                            seen_originals.add(ref)

        return referenties

    except (json.JSONDecodeError, KeyError, TypeError):
        # Fallback naar oude regex methode als JSON parsing mislukt
        pass

    # Oude regex methode (fallback)
    patronen = [
        # Markdown patronen
        # Updated regex to capture multi-part references like "Sefanja 2:3 en 3:12-13"
        r'(?:Eerste|Tweede|Derde)?\s*(?:lezing|Lezing)[:\s]+([A-Za-zëïüéèöä\d\s]+\d+:\d+(?:[-–][\d\.]+)?(?:(?:\s+(?:en|&)\s+|[;,]\s*)(?:(?:\d+[:])?\d+(?:[-–][\d\.]+)?))*(?:\s*\([^)]+\))?)',
        r'(?:Evangelie|Epistel)(?:lezing)?[:\s]+([A-Za-zëïüéèöä\d\s]+\d+:\d+(?:[-–][\d\.]+)?(?:(?:\s+(?:en|&)\s+|[;,]\s*)(?:(?:\d+[:])?\d+(?:[-–][\d\.]+)?))*(?:\s*\([^)]+\))?)',
        r'Psalm(?:\s+van\s+de\s+\w+)?[:\s]+(?:Psalm\s+)?(\d+)',
        r'\*\*(?:Eerste|Evangelie|Epistel)lezing:\*\*\s+([A-Za-zëïüéèöä\d\s]+\d+:\d+(?:[-–][\d\.]+)?(?:(?:\s+(?:en|&)\s+|[;,]\s*)(?:(?:\d+[:])?\d+(?:[-–][\d\.]+)?))*)',
        # JSON patroon ("referentie": "...")
        r'"referentie":\s*"([^"]+)"'
    ]
    for patroon in patronen:
        for match in re.findall(patroon, liturgie_tekst, re.IGNORECASE):
            # Als match een tuple is (bij groepen), pak de eerste niet-lege
            if isinstance(match, tuple):
                ref = next((m for m in match if m), "").strip()
            else:
                ref = match.strip()

            if re.match(r'^\d+$', ref): ref = f"Psalm {ref}"
            if ref and len(ref) > 3: # min length check
                if ref not in seen_originals:
                    # Normaliseer de referentie (verwijder a/b, split cross-hoofdstuk)
                    normalized = normalize_scripture_reference(ref)
                    referenties.append((ref, normalized))
                    seen_originals.add(ref)

    bullet_pattern = r'[-*]\s*\*?\*?([A-Za-zëïüéèöä]+(?:\s+\d)?)\s+(\d+):(\d+)(?:[-–](\d+))?(?:\s*\([^)]+\))?'
    for match in re.finditer(bullet_pattern, liturgie_tekst):
        ref = f"{match.group(1).strip()} {match.group(2)}:{match.group(3)}-{match.group(4) or match.group(3)}"
        if ref not in seen_originals:
            normalized = normalize_scripture_reference(ref)
            referenties.append((ref, normalized))
            seen_originals.add(ref)

    return referenties


PSALM_LENGTES = {
    1: 6, 2: 12, 3: 9, 4: 9, 5: 13, 6: 11, 7: 18, 8: 10, 9: 21, 10: 18,
    23: 6, 24: 10, 25: 22, 27: 14, 42: 12, 51: 21, 91: 16, 96: 13, 100: 5,
    103: 22, 104: 35, 121: 8, 122: 9, 130: 8, 139: 24, 150: 6,
}


def download_lezingen(output_dir: Path, liturgie_tekst: str) -> dict[str, str]:
    """Download lezingen en sla ze op als TXT en JSON."""
    print("\nBijbelteksten ophalen van naardensebijbel.nl...")
    bijbel_dir = output_dir / "bijbelteksten"
    bijbel_dir.mkdir(exist_ok=True)

    referenties_tuples = extract_lezingen_uit_liturgie(liturgie_tekst)
    if not referenties_tuples:
        print("  Geen bijbelreferenties gevonden.")
        return {}

    # Print alleen de originele referenties
    original_refs = [orig for orig, _ in referenties_tuples]
    print(f"  Gevonden referenties: {', '.join(original_refs)}")
    resultaten = {}
    seen_refs = set()

    for original_ref, normalized_ref in referenties_tuples:
        # Skip duplicates based on the original string
        if original_ref in seen_refs: continue
        seen_refs.add(original_ref)

        print(f"  Verwerken: {original_ref}")

        # 1. Parse into sub-references (handling ; and "en")
        # Normalize separators: Replace ' en ' and '&' with ';'
        normalized_ref_for_split = re.sub(r'\s+(?:en|&)\s+', ';', normalized_ref)
        parts = re.split(r'[;]', normalized_ref_for_split)
        
        sub_refs = []
        last_book = None
        
        for part in parts:
            part = part.strip()
            if not part: continue
            
            # Check for Book Name (Start of string)
            book_match = re.match(r'^((?:\d\s+)?[A-Za-zëïüéèöä]+(?:\s+[A-Za-zëïüéèöä]+)*)', part)
            
            # Verify if it's a real book
            is_book = False
            if book_match:
                potential_book = book_match.group(1)
                if get_boek_slug(potential_book) or NAME_TO_CODE.get(potential_book.upper()):
                    is_book = True

            if is_book:
                last_book = book_match.group(1)
                sub_refs.append(part)
            elif last_book:
                # Inherit book
                sub_refs.append(f"{last_book} {part}")
            else:
                # Fallback
                sub_refs.append(part)

        # 2. Fetch verses for all sub-refs
        all_pericopes = []
        
        for ref_str in sub_refs:
            # Check for multi-range syntax within one chapter (e.g. "1, 3-5")
            # Or standard "Book Chapter:Verses"
            
            # Simple parsing first
            # Logic: We treat each sub_ref as a potential BijbelReferentie
            # But we must handle "Genesis 1:1.3" (discontinuous verses)
            
            # Check for complex verse part with dots
            complex_match = re.match(r"^\s*((?:\d\s)?[A-Za-zëïüöä\s]+?)\s+(\d+)[\s,:]+([\d\-–.;a-z]+)", ref_str)
            
            if complex_match:
                book_chapter_base = f"{complex_match.group(1).strip()} {complex_match.group(2)}"
                verse_part = complex_match.group(3)
                # Split verse part on . 
                # Note: previously we split on ; too, but we handled ; above.
                verse_ranges = re.split(r'[.]', verse_part)
                
                for v_range in verse_ranges:
                    v_range = v_range.strip()
                    if not v_range: continue
                    
                    sub_sub_ref_str = f"{book_chapter_base}:{v_range}"
                    referentie = parse_bijbelreferentie(sub_sub_ref_str)
                    
                    if referentie:
                        md_text, verses_data = haal_bijbeltekst_op(referentie)
                        if verses_data:
                            all_pericopes.append({
                                "book": get_boek_code(referentie.boek),
                                "chapter": referentie.hoofdstuk,
                                "verses": verses_data,
                                "translation": "NB"
                            })
                        time.sleep(0.3)
            else:
                # Standard single reference
                referentie = parse_bijbelreferentie(ref_str)
                if referentie:
                    md_text, verses_data = haal_bijbeltekst_op(referentie)
                    if verses_data:
                        all_pericopes.append({
                            "book": get_boek_code(referentie.boek),
                            "chapter": referentie.hoofdstuk,
                            "verses": verses_data,
                            "translation": "NB"
                        })
                    time.sleep(0.3)

        # 3. Save combined result
        if all_pericopes:
            # Filename generation based on the ORIGINAL reference (not normalized)
            safe_name = original_ref.replace(':', '_').replace(' ', '_').replace(';', '_')
            safe_name = re.sub(r'[^\w\-.]', '', safe_name)
            # Limit length
            if len(safe_name) > 60: safe_name = safe_name[:60]

            json_path = bijbel_dir / f"{safe_name}_NB.json"

            # If single pericope, save as object (for backward compatibility if preferred, but list is safer for generic)
            # However, existing loaders might expect object for single files.
            # nbv21 saves list if > 1. Let's do same.
            final_data = all_pericopes if len(all_pericopes) > 1 else all_pericopes[0]

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=2, ensure_ascii=False)

            print(f"  ✓ Opgeslagen: {json_path.name}")
            resultaten[original_ref] = str(json_path)
        else:
            print(f"  ✗ Kon niet ophalen: {original_ref}")

    return resultaten


def laad_bijbelteksten(output_dir: Path) -> str:
    """Laad alle bijbelteksten (JSON) en formatteer als Markdown."""
    bijbel_dir = output_dir / "bijbelteksten"
    if not bijbel_dir.exists():
        return ""

    teksten = []
    for json_file in sorted(bijbel_dir.glob("*.json")):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            book = data.get("book", "Onbekend")
            chapter = data.get("chapter", "")
            verses = data.get("verses", [])

            md_lines = [f"# {book} {chapter}", "# Bron: Naardense Bijbel (Pieter Oussoren)\n"]
            for v in verses:
                md_lines.append(f"**{chapter}:{v['verse']}** {v['text']}")

            teksten.append("\n\n".join(md_lines))
        except Exception as e:
            print(f"Fout bij laden {json_file}: {e}")

    return "\n\n---\n\n".join(teksten)
            

if __name__ == "__main__":
    print("Test run...")
    ref = parse_bijbelreferentie("Johannes 1:1-5")
    if ref:
        md, data = haal_bijbeltekst_op(ref)
        if md:
            print(f"Markdown:\n{md[:100]}...")
            print(f"JSON Structure: {json.dumps({'book': 'JHN', 'chapter': 1, 'verses': data}, indent=2)}")