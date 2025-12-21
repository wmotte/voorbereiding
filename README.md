![Voorbereiding Banner](misc/banner.png)

**Bekijk concrete voorbeelden op: [wmotte.github.io/voorbereiding/](https://wmotte.github.io/voorbereiding/)**

# Preekvoorbereiding

Een hulpmiddel voor protestantse preekvoorbereiding in de PKN dat twee functies combineert:

1. **Hoordersanalyse** — Uitgebreide contextanalyse gebaseerd op de homiletische methodiek van De Leede & Stark (2017): sociaal-maatschappelijke context, waardenoriëntatie, geloofsoriëntatie, actueel nieuws en politieke oriëntatie.

2. **Liturgische bouwstenen** — Concrete aanzetten voor de eredienst: liedsuggesties uit het Liedboek, exegese van de Schriftlezingen, kunst en cultuur bij de lezingen, een preekschets volgens Lowry's narratieve methode, en vijf gebeden (drempelgebed, kyrie, epiclese, dankgebed, voorbeden).

Het script brengt deze elementen samen in een coherent geheel, waarbij de lokale context, de Schriftlezingen en de liturgische tijd op elkaar worden afgestemd.

## ⚠️ Beperkingen en waarschuwingen

Dit script maakt gebruik van een Large Language Model (Gemini) met Google Search grounding. Ondanks maatregelen om hallucinaties te beperken (lage temperature, zoekverificatie), kunnen er onjuistheden in de output voorkomen.

### Bekende risico's

**Kerkelijke gemeenten**
In plaatsen met meerdere protestantse kerken (bijv. Hervormde Gemeente, Gereformeerde Kerk, PKN-fusiegemeente) kan het model informatie van verschillende gemeenten door elkaar halen of verkeerde aannames doen over de bedoelde gemeente. Controleer altijd of de informatie over *uw specifieke gemeente* klopt.

**Onduidelijke of verouderde bronnen**
Het model baseert zich op online beschikbare informatie. Als recente gegevens ontbreken of bronnen tegenstrijdig zijn, kan het model:
- Verouderde cijfers presenteren als actueel
- Informatie "invullen" die niet geverifieerd is
- Gegevens van nabijgelegen plaatsen of vergelijkbare gemeenten overnemen

**Verkiezingsuitslagen en statistieken**
Cijfers en percentages dienen altijd gecontroleerd te worden bij de primaire bron (CBS, Kiesraad, gemeente).

### Aanbeveling

Beschouw de output als een *startpunt* voor uw voorbereiding, niet als feitelijke waarheid. Verifieer cruciale informatie, vooral over:
- Uw specifieke kerkelijke gemeente
- Recente lokale gebeurtenissen
- Statistische gegevens

## 📂 Voorbeelden

In de `output/` map staan concrete voorbeelden van gegenereerde analyses:

| Locatie | Datum | Overzicht |
|---------|-------|-----------|
| Waddinxveen (Bethelkerk) | 4 januari 2026 | [00_overzicht.md](output/Waddinxveen_4_januari_2026_Bethelkerk/00_overzicht.md) |

## 📖 Achtergrond

Friedrich Niebergall constateerde: *"Menige preek geeft antwoorden op vragen die niemand stelt, en gaat niet in op vragen die iedereen stelt."*

Dit script helpt predikanten op twee manieren:
- **Kennen:** Systematisch de context in kaart brengen — wie zijn de hoorders, wat houdt hen bezig, welke vragen leven er?
- **Vormgeven:** Concrete bouwstenen aanreiken voor de liturgie — van liedkeuze tot gebeden, van exegese tot preekschets.

De analyses en suggesties zijn geen kant-en-klare producten, maar *aanzetten* die de predikant kan gebruiken, aanpassen of terzijde leggen. Het eigenlijke werk — de ontmoeting tussen Woord en gemeente — blijft mensenwerk.

## 🔍 Wat doet dit script?

Het script voert zeven uitgebreide analyses uit met behulp van Gemini API en Google Search, in twee fasen:

### Fase 1: Liturgische context
0. **Zondag van het Kerkelijk Jaar** - Lezingen, liturgische kleur, thematiek, liedsuggesties (PKN/Liedboek 2013)

### Fase 2: Contextanalyses (met liturgische informatie)
1. **Sociaal-maatschappelijke context** - Demografische, economische en sociale gegevens
2. **Waardenoriëntatie** - De vijf V's en Motivaction Mentality-analyse
3. **Geloofsoriëntatie** - Hoe staan de hoorders geloofsmatig in het leven?
4. **Interpretatieve synthese** - Duiding en vertaling naar homiletische handvatten
5. **Actueel wereldnieuws** - Schokkend nieuws van de afgelopen dagen dat hoorders bezighoudt
6. **Politieke oriëntatie** - Stemgedrag (landelijk, provinciaal, gemeentelijk) en politieke cultuur

De liturgische context uit fase 1 wordt meegegeven aan alle analyses in fase 2, zodat bijvoorbeeld het wereldnieuws gerelateerd kan worden aan de Schriftlezingen.

### 📚 Verdieping (verdieping.py)

Na de basisanalyse kan een verdieping worden uitgevoerd met zeven extra analyses:

7. **Exegese** - Gedegen schriftuitleg van de lezingen (tekstkritiek, literaire analyse, theologische lijnen)
8. **Kunst en Cultuur** - Schilderijen, iconen, films en muziek die aansluiten bij de lezingen en gemeentecontext
9. **Focus en Functie** - [Focus en Functie: Kern van de Preekvoorbereiding](misc/Focus_en_Functie.md) (Gebaseerd op De Leede & Stark)
10. **Kalender** - Gedenkdagen, heiligen, Joodse feestdagen, VN-dagen, nationale feestdagen, schoolvakanties, astronomie en weer
11. **Representatieve Hoorders** - Vijf fictieve personages (16-80 jaar) die de diversiteit van de gemeente representeren
12. **Homiletische Analyse** - [Lowry's Homiletical Plot: De Preek als Narratieve Kunstvorm](misc/Lowrys_Homiletical_Plot.md) - Preekschets volgens de vijf stadia van Eugene Lowry (OOPS! → UGH! → AHA! → WHEE! → YEAH!)
13. **Gebeden** - [Liturgische Gebeden in de PKN](misc/Liturgische_Gebeden.md) - Drempelgebed, kyrie, epiclese, dankgebed en voorbeden voor de eredienst

Deze verdieping leest de output van de basisanalyse (00-06) en gebruikt deze als context.

**Bijbelteksten ophalen:** Het script haalt automatisch de bijbelteksten op van [naardensebijbel.nl](https://www.naardensebijbel.nl/) (de literaire vertaling van Pieter Oussoren). De teksten worden opgeslagen in `bijbelteksten/*.txt` en meegenomen in het exegese-prompt.

### 📜 Naardense Bijbel Tool

Het script `naardense_bijbel.py` is een hulpmiddel dat specifiek is ontwikkeld om bijbelteksten op te halen voor de exegese-fase.

**Functies:**
- **Automatisch ophalen:** Haalt teksten op van naardensebijbel.nl op basis van referenties (bijv. "Jesaja 9:1-6", "Psalm 121").
- **Slimme fallback:** Probeert eerst directe vers-URLs; als dat faalt (bijv. bij hele hoofdstukken of afwijkende URL-structuren), gebruikt het de zoekfunctie van de website.
- **Caching:** Slaat teksten op in de `bijbelteksten/` map binnen de output-directory. Als een tekst al is gedownload, wordt deze niet opnieuw opgehaald om de server te ontlasten en snelheid te winnen.
- **Ondersteuning:** Werkt voor alle boeken van de protestantse canon, inclusief specifieke versranges en hele hoofdstukken.

Dit script wordt automatisch aangeroepen door `verdieping.py`, maar kan ook standalone worden gebruikt of geïmporteerd in andere scripts.

### 📊 Token-teller (count_tokens.py)

Het script `count_tokens.py` telt het aantal tokens in alle gegenereerde markdown-bestanden per dienst. Dit is nuttig om inzicht te krijgen in de omvang van de output en de verwachte kosten bij gebruik van LLM's.

**Gebruik:**
```bash
python count_tokens.py              # Scan de standaard output/ map
python count_tokens.py -v           # Toon ook per-bestand statistieken
python count_tokens.py -o /pad/naar/output
```

**Output-omvang:** Een volledige analyse (basisanalyse + verdieping) genereert gemiddeld **~30.000 tokens** per dienst. Dit omvat alle 12 markdown-bestanden (00-11) inclusief de bijbelteksten.

**Tokenizer:** Het script gebruikt `tiktoken` (cl100k_base encoding) voor nauwkeurige token-telling. Als tiktoken niet geïnstalleerd is, wordt een schatting gemaakt op basis van karakters (chars/4).

## 🛠️ Installatie

```bash
# Clone of download de repository
cd contextduiding

# Installeer dependencies
pip install google-genai requests beautifulsoup4

# Stel je Gemini API key in
export GEMINI_API_KEY='jouw-api-key'

# Of maak een .env bestand:
echo "GEMINI_API_KEY=jouw-api-key" > .env
```

## 🚀 Gebruik

### Basisanalyse

```bash
python contextduiding.py
```

Het script vraagt interactief om:

1. **Plaatsnaam** - Waar wordt de preek gehouden?
2. **Gemeente** - Welke kerkelijke gemeente?
3. **Datum** - Wanneer is de preek? (bijv. "25 december 2025")
4. **Extra context** (optioneel) - Bijzondere dienst, thema, etc.

### Verdieping (exegese en kunst)

```bash
python verdieping.py
```

Dit script toont een lijst van beschikbare basisanalyses en laat je er een kiezen. Vervolgens worden de exegese en kunst/cultuur analyses gegenereerd op basis van alle eerdere context.

## 📁 Output

Het script genereert een map in `output/` met:

```
output/Plaatsnaam_datum_timestamp/
├── 00_overzicht.md                        # Samenvattend overzicht met links
├── 00_zondag_kerkelijk_jaar.md            # Liturgische context, lezingen, liederen
├── 01_sociaal_maatschappelijke_context.md # Demografische en sociale analyse
├── 02_waardenorientatie.md                # Vijf V's, Motivaction, trends
├── 03_geloofsorientatie.md                # Religieuze context en geloofstaal
├── 04_interpretatieve_synthese.md         # Homiletische aanbevelingen
├── 05_actueel_wereldnieuws.md             # Recent wereldnieuws met duiding
├── 06_politieke_orientatie.md             # Stemgedrag en politieke cultuur
├── 07_exegese.md                          # Exegese van de Schriftlezingen (via verdieping.py)
├── 08_kunst_cultuur.md                    # Kunst, cultuur en film (via verdieping.py)
├── 09_focus_en_functie.md                 # Focus en Functie (via verdieping.py)
├── 10_kalender.md                         # Kalender met gedenkdagen (via verdieping.py)
├── 11_representatieve_hoorders.md         # Vijf personages (via verdieping.py)
├── 12_homiletische_analyse.md             # Lowry's Homiletical Plot (via verdieping.py)
├── 13_gebeden.md                          # Gebeden voor de eredienst (via verdieping.py)
└── bijbelteksten/                         # Naardense Bijbel teksten (via verdieping.py)
    ├── jesaja_91-6.txt
    ├── lucas_21-14.txt
    └── ...
```

## 🗂️ Projectstructuur

```
contextduiding/
├── contextduiding.py                       # Hoofdscript basisanalyse
├── verdieping.py                           # Verdieping: exegese en kunst/cultuur
├── naardense_bijbel.py                     # Module voor ophalen bijbelteksten
├── count_tokens.py                         # Token-teller voor output-analyse
├── prompts/                                # Prompt-bestanden (aanpasbaar)
│   ├── base_prompt.md                      # Basis rol en werkwijze
│   ├── 00_zondag_kerkelijk_jaar.md         # Liturgische context (eerst)
│   ├── 01_sociaal_maatschappelijke_context.md
│   ├── 02_waardenorientatie.md
│   ├── 03_geloofsorientatie.md
│   ├── 04_interpretatieve_synthese.md
│   ├── 05_actueel_wereldnieuws.md
│   ├── 06_politieke_orientatie.md          # Politieke oriëntatie
│   ├── 07_exegese.md                       # Exegese (verdieping)
│   ├── 08_kunst_cultuur.md                 # Kunst en cultuur (verdieping)
│   ├── 09_focus_en_functie.md              # Focus en Functie (verdieping)
│   ├── 10_kalender.md                      # Kalender met gedenkdagen (verdieping)
│   ├── 11_representatieve_hoorders.md      # Personages (verdieping)
│   ├── 12_homiletische_analyse.md          # Lowry's Homiletical Plot (verdieping)
│   └── 13_gebeden.md                       # Gebeden voor de eredienst (verdieping)
├── system_prompt_contextduiding.md         # Referentiedocumentatie methodiek
├── homiletisch_kader_hoordersanalyse.md    # Theoretisch kader De Leede & Stark
├── .env                                    # API key (niet in git)
└── output/                                 # Gegenereerde analyses
```

## ✏️ Prompts aanpassen

De prompts staan als losse markdown-bestanden in de `prompts/` map. Je kunt deze bewerken zonder de Python code aan te passen.

**Placeholders** die automatisch worden vervangen:
- `{{plaatsnaam}}` - De ingevoerde plaatsnaam
- `{{gemeente}}` - De ingevoerde gemeente
- `{{datum}}` - De ingevoerde preekdatum
- `{{huidige_datum}}` - De datum waarop het script draait (voor actueel nieuws)

## 📋 Methodiek

De analyse is gebaseerd op de vier pijlers van hoordersanalyse volgens De Leede & Stark (2017), aangevuld met liturgische context en actueel nieuws:

### 0. Zondag van het Kerkelijk Jaar (PKN)
- Positie in het kerkelijk jaar (A/B/C cyclus)
- Lezingen volgens Gemeenschappelijk Leesrooster
- Liturgische kleur en sfeer
- Liedsuggesties uit Liedboek 2013
- Bijzondere zondagen (Israëlzondag, Vredeszondag, etc.)

### 1. Sociaal-maatschappelijke context
- Demografische gegevens (CBS, AlleCijfers)
- Economische situatie
- Sociale structuur
- Recente lokale gebeurtenissen
- Kerkelijke context

### 2. Waardenoriëntatie
**De vijf V's:** Visioenen, Verlangens, Vreugden, Verdriet, Vragen

**Motivaction Mentality-groepen:**
- Traditionele burgerij, Gemaksgeoriënteerden, Moderne burgerij
- Nieuwe conservatieven, Kosmopolieten, Postmaterialisten
- Postmoderne hedonisten, Opwaarts mobielen

**Trendanalyse:** Meso- en microtrends

### 3. Geloofsoriëntatie
Zes ervaringsgebieden: Schepping, Eindigheid, Menselijk tekort, Lijden, Wijsheid der volken, Humaniteit

### 4. Interpretatieve synthese
- Congruentie officieel geloof vs. praktijk
- Verbindings- en confrontatiepunten
- Homiletische aanbevelingen (toon, taal, beelden)

### 5. Actueel wereldnieuws
- Schokkende wereldgebeurtenissen (3-5 dagen)
- Theologische en existentiële vragen
- Pastorale, profetische en diaconale relevantie
- Relatie tot de Schriftlezingen

### 6. Politieke oriëntatie
- Landelijk stemgedrag (Tweede Kamerverkiezingen)
- Provinciaal stemgedrag (Provinciale Staten)
- Gemeentelijk stemgedrag (gemeenteraadsverkiezingen)
- Waterschapsverkiezingen
- Politieke cultuur (progressief/conservatief, vertrouwen in overheid)
- Spanningsvelden en gevoelige lokale kwesties
- Relevantie voor de prediking

Bronnen: kiesraad.nl, gemeente.nl, lokale nieuwsmedia

### 7. Exegese (verdieping)
- Tekstkritische opmerkingen en vertaalkeuzes
- Literaire analyse (genre, structuur, stijlfiguren)
- Historische context van de tekst
- Theologische lijnen en intertekstualiteit
- **Zoekmodellen voor Gods-, mens- en Jezusbeelden** (zie hieronder)
- Samenhang van de lezingen
- Receptiegeschiedenis
- Homiletische doorvertaling

#### Zoekmodellen (Hans Snoek)

De exegese maakt gebruik van de zoekmodellenmethode van Hans Snoek (*Een huis om in te wonen*, 2010). Deze methode biedt een systematische manier om de belangrijkste actanten in de Bijbel — God, mens en Jezus — te analyseren. Het zijn geen rigide rasters, maar heuristische hulpmiddelen die van geval tot geval hun nut moeten bewijzen.

**A. Godsbeelden (OT)**

Het OT kent drie soorten uitspraken over God:

1. *Werkwoordelijke uitspraken* — God bevrijdt, schept, leidt, spreekt (Brueggemann: Israël leerde God kennen in concrete historische gebeurtenissen)
2. *Metaforische uitspraken* — "De HEER is koning/herder/rechter/vader"
3. *Uitspraken over eigenschappen* — onderverdeeld in:
   - Overstijgende (transcendente): almachtig, eeuwig, heilig
   - Toebuigende (condescendente): barmhartig, trouw, genadig (Berkhof)

```
            overstijgende eigenschappen
                        |
metaforische uitspraken — God — werkwoordelijke uitspraken
                        |
            toebuigende eigenschappen
```

**B. Mensbeelden (OT)**

```
                    God
        (gebed, aanbidding, luisteren)
                    |
    kwaad doen — mens/mensen — goed doen
                    |
                    wereld
        (zorg voor naaste, belangen)
```

Gerichtheid op God en wereld sluiten elkaar niet uit — profeten roepen met beroep op Gods wil juist op tot zorg voor de naaste.

**C. Jezusbeelden (NT)**

Gebaseerd op Berkhof, aangepast door Snoek:

```
            van boven: Zoon van God
                        |
van achteren: jood — Jezus — van voren: aankondiger Koninkrijk
                        |
            van beneden: mens
```

- **Van achteren**: geworteld in Israëls traditie, Messias
- **Van boven**: goddelijke identiteit, zending, pre-existentie
- **Van beneden**: mens van vlees en bloed, emoties, lijden
- **Van voren**: uitspraken over Koninkrijk, eeuwig leven, toekomst

### 8. Kunst en Cultuur (verdieping)
- Klassieke christelijke kunst (schilderijen, iconen, miniaturen)
- Moderne en hedendaagse kunst
- Film en documentaire
- Muziek (klassiek, oratoria, populair)
- Literatuur en poëzie
- Praktische tips voor gebruik in de eredienst

Bronnen: artbible.info, De Bijbel Cultureel (Barnard), Rijksmuseum, Web Gallery of Art

### 10. Kalender (verdieping)
- Kerkelijke gedenkdagen en heiligen
- Joodse kalender (feestdagen, parasja)
- Internationale en VN-dagen
- Nationale feest- en gedenkdagen (Nederland en België)
- Seizoensgebonden momenten (schoolvakanties, carnaval, Sinterklaas)
- Astronomische gebeurtenissen (maanfasen, zonsopgang/-ondergang)
- Weersverwachting voor de week

Bronnen: heiligen.net, chabad.org, un.org/observances, rijksoverheid.nl, knmi.nl, timeanddate.com

### 11. Representatieve Hoorders (verdieping)
Vijf fictieve personages die de diversiteit van de gemeente representeren:
- **Leeftijdsrange:** 16-80 jaar (jongere, young professional, middelbaar, senior, oudere)
- **Levensfases:** Scholier/student, alleenstaand, gezin, gescheiden, weduwe/weduwnaar
- **Per personage (400-600 woorden):**
  - Basisgegevens (naam, leeftijd, fysieke verschijning)
  - Relaties en sociaal netwerk
  - Opleiding, werk en financiën
  - Gezondheid (lichamelijk en mentaal)
  - Trauma's en zorgen
  - Geloof en spiritualiteit
  - Hobby's en interesses
  - Aansluiting bij de Schriftlezingen

Bronnen: gebaseerd op de sociaal-maatschappelijke context, waardenoriëntatie en geloofsoriëntatie analyses

### 12. Homiletische Analyse (verdieping)
Een preekschets volgens Eugene Lowry's "Homiletical Plot" — de preek als narratieve kunstvorm. Lowry ziet de preek niet als een statische constructie van punten, maar als een **narratieve reis**: een gebeurtenis-in-de-tijd met spanning die wordt opgebouwd en opgelost.

**De vijf stadia:**
1. **OOPS!** (Verstoren van het evenwicht) — Een concrete, herkenbare ongerijmdheid of vraag introduceren
2. **UGH!** (Analyseren van de discrepantie) — Het probleem niet wegpoetsen, maar uitdiepen. Waarom is dit zo hardnekkig?
3. **AHA!** (Onthullen van de sleutel) — De verrassende wending vanuit de tekst, het "scharnierpunt"
4. **WHEE!** (Ervaren van het evangelie) — De opluchting dat het anders kan, de rust van het evangelie
5. **YEAH!** (Anticiperen op de gevolgen) — De vertaling naar het gewone leven, open en hoopvol

**Kernprincipes:**
- De preek beweegt van "itch" (jeuk/probleem) naar "scratch" (krabben/oplossing)
- Het principe van **omkering**: de sleutel komt vaak als verrassing, keert conventionele wijsheid om
- Ambiguïteit houdt de aandacht vast; geef de oplossing niet te vroeg weg
- Het hoogtepunt ligt bij stadium 4 (evangelie), niet bij stadium 5 (toepassing)

**Integratie van voorgaande analyses:**
De schets maakt expliciet gebruik van de sociaal-maatschappelijke context, representatieve hoorders, exegese, kunst/cultuur en actualiteit. De LLM kiest welke lezing centraal staat op basis van waar de meeste spanning of urgentie ligt voor de hoorders.

Zie: [Lowry's Homiletical Plot: De Preek als Narratieve Kunstvorm](misc/Lowrys_Homiletical_Plot.md)

### 13. Gebeden voor de Eredienst (verdieping)
Vijf liturgische gebeden voor de Protestantse eredienst, afgestemd op de Schriftlezingen en de lokale context:

1. **Drempelgebed** - Het openingsgebed bij binnenkomst dat de overgang markeert van het dagelijks leven naar de ontmoeting met God. Bevat verootmoediging en verlangen.
2. **Kyrie** - Het gebed om ontferming dat de nood van de wereld en de schepping voor Gods aangezicht brengt. Concreet en actueel, gevolgd door het Gloria.
3. **Epiclese** - Het gebed om de Heilige Geest voordat de Schriften opengaan. Vraagt om verlichting van het verstand en opening van het hart.
4. **Dankgebed** - Het gebed na de verkondiging dat dankt voor het gehoorde Woord en vraagt om kracht het te bewaren en te doen.
5. **Voorbeden** - De gebeden der gemeente in concentrische cirkels: de wereld, de kerk, de naasten, de eigen gemeente. Afgesloten met het Onze Vader.

**Theologische uitgangspunten:**
- Trinitarisch: tot de Vader, door Christus, in de kracht van de Geest
- Bijbels gefundeerd: de Schriftlezingen klinken door in de gebeden
- Contextueel: lokale situatie en actuele context worden meegenomen
- Liturgische economie: elk gebed heeft zijn eigen "toonhoogte", geen overlappingen

Zie: [Liturgische Gebeden in de PKN](misc/Liturgische_Gebeden.md)

## 📚 Bronnen

### Gebruikte bronnen door het script
- **CBS / AlleCijfers** - Demografische statistieken
- **NOS, NRC, Trouw, ND** - Nieuws en actualiteit
- **protestantsekerk.nl** - PKN-informatie, leesrooster
- **Liedboek 2013** - Liedsuggesties
- **naardensebijbel.nl** - Naardense Bijbel (Pieter Oussoren)
- **artbible.info** - Bijbelse kunst database
- **wga.hu** - Web Gallery of Art
- **De Bijbel Cultureel** - Barnard & Van der Meiden

### Literatuur
- De Leede, H. & Stark, C. (2017). *Ontvouwen: Protestantse prediking in de praktijk*. Zoetermeer: Boekencentrum, pp. 73-81.
- [Focus en Functie: Kern van de Preekvoorbereiding](misc/Focus_en_Functie.md) (Gebaseerd op De Leede & Stark)
- Lowry, E.L. (1980/2001). *The Homiletical Plot: The Sermon as Narrative Art Form*. Expanded Edition. Louisville: Westminster John Knox Press.
- [Lowry's Homiletical Plot: De Preek als Narratieve Kunstvorm](misc/Lowrys_Homiletical_Plot.md) (Uitgebreide samenvatting in het Nederlands)
- [Liturgische Gebeden in de PKN](misc/Liturgische_Gebeden.md) (Analyse van karakteristieken, structuur en best practices)
- Niebergall, F. (1971). 'Die moderne Predigt', in: Hummel, G., *Aufgabe der Predigt*. Darmstadt: Wissenschaftliche Buchgesellschaft.
- Snoek, H. (2010). *Een huis om in te wonen: Uitleg en interpretatie van de Bijbel*. Kampen: Kok, 2e druk, pp. 180-199. (Zoekmodellen voor Gods-, mens- en Jezusbeelden)
- Motivaction. *Mentality-model*. https://www.motivaction.nl/mentality

## 🔑 API Key

Je hebt een Gemini API key nodig: https://aistudio.google.com/app/apikey
