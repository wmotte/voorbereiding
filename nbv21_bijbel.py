#!/usr/bin/env python3
"""
NBV21 Bijbel Tekstophaler

Haalt NBV21 teksten op uit lokale JSON-bestanden in de nbv21/ map.
Bedoeld om samen te werken met contextduiding.py en verdieping.py.
"""

import json
import re
from pathlib import Path
from typing import Optional, List, Dict

# Probeer BijbelReferentie te importeren uit naardense_bijbel voor consistentie
try:
    from naardense_bijbel import parse_bijbelreferentie, BijbelReferentie
except ImportError:
    # Fallback definitie als naardense_bijbel niet beschikbaar is
    from dataclasses import dataclass
    
    @dataclass
    class BijbelReferentie:
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

    def parse_bijbelreferentie(tekst: str) -> Optional[BijbelReferentie]:
        tekst = tekst.strip()
        haakjes_match = re.search(r'\((?:vers\s*)?(\d+)[-–]?(\d+)?\)', tekst)
        extra_eind = None
        if haakjes_match:
            extra_eind = int(haakjes_match.group(2)) if haakjes_match.group(2) else int(haakjes_match.group(1))
            tekst = re.sub(r'\s*\([^)]+\)', '', tekst)

        pattern = r'^(\d?\s*[A-Za-zëïüéèöä]+)\s+(\d+)(?::(\d+)(?:[-–](\d+))?)?'
        match = re.match(pattern, tekst, re.IGNORECASE)
        if not match: return None
        
        boek = match.group(1).strip().lower()
        hoofdstuk = int(match.group(2))
        vers_start = int(match.group(3)) if match.group(3) else None
        vers_eind = int(match.group(4)) if match.group(4) else vers_start
        
        if extra_eind and (vers_eind is None or extra_eind > vers_eind):
            vers_eind = extra_eind
            
        return BijbelReferentie(boek, hoofdstuk, vers_start, vers_eind)

# Pad configuratie
SCRIPT_DIR = Path(__file__).parent.resolve()
NBV21_DIR = SCRIPT_DIR / "nbv21"

# Mapping configuratie (Bron: get_chapter.R)
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
  "1CO": ["1CO", "1 Korinthiërs", "1Korinthiërs", "1 Corinthians", "1Corinthians", "1 Kor", "1Kor", "1 Korintiers"],
  "2CO": ["2CO", "2 Korinthiërs", "2Korinthiërs", "2 Corinthians", "2Corinthians", "2 Kor", "2Kor", "2 Korintiers"],
  "GAL": ["GAL", "Galaten", "Galatians"],
  "EPH": ["EPH", "Efeziërs", "Ephesians", "Efeze"],
  "PHP": ["PHP", "Filippenzen", "Philippians"],
  "COL": ["COL", "Kolossenzen", "Colossians"],
  "1TH": ["1TH", "1 Tessalonicenzen", "1Tessalonicenzen", "1 Thessalonians", "1Thessalonians", "1 Thess", "1Thess"],
  "2TH": ["2TH", "2 Tessalonicenzen", "2Tessalonicenzen", "2 Thessalonians", "2Thessalonians", "2 Thess", "2Thess"],
  "1TI": ["1TI", "1 Timoteüs", "1Timoteüs", "1 Timothy", "1Timothy", "1 Tim", "1Tim", "1 Timoteus"],
  "2TI": ["2TI", "2 Timoteüs", "2Timoteüs", "2 Timothy", "2Timothy", "2 Tim", "2Tim", "2 Timoteus"],
  "TIT": ["TIT", "Titus"],
  "PHM": ["PHM", "Filemon", "Philemon"],
  "HEB": ["HEB", "Hebreeën", "Hebrews", "Hebreeen"],
  "JAS": ["JAS", "Jakobus", "James"],
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

def get_book_code(book_name: str) -> Optional[str]:
    return NAME_TO_CODE.get(book_name.upper().strip())

def get_nbv21_text(ref: BijbelReferentie) -> Optional[str]:
    """Haalt tekst op voor een gegeven referentie uit de lokale JSON bestanden."""
    code = get_book_code(ref.boek)
    if not code:
        # Probeer het boeknaam nog iets losser te matchen als het niet direct gevonden wordt
        # Bijv. "1 samuel" -> "1 SAMUEL"
        return None

    json_path = NBV21_DIR / code / f"{code}.{ref.hoofdstuk}.json"
    
    if not json_path.exists():
        # Misschien is het hoofdstuk nog niet gedownload
        return None

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Fout bij lezen NBV21 bestand {json_path}: {e}")
        return None

    verses = data.get('verses', [])
    selected_text = []

    # Bepaal start en eind vers
    start = ref.vers_start if ref.vers_start else 1
    
    # Als er geen eindvers is opgegeven, zijn er twee mogelijkheden:
    # 1. Het was "Jesaja 9" -> heel hoofdstuk
    # 2. Het was "Jesaja 9:6" -> alleen vers 6
    # BijbelReferentie maakt hier geen onderscheid in structuur (behalve dat start=None betekent heel hoofdstuk)
    # Maar als start=6 en eind=None, dan bedoelen we meestal vers 6.
    
    if ref.vers_start is None:
        # Heel hoofdstuk
        end = 9999
    elif ref.vers_eind is None:
        # Alleen startvers
        end = start
    else:
        end = ref.vers_eind

    for v in verses:
        v_num = v.get('verse')
        if v_num >= start and v_num <= end:
            text = v.get('text')
            # Maak de tekst schoon (verwijder onnodige spaties)
            text = re.sub(r'\s+', ' ', text).strip()
            selected_text.append(f"{v_num}. {text}")

    if not selected_text:
        return None

    header = f"### {ref.boek.title()} {ref.hoofdstuk}"
    if ref.vers_start:
        header += f":{ref.vers_start}"
        if ref.vers_eind and ref.vers_eind != ref.vers_start:
            header += f"-{ref.vers_eind}"
    
    return f"{header} (NBV21)\n" + "\n".join(selected_text)

def get_nbv21_lezingen_text(context_text: str) -> str:
    """
    Zoekt naar lezingen in de context tekst (markdown) en haalt de NBV21 teksten op.
    Gebruikt dezelfde logica als naardense_bijbel.download_lezingen.
    """
    regex = r'(?:lezing|evangelie|schriftlezing).*?[:]\s*([A-Za-z0-9\s:,-–\(\)]+)'
    matches = re.finditer(regex, context_text, re.IGNORECASE)
    
    results = []
    seen_refs = set()

    for match in matches:
        raw_ref = match.group(1).strip()
        
        # Splits op komma's voor meerdere lezingen (bijv. "Jesaja 1:1-10, Lucas 2:1-10")
        # Maar pas op met komma's binnen een referentie als die zouden voorkomen (hier niet waarschijnlijk)
        sub_refs = [r.strip() for r in raw_ref.split(',')]
        
        for sub_ref in sub_refs:
            if not sub_ref: continue
            
            ref = parse_bijbelreferentie(sub_ref)
            if ref and get_book_code(ref.boek):
                ref_str = str(ref)
                if ref_str not in seen_refs:
                    text = get_nbv21_text(ref)
                    if text:
                        results.append(text)
                        seen_refs.add(ref_str)

    if not results:
        return ""

    return "\n\n".join(results)
