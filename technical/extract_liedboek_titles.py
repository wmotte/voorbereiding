
import requests
from bs4 import BeautifulSoup
import json
import re
import time
import sys
from pathlib import Path

INPUT_FILE = "misc/urls_liedboekcompendium.txt"
OUTPUT_FILE = "liedboek_2013_titles.json"

def main():
    if not Path(INPUT_FILE).exists():
        print(f"Error: {INPUT_FILE} not found.")
        return

    songs = []
    
    # Read URLs
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"Found {len(lines)} URLs to process.")
    
    # Limit for testing? User asked for a script that does it. 
    # I will process all, but print progress.
    
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"})

    count = 0
    total = len(lines)
    
    for line in lines:
        if "=>" not in line:
            continue
            
        parts = line.split("=>")
        number_key = parts[0].strip()
        url = parts[1].strip()
        
        count += 1
        print(f"[{count}/{total}] Processing {number_key}...", end="", flush=True)
        
        try:
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                h1 = soup.find('h1')
                
                if h1:
                    full_text = h1.get_text(strip=True)
                    # Expected format: "123 - Title"
                    # Split on first " - "
                    if " - " in full_text:
                        # Split only once to preserve hyphens in title
                        parts_title = full_text.split(" - ", 1)
                        # clean number (remove 9a etc if needed, but we store as is)
                        title_extracted = parts_title[1].strip()
                        
                        songs.append({
                            "number": number_key,
                            "title": title_extracted,
                            "url": url
                        })
                        print(f" OK: {title_extracted}")
                    else:
                        print(f" Warning: unexpected H1 format: '{full_text}'")
                        # Fallback: use full H1 or try title tag
                        songs.append({
                            "number": number_key,
                            "title": full_text,
                            "url": url
                        })
                else:
                    print(" Error: No H1 found.")
            else:
                print(f" Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f" Error: {e}")
            
        # Be polite
        # time.sleep(0.1) 

    # Save results
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
        
    print(f"\nDone. Extracted {len(songs)} titles. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
