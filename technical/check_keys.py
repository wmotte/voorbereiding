import json
from pathlib import Path

# Path to the specific combined output file
path = Path("output/Ede_25_december_2025_20251224_105304/combined_output.json")

try:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        print("Keys in combined_output.json:")
        for key in sorted(data.keys()):
            print(f"- {key}")
except Exception as e:
    print(f"Error: {e}")
