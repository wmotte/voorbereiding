# Representatieve Hoorders: Personaprofielen voor {{gemeente}}

Creëer vijf gedetailleerde fictieve personages die representatief zijn voor de hoorders in {{gemeente}} te {{plaatsnaam}}. Deze persona's dienen als concrete 'gezichten' bij de abstracte hoordersanalyse en helpen de predikant om de preek te richten op werkelijke mensen.

## Instructies

### Basisprincipe
De personages moeten **realistisch en herkenbaar** zijn voor de specifieke gemeente. Gebruik de informatie uit de voorgaande analyses (sociaal-maatschappelijke context, waardenoriëntatie, geloofsoriëntatie, etc.) om personages te creëren die de diversiteit van de gemeente weerspiegelen.

### Diversiteit
Zorg voor spreiding over:
- **Leeftijd:** Brede range van 16 tot 80 jaar (minimaal één jongere 16-25, één 30-50, één 50-65, één 70+)
- **Geslacht:** Mix van mannen en vrouwen
- **Levensfase:** Jongeren (scholier/student), young professionals, gezinnen, alleenstaanden, gescheidenen, weduwen/weduwnaars, stellen zonder kinderen, gepensioneerden
- **Woonsituatie:** Thuiswonend bij ouders, zelfstandig, samenwonend, getrouwd - niet iedereen heeft een gezin!
- **Sociaal-economisch:** Reflecteer de lokale economische realiteit
- **Kerkelijke betrokkenheid:** Van kernlid tot randkerkelijke, van meegebracht door ouders tot eigen keuze

### Per personage beschrijven (400-600 woorden)

#### 1. Basisgegevens
- **Naam:** Kies een passende, realistische Nederlandse naam (voornaam en achternaam)
- **Leeftijd:** Specifiek jaar
- **Fysieke verschijning:** Lengte, lichaamsbouw, huidskleur, haarkleur en -stijl, opvallende kenmerken
- **Woonplaats:** Specifieke wijk of straat in {{plaatsnaam}} indien relevant

#### 2. Relaties en sociaal netwerk
- **Woonsituatie:** Thuiswonend bij ouders, zelfstandig (huur/koop), studentenkamer, samenwonend, verzorgingshuis
- **Relatiestatus:** Single, daten, relatie, samenwonend, getrouwd, gescheiden, weduwe/weduwnaar
- **Kinderen:** Geen, wens, thuiswonend, uitgevlogen, kleinkinderen (indien van toepassing)
- **Familie:** Relatie met ouders, broers/zussen, verdere familie
- **Sociaal netwerk:** Vrienden, buren, verenigingen, collega's, mate van sociale inbedding of eenzaamheid

#### 3. Opleiding en werk
- **Scholing:** Hoogst genoten opleiding, eventuele cursussen of bijscholing
- **Intelligentie en leerstijl:** Praktisch vs. theoretisch, verbaal vs. visueel
- **Werkachtergrond:** Huidige of voormalige beroep(en), sector, werkdruk
- **Financiële situatie:** Inkomensniveau, eventuele zorgen of schulden

#### 4. Gezondheid
- **Lichamelijke gezondheid:** Chronische aandoeningen, beperkingen, medicijngebruik
- **Mentale gezondheid:** Stressniveau, eventuele psychische klachten (angst, depressie, burn-out)
- **Leefstijl:** Beweging, voeding, slaap, eventueel roken/alcohol

#### 5. Trauma's en zorgen
- **Verleden:** Ingrijpende gebeurtenissen (verlies, ziekte, scheiding, faillissement, ongeluk)
- **Heden:** Huidige zorgen en stress (werk, gezondheid, relaties, financiën, kinderen)
- **Onverwerkte pijn:** Wat draagt deze persoon nog met zich mee?

#### 6. Geloof en spiritualiteit
- **Kerkelijke achtergrond:** Opvoeding, doopsel, belijdenis, eventuele kerkwisselingen
- **Huidige betrokkenheid:** Frequentie kerkbezoek, taken in de gemeente, deelname aan activiteiten
- **Geloofsbeleving:** Hoe ervaart deze persoon God? Welke geloofstaal spreekt aan?
- **Twijfels en vragen:** Waar worstelt deze persoon mee op geloofsvlak?
- **Spirituele behoeften:** Wat zoekt deze persoon in de kerk en in de preek?

#### 7. Hobby's en interesses
- **Vrijetijdsbesteding:** Sport, cultuur, natuur, muziek, lezen, handwerk
- **Media:** Welke kranten, programma's, podcasts, sociale media?
- **Verenigingen:** Lidmaatschappen buiten de kerk

### Aansluiting bij de Schriftlezingen

Geef per personage kort aan:
- Welk aspect van de Schriftlezing(en) van deze zondag zou deze persoon **raken**?
- Welk aspect zou deze persoon mogelijk **afstoten** of **niet begrijpen**?
- Welke **existentiële vraag** uit het leven van dit personage zou de tekst kunnen adresseren?

## Outputformaat

Gebruik de volgende structuur voor elk personage:

---

## [Nummer]. [Voornaam Achternaam] ([leeftijd])

### Wie is [voornaam]?
[Inleidende paragraaf met kernschets van het personage]

### Relaties en sociaal netwerk
[Beschrijving van woonsituatie, relaties en sociale context]

### Opleiding, werk en financiën
[Beschrijving van achtergrond en huidige situatie]

### Gezondheid
[Lichamelijke en mentale gezondheid]

### Zorgen en trauma's
[Wat draagt deze persoon met zich mee?]

### Geloof en spiritualiteit
[Kerkelijke betrokkenheid en geloofsbeleving]

### Hobby's en interesses
[Vrijetijdsbesteding en media]

### Aansluiting bij de Schriftlezingen
[Hoe raakt de tekst dit personage?]

---

## Bronnen
Baseer de personages op de informatie uit:
- Sociaal-maatschappelijke context (demografie, economie, woningmarkt)
- Waardenoriëntatie (milieus, trends, zorgen)
- Geloofsoriëntatie (kerkelijke achtergrond, geloofstaal)
- Interpretatieve synthese

Verwijs expliciet naar lokale omstandigheden die je in deze analyses hebt gevonden.

## JSON Output Schema

Retourneer UITSLUITEND een JSON object volgens onderstaand schema:

```json
{
  "personas": [
    {
      "nummer": 1,
      "naam": {
        "voornaam": "string",
        "achternaam": "string"
      },
      "leeftijd": "number",
      "kernschets": "string - 2-3 zinnen die de essentie van dit personage vangen",
      "basisgegevens": {
        "fysieke_verschijning": "string - lengte, lichaamsbouw, haarkleur, opvallende kenmerken",
        "woonwijk": "string - specifieke wijk of straat in {{plaatsnaam}}"
      },
      "relaties_sociaal": {
        "woonsituatie": "string - thuiswonend|zelfstandig|samenwonend|verzorgingshuis|etc.",
        "relatiestatus": "string - single|relatie|getrouwd|gescheiden|weduwe|etc.",
        "kinderen": "string|null - geen|wens|thuiswonend|uitgevlogen|kleinkinderen",
        "familie_relatie": "string - relatie met ouders/broers/zussen",
        "sociaal_netwerk": "string - vrienden, buren, mate van eenzaamheid"
      },
      "opleiding_werk": {
        "opleiding": "string - hoogst genoten opleiding",
        "intelligentie_leerstijl": "string - praktisch vs. theoretisch",
        "huidige_werk": "string - beroep, sector, werkdruk",
        "voormalig_werk": "string|null",
        "financiele_situatie": "string - inkomensniveau, zorgen, schulden"
      },
      "gezondheid": {
        "lichamelijk": "string - chronische aandoeningen, beperkingen, medicijnen",
        "mentaal": "string - stressniveau, psychische klachten",
        "leefstijl": "string - beweging, voeding, roken/alcohol"
      },
      "traumas_zorgen": {
        "verleden": ["string - ingrijpende gebeurtenissen"],
        "heden": ["string - huidige zorgen"],
        "onverwerkt": "string - wat draagt deze persoon nog mee?"
      },
      "geloof_spiritualiteit": {
        "kerkelijke_achtergrond": "string - opvoeding, doopsel, belijdenis",
        "huidige_betrokkenheid": "string - frequentie kerkbezoek, taken",
        "geloofsbeleving": "string - hoe ervaart deze persoon God?",
        "geloofstaal": "string - welke taal spreekt aan?",
        "twijfels_vragen": ["string - geloofsworstellingen"],
        "spirituele_behoeften": "string - wat zoekt deze persoon?"
      },
      "hobbys_interesses": {
        "vrijetijd": ["string - sport, cultuur, natuur"],
        "media": ["string - kranten, programma's, podcasts, sociale media"],
        "verenigingen": ["string - lidmaatschappen buiten kerk"]
      },
      "aansluiting_schriftlezingen": {
        "wat_raakt": "string - welk aspect van de lezingen raakt dit personage?",
        "wat_afstoot": "string - welk aspect zou kunnen afstoten of niet begrepen worden?",
        "existentiele_vraag": "string - welke vraag uit dit leven adresseert de tekst?"
      }
    }
  ]
}
```

**BELANGRIJK:**
- Retourneer ALLEEN valide JSON, geen markdown of toelichting.
- Precies 5 personas met spreiding over leeftijd (16-80), geslacht, en levensfase.
- Per persona 400-600 woorden inhoud, verdeeld over de velden.
- Gebruik realistische Nederlandse namen.
