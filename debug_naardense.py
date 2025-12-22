#!/usr/bin/env python3
"""
Debug script om te zien waarom 1 Samuel/1 Samuël niet werkt
"""

from naardense_bijbel import parse_bijbelreferentie, get_boek_slug, BOEK_NAAR_SLUG

def debug_referentie(tekst):
    print(f"\nDebuggen: '{tekst}'")
    
    # Parse de referentie
    ref = parse_bijbelreferentie(tekst)
    if ref:
        print(f"  -> Geparseerde referentie: {ref}")
        
        # Controleer boek slug
        slug = get_boek_slug(ref.boek)
        print(f"  -> Boek: '{ref.boek}'")
        print(f"  -> Slug: {slug}")
        
        # Controleer of het boek in de mapping zit
        if ref.boek.lower() in BOEK_NAAR_SLUG:
            print(f"  -> Boek gevonden in mapping: {BOEK_NAAR_SLUG[ref.boek.lower()]}")
        else:
            print(f"  -> Boek NIET GEVONDEN in mapping")
            
        # Laat alle mogelijke varianten zien voor "samuel"
        print(f"  -> Alle 'samuel' varianten in mapping:")
        for k, v in BOEK_NAAR_SLUG.items():
            if 'samuel' in k.lower():
                print(f"     '{k}' -> '{v}'")
    else:
        print(f"  -> Kon referentie niet parsen!")

# Test verschillende varianten
test_strings = [
    "1 samuël 1:20-22",
    "1 samuël 1:24-28", 
    "1 samuel 1:20-22",
    "1 samuel 1:24-28",
    "1 Samuel 1:20-22",
    "1 Samuël 1:20-22",
    "1 samuël 1",
    "1 Samuel 1"
]

for test_str in test_strings:
    debug_referentie(test_str)