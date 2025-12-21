#!/bin/bash

# Controleer of docs/generate_data.py bestaat
if [ ! -f "docs/generate_data.py" ]; then
    echo "❌ Fout: Draai dit script vanuit de root van het project."
    exit 1
fi

echo "🚀 Website bijwerken met gegevens uit output/..."

# Voer het generatie script uit
python3 docs/generate_data.py

echo "🎉 Klaar! De website is bijgewerkt in docs/data.js."