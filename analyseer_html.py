#!/usr/bin/env python3
"""
Test hoe de poëtische structuur in de HTML van de Naardense Bijbel zit
"""

import requests
from bs4 import BeautifulSoup

def analyseer_html_structuur():
    """Analyseer hoe de poëtische structuur in de HTML zit"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Test met een poëtisch hoofdstuk zoals Psalm 23 of een deel van Jesaja
    url = "https://www.naardensebijbel.nl/psalm/23/"
    
    print(f"Analyseren van: {url}")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Zoek naar de bijbeltekst (verwijder navigatie, headers, etc.)
        for tag in soup.find_all(['nav', 'script', 'style', 'header', 'footer', 'aside']):
            tag.decompose()

        # Zoek naar de inhoud van het hoofdstuk
        body = soup.find('body')
        if body:
            # Zoek naar paragrafen of andere structurerende elementen die de poëzie bevatten
            print("HTML structuur van het hoofdstuk:")
            print("="*50)
            
            # Zoek naar alle elementen die bijbeltekst kunnen bevatten
            content_elements = body.find_all(['p', 'div', 'section', 'article', 'main'])
            
            for i, elem in enumerate(content_elements[:5]):  # Eerste 5 elementen
                print(f"\nElement {i+1}: {elem.name}")
                print(f"Klassen: {elem.get('class', [])}")
                print(f"Tekstvoorbeeld: {elem.get_text()[:200]}...")
                
                # Zoek naar paragraaf of div met bijbeltekst
                if any(keyword in str(elem.get_text()).lower() for keyword in ['heer', 'herder', 'psalm', '23']):
                    print("\n" + "="*30 + f" MOGELIJK BIJBELTEKST ELEMENT {i+1} " + "="*30)
                    print(elem.prettify())
                    break
    
    # Test ook een vers-URL om te zien hoe dat is opgebouwd
    print("\n" + "="*70)
    print("Test met vers-URL:")
    
    vers_url = "https://www.naardensebijbel.nl/vers/psalm-23-1/"
    response2 = requests.get(vers_url, headers=headers)
    
    if response2.status_code == 200:
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        for tag in soup2.find_all(['nav', 'script', 'style', 'header', 'footer', 'aside']):
            tag.decompose()
        
        print(f"Vers-URL: {vers_url}")
        print("Body structuur:")
        body2 = soup2.find('body')
        if body2:
            print(body2.prettify()[:1000])  # Eerste 1000 karakters

analyseer_html_structuur()