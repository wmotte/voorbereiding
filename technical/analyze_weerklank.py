#!/usr/bin/env python3

import json
from pathlib import Path

weerklank_file = Path("song_titles/weerklank_titles.json")
with open(weerklank_file) as f:
    data = json.load(f)

psalmen = [x for x in data if x.get('category') == 'Psalmen']
non_psalmen = [x for x in data if x.get('category') != 'Psalmen']

print(f"Total songs: {len(data)}")
print(f"Psalmen: {len(psalmen)}")
print(f"Non-Psalmen: {len(non_psalmen)}")

print("\nFirst 5 Psalmen:")
for song in psalmen[:5]:
    print(f"  {song['number']}: {song['title']}")

print("\nFirst 10 Non-Psalmen:")
for song in non_psalmen[:10]:
    print(f"  {song['number']}: {song['title']} (category: {song.get('category', 'N/A')})")
