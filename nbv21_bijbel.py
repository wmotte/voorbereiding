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
    from naardense_bijbel import parse_bijbelreferentie, BijbelReferentie, normalize_scripture_reference
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
        """Handles verse suffixes like 'a' or 'b' (e.g., "3a") by ignoring them."""
        tekst = tekst.strip()
        haakjes_match = re.search(r'\((?:vers\s*)?(\d+)[-–]?(\d+)?\)', tekst)
        extra_eind = None
        if haakjes_match:
            extra_eind = int(haakjes_match.group(2)) if haakjes_match.group(2) else int(haakjes_match.group(1))
            tekst = re.sub(r'\s*\([^)]+\)', '', tekst)

        # Allow optional letter suffix (a, b, etc.) after verse numbers
        pattern = r'^(\d?\s*[A-Za-zëïüéèöä]+)\s+(\d+)(?::(\d+)[a-z]?(?:[-–](\d+)[a-z]?)?)?'
        match = re.match(pattern, tekst, re.IGNORECASE)
        if not match: return None

        boek = match.group(1).strip().lower()
        hoofdstuk = int(match.group(2))
        vers_start = int(match.group(3)) if match.group(3) else None
        vers_eind = int(match.group(4)) if match.group(4) else vers_start

        if extra_eind and (vers_eind is None or extra_eind > vers_eind):
            vers_eind = extra_eind

        return BijbelReferentie(boek, hoofdstuk, vers_start, vers_eind)

    def normalize_scripture_reference(reference: str) -> str:
        """Fallback normalisatie functie."""
        if not reference or not isinstance(reference, str):
            return reference
        normalized = re.sub(r'(\d+)[ab]\b', r'\1', reference)
        cross_chapter_pattern = r'^((?:\d\s+)?[A-Za-zëïüéèöä]+(?:\s+[A-Za-zëïüéèöä]+)*)\s+(\d+):(\d+)[-–](\d+):(\d+)$'
        match = re.match(cross_chapter_pattern, normalized)
        if match:
            book, ch1, v1, ch2, v2 = match.groups()
            normalized = f"{book} {ch1}:{v1} en {book} {ch2}:1-{v2}"
        return normalized

# Pad configuratie
SCRIPT_DIR = Path(__file__).parent.resolve()
NBV21_DIR = SCRIPT_DIR / "nbv21"

# Mapping configuratie (Bron: get_chapter.R)
MAPPINGS_SOURCE = {
    # Old Testament
    "GEN": ["GEN", "Gen", "Genesis", "1 Mozes", "1Mozes"],
    "EXO": ["EXO", "Exo", "Exodus", "2 Mozes", "2Mozes"],
    "LEV": ["LEV", "Lev", "Leviticus", "3 Mozes", "3Mozes"],
    "NUM": ["NUM", "Num", "Numeri", "4 Mozes", "4Mozes"],
    "DEU": ["DEU", "Deut", "Deuteronomium", "5 Mozes", "5Mozes"],
    "JOS": ["JOS", "Jozua", "Joshua"],
    "JDG": ["JDG", "Rechters", "Judges", "Richteren"],
    "RUT": ["RUT", "Ruth"],
    "1SA": ["1SA", "1 Samuel", "1 Samuël", "1Samuel", "1Samuël", "1 Sam", "1Sam", "1 Samuël"],
    "2SA": ["2SA", "2 Samuel", "2 Samuël", "2Samuel", "2Samuël", "2 Sam", "2Sam", "2 Samuël"],
    "1KI": ["1KI", "1 Koningen", "1Koningen", "1 Kings", "1Kings"],
    "2KI": ["2KI", "2 Koningen", "2Koningen", "2 Kings", "2Kings"],
    "1CH": ["1CH", "1 Kronieken", "1Kronieken", "1 Chronicles", "1Chronicles"],
    "2CH": ["2CH", "2 Kronieken", "2Kronieken", "2 Chronicles", "2Chronicles"],
    "EZR": ["EZR", "Ezra"],
    "NEH": ["NEH", "Nehemia", "Nehemiah"],
    "EST": ["EST", "Esther", "Ester"],
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
    "HAG": ["HAG", "Haggai", "Haggaï"],
    "ZEC": ["ZEC", "Zacharia", "Zechariah"],
    "MAL": ["MAL", "Maleachi", "Malachi"],
    # New Testament
    "MAT": ["MAT", "Matteüs", "Matthew", "Matt", "Matteus", "Mattheus", "Mattheüs"],
    "MRK": ["MRK", "Marcus", "Mark", "Markus"],
    "LUK": ["LUK", "Lucas", "Luke", "Lukas"],
    "JHN": ["JHN", "Johannes", "John"],
    "ACT": ["ACT", "Handelingen", "Acts"],
    "ROM": ["ROM", "Romeinen", "Romans"],
    "1CO": ["1CO", "1 Korinthiërs", "1Korinthiërs", "1 Korintiërs", "1Korintiërs", "1 Corinthians", "1Corinthians", "1 Kor", "1Kor"],
    "2CO": ["2CO", "2 Korinthiërs", "2Korinthiërs", "2 Korintiërs", "2Korintiërs", "2 Corinthians", "2Corinthians", "2 Kor", "2Kor"],
    "GAL": ["GAL", "Galaten", "Galatians"],
    "EPH": ["EPH", "Efeziërs", "Ephesians", "Efeze", "Efesiërs", "Efesiers"],
    "PHP": ["PHP", "Filippenzen", "Philippians"],
    "COL": ["COL", "Kolossenzen", "Colossians"],
    "1TH": ["1TH", "1 Tessalonicenzen", "1Tessalonicenzen", "1 Thessalonians", "1Thessalonians", "1 Thess", "1Thess"],
    "2TH": ["2TH", "2 Tessalonicenzen", "2Tessalonicenzen", "2 Thessalonians", "2Thessalonians", "2 Thess", "2Thess"],
    "1TI": ["1TI", "1 Timoteüs", "1Timoteüs", "1 Timotheüs", "1Timotheüs", "1 Timothy", "1Timothy", "1 Tim", "1Tim"],
    "2TI": ["2TI", "2 Timoteüs", "2Timoteüs", "2 Timotheüs", "2Timotheüs", "2 Timothy", "2Timothy", "2 Tim", "2Tim"],
    "TIT": ["TIT", "Titus"],
    "PHM": ["PHM", "Filemon", "Philemon"],
    "HEB": ["HEB", "Hebreeën", "Hebreeen", "Hebrews"],
    "JAS": ["JAS", "Jakobus", "Jacobus", "James"],
    "1PE": ["1PE", "1 Petrus", "1Petrus", "1 Peter", "1Peter", "1 Pet", "1Pet"],
    "2PE": ["2PE", "2 Petrus", "2Petrus", "2 Peter", "2Peter", "2 Pet", "2Pet"],
    "1JN": ["1JN", "1 Johannes", "1Johannes", "1 John", "1John"],
    "2JN": ["2JN", "2 Johannes", "2Johannes", "2 John", "2John"],
    "3JN": ["3JN", "3 Johannes", "3Johannes", "3 John", "3John"],
    "JUD": ["JUD", "Judas", "Jude"],
    "REV": ["REV", "Openbaring", "Revelation", "Openbaring van Johannes", "Openbaringen"],
    # Deuterocanonical
    "TOB": ["TOB", "Tobit"],
    "JDT": ["JDT", "Judith", "Judit"],
    "ESG": ["ESG", "Ester (Gr)", "Esther (Gr)", "Esther (Greek)"],
    "WIS": ["WIS", "Wijsheid", "Wijsheid van Salomo", "Wisdom", "Wisdom of Solomon"],
    "SIR": ["SIR", "Sirach", "Jezus Sirach", "Ecclesiasticus"],
    "BAR": ["BAR", "Baruch"],
    "LJE": ["LJE", "Brief van Jeremia", "Letter of Jeremiah"],
    "DAG": ["DAG", "Daniël (Gr)", "Daniel (Gr)", "Daniel (Greek)"], # Azarja, Susanna, Bel en de Draak vaak hieronder of apart
    "1MA": ["1MA", "1 Makkabeeën", "1Makkabeeën", "1 Maccabees"],
    "2MA": ["2MA", "2 Makkabeeën", "2Makkabeeën", "2 Maccabees"],
    "3MA": ["3MA", "3 Makkabeeën", "3Makkabeeën", "3 Maccabees"],
    "4MA": ["4MA", "4 Makkabeeën", "4Makkabeeën", "4 Maccabees"],
    "MAN": ["MAN", "Gebed van Manasse", "Prayer of Manasseh"]
}

NAME_TO_CODE = {}
for code, names in MAPPINGS_SOURCE.items():
    for name in names:
        NAME_TO_CODE[name.upper()] = code

def get_book_code(book_name: str) -> Optional[str]:
    return NAME_TO_CODE.get(book_name.upper().strip())

def get_nbv21_data(ref: BijbelReferentie) -> Optional[List[Dict]]:
    """Haalt data (verzen) op voor een gegeven referentie."""
    code = get_book_code(ref.boek)
    if not code:
        return None

    json_path = NBV21_DIR / code / f"{code}.{ref.hoofdstuk}.json"
    
    if not json_path.exists():
        return None

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Fout bij lezen NBV21 bestand {json_path}: {e}")
        return None

    verses = data.get('verses', [])
    selected_verses = []

    start = ref.vers_start if ref.vers_start else 1
    if ref.vers_start is None:
        end = 9999
    elif ref.vers_eind is None:
        end = start
    else:
        end = ref.vers_eind

    for v in verses:
        v_num = v.get('verse')
        if v_num >= start and v_num <= end:
            text = re.sub(r'\s+', ' ', v.get('text')).strip()
            selected_verses.append({
                "verse": v_num,
                "text": text
            })

    if not selected_verses:
        return None
        
    return selected_verses

def get_nbv21_text(ref: BijbelReferentie) -> Optional[str]:
    """Haalt tekst op voor een gegeven referentie uit de lokale JSON bestanden."""
    selected_verses = get_nbv21_data(ref)
    if not selected_verses:
        return None

    header = f"### {ref.boek.title()} {ref.hoofdstuk}"
    if ref.vers_start:
        header += f":{ref.vers_start}"
        if ref.vers_eind and ref.vers_eind != ref.vers_start:
            header += f"-{ref.vers_eind}"
    
    lines = [f"{v['verse']}. {v['text']}" for v in selected_verses]
    return f"{header} (NBV21)\n" + "\n".join(lines)

def save_nbv21_lezingen(output_dir: Path, context_text: str) -> dict[str, str]:
    """Sla NBV21 lezingen op als JSON bestanden."""
    print("\nNBV21 teksten verwerken...")

    # Check of NBV21 data aanwezig is
    if not NBV21_DIR.exists() or not any(NBV21_DIR.iterdir()):
        print(f"  ⚠ WAARSCHUWING: NBV21 data map is leeg of bestaat niet: {NBV21_DIR}")
        print("  Plaats de NBV21 JSON bestanden in deze map (structuur: nbv21/BOEK/BOEK.HOOFDSTUK.json)")
        print("  NBV21 teksten worden niet online opgehaald.")
        return {}

    bijbel_dir = output_dir / "bijbelteksten"
    bijbel_dir.mkdir(exist_ok=True)

    resultaten = {}
    seen_refs = set()
    found_refs_raw = []

    # Probeer eerst de context_text te parsen als JSON en haal alleen lezingen op
    try:
        data = json.loads(context_text)

        # Haal alleen referenties uit de 'lezingen' key
        if 'lezingen' in data:
            lezingen_obj = data['lezingen']

            # Haal referenties uit de standaard lezingen
            for key in ['eerste_lezing', 'tweede_lezing', 'derde_lezing', 'epistel', 'evangelie', 'psalm']:
                if key in lezingen_obj and isinstance(lezingen_obj[key], dict):
                    ref = lezingen_obj[key].get('referentie', '')
                    if ref and ref not in seen_refs:
                        # Speciale behandeling voor psalm nummers
                        if key == 'psalm' and re.match(r'^\d+$', ref):
                            ref = f"Psalm {ref}"
                        found_refs_raw.append(ref)
                        seen_refs.add(ref)

            # Haal referenties uit alternatieve lezingen
            if 'alternatieve_lezingen' in lezingen_obj and isinstance(lezingen_obj['alternatieve_lezingen'], list):
                for alt in lezingen_obj['alternatieve_lezingen']:
                    if isinstance(alt, dict):
                        ref = alt.get('referentie', '')
                        if ref and ref not in seen_refs:
                            found_refs_raw.append(ref)
                            seen_refs.add(ref)

    except (json.JSONDecodeError, KeyError, TypeError):
        # Fallback naar oude regex methode als JSON parsing mislukt
        # 1. Probeer JSON style referenties
        json_matches = re.findall(r'"referentie":\s*"([^"]+)"', context_text)
        found_refs_raw.extend(json_matches)

        # 2. Probeer Markdown style referenties
        regex = r'(?:lezing|evangelie|schriftlezing).*?[:]\s*([A-Za-z0-9\s:,-–\(\)]+)'
        matches = re.finditer(regex, context_text, re.IGNORECASE)
        for match in matches:
            found_refs_raw.append(match.group(1).strip())

    # Reset seen_refs voor verwerking
    seen_refs = set()

    processed_refs = []
    # 1. Parse all references first
    for raw_ref in found_refs_raw:
        # Normaliseer eerst (verwijder a/b, split cross-hoofdstuk)
        normalized_ref = normalize_scripture_reference(raw_ref)

        # Check for complex references with semicolons and " en " (e.g., "Sefanja 2:3; 3:12-13" or "Jesaja 8:23 en Jesaja 9:1-3")
        # Replace " en " with "; " for uniform splitting
        normalized_ref = re.sub(r'\s+en\s+', '; ', normalized_ref)
        parts = normalized_ref.split(';')
        sub_refs = []
        last_book = None
        
        for part in parts:
            part = part.strip()
            if not part: continue
            
            # Check if part starts with a book name
            book_match = re.match(r'^(\d?\s*[A-Za-zëïüéèöä]+(?:\s+[A-Za-zëïüéèöä]+)*)', part)
            if book_match and get_book_code(book_match.group(1)):
                last_book = book_match.group(1)
                sub_refs.append(part)
            elif last_book and re.match(r'^\d+[:]', part):
                # Starts with chapter:verse, prepend last book
                sub_refs.append(f"{last_book} {part}")
            else:
                # Fallback
                sub_refs.append(part)
        
        processed_refs.append({'original': raw_ref, 'subs': sub_refs})

    # 2. Fetch and save
    for item in processed_refs:
        raw_ref = item['original']
        sub_refs = item['subs']
        
        all_pericopes = []
        full_ref_key = raw_ref # Use full string as key
        
        if full_ref_key in seen_refs: continue
        
        for sub_ref_str in sub_refs:
            # Check for multi-range syntax (e.g. "1, 3-5") in this sub part
            # Use existing regex for book chapter verses
            complex_match = re.match(r"^\s*((?:\d\s)?[A-Za-zëïüéèöä\s]+?)\s+(\d+)[\s,:]+([\d\-–.;a-z]+)", sub_ref_str)
            
            if complex_match:
                book_name = complex_match.group(1).strip()
                chapter = int(complex_match.group(2))
                verse_part = complex_match.group(3)
                
                # Split verse part on . or , if they imply ranges within same chapter
                # But here we assume sub_ref_str is already split by semicolon (chapters)
                # So just handle verses in one chapter
                verse_ranges = re.split(r'[.,]', verse_part)
                
                for v_range in verse_ranges:
                    v_range = v_range.strip()
                    if not v_range: continue
                    
                    ref_obj = parse_bijbelreferentie(f"{book_name} {chapter}:{v_range}")
                    if ref_obj and get_book_code(ref_obj.boek):
                        verses_data = get_nbv21_data(ref_obj)
                        if verses_data:
                            all_pericopes.append({
                                "book": get_book_code(ref_obj.boek),
                                "chapter": ref_obj.hoofdstuk,
                                "verses": verses_data,
                                "translation": "NBV21"
                            })
            else:
                # Fallback for simple parse
                ref_obj = parse_bijbelreferentie(sub_ref_str)
                if ref_obj and get_book_code(ref_obj.boek):
                    verses_data = get_nbv21_data(ref_obj)
                    if verses_data:
                        all_pericopes.append({
                            "book": get_book_code(ref_obj.boek),
                            "chapter": ref_obj.hoofdstuk,
                            "verses": verses_data,
                            "translation": "NBV21"
                        })

        if all_pericopes:
            seen_refs.add(full_ref_key)
            
            # Filename generation based on the full original string (sanitized)
            safe_name = raw_ref.replace(':', '_').replace(' ', '_').replace(';', '_')
            safe_name = re.sub(r'[^\w\-.]', '', safe_name)
            # Limit length
            if len(safe_name) > 50: safe_name = safe_name[:50]
            
            json_path = bijbel_dir / f"{safe_name}_NBV21.json"
            
            # If we have only one pericope, save as object (backward compat for clean single files)
            # But wait, user wants consistency. The loader now supports list.
            # Let's save as list if > 1, else object? 
            # No, if I save as object, the loader appends it. If list, loader extends it. 
            # Both result in flat list in combined_output.
            # So it doesn't matter for the structure, but "one file" matters.
            
            final_data = all_pericopes if len(all_pericopes) > 1 else all_pericopes[0]
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=2, ensure_ascii=False)
                
            print(f"  ✓ NBV21 Opgeslagen: {json_path.name}")
            resultaten[full_ref_key] = str(json_path)
        else:
             print(f"  ✗ NBV21 Niet gevonden of incompleet: {raw_ref}")

    return resultaten

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
