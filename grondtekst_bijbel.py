import csv
import json
import re
from pathlib import Path

# Configuratie
SCRIPT_DIR = Path(__file__).parent.resolve()
MISC_DIR = SCRIPT_DIR / "misc"

BHS_PATH = MISC_DIR / "BHS.tsv"
NA28_PATH = MISC_DIR / "NA28.tsv"

# Mappings - Keys are all lowercase for case-insensitive matching
BHS_MAPPING = {
    "genesis": "Genesis",
    "exodus": "Exodus",
    "leviticus": "Leviticus",
    "numeri": "Numeri",
    "deuteronomium": "Deuteronomium",
    "jozua": "Josua",
    "rechters": "Judices",
    "rech": "Judices",
    "ruth": "Ruth",
    "1 samuël": "Samuel_I", "1 samuel": "Samuel_I",
    "2 samuël": "Samuel_II", "2 samuel": "Samuel_II",
    "1 koningen": "Reges_I",
    "2 koningen": "Reges_II",
    "1 kronieken": "Chronica_I",
    "2 kronieken": "Chronica_II",
    "ezra": "Esra",
    "nehemia": "Nehemia",
    "esther": "Esther",
    "job": "Iob",
    "psalmen": "Psalmi",
    "psalm": "Psalmi",
    "spreuken": "Proverbia",
    "prediker": "Ecclesiastes",
    "hooglied": "Canticum",
    "jesaja": "Jesaia",
    "jeremia": "Jeremia",
    "klaagliederen": "Threni",
    "ezechiël": "Ezechiel", "ezechiel": "Ezechiel",
    "daniël": "Daniel", "daniel": "Daniel",
    "hosea": "Hosea",
    "joël": "Joel", "joel": "Joel",
    "amos": "Amos",
    "obadja": "Obadia",
    "jona": "Jona",
    "micha": "Micha",
    "nahum": "Nahum",
    "habakuk": "Habakuk",
    "sefanja": "Zephania",
    "haggai": "Haggai",
    "zacharia": "Sacharia",
    "maleachi": "Maleachi"
}

# Dutch Name -> NA28 Code (lowercase keys)
NA28_MAPPING = {
    "matteüs": "MAT", "matteus": "MAT", "mattheüs": "MAT",
    "marcus": "MRK",
    "lucas": "LUK",
    "johannes": "JHN",
    "handelingen": "ACT",
    "romeinen": "ROM",
    "1 korintiërs": "1CO", "1 korintiers": "1CO",
    "2 korintiërs": "2CO", "2 korintiers": "2CO",
    "galaten": "GAL",
    "efeziërs": "EPH", "efeze": "EPH",
    "filippenzen": "PHP",
    "kolossenzen": "COL",
    "1 tessalonicenzen": "1TH",
    "2 tessalonicenzen": "2TH",
    "1 timoteüs": "1TI", "1 timoteus": "1TI",
    "2 timoteüs": "2TI", "2 timoteus": "2TI",
    "titus": "TIT",
    "filemon": "PHM",
    "hebreeën": "HEB",
    "jakobus": "JAS",
    "1 petrus": "1PE",
    "2 petrus": "2PE",
    "1 johannes": "1JN",
    "2 johannes": "2JN",
    "3 johannes": "3JN",
    "judas": "JUD",
    "openbaring": "REV"
}

# Cache for loaded texts
_BHS_DATA = None
_NA28_DATA = None

def load_bhs():
    global _BHS_DATA
    if _BHS_DATA is not None:
        return _BHS_DATA
    
    data = {}
    if not BHS_PATH.exists():
        print(f"Warning: BHS file not found at {BHS_PATH}")
        return {}

    try:
        with open(BHS_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t', quotechar='"')
            for row in reader:
                if not row['name']: continue 
                
                book = row['name'].strip('"')
                try:
                    chapter = int(row['chapter'])
                    verse = int(row['verse'])
                except ValueError:
                    continue
                    
                text = row['hebrew_sentence'].strip('"')
                
                if book not in data:
                    data[book] = {}
                if chapter not in data[book]:
                    data[book][chapter] = {}
                
                data[book][chapter][verse] = text
    except Exception as e:
        print(f"Error loading BHS: {e}")
        return {}
            
    _BHS_DATA = data
    return data

def load_na28():
    global _NA28_DATA
    if _NA28_DATA is not None:
        return _NA28_DATA
        
    data = {}
    if not NA28_PATH.exists():
        print(f"Warning: NA28 file not found at {NA28_PATH}")
        return {}
    
    try:
        with open(NA28_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t', quotechar='"')
            for row in reader:
                if not row['book']: continue
                
                book = row['book'].strip('"')
                try:
                    chapter = int(row['chapter'])
                    verse = int(row['verse'])
                except ValueError:
                    continue

                text = row['text'].strip('"')
                
                if book not in data:
                    data[book] = {}
                if chapter not in data[book]:
                    data[book][chapter] = {}
                
                data[book][chapter][verse] = text
    except Exception as e:
        print(f"Error loading NA28: {e}")
        return {}
            
    _NA28_DATA = data
    return data

def parse_reference(reference):
    """
    Parses a reference string like "Genesis 1:1-5" or "Psalm 122".
    Returns (book_nl, chapter, verse_start, verse_end).
    If no verses are given, verse_start and verse_end are None.
    """
    match = re.match(r"^\s*((?:\d\s)?[a-zA-Zëïüöä\s]+?)\s+(\d+)(?:[,.:\s]+(\d+)(?:[-–](\d+))?)?\s*$", reference)
    if not match:
        return None
    
    book_nl = match.group(1).strip()
    try:
        chapter = int(match.group(2))
        if match.group(3):
            verse_start = int(match.group(3))
            verse_end = int(match.group(4)) if match.group(4) else verse_start
        else:
            # No verse specified, indicates whole chapter
            verse_start = None
            verse_end = None
    except (ValueError, IndexError):
        return None
    
    return book_nl, chapter, verse_start, verse_end

def get_grondtekst(reference):
    """
    Retrieves the original text (Hebrew/Greek) for a reference.
    Returns a dict with metadata and text.
    """
    parsed = parse_reference(reference)
    if not parsed:
        return None
        
    book_nl, chapter, v_start, v_end = parsed
    book_key = book_nl.lower()
    
    # Try BHS (OT)
    if book_key in BHS_MAPPING:
        bhs_name = BHS_MAPPING[book_key]
        bhs_data = load_bhs()
        
        if bhs_name in bhs_data and chapter in bhs_data[bhs_name]:
            verses = []
            
            verse_iterator = []
            if v_start is None: # Whole chapter
                verse_iterator = sorted(bhs_data[bhs_name][chapter].keys())
            else: # Specific range
                verse_iterator = range(v_start, v_end + 1)

            for v in verse_iterator:
                if v in bhs_data[bhs_name][chapter]:
                    verses.append({
                        "verse": v,
                        "text": bhs_data[bhs_name][chapter][v]
                    })
            
            if verses:
                return {
                    "source": "BHS (Biblia Hebraica Stuttgartensia)",
                    "book_nl": book_nl,
                    "book_original": bhs_name,
                    "chapter": chapter,
                    "verses": verses,
                    "language": "Hebrew"
                }

    # Try NA28 (NT)
    if book_key in NA28_MAPPING:
        na28_code = NA28_MAPPING[book_key]
        na28_data = load_na28()
        
        if na28_code in na28_data and chapter in na28_data[na28_code]:
            verses = []

            verse_iterator = []
            if v_start is None: # Whole chapter
                verse_iterator = sorted(na28_data[na28_code][chapter].keys())
            else: # Specific range
                verse_iterator = range(v_start, v_end + 1)
            
            for v in verse_iterator:
                if v in na28_data[na28_code][chapter]:
                    verses.append({
                        "verse": v,
                        "text": na28_data[na28_code][chapter][v]
                    })
                    
            if verses:
                return {
                    "source": "NA28 (Novum Testamentum Graece)",
                    "book_nl": book_nl,
                    "book_original": na28_code,
                    "chapter": chapter,
                    "verses": verses,
                    "language": "Greek"
                }
                
    return None

def save_grondtekst_lezingen(folder, liturgische_context_json):
    """
    Extracts references from the liturgical context and saves source texts to JSON.
    Handles complex references with multiple verse ranges.
    """
    try:
        context = json.loads(liturgische_context_json) if isinstance(liturgische_context_json, str) else liturgische_context_json
    except:
        print("Fout bij parsen liturgische context voor grondtekst.")
        return []
        
    lezingen = context.get("lezingen", {})
    files_saved = []
    
    references_to_process = []
    keys = ["eerste_lezing", "tweede_lezing", "epistel", "evangelie", "psalm"]
    for key in keys:
        if key in lezingen and isinstance(lezingen[key], dict) and lezingen[key].get("referentie"):
            references_to_process.append(lezingen[key]["referentie"])

    alternatives = lezingen.get("alternatieve_lezingen", [])
    if isinstance(alternatives, list):
        for alt in alternatives:
            if isinstance(alt, dict) and "referentie" in alt:
                references_to_process.append(alt["referentie"])

    bijbel_dir = folder / "bijbelteksten"
    bijbel_dir.mkdir(parents=True, exist_ok=True)
    
    for ref_str in references_to_process:
        print(f"  Processing reference: '{ref_str}'")
        
        all_verses_for_ref = []
        collected_data_header = {}
        
        # 1. Separate book/chapter from verse string
        match = re.match(r"^\s*((?:\d\s)?[A-Za-zëïüöä\s]+?)\s+(\d+)[\s,:]+(.*)", ref_str)
        
        sub_refs = []
        if match:
            book_chapter_base = f"{match.group(1).strip()} {match.group(2)}"
            verse_part = match.group(3)
            # Split verse part by '.', ';', or ',' (but not if it's the main chapter separator)
            verse_ranges = re.split(r'[.;]', verse_part)
            for verse_range in verse_ranges:
                if verse_range.strip():
                    sub_refs.append(f"{book_chapter_base}:{verse_range.strip()}")
        else:
            # Cannot parse complex, treat as single reference (e.g., "Psalm 128")
            sub_refs.append(ref_str)

        # 2. Fetch data for each sub-reference
        for sub_ref in sub_refs:
            data = get_grondtekst(sub_ref)
            if data and "verses" in data:
                if not collected_data_header:
                    # Store header info from the first successful fetch
                    collected_data_header = data.copy()
                    del collected_data_header["verses"]
                all_verses_for_ref.extend(data["verses"])
        
        # 3. If any verses were found, combine and save
        if collected_data_header and all_verses_for_ref:
            # Sort verses by verse number and remove duplicates
            unique_verses = {v['verse']: v for v in all_verses_for_ref}.values()
            sorted_verses = sorted(list(unique_verses), key=lambda x: x['verse'])
            
            collected_data_header["verses"] = sorted_verses
            
            # Construct filename with only book and chapter
            book_name_for_file = collected_data_header["book_nl"].title()
            chapter_for_file = collected_data_header["chapter"]
            
            safe_name = f"{book_name_for_file}_{chapter_for_file}"
            safe_name = re.sub(r'[^\w_]', '', safe_name.replace(" ", "_"))
            
            filename = f"{safe_name}_Grondtekst.json"
            filepath = bijbel_dir / filename
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(collected_data_header, f, ensure_ascii=False, indent=2)
            
            print(f"    -> Success: Saved combined text to {filename}")
            files_saved.append(filepath)
        else:
            print(f"    -> No text found for '{ref_str}'")
            
    return files_saved

if __name__ == "__main__":
    # Test basic fetching
    print("Testing Genesis 1:1-3 (BHS)...")
    gen_data = get_grondtekst("Genesis 1:1-3")
    if gen_data:
        print(f"Success! Found {len(gen_data['verses'])} verses.")
        print(json.dumps(gen_data, indent=2, ensure_ascii=False))
    else:
        print("Failed to fetch Genesis 1:1-3")

    print("\nTesting Matteüs 1:18-20 (NA28)...")
    mat_data = get_grondtekst("Matteüs 1:18-20")
    if mat_data:
        print(f"Success! Found {len(mat_data['verses'])} verses.")
        print(json.dumps(mat_data, indent=2, ensure_ascii=False))
    else:
        print("Failed to fetch Matteüs 1:18-20")

    print("\nTesting 1 Samuël 1:1-3 (BHS)...")
    sam_data = get_grondtekst("1 Samuël 1:1-3")
    if sam_data:
        print(f"Success! Found {len(sam_data['verses'])} verses.")
        print(json.dumps(sam_data, indent=2, ensure_ascii=False))
    else:
        print("Failed to fetch 1 Samuël 1:1-3")
