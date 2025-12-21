![Voorbereiding Banner](misc/banner.png)

# Preekvoorbereiding

**Een door een LLM (taalmodel) ondersteund hulpmiddel voor protestantse preekvoorbereiding (PKN).**

Dit project combineert diepgaande **contextanalyse** (hoorders, samenleving) met concrete **liturgische bouwstenen** (exegese, preekschets, gebeden). Het doel is niet om de preek te *schrijven*, maar om de predikant te voorzien van een rijke, contextuele basis.

---

### 📑 Inhoudsopgave
1. [Over dit Project](#-over-dit-project)
2. [Installatie & Setup](#-installatie--setup)
3. [Bijbelvertalingen (Naardense & NBV21)](#-bijbelvertalingen)
4. [Stappenplan Gebruik](#-stappenplan-gebruik)
5. [Overzicht van de Analyses](#-overzicht-van-de-analyses)
6. [Methodiek & Achtergrond](#-methodiek--achtergrond)
7. [Aanvullende Tools](#-aanvullende-tools)
8. [Beperkingen & Disclaimer](#-beperkingen--disclaimer)

---

## 📖 Over dit Project

Friedrich Niebergall stelde ooit: *"Menige preek geeft antwoorden op vragen die niemand stelt, en gaat niet in op vragen die iedereen stelt."* 

Dit project helpt die valkuil te vermijden door twee werelden te verbinden met behulp van een modern taalmodel (Gemini):
1.  **De Wereld van de Hoorder:** Een systematische analyse van de lokale context (wie zijn de hoorders, wat houdt hen bezig?).
2.  **De Wereld van de Tekst:** Exegese, kunst & cultuur, en liturgische vormgeving.

---

## 🛠 Installatie & Setup

### 1. Vereisten
*   Python 3.8 of hoger
*   Een **Google Gemini API Key** (via Google AI Studio)

### 2. Installatie
```bash
# Installeer dependencies
pip install google-genai requests beautifulsoup4 tiktoken
```

### 3. Configuratie
Stel je API key in als environment variable of via een `.env` bestand:
```text
GEMINI_API_KEY=jouw-api-key-hier
```

---

## 📚 Bijbelvertalingen

### Naardense Bijbel (Automatisch)
De literaire vertaling van Pieter Oussoren wordt **automatisch opgehaald** van [naardensebijbel.nl](https://www.naardensebijbel.nl/).
*   **Werking:** Het script `naardense_bijbel.py` zoekt de lezingen, downloadt de tekst en slaat deze op in `output/.../bijbelteksten/`.

### NBV21 (Lokaal)
Vanwege auteursrechten werkt de NBV21 alleen met **lokale JSON-bestanden**.
*   **Locatie:** Plaats bestanden in `nbv21/[BOEKCODE]/[BOEKCODE].[HOOFDSTUK].json`.
*   **Ondersteuning:** Robuuste naamherkenning voor alle boeken (incl. Richteren, Mattheüs, Sirach, etc.).

---

## 🚀 Stappenplan Gebruik

### Stap 1: Basisanalyse
```bash
python contextduiding.py
```
*   Invoer van Plaatsnaam, Gemeente en Datum. Genereert de basiscontext (00-06).

### Stap 2: Verdieping
```bash
python verdieping.py
```
*   Kies een eerdere analyse. Haalt bijbelteksten op en genereert de theologische verdieping (07-13).

### Stap 3: Resultaat
Open `00_overzicht.md` in de gegenereerde output-map voor een centraal overzicht.

---

## 📊 Overzicht van de Analyses

| Nr | Naam | Omschrijving |
|:---|:---|:---|
| 00 | **Liturgische Context** | Zondag van het jaar, lezingen, kleur, liedsuggesties (Liedboek 2013). |
| 01 | **Sociaal-maatschappelijk** | Demografie, economie en sociale structuur van de burgerlijke gemeente. |
| 02 | **Waardenoriëntatie** | De "Vijf V's" en Motivaction Mentality-groepen. |
| 03 | **Geloofsoriëntatie** | Verhouding tussen officieel geloof en het geleefde geloof van hoorders. |
| 04 | **Synthese** | Homiletische aanbevelingen (toon, taal, beelden). |
| 05 | **Wereldnieuws** | Schokkend nieuws van de afgelopen dagen gerelateerd aan de zondag. |
| 06 | **Politieke Oriëntatie** | Stemgedrag en politieke cultuur in de regio. |
| 07 | **Exegese** | Tekstkritiek, historische context en theologische lijnen. |
| 08 | **Kunst & Cultuur** | Beelden, film en muziek bij de lezingen (incl. bronverificatie). |
| 09 | **Focus & Functie** | De kernboodschap en het beoogde effect van de preek. |
| 10 | **Kalender** | Gedenkdagen, heiligen, astronomie en weer. |
| 11 | **Representatieve Hoorders** | Vijf fictieve personages (16-80 jaar) als spiegel voor de prediking. |
| 12 | **Homiletische Analyse** | Preekschets volgens Lowry's narratieve methode (Hè?/Oops!, Oei.../Ugh!, etc.). |
| 13 | **Gebeden** | Drempelgebed, Kyrie, Epiclese, Dankgebed en Voorbeden. |

---

## 🧠 Methodiek & Achtergrond

De analyses in dit project zijn niet willekeurig, maar gebaseerd op gevestigde homiletische en liturgische methodieken. Voor diepgaande studie zijn de achtergrondartikelen beschikbaar in de `misc/` map.

### 1. Contextanalyse: De Leede & Stark
De analyse van de hoorders en hun context volgt de methode uit *Tekst in Context*. We kijken naar vier lagen:
*   **Sociaal-maatschappelijk:** De feitelijke leefwereld.
*   **Waardenoriëntatie:** Wat drijft hen? (De vijf V's).
*   **Geloofsoriëntatie:** Hoe verhoudt men zich tot God en zingeving?
*   **Interpretatie:** De synthese van deze waarnemingen.
📄 **[Lees de volledige methodiekbeschrijving](misc/De_Leede_Stark__Tekst_in_Context.md)**

### 2. Exegese: Zoekmodellen (Hans Snoek)
Het script analyseert de Schrifttekst aan de hand van de modellen uit *Een huis om in te wonen*:
*   **Godsbeelden:** Werkwoordelijk (bevrijden), metaforisch (herder) en eigenschappen (heilig vs. barmhartig).
*   **Mensbeelden:** De mens in verhouding tot God (aanbidding) en de wereld (zorg voor de naaste).
*   **Jezusbeelden:** Van achteren (Joods), van boven (Zoon van God), van beneden (mens) en van voren (Koninkrijk).

### 3. Focus & Functie
Om structuur aan te brengen, wordt onderscheid gemaakt tussen de inhoudelijke kern en het beoogde doel:
*   **Focus:** Wat wil je zeggen? (De ene zin).
*   **Functie:** Wat moet de preek doen? (Het effect op de hoorder).
📄 **[Lees meer over Focus & Functie](misc/Focus_en_Functie.md)**

### 4. Preekstructuur: Lowry's Homiletical Plot
De preek wordt vormgegeven als een narratieve reis (creatie/ontwikkeling in plaats van constructie) in vijf stadia:
1.  **HÈ? (OOPS!)**: Verstoren van het evenwicht (de vraag/jeuk).
2.  **OEI... (UGH!)**: Analyseren van de discrepantie (waarom is het probleem zo hardnekkig?).
3.  **AHA! (AHA!)**: Onthullen van de sleutel (de verrassing uit de tekst).
4.  **JA! (WHEE!)**: Ervaren van het evangelie (de opluchting).
5.  **ZÓ! (YEAH!)**: Anticiperen op de gevolgen (het gewone leven).
📄 **[Lees de diepte-analyse van Lowry's methode](misc/Lowrys_Homiletical_Plot.md)**

### 5. Liturgische Gebeden
De gebeden volgen de klassieke en protestantse (PKN) traditie, met oog voor de specifieke functie van elk gebedsmoment:
*   **Kyrie:** Nood van de wereld, concreet en actueel.
*   **Epiclese:** Gebed om de Geest bij de opening van de Schriften.
*   **Voorbeden:** Concentrische cirkels (wereld, kerk, naaste, eigen gemeente).
📄 **[Lees de achtergrond van de liturgische gebeden](misc/Liturgische_Gebeden.md)**

---

## 🛠 Aanvullende Tools

### Token-teller (`count_tokens.py`)
Telt het aantal tokens in de gegenereerde bestanden om inzicht te krijgen in de omvang van de analyse (gemiddeld ~30.000 tokens voor een volledig dossier).
```bash
python count_tokens.py -v
```

## 📚 Literatuur & Bronnen

*   **De Leede, H. & Stark, C. (2017).** *Ontvouwen: Protestantse prediking in de praktijk.* Zoetermeer: Boekencentrum, pp. 73-81.
*   **Lowry, E.L. (2001).** *The Homiletical Plot: The Sermon as Narrative Art Form.* Expanded Edition. Louisville: Westminster John Knox Press.
*   **Snoek, H. (2023).** *Een huis om in te wonen: Zoekmodellen voor exegese.* (Theologische basis voor de exegese-analyses).

---

## ⚠️ Beperkingen & Disclaimer

**Dit is een assistent, geen predikant.**

*   **Verificatie:** Het taalmodel baseert zich op online informatie. Controleer cruciale feiten, zeker bij kerkelijke fusiegemeenten of specifieke statistieken.
*   **Hallucinaties:** Hoewel het taalmodel wordt gedwongen tot bronverificatie (Google Search grounding), kunnen er onjuistheden voorkomen in kunstsuggesties of lokale nieuwsdetails.
*   **Methodiek:** De analyses zijn aanzetten. Het eigenlijke werk — de ontmoeting tussen Woord en gemeente — blijft mensenwerk.

---
*Gemaakt door W.M. Otte | [GitHub Repository](https://github.com/wmotte/voorbereiding)*
