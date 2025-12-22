import csv
import json
import re
from pathlib import Path

# Configuratie
SCRIPT_DIR = Path(__file__).parent.resolve()
MISC_DIR = SCRIPT_DIR / "misc"

BHS_PATH = MISC_DIR / "BHS.tsv"
NA28_PATH = MISC_DIR / "NA28.tsv"

# Mappings
# Dutch Name -> BHS Name (or None if NT/Deutero)
BHS_MAPPING = {
    "Genesis": "Genesis",
    "Exodus": "Exodus",
    "Leviticus": "Leviticus",
    "Numeri": "Numeri",
    "Deuteronomium": "Deuteronomium",
    "Jozua": "Josua",
    "Rechters": "Judices",
    "Rech": "Judices",
    "Ruth": "Ruth",
    "1 Samuël": "Samuel_I",
    "2 Samuël": "Samuel_II",
    "1 Koningen": "Reges_I",
    "2 Koningen": "Reges_II",
    "1 Kronieken": "Chronica_I",
    "2 Kronieken": "Chronica_II",
    "Ezra": "Esra",
    "Nehemia": "Nehemia",
    "Esther": "Esther",
    "Job": "Iob",
    "Psalmen": "Psalmi",
    "Psalm": "Psalmi",
    "Spreuken": "Proverbia",
    "Prediker": "Ecclesiastes",
    "Hooglied": "Canticum",
    "Jesaja": "Jesaia",
    "Jeremia": "Jeremia",
    "Klaagliederen": "Threni",
    "Ezechiël": "Ezechiel",
    "Daniël": "Daniel",
    "Hosea": "Hosea",
    "Joël": "Joel",
    "Amos": "Amos",
    "Obadja": "Obadia",
    "Jona": "Jona",
    "Micha": "Micha",
    "Nahum": "Nahum",
    "Habakuk": "Habakuk",
    "Sefanja": "Zephania",
    "Haggai": "Haggai",
    "Zacharia": "Sacharia",
    "Maleachi": "Maleachi"
}

# Dutch Name -> NA28 Code
NA28_MAPPING = {
    "Matteüs": "MAT",
    "Marcus": "MRK",
    "Lucas": "LUK",
    "Johannes": "JHN",
    "Handelingen": "ACT",
    "Romeinen": "ROM",
    "1 Korintiërs": "1CO",
    "2 Korintiërs": "2CO",
    "Galaten": "GAL",
    "Efeziërs": "EPH",
    "Filippenzen": "PHP",
    "Kolossenzen": "COL",
    "1 Tessalonicenzen": "1TH",
    "2 Tessalonicenzen": "2TH",
    "1 Timoteüs": "1TI",
    "2 Timoteüs": "2TI",
    "Titus": "TIT",
    "Filemon": "PHM",
    "Hebreeën": "HEB",
    "Jakobus": "JAS",
    "1 Petrus": "1PE",
    "2 Petrus": "2PE",
    "1 Johannes": "1JN",
    "2 Johannes": "2JN",
    "3 Johannes": "3JN",
    "Judas": "JUD",
    "Openbaring": "REV"
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
    Parses a reference string like "Genesis 1:1-5" or "Matteüs 5,1-12".
    Returns (book_nl, chapter, verse_start, verse_end).
    """
    # Regex to handle variations like "1 Koningen 12,3", "Jesaja 2:1-5", "Psalm 122"
    match = re.match(r"^\s*((?:\d\s)?[a-zA-Zëïüöä\s]+?)\s+(\d+)(?:[,.:\s]+(\d+)(?:[-–](\d+))?)?\s*$", reference)
    if not match:
        return None
    
    book_nl = match.group(1).strip()
    try:
        chapter = int(match.group(2))
        # Handle references with only book and chapter (e.g. "Psalm 122")
        verse_start = int(match.group(3)) if match.group(3) else 1
        verse_end = int(match.group(4)) if match.group(4) else verse_start
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
    
    # Try BHS (OT)
    if book_nl in BHS_MAPPING:
        bhs_name = BHS_MAPPING[book_nl]
        bhs_data = load_bhs()
        
        if bhs_name in bhs_data and chapter in bhs_data[bhs_name]:
            verses = []
            # Handle potential verse ranges that go beyond what we naively parsed? 
            # No, assume the parser captured the requested range.
            # But ensure we don't crash if a verse is missing.
            
            for v in range(v_start, v_end + 1):
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
    if book_nl in NA28_MAPPING:
        na28_code = NA28_MAPPING[book_nl]
        na28_data = load_na28()
        
        if na28_code in na28_data and chapter in na28_data[na28_code]:
            verses = []
            for v in range(v_start, v_end + 1):
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
    """
    try:
        if isinstance(liturgische_context_json, str):
            context = json.loads(liturgische_context_json)
        else:
            context = liturgische_context_json
    except:
        print("Fout bij parsen liturgische context voor grondtekst.")
        return []
        
    lezingen = context.get("lezingen", {})
    files_saved = []
    
    # References to fetch
    references_to_process = []

    # Standard keys
    keys = ["eerste_lezing", "tweede_lezing", "epistel", "evangelie", "psalm"]
    for key in keys:
        if key in lezingen and isinstance(lezingen[key], dict):
            ref = lezingen[key].get("referentie")
            if ref:
                references_to_process.append(ref)

    # Alternatives
    alternatives = lezingen.get("alternatieve_lezingen", [])
    if isinstance(alternatives, list):
        for alt in alternatives:
            if isinstance(alt, dict) and "referentie" in alt:
                references_to_process.append(alt["referentie"])

    bijbel_dir = folder / "bijbelteksten"
    bijbel_dir.mkdir(parents=True, exist_ok=True)
    
    for ref in references_to_process:
        # Avoid duplicates or reprocessing
        # (Could add check if file exists, but overwriting is safer for updates)
        
        # Handle complex references like "Handelingen 6,8-10; 7,54-60"
        # My simple parser only handles the first part. 
        # For now, let's just split by ';' and try to fetch each part
        
        sub_refs = ref.split(';')
        for sub_ref in sub_refs:
            sub_ref = sub_ref.strip()
            # If sub_ref starts with a digit but no book name (e.g. "7,54-60"), 
            # we need to infer the book from the previous part.
            # This is complex. For MVP, we stick to the main simple parser or try to handle simple "Book Ch:V"
            # If parse fails, we skip.
            
            # Simple heuristic for book carry-over:
            if re.match(r"^\d+[,:]", sub_ref):
                # This is a continuation like "7,54-60". 
                # We need the book from the previous valid ref.
                # IMPLEMENTATION DETAIL: This requires tracking state.
                # For safety, I'll only process fully qualified references for now to avoid errors.
                # However, the simple parser requires a book name.
                pass
            
            data = get_grondtekst(sub_ref)
            if data:
                # Create a safe filename
                safe_ref = sub_ref.replace(" ", "_").replace(":", "_").replace(",", "_")
                
                filename = f"{safe_ref}_Grondtekst.json"
                filepath = bijbel_dir / filename
                
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                files_saved.append(filepath)
            
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
