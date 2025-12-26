#!/usr/bin/env python3
"""
Shared utilities for Bible text extraction and reference normalization.

This module provides centralized functions for extracting liturgical readings
and normalizing scripture references, used by naardense_bijbel, nbv21_bijbel,
and grondtekst_bijbel modules.
"""

import json
import re
from typing import List, Tuple


def normalize_scripture_reference(reference: str) -> str:
    """
    Normaliseer schriftverwijzingen door 'a'/'b' suffixen te verwijderen en
    cross-hoofdstuk referenties te splitsen.

    Bijvoorbeeld:
    - "Jesaja 8:23b-9:3" -> "Jesaja 8:23 en Jesaja 9:1-3"
    - "Marcus 1:14a-20" -> "Marcus 1:14-20"

    Args:
        reference: De originele bijbelreferentie

    Returns:
        De genormaliseerde referentie
    """
    if not reference or not isinstance(reference, str):
        return reference

    # Verwijder 'a' of 'b' achter versnummers
    normalized = re.sub(r'(\d+)[ab]\b', r'\1', reference)

    # Detecteer cross-hoofdstuk referenties (bijv. "Jesaja 8:23-9:3")
    # Pattern: Book Chapter:Verse-Chapter:Verse
    cross_chapter_pattern = r'^((?:\d\s+)?[A-Za-zëïüéèöä]+(?:\s+[A-Za-zëïüéèöä]+)*)\s+(\d+):(\d+)[-–](\d+):(\d+)$'
    match = re.match(cross_chapter_pattern, normalized)

    if match:
        book = match.group(1)
        chapter1 = match.group(2)
        verse1 = match.group(3)
        chapter2 = match.group(4)
        verse2 = match.group(5)

        # Split in twee delen: eerste hoofdstuk tot einde, tweede hoofdstuk vanaf vers 1
        normalized = f"{book} {chapter1}:{verse1} en {book} {chapter2}:1-{verse2}"

    return normalized


def extract_lezingen_uit_liturgie(liturgie_tekst: str) -> List[Tuple[str, str]]:
    """
    Extraheer bijbelreferenties uit de liturgische context.

    Haalt alleen de officiële lezingen uit de 'lezingen' key van de JSON.
    Dit voorkomt dat andere bijbelreferenties (bijvoorbeeld in toelichtingen)
    ook worden gedownload.

    Args:
        liturgie_tekst: De liturgische context als JSON string

    Returns:
        List of tuples (original_reference, normalized_reference)
    """
    referenties = []  # List of (original, normalized) tuples
    seen_originals = set()

    # Probeer de liturgie_tekst te parsen als JSON
    try:
        data = json.loads(liturgie_tekst)

        # Haal alleen referenties uit de 'lezingen' key
        if 'lezingen' in data:
            lezingen_obj = data['lezingen']

            # Haal ALLEEN de primaire lezingen op (geen alternatieve lezingen)
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

        return referenties

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"  WAARSCHUWING: Kon liturgische context niet parsen als JSON: {e}")
        return []
