#!/usr/bin/env python3
"""
Debug script om te zien hoe het complexe referentiepatroon werkt
"""

import re
from naardense_bijbel import parse_bijbelreferentie, get_boek_slug

def debug_complex_pattern():
    # Test de exacte regex die gebruikt wordt in het script
    ref_str = "1 Samuël 1,20-22.24-28"
    print(f"Test referentie: '{ref_str}'")
    
    # Exacte regex zoals gebruikt in het script
    complex_match = re.match(r"^\s*((?:\d\s)?[A-Za-zëïüöä\s]+?)\s+(\d+)[\s,:]+([\d\-–.;a-z]+)", ref_str)
    
    if complex_match:
        print(f"  -> Match groep 1 (boek): '{complex_match.group(1).strip()}'")
        print(f"  -> Match groep 2 (hoofdstuk): '{complex_match.group(2)}'")
        print(f"  -> Match groep 3 (verzen): '{complex_match.group(3)}'")
        
        book_chapter_base = f"{complex_match.group(1).strip()} {complex_match.group(2)}"
        verse_part = complex_match.group(3)
        
        print(f"  -> Book-chapter base: '{book_chapter_base}'")
        print(f"  -> Verse part: '{verse_part}'")
        
        # Split verse part op . of ;
        verse_ranges = re.split(r'[.;]', verse_part)
        print(f"  -> Verse ranges: {verse_ranges}")
        
        for verse_range in verse_ranges:
            verse_range = verse_range.strip()
            if not verse_range:
                continue
                
            print(f"    -> Verwerken range: '{verse_range}'")
            sub_ref_str = f"{book_chapter_base}:{verse_range}"
            print(f"    -> Sub referentie: '{sub_ref_str}'")
            
            referentie = parse_bijbelreferentie(sub_ref_str)
            if referentie:
                print(f"    -> Geparseerde referentie: {referentie}")
                slug = get_boek_slug(referentie.boek)
                print(f"    -> Boek slug: {slug}")
            else:
                print(f"    -> Kon referentie niet parsen!")
    else:
        print("  -> Geen match voor complex patroon")
        
        # Probeer simpele parsing
        referentie = parse_bijbelreferentie(ref_str)
        if referentie:
            print(f"  -> Simpel geparseerd: {referentie}")
            slug = get_boek_slug(referentie.boek)
            print(f"  -> Boek slug: {slug}")
        else:
            print("  -> Ook geen simpele match")

debug_complex_pattern()