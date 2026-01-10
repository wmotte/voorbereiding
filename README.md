![Voorbereiding Banner](misc/banner.png)

# Preekvoorbereiding

**Een LLM-ondersteund hulpmiddel voor het voorbereiden van protestantse diensten.**

**Let op: Dit materiaal is bedoeld ter inspiratie. De uiteindelijke verantwoordelijkheid voor de dienst (en in het bijzonder de preek) ligt bij de voorganger.**

⚡ **UPDATE 10 januari 2026**: ⚡ *Naar aanleiding van de verzoeken van voorgangers om gebruik te maken van deze tool, start er een publieke pilot. Elke maandagochtend verschijnt hier een contextuele analyse van de lezingen uit het oecumenisch leesrooster voor de komende zondag, uitgewerkt voor drie willekeurige PKN-gemeenten.*

1. Bekijk de online webviewer met *100% automatisch-gegenereerde* voorbeelddata: 

[**Voorbereiding**](https://wmotte.github.io/voorbereiding/)

**❓ [Q&A voor (kritische) lezers](misc/QandA.md)** — over de Heilige Geest, energieverbruik, plagiaat en meer.

2. Om een idee te krijgen hoe dit hulpmiddel ingezet zou kunnen worden om gedegen feedback te leveren tijdens of na het schrijven van een preek, zie:

[**Feedback**](https://wmotte.github.io/homiletiek_feedback/)

Dit project combineert **contextanalyse** (hoorders, samenleving) met concrete **liturgische bouwstenen** (exegese, preekschets, gebeden). Het doel is niet om de preek/gebeden te *schrijven*, maar om de voorganger te voorzien van een rijke, contextuele basis.

Het totaal aan modelinstructies (prompts) bedraagt 15.000 zinnen (~116.000 woorden).

---

### 📑 Inhoudsopgave
1. [Over dit Project](#-over-dit-project)
2. [Overzicht van de Analyses & Methodiek](#-overzicht-van-de-analyses--methodiek)
3. [Database Grounding: Preventie van Hallucinaties](#-database-grounding-preventie-van-hallucinaties)
4. [Toelichting per Onderdeel](#00-meta-data)
5. [Preekschetsen: Tekstkeuze en Diversiteit](#-preekschetsen-tekstkeuze-en-diversiteit)
6. [Literatuur & Bronnen](#-literatuur--bronnen)

---

## 📖 Over dit Project

Inspiratie voor dit hulpmiddel is geput uit **"De Eerste Dag"**, de officiële, oecumenische handreiking van de Raad van Kerken in Nederland. "De Eerste Dag" ondersteunt bij de voorbereiding van de wekelijkse eredienst, aansluitend bij het kerkelijk jaar en de liturgie. Het biedt commentaren bij de lezingen, suggesties voor de liturgie, gebeden en toepassingen voor kinderwerk, en helpt bij het structureren van de dienst (de "orde").

Met dit digitale hulpmiddel wordt die voorbereiding veel dynamischer én contextueler. De voorganger kan specifiek aangeven wie de hoorders zijn, in welke tijd en op welke plaats. Ook kan hij of zij nu zelf bepalen welke onderdelen van belang zijn in de voorbereiding. De output van de tool biedt de mogelijkheid om de eigen exegesetische inzichten en eigen homiletische structuur te toetsen. Sommigen willen meer informatie over interactieve momenten (zoals het kindermoment), terwijl weer anderen geholpen zijn bij de identificatie van relevante kunst- en cultuurartefacten. 
Een enkeling zoekt inspiratie in *hypothetische* preekschetsen van belangrijke historische voorgangers; de tool demonstreert hoe dat eruit zou kunnen zien. 

Het belangrijkste element is en blijft de contextuele verwerking in de verschillende voorbereidende stappen. 

Friedrich Niebergall stelde ooit: *"Menige preek geeft antwoorden op vragen die niemand stelt, en gaat niet in op vragen die iedereen stelt."* 

Dit project helpt die valkuil te vermijden door twee werelden te verbinden met behulp van een modern taalmodel:
1.  **De Wereld van de Hoorder:** Een systematische analyse van de lokale context (wie zijn de hoorders, wat houdt hen bezig?).
2.  **De Wereld van de Tekst:** Exegese, kunst & cultuur, en liturgische vormgeving.

---

## 📊 Overzicht van de Analyses & Methodiek

De analyses in dit project zijn niet willekeurig, maar gebaseerd op gevestigde homiletische en liturgische methodieken. Hieronder volgt een uitleg per onderdeel, in de volgorde waarin ze worden gegenereerd. Voor meer informatie zijn er een aantal achtergrondartikelen beschikbaar in de `misc/` map.

| Nr | Naam | Omschrijving |
|:---|:---|:---|
| 00 | **Meta-data** | `00_meta.json`: Centrale opslag van user input en geverifieerd adres. |
| 01 | **Liturgische Context** | Zondag van het jaar, lezingen, liturgische kleur en seizoen. |
| 02 | **Sociaal-maatschappelijk** | Demografie, economie en sociale structuur van de burgerlijke gemeente. |
| 03 | **Waardenoriëntatie** | De "Vijf V's" en Motivaction Mentality-groepen. |
| 04 | **Geloofsoriëntatie** | Verhouding tussen officieel geloof en het geleefde geloof van hoorders. |
| 05 | **Synthese** | Homiletische aanbevelingen (toon, taal, beelden). |
| 06 | **Wereldnieuws** | Relevant actueel nieuws van de afgelopen dagen gerelateerd aan de zondag. |
| 07 | **Politieke Oriëntatie** | Stemgedrag en politieke cultuur in de regio. |
| 07a | **Wetslezing Voorstel** | Voorstel voor Wetslezing (OT), bijbehorende psalm en genade-verkondiging. |
| 08a | **Exegese** | Tekstkritiek, historische context en theologische lijnen (zoekmodellen Snoek). |
| 08b | **Liedsuggesties** | Database-analyse met liederen uit Liedboek, Weerklank, Op Toonhoogte, Hemelhoog. |
| 08c | **Commentaren** | Database-analyse van professionele exegetische commentaren via database. |
| 08d | **Theologie** | Diepgaande analyse van drie theologische noties met dwarsverbanden in de dogmatische traditie. |
| 09 | **Kunst & Cultuur** | Beelden, film en muziek bij de lezingen (incl. bronverificatie). |
| 10 | **Focus & Functie** | De kernboodschap en het beoogde effect van de preek. |
| 11 | **Kalender** | Gedenkdagen, heiligen, astronomie en weer. |
| 12 | **Representatieve Hoorders** | Vijf fictieve personages (16-80 jaar) als spiegel voor de prediking. |
| 13 | **Homiletische Analyse** | Preekschets (Lowry; narratief), elementen (Chapell; FCF & Christocentrisch) en inductie (Buttrick; Moves & Structures). |
| 13b | **Homiletische Illustraties** | Minimaal 20 concrete illustraties (verhalen, metaforen, voorbeelden). |
| 14 | **Klassieke Retorica** | Aristotelische analyse (ethos, pathos, logos) en klassieke dispositio. |
| 14 (varianten) | **Gebeden** | Standaard (liturgisch), Profetisch (Brueggemann), Dialogisch (Dumas), en Eenvoudige B1-niveau gebeden. |
| 15 | **Kindermoment** | Vijf totaal verschillende opties (Klassiek, Doe-het-zelf, Gekke Twist, Bizarre Inval, Ernstig). |
| 15 (variant) | **Moment van Bezinning** | Een specifieke vorm van gebed of meditatie die inkeer biedt binnen de eredienst. |
| 16 | **Preekschets Sölle** | Preekschets in de stijl van Dorothee Sölle: mystiek en politiek verzet. |
| 17 | **Preekschets Jüngel** | Preekschets in de stijl van Eberhard Jüngel: paradox en evangelische doorbraak. |
| 18 | **Preekschets Brueggemann** | Preekschets in de stijl van Walter Brueggemann: profetische verbeelding en verzet. |
| 18b | **Preekschets Brueggemann (Poet)** | Preekschets gebaseerd op *Finally Comes the Poet*: 4 homiletische methoden. |
| 19 | **Preekschets Noordmans** | Preekschets in de stijl van Oepke Noordmans: trinitarisch en gericht op 'herschepping' door de Heilige Geest. |
| 20 | **Preekschets Peterson** | Preekschets in de stijl van Eugene Peterson: contemplatief en pastoraal. |
| 24 | **Preekschets Rutledge** | Preekschets in de stijl van Fleming Rutledge: apocalyptisch en kruistheologisch. |
| 25 | **Preekschets Koyama** | Preekschets in de stijl van Kosuke Koyama: contextueel en dialogisch. |
| 26 | **Preekschets Taylor** | Preekschets in de stijl van Gardner C. Taylor: eloquent en narratief. |
| 21 | **Midjourney Prompts** | Visuele thema's en prompts voor beeldgeneratie bij de preek. |
| 23 | **Literaire Preekschets** | Transformatie van de Buttrick-analyse naar een literaire preekschets, met nadruk op verhalende taal, concrete beelden en dialoog. |

---

### 🔍 Database Grounding: Preventie van Hallucinaties

Een van de grootste uitdagingen bij het gebruik van taalmodellen is het risico op **hallucinaties**: het model verzint feiten, bronnen of citaten die niet bestaan. Om dit te voorkomen gebruikt dit project **database grounding**.

#### Hoe werkt Database Grounding?

In plaats van het taalmodel te vragen "geef liederen die passen bij deze preek", wordt het model toegang gegeven tot een **database** met daadwerkelijke data. Het model kan zelf queries uitvoeren en alleen informatie gebruiken die daadwerkelijk in de database staat.

##### 07a: Wetslezing Verificatie
*   **Verificatie:** Het voorgestelde psalm-gezang wordt na generatie gecontroleerd in de Weerklank database

#### Waarom is dit cruciaal?

Zonder database grounding zou het model kunnen suggereren:
*   "Lied 1017 uit het Liedboek" (terwijl het Liedboek 1016 nummers heeft)
*   "Zie commentaar van N.T. Wright op Jeremia 5" (terwijl dit commentaar niet bestaat)
*   "Weerklank (Psalm) 94:12" (terwijl dit psalm-nummer niet bestaat)

Met database grounding zijn alle suggesties **verifieerbaar en bruikbaar** in de praktijk.

---

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

### 07a Wetslezing Voorstel
Voorstel voor Wetslezing (OT), bijbehorende psalm en genade-verkondiging, inclusief automatische verificatie van de liedsuggesties.

### 08a Exegese: Zoekmodellen (Hans Snoek)
Tekstkritiek, historische context en theologische lijnen. Het script analyseert de Schrifttekst aan de hand van de modellen uit *Een huis om in te wonen*:
*   **Godsbeelden:** Werkwoordelijk (bevrijden), metaforisch (herder) en eigenschappen (heilig vs. barmhartig).
*   **Mensbeelden:** De mens in verhouding tot God (aanbidding) en de wereld (zorg voor de naaste).
*   **Jezusbeelden:** Van achteren (Joods), van boven (Zoon van God), van beneden (mens) en van voren (Koninkrijk).

### 08b Liedsuggesties
Geautomatiseerde zoektocht naar passende liederen in de database (Liedboek, Weerklank, Op Toonhoogte, Hemelhoog) op basis van tekstuele en thematische matches.

### 08c Commentaren
Analyse van professionele exegetische commentaren via een kennisgraaf (Neo4j), gericht op diepgaande tekstuele duiding.

### 08d Theologie
Een diepteboring die drie theologische noties uit de lezingen identificeert en analyseert. In tegenstelling tot de exegese (die de tekst voornamelijk in zijn context leest), zoekt deze analyse naar bredere dogmatische dwarsverbanden en concepten (zoals 'verbond', 'gerechtigheid' of 'eschatologie') in de theologische traditie. Deze sectie gebruikt een kennisgraaf (Neo4j) met theologische commentaren om systematisch-theologische reflecties van verschillende denkers te verzamelen en te verbinden, wat resulteert in drie uitgebreide theologische analyses van elk 800-1000 woorden.

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

### 13b Homiletische Illustraties
Minimaal 20 concrete illustraties (verhalen, metaforen, voorbeelden) die de brug slaan tussen de exegese en de leefwereld van de hoorder.

---

### 📖 Preekschetsen: Tekstkeuze en Diversiteit

Het project genereert meerdere preekschetsen voor dezelfde zondag, elk vanuit een andere theologische traditie. Om te voorkomen dat alle schetsen dezelfde tekst kiezen en op dezelfde "angle" focussen, heeft elke prompt een **unieke tekstkeuze-strategie** die past bij de theologische identiteit van de auteur.

#### Overzicht Tekstkeuze-Strategieën

| Prompt | Tekstkeuze-Focus | OT-Prioriteit | Unieke Lens |
|--------|------------------|---------------|-------------|
| **BUTTRICK** | Narratieve structuur + visuele beelden | Neutraal (verhaal > genre) | "Moves"-potentie, groepsbewustzijn |
| **LOWRY** | Omkerings-potentie | Neutraal (omkering > genre) | Discontinuïteit, narratieve spanning |
| **SÖLLE** | Profetisch-politiek | Preferentie OT-profeten | Ontmaskering systemen, plaatsbekleding |
| **JÜNGEL** | Paradox + theologia crucis | Neutraal (paradox > genre) | Onderbreking, "Niets naar Ja" |
| **BRUEGGEMANN** | OT-profeten/psalmen | Zeer sterke preferentie OT | Klacht + visioen, economische rechtvaardigheid |
| **NOORDMANS** | Breuk + verbreking | Neutraal (spanning > harmonie) | Geen rozentuin, publiek karakter |
| **PETERSON** | Kleine/stille teksten | Neutraal (contemplatief > dramatisch) | Incarnatie (vlees & bloed), Taal I |
| **RUTLEDGE** | Apocalyptisch/Kruis | Neutraal (kruis > moraal) | Kosmische invasie, God als handelend subject |
| **KOYAMA** | Contextueel/Dialogisch | Neutraal (concrete context > abstractie) | Neighbourology, "Three Mile an Hour God" |
| **TAYLOR** | Narratief/Eloquent | Neutraal (verhaal > doctrine) | Scharlaken Draad, "Sweet Torture" |
| **ZORNBERG** | Torah/Profeten | Zeer sterke preferentie OT | Midrasjische potentie, psychologische diepte |

#### Waarom deze Diversiteit?

Zonder deze strategieën zouden alle prompts dezelfde kerntekst kiezen (vaak de evangelielezing) omdat de exegese en commentaren daar het meest op focussen. Door elke theologische stem zijn eigen criteria te geven, ontstaat er natuurlijke spreiding over de beschikbare lezingen:

**Voorbeeld:** Voor een zondag met Jesaja 49, Psalm 40, Johannes 1 en 1 Korintiërs 1:
- **Brueggemann & Zornberg**: Zeer waarschijnlijk Jesaja 49 (OT-profeet)
- **Buttrick**: Johannes 1 (narratieve beweging) OF Psalm 40 (emotionele curve)
- **Lowry**: Psalm 40 (oriëntatie → crisis → doorbraak)
- **Sölle**: Jesaja 49 (politiek - licht voor volken)
- **Jüngel**: Johannes 1 (paradox - Woord wordt vlees)
- **Noordmans**: Psalm 40 (spanning, verbreking)
- **Peterson**: Psalm 40 (contemplatief) OF 1 Kor 1 (intiem, relationeel)

Dit zorgt ervoor dat predikanten verschillende invalshoeken en tekstkeuzes kunnen overwegen, in plaats van één uniforme benadering.

---

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

### 15 (variant) Moment van Bezinning
Een specifieke vorm van gebed of meditatie die inkeer biedt binnen de eredienst. Dit moment is bedoeld voor reflectie, stilte en persoonlijke benadering van God.
*   **Kenmerken:** Korte, rustgevende teksten, ruimte voor stilte, nadruk op Gods nabijheid en troost.
*   **Functie:** Ruimte creëren voor innerlijke rust en bezinning in het drukke leven.

### 16 Preekschets in de geest van Sölle
Preekschets in de stijl van Dorothee Sölle: mystiek en politiek verzet. Deze benadering verbindt de bijbeltekst met maatschappelijk engagement en een diepe spiritualiteit van verzet tegen onrecht.

📄 **[Lees meer over de homiletiek van Sölle](misc/Solle_Homiletiek.md)**

### 17 Preekschets in de geest van Jüngel
Preekschets in de stijl van Eberhard Jüngel: paradox en evangelische doorbraak. Jüngels methode focust op de 'taal van de liefde' en de verrassing van het evangelie die de menselijke logica doorbreekt.

📄 **[Lees meer over de homiletiek van Jüngel](misc/Jungel_Homiletiek.md)**

### 18 Preekschets in de geest van Brueggemann
Preekschets in de stijl van Walter Brueggemann: profetische verbeelding en verzet. Deze benadering verbindt de bijbeltekst met maatschappelijk engagement en een diepe spiritualiteit van verzet tegen onrecht.

### 18b Preekschets Brueggemann (Finally Comes The Poet)
Een geavanceerde variant gebaseerd op Brueggemanns latere werk *Finally Comes the Poet*.
*   **Methodiek:** Het systeem kiest autonoom één van de vier specifieke homiletische strategieën:
    1.  [*Schuld en Genezing*](prompts/finally_comes_the_poet__prompts/Methode_1_Schuld_en_Genezing.md) (verzoening)
    2.  [*Klacht naar Lofprijzing*](prompts/finally_comes_the_poet__prompts/Methode_2_Klacht_naar_Lofprijzing.md) (oriëntatie - desoriëntatie - nieuwe oriëntatie)
    3.  [*Rusteloosheid en Hebzucht*](prompts/finally_comes_the_poet__prompts/Methode_3_Rusteloosheid_en_Hebzucht.md) (sabbat als verzet)
    4.  [*Verzet en Overgave*](prompts/finally_comes_the_poet__prompts/Methode_4_Verzet_en_Overgave.md) (de vreemde nieuwe wereld van de bijbel)
*   **Proces:** De analyse verloopt in twee stappen: eerst selecteert het model de meest passende strategie bij de lezingen, daarna wordt de preekschets geschreven volgens die specifieke methode.

### 19 Preekschets in de geest van Noordmans
Preekschets in de stijl van Oepke Noordmans. Zijn homiletiek biedt een unieke benadering gebaseerd op de leer van de Drie-eenheid en het begrip 'herschepping'.
*   **Centraal thema:** De rol van de Heilige Geest in het creëren van een nieuwe werkelijkheid (herschepping) door de prediking.
*   **Structuur:** "Scheppen is scheiden" - een preek die zich toespitst op één punt en de Geest laat werken door te onderscheiden.

📄 **[Lees meer over de homiletiek van Noordmans](misc/Noordmans_Homiletiek.md)**

### 20 Preekschets in de geest van Peterson
Preekschets in de stijl van Eugene Peterson: contemplatief en pastoraal. Gericht op 'A Long Obedience in the Same Direction' en het alledaagse leven doordesemen met de bijbelse verbeelding.

### 24 Preekschets in de geest van Rutledge
Preekschets in de stijl van Fleming Rutledge: apocalyptisch en kruistheologisch. Rutledge's homiletiek is geworteld in de "apocalyptische theologie" van de Union School en Karl Barth.
*   **Centraal thema:** God als het handelend subject ("God is the subject of the verbs") in een kosmische strijd tegen de Machten van Zonde en Dood.
*   **Kenmerken:** Nadruk op het "Christus Kerygma" (de Kosmische Overwinnaar) boven het "Jezus Kerygma" (moreel voorbeeld), verwerping van therapeutisch moralisme, en de preek als proclamatie van goddelijke invasie.

📄 **[Lees meer over de homiletiek van Rutledge](misc/Fleming_Rutledge_Homiletiek.md)**

### 25 Preekschets in de geest van Koyama
Preekschets in de stijl van Kosuke Koyama: contextueel en dialogisch. Koyama's homiletiek is een radicale heroriëntatie van de houding van de prediker ten opzichte van God, de tekst en de naaste.
*   **Centraal thema:** "Neighbourology" – de studie van God is onlosmakelijk verbonden met de studie van de naaste. De "Three Mile an Hour God" – God beweegt langzaam omdat Hij liefde is.
*   **Kenmerken:** Inductieve structuur, "Kitchen Theology" (theologie bereid met lokale ingrediënten), de "Crucified Mind" versus de "Crusading Mind", en zintuiglijke prediking.

📄 **[Lees meer over de homiletiek van Koyama](misc/Kosuke_Koyama_Homiletiek.md)**

### 26 Preekschets in de geest van Taylor
Preekschets in de stijl van Gardner C. Taylor: eloquent en narratief. Taylor, "de Deken van de predikers", vertegenwoordigt een unieke synthese van klassieke westerse theologie en de Afro-Amerikaanse predikingstraditie.
*   **Centraal thema:** De "Scharlaken Draad" – de rode draad van verlossing die door de hele Schrift loopt. De "Sweet Torture of Sunday Morning" – prediking als existentiële worsteling en genade.
*   **Kenmerken:** "Split Vision" (Bijbel en krant), narratieve eloquentie, het "penseel van de prediker" (beeldende taal), en de integratie van lijden in het geloof via de theologie van Unamuno.

📄 **[Lees meer over de homiletiek van Taylor](misc/Gardner_Taylor_homiletiek.md)**

### 21 Midjourney Prompts
Visuele thema's en prompts voor beeldgeneratie bij de preek. Deze prompts helpen bij het visueel ondersteunen van de boodschap via projectie of sociale media.

### 23 Literaire Preekschets
Een volledig uitgeschreven preekschets in literaire stijl, gebaseerd op de homiletische structuur van Buttrick (Moves & Structures). Deze benadering transformeert de theologische analyse naar toegankelijke, verhalende taal.

*   **Methodiek:** Transformatie van complexe theologische taal naar eenvoudige, concrete beelden
*   **Stijlkenmerken:**
    *   Verhalende schrijfstijl met filmische scènebeschrijvingen
    *   Uitgebreide zinnen (70-80% lange zinnen van 15-35 woorden) voor natuurlijke flow
    *   Verplichte dialogen (minimaal 3-5) - Bijbelse figuren en hedendaagse mensen laten spreken
    *   Concrete, zintuiglijke details in plaats van abstracte theologische jargon
    *   **Actieve vermijding van clichés** - verse beelden specifiek voor de context
*   **Doel:** Een preekschets die de luisteraar meeneemt in het verhaal, niet uitlegt maar laat zien, en theologische diepgang verbindt met alledaagse herkenning

Deze transformatie is gebaseerd op literaire voorbeelden en gebruikt moderne technieken uit creative writing (show don't tell, cinematografische beschrijvingen, karakterontwikkeling) om de boodschap levendig en toegankelijk te maken.
 
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
*Gemaakt door W.M. Otte | [GitHub Repository](https://github.com/wmotte/voorbereiding)*
