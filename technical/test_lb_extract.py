
import requests
from bs4 import BeautifulSoup

url = "https://www.liedboekcompendium.nl/lied/9a-uit-het-diepst-van-mijn-hart-wil-ik-zingen-1_2_8_4"
print(f"Fetching {url}...")

try:
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Try finding H1
    h1 = soup.find('h1')
    if h1:
        print(f"H1: {h1.get_text(strip=True)}")
        
    # Check for title tag
    title_tag = soup.find('title')
    if title_tag:
        print(f"Title tag: {title_tag.get_text(strip=True)}")
        
    # Check for specific meta tags or classes that might hold the clean title
    # Often there is a dedicated title div
    
except Exception as e:
    print(f"Error: {e}")
