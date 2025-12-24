![Voorbereiding Banner](misc/banner.png)

# Preekvoorbereiding

**Een LLM-ondersteund hulpmiddel voor protestantse preekvoorbereiding (PKN).**

**Let op: Dit materiaal is bedoeld ter inspiratie en als 'feedback' op eigen werk. De uiteindelijke verantwoordelijkheid voor de preek ligt bij de predikant zelf.**

Bekijk de online webviewer met *100% automatisch-gegenereerde* voorbeelddata: [https://wmotte.github.io/voorbereiding/](https://wmotte.github.io/voorbereiding/)

Dit project combineert diepgaande **contextanalyse** (hoorders, samenleving) met concrete **liturgische bouwstenen** (exegese, preekschets, gebeden). Het doel is niet om de preek te *schrijven*, maar om de predikant te voorzien van een rijke, contextuele basis.

---

### 📑 Inhoudsopgave
1. [Over dit Project](#-over-dit-project)
2. [Installatie & Setup](#-installatie--setup)
3. [Bijbelvertalingen (Naardense & NBV21)](#-bijbelvertalingen)
4. [Stappenplan Gebruik](#-stappenplan-gebruik)
5. [Overzicht van de Analyses & Methodiek](#-overzicht-van-de-analyses--methodiek)
6. [Aanvullende Tools](#-aanvullende-tools)
7. [Literatuur & Bronnen](#-literatuur--bronnen)
8. [Beperkingen & Disclaimer](#-beperkingen--disclaimer)

---

## 📖 Over dit Project

Inspiratie voor dit hulpmiddel is geput uit **"De Eerste Dag"**, de officiële, oecumenische handreiking van de Raad van Kerken in Nederland. "De Eerste Dag" ondersteunt bij de voorbereiding van de wekelijkse eredienst, aansluitend bij het kerkelijk jaar en de liturgie. Het biedt commentaren bij de lezingen, suggesties voor de liturgie, gebeden en toepassingen voor kinderwerk, en helpt bij het structureren van de dienst (de "orde").

Met dit digitale hulpmiddel wordt die voorbereiding veel dynamischer én contextueler. De voorganger kan specifiek aangeven wie de hoorders zijn, in welke tijd en op welke plaats. Ook kan hij of zij nu zelf bepalen welke onderdelen van belang zijn in de voorbereiding. De output van de tool biedt de mogelijkheid om de eigen exegesetische inzichten en eigen homiletische structuur te toetsen. Sommigen willen meer informatie over interactieve momenten (zoals het kindermoment), terwijl weer anderen geholpen zijn bij de identificatie van relevante kunst- en cultuurartefacten. 
Een enkeling zoekt inspiratie in *hypothetische* preekschetsen van belangrijke historische voorgangers; de tool demonstreert hoe dat eruit zou kunnen zien (op basis van een drietal theologen). 

Het belangrijkste element is en blijft de contextuele verwerking in de verschillende voorbereidende stappen. 

Friedrich Niebergall stelde ooit: *"Menige preek geeft antwoorden op vragen die niemand stelt, en gaat niet in op vragen die iedereen stelt."* 

Dit project helpt die valkuil te vermijden door twee werelden te verbinden met behulp van een modern taalmodel:
1.  **De Wereld van de Hoorder:** Een systematische analyse van de lokale context (wie zijn de hoorders, wat houdt hen bezig?).
2.  **De Wereld van de Tekst:** Exegese, kunst & cultuur, en liturgische vormgeving.

---

## 🛠 Installatie & Setup

In theorie is deze tool te gebruiken met elk hedendaags taalmodel. Om betrouwbare output te genereren, is enige vorm van 'grounding' handig.
Om die reden is gekozen voor Google Gemini. Dit valt eenvoudig aan te passen. Er zijn diverse open-weights taalmodellen als alternatief beschikbaar (Kimi, DeepSeek, etc.).
Deze zijn echter niet getest.

### 1. Vereisten
*   Python 3.8 of hoger
*   Een **Google Gemini API Key** (via Google AI Studio)

### 2. Installatie (Aanbevolen: met virtuele omgeving)
```bash
# Maak een virtuele omgeving aan
python3 -m venv venv

# Activeer de omgeving
source venv/bin/activate  # macOS/Linux
# OF
venv\Scripts\activate  # Windows

# Installeer dependencies
pip install google-genai requests beautifulsoup4 tiktoken
```

### 3. Configuratie
Stel je API key in als environment variable of via een `.env` bestand:
```text
GEMINI_API_KEY=jouw-api-key-hier
```

### 4. Troubleshooting
**Probleem:** `ModuleNotFoundError` bij `import google.genai`
**Oplossing:** Controleer of je `google-genai` hebt geïnstalleerd (niet `google-generativeai`).

**Probleem:** API Key niet gevonden
**Oplossing:** Zorg dat je `.env` bestand in dezelfde map staat als je scripts, of export de variabele handmatig: `export GEMINI_API_KEY="jouw-key"`.

**Probleem:** Rate limit errors
**Oplossing:** Het script heeft ingebouwde retry-logica, maar bij frequente errors kun je de API quota verhogen in Google AI Studio.

### 💰 Kosten & Privacy
*   **API Kosten:** Het gebruik van Google Gemini API wordt per token in rekening gebracht. Een volledige analyse (~85.000 tokens) kost ongeveer €0,10-€0,50, afhankelijk van het gekozen model.
*   **Privacy:** Bijbelteksten en gegenereerde analyses worden naar Google's API gestuurd. Voer geen privacygevoelige informatie in.
*   **Alternatief:** Voor lokaal gebruik zonder externe API-aanroepen zijn open-weights modellen een goed alternatief.

---

## 🚀 Stappenplan Gebruik

### Stap 1: Basisanalyse
```bash
python 00__contextduiding.py
```
*   Voer Plaatsnaam, Gemeente en Datum in. Genereert de basiscontext (01-07) en `00_meta.json`.

### Stap 2: Verdieping
```bash
python 01__verdieping.py
```
*   Kies een eerdere analyse. Haalt bijbelteksten op en genereert de theologische verdieping (08-15). Alle JSON-bestanden worden aan het einde gecombineerd in `combined_output.json`.

### Stap 3: Resultaat
Open `combined_output.json` of gebruik de webviewer in de `docs/` map.

### 📸 Voorbeeld Output
Hieronder zie je een voorbeeld van de gegenereerde contextanalyse voor een gemeente op een specifieke zondag:

**02 Sociaal-maatschappelijk:**
> "Utrecht Noordwest is een divers stadsdeel met 23.000 inwoners, waarvan 42% een migratieachtergrond heeft..."

**Bekijk de volledige voorbeeldoutput:** [https://wmotte.github.io/voorbereiding/](https://wmotte.github.io/voorbereiding/)

---

## 📊 Overzicht van de Analyses & Methodiek

De analyses in dit project zijn niet willekeurig, maar gebaseerd op gevestigde homiletische en liturgische methodieken. Hieronder volgt een uitleg per onderdeel, in de volgorde waarin ze worden gegenereerd. Voor meer informatie zijn er een aantal achtergrondartikelen beschikbaar in de `misc/` map.

### 00 Meta-data
`00_meta.json`: Centrale opslag van user input en geverifieerd adres.

### 01 Liturgische Context
Zondag van het jaar, lezingen, kleur, liedsuggesties (Liedboek 2013).

### 02 t/m 05 Contextanalyse: De Leede & Stark
De analyse van de hoorders en hun context volgt de methode uit *Tekst in Context*. We kijken naar vier lagen:

*   **02 Sociaal-maatschappelijk:** De feitelijke leefwereld. Demografie, economie en sociale structuur van de burgerlijke gemeente.
*   **03 Waardenoriëntatie:** Wat drijft hen? De "Vijf V's" en Motivaction Mentality-groepen.
*   **04 Geloofsoriëntatie:** Hoe verhoudt men zich tot God en zingeving? Verhouding tussen officieel geloof en het geleefde geloof van hoorders.
*   **05 Synthese:** Homiletische aanbevelingen (toon, taal, beelden) op basis van de voorgaande lagen.

📄 **[Lees de volledige methodiekbeschrijving](misc/De_Leede_Stark__Tekst_in_Context.md)**

### 06 Wereldnieuws
Relevant actueel nieuws van de afgelopen dagen gerelateerd aan de zondag, om de actualiteit te verbinden met de theologie.

### 07 Politieke Oriëntatie
Stemgedrag en politieke cultuur in de regio.

### 08 Exegese: Zoekmodellen (Hans Snoek)
Tekstkritiek, historische context en theologische lijnen. Het script analyseert de Schrifttekst aan de hand van de modellen uit *Een huis om in te wonen*:
*   **Godsbeelden:** Werkwoordelijk (bevrijden), metaforisch (herder) en eigenschappen (heilig vs. barmhartig).
*   **Mensbeelden:** De mens in verhouding tot God (aanbidding) en de wereld (zorg voor de naaste).
*   **Jezusbeelden:** Van achteren (Joods), van boven (Zoon van God), van beneden (mens) en van voren (Koninkrijk).

### 09 Kunst & Cultuur
Beelden, film en muziek bij de lezingen (incl. bronverificatie).

### 10 Focus & Functie
Om structuur aan te brengen, wordt onderscheid gemaakt tussen de inhoudelijke kern en het beoogde doel:
*   **Focus:** Wat wil je zeggen? (De ene zin).
*   **Functie:** Wat moet de preek doen? (Het effect op de hoorder).

📄 **[Lees meer over Focus & Functie](misc/Focus_en_Functie.md)**

### 11 Kalender
Gedenkdagen, heiligen, astronomie en weer.

### 12 Representatieve Hoorders
Vijf fictieve personages (16-80 jaar) als spiegel voor de prediking.

### 13 Homiletische Analyse
Een combinatie van drie invloedrijke homiletische methodieken:

#### A. Homiletical Plot (Eugene Lowry)
De preek wordt vormgegeven als een narratieve reis (creatie/ontwikkeling in plaats van constructie) in vijf stadia:
1.  **HÈ? (OOPS!)**: Verstoren van het evenwicht (de vraag/jeuk).
2.  **OEI... (UGH!)**: Analyseren van de discrepantie (waarom is het probleem zo hardnekkig?).
3.  **AHA! (AHA!)**: Onthullen van de sleutel (de verrassing uit de tekst).
4.  **JA! (WHEE!)**: Ervaren van het evangelie (de opluchting).
5.  **ZÓ! (YEAH!)**: Anticiperen op de gevolgen (het gewone leven).
📄 **[Lees de diepte-analyse van Lowry's methode](misc/Lowrys_Homiletical_Plot.md)**

#### B. Homiletische Brug (Bryan Chapell)
De vertaalslag van exegese naar preek wordt gemaakt met de inzichten uit *Christ-Centered Preaching*:
*   **Fallen Condition Focus (FCF):** De gemeenschappelijke menselijke gebrokenheid die de tekst adresseert en de genade noodzakelijk maakt.
*   **Christocentrische Duiding:** Hoe onthult de tekst Gods verlossingsplan? (Predictive, Preparatory, Reflective, Resultant).
*   **Motivatie:** De "chemie van het hart": heiliging als dankbare reactie op genade, niet als voorwaarde.
📄 **[Lees de volledige methodiek van Chapell](misc/Bryan_Chapells_Expositie_Homiletiek.md)**

#### C. Moves & Structures (David Buttrick)
*   **Moves:** Preken als een reeks taalbewegingen in plaats van statische punten.
*   **Fenomenologie:** Focus op hoe taal werkt in het bewustzijn van de hoorder.
*   **Structuur:** Zorgvuldige opbouw van openingsstatement, ontwikkeling en afsluiting per move.
📄 **[Lees de volledige methodiek van Buttrick](misc/Buttricks_Moves_and_Structures.md)**

### 14 Gebeden
De tool biedt vier verschillende benaderingen voor de gebeden, elk met een eigen theologische en stilistische kleur:

#### A. Standaard Liturgisch
Volgt de klassieke en protestantse (PKN) traditie, met oog voor de specifieke functie van elk gebedsmoment (Kyrie, Epiclese, Voorbeden).
📄 **[Lees de achtergrond van de liturgische gebeden](misc/Liturgische_Gebeden.md)**

#### B. Profetisch Bidden (Walter Brueggemann)
Gebaseerd op de theologie van *The Prophetic Imagination*. Deze gebeden doorbreken de "koninklijke bewustheid" (status quo) en gebruiken "gevaarlijke taal" om pijn te benoemen en hoop te wekken.
*   **Kenmerken:** Rauwe klacht (lamentatie), verzet tegen imperiale macht, en radicale hoop.
📄 **[Lees meer over Brueggemanns gebedstaal](misc/Brueggemanns_Gebeden.md)**

#### C. Dialogisch Bidden (André Dumas)
Gebaseerd op de "theologie van de realiteit" van André Dumas. Deze gebeden zijn een directe, soms stroeve dialoog met God ("Brusquerie").
*   **Kenmerken:** Geen vrome maskers, "stijve knieën" (moderne autonomie), en ethische verantwoordelijkheid ("Exaucer Dieu": God verhoren).
📄 **[Lees de analyse van Dumas' dialogische stijl](misc/Andre_Dumas_Dialogisch_Bidden.md)**

#### D. Eenvoudige B1-niveau Gebeden
Voor gemeenten of hoorders met beperkte kennis van de godsdienstige taal biedt het programma ook eenvoudige gebeden op B1-taalniveau (Europees Referentiekader voor Talen).
*   **Kenmerken:** Toegankelijke taal, korte zinnen, concrete beelden en duidelijke christelijke inhoud.
*   **Doel:** Toegankelijk maken van gebed voor nieuwkomers, taalstudenten of mensen met beperkte geletterdheid.

### 15 Kindermoment
Vijf totaal verschillende opties voor een interactief en creatief kindermoment:
*   **Optie 1: De Klassieke Verrassing:** Warm verhaal met een herkenbaar voorwerp.
*   **Optie 2: De Doe-het-zelf:** Focus op actie en beweging.
*   **Optie 3: De 'Gekke' Twist:** Onconventionele of humoristische benadering.
*   **Optie 4: De Bizarre Inval:** Een totaal onverwacht object of concept.
*   **Optie 5: De Ernstige Toon:** Ingetogen benadering die kinderen serieus neemt.

### 16 Moment van Bezinning
Een specifieke vorm van gebed of meditatie die inkeer biedt binnen de eredienst. Dit moment is bedoeld voor reflectie, stilte en persoonlijke benadering van God.
*   **Kenmerken:** Korte, rustgevende teksten, ruimte voor stilte, nadruk op Gods nabijheid en troost.
*   **Functie:** Ruimte creëren voor innerlijke rust en bezinning in het drukke leven.

### 17 Preekschets in de geest van Sölle
Preekschets in de stijl van Dorothee Sölle: mystiek en politiek verzet. Deze benadering verbindt de bijbeltekst met maatschappelijk engagement en een diepe spiritualiteit van verzet tegen onrecht.
📄 **[Lees meer over de homiletiek van Sölle](misc/Solle_Homiletiek.md)**

### 18 Preekschets in de geest van Jüngel
Preekschets in de stijl van Eberhard Jüngel: paradox en evangelische doorbraak. Jüngels methode focust op de 'taal van de liefde' en de verrassing van het evangelie die de menselijke logica doorbreekt.
📄 **[Lees meer over de homiletiek van Jüngel](misc/Jungel_Homiletiek.md)**

### 19 Preekschets in de geest van Noordmans
Preekschets in de stijl van Oepke Noordmans. Zijn homiletiek biedt een unieke benadering gebaseerd op de leer van de Drie-eenheid en het begrip 'herschepping'.
*   **Centraal thema:** De rol van de Heilige Geest in het creëren van een nieuwe werkelijkheid (herschepping) door de prediking.
*   **Structuur:** "Scheppen is scheiden" - een preek die zich toespitst op één punt en de Geest laat werken door te onderscheiden.
📄 **[Lees meer over de homiletiek van Noordmans](misc/Noordmans_Homiletiek.md)**

---

## 🛠 Aanvullende Tools

### JSON-validator (`validate_json.py`)
Valideert de structuur van gegenereerde JSON-bestanden tegen het verwachte schema. Controleert op ontbrekende secties, vereiste velden en correcte datatypen.
```bash
python validate_json.py output/Sessie_Naam/combined_output.json
```

### Token-teller (`count_tokens.py`)
Telt het aantal tokens in de gegenereerde bestanden om inzicht te krijgen in de omvang van de analyse (gemiddeld ~85.000 tokens voor een volledig dossier, opgeslagen in `combined_output.json`).
```bash
python count_tokens.py --file output/Sessie_Naam/combined_output.json
```

---

## ❓ Veelgestelde Vragen (FAQ)

**Q: Hoelang duurt een volledige analyse?**
A: Een basisanalyse (contextduiding.py) duurt 5-10 minuten. De verdieping (verdieping.py) neemt 15-25 minuten in beslag, afhankelijk van het aantal geselecteerde onderdelen.

**Q: Kan ik het systeem offline gebruiken?**
A: Nee, het systeem vereist een actieve internetverbinding voor de Gemini API. Voor offline gebruik kun je overstappen naar lokale modellen zoals Ollama met DeepSeek.

**Q: Welke bijbelvertalingen worden ondersteund?**
A: De tool haalt automatisch de NBV21 en Naardense Bijbel op via online bronnen.

**Q: Kan ik eigen methodieken toevoegen?**
A: Ja, het systeem is modulair opgezet. Bekijk de code in `01__verdieping.py` voor voorbeelden van hoe analyses worden gestructureerd.

---

## 📚 Literatuur & Bronnen

*   **Brueggemann, W. (1978).** *The Prophetic Imagination.* Fortress Press.
*   **Buttrick, D. (1987).** *Homiletic: Moves and Structures.* Philadelphia: Fortress Press.
*   **Chapell, B. (2018).** *Christ-Centered Preaching: Redeeming the Expository Sermon.* 3rd Edition. Grand Rapids: Baker Academic.
*   **De Leede, H. & Stark, C. (2017).** *Ontvouwen: Protestantse prediking in de praktijk.* Zoetermeer: Boekencentrum, pp. 73-81.
*   **Dumas, A. (1991).** *Cent prières possibles.* Paris: Albin Michel.
*   **Lowry, E.L. (2001).** *The Homiletical Plot: The Sermon as Narrative Art Form.* Expanded Edition. Louisville: Westminster John Knox Press.
*   **Snoek, H. (2010).** *Een huis om in te wonen: Uitleg en interpretatie van de Bijbel.* Kampen: Kok, 2e druk, pp. 180-199. (Zoekmodellen voor Gods-, mens- en Jezusbeelden).

---

## 🤝 Bijdragen

Suggesties en verbeteringen zijn welkom!
*   **Issues:** Meld bugs of feature requests via [GitHub Issues](https://github.com/wmotte/voorbereiding/issues)
*   **Pull Requests:** Fork het project en dien een PR in
*   **Theologische feedback:** Heb je expertise in homiletiek of liturgie en zie je verbeteringsmogelijkheden? Laat het weten!

---

## ⚠️ Beperkingen & Disclaimer

**Dit is een assistent, geen predikant.**

*   **Verificatie:** Het taalmodel baseert zich op online informatie. Controleer cruciale feiten, zeker bij kerkelijke fusiegemeenten of specifieke statistieken.
*   **Hallucinaties:** Hoewel het taalmodel wordt gedwongen tot bronverificatie (Google Search grounding), kunnen er onjuistheden voorkomen. Bijvoorbeeld: kunstsuggesties kunnen verwijzen naar niet-bestaande schilderijen. Controleer altijd de bronnen.
*   **Lokale kennis:** Bij fusiegemeenten kan de tool de verkeerde kerk selecteren. Verifieer altijd het adres in `00_meta.json`.
*   **Theologische nuance:** De tool geeft aanzetten, geen pasklare preken. De voorganger blijft verantwoordelijk voor de theologische lijn en pastorale afweging.
*   **Methodiek:** De analyses zijn aanzetten. Het eigenlijke werk — de ontmoeting tussen Woord, voorganger en gemeente — blijft een fysiek gebeuren.

---
*Gemaakt door W.M. Otte | [GitHub Repository](https://github.com/wmotte/voorbereiding)*