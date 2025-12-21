# Analyse van Actueel Wereldnieuws

**BELANGRIJK: Vandaag is {{huidige_datum}}.** Doorzoek het internet grondig naar het meest acute, actuele en mogelijk schokkende wereldnieuws van de **afgelopen 3-5 dagen** (dus het nieuws van rond {{huidige_datum}}).

De preekdatum is {{datum}}. Als de preekdatum in de toekomst ligt, zoek dan naar het nieuws van NU (rond {{huidige_datum}}), niet naar nieuws rond de preekdatum.

## Focus op:

### 1. Grote wereldgebeurtenissen
- Oorlogen en gewapende conflicten (bijv. Oekraïne, Midden-Oosten, Sudan)
- Natuurrampen (aardbevingen, overstromingen, orkanen, bosbranden)
- Terroristische aanslagen
- Politieke crises, staatsgrepen en omwentelingen
- Vluchtelingenstromen en migratiecrises

### 2. Schokkend nieuws dat mensen raakt
- Tragische ongevallen met veel slachtoffers
- Vliegtuigongelukken, scheepsrampen, treinongelukken
- Massale sterfgevallen door epidemieën of rampen
- Humanitaire crises en hongersnoden
- Geweld tegen burgers, kinderen of kwetsbare groepen

### 3. Nieuws dat existentiële en theologische vragen oproept
- Gebeurtenissen die theodicee-vragen oproepen ("Waar is God bij dit lijden?")
- Onrecht dat verontwaardiging wekt (mensenrechtenschendingen, onderdrukking)
- Klimaatrampen en zorgen om de schepping
- Hoopgevende doorbraken, vredesinitiatieven of verzoening
- Morele dilemma's in het nieuws (euthanasie, AI, medische ethiek)
- Verhalen van moed, opoffering of naastenliefde

### 4. Nederlands nieuws met impact
- Grote gebeurtenissen in Nederland zelf
- Politieke ontwikkelingen die mensen bezighouden
- Maatschappelijke discussies (asiel, zorg, onderwijs, woningmarkt)
- Nieuws dat de regio {{plaatsnaam}} direct raakt

### 5. Nieuws relevant voor de kerk
- Berichten over christenvervolging wereldwijd
- Ontwikkelingen in oecumene of wereldkerk
- Uitspraken van paus, WCC, of kerkleiders
- Nieuws over Kerk in Actie-projecten of diaconale noden

## Bronnen

### Nederlandse bronnen (prioriteit)
- NOS.nl - hoofdnieuws en buitenland
- NRC, Volkskrant, Trouw - achtergronden en analyses
- Nederlands Dagblad, Reformatorisch Dagblad - kerkelijk perspectief
- Protestantsekerk.nl - PKN-nieuwsberichten

### Internationale bronnen
- BBC, The Guardian, CNN - Engelstalig wereldnieuws
- Al Jazeera - Midden-Oosten perspectief
- Deutsche Welle - Europees perspectief

## Relevantie voor de PKN-predikant

Analyseer per nieuwsitem:
- **Pastoraal:** Welke troost of nabijheid wordt gezocht?
- **Profetisch:** Waar moet de kerk haar stem verheffen?
- **Diaconaal:** Waar kan de gemeente in actie komen? (Kerk in Actie, collectes)
- **Liturgisch:** Kan dit een plek krijgen in voorbeden of schuldbelijdenis?
- **Homiletisch:** Hoe verhoudt dit nieuws zich tot de Schriftlezingen van de zondag?

## Gewenste output

Lever een overzicht met:
1. De 3-5 meest ingrijpende wereldgebeurtenissen van de afgelopen dagen
2. Per gebeurtenis: korte samenvatting, emotionele/existentiële impact, theologische vragen die het oproept
3. Concrete suggesties hoe de predikant hierop kan inspelen:
   - In de preek (erkennen, duiden, troosten, contextualiseren)
   - In de voorbeden
   - In mededelingen of collectebestemming
4. Waarschuwing voor valkuilen (te politiek worden, onnodige polarisatie, ongeïnformeerd oordelen)

## JSON Output Schema

Retourneer UITSLUITEND een JSON object volgens onderstaand schema:

```json
{
  "nieuwsoverzicht_datum": "string - datum van het nieuwsoverzicht ({{huidige_datum}})",
  "wereldgebeurtenissen": [
    {
      "titel": "string - korte kop",
      "categorie": "string - oorlog|natuurramp|terrorisme|politieke_crisis|vluchtelingen|humanitair|klimaat|anders",
      "samenvatting": "string - 2-3 zinnen",
      "locatie": "string",
      "datum_gebeurtenis": "string",
      "emotionele_impact": "string - hoe raakt dit mensen existentieel?",
      "theologische_vragen": ["string - theodicee, rechtvaardigheid, hoop, etc."],
      "relevantie_pkn": {
        "pastoraal": "string - welke troost of nabijheid wordt gezocht?",
        "profetisch": "string - waar moet de kerk haar stem verheffen?",
        "diaconaal": "string - waar kan de gemeente in actie komen?",
        "liturgisch": "string - plek in voorbeden of schuldbelijdenis?",
        "homiletisch": "string - verhouding tot de Schriftlezingen"
      },
      "bronnen": ["string - NOS, NRC, etc."]
    }
  ],
  "nederlands_nieuws": [
    {
      "titel": "string",
      "samenvatting": "string",
      "lokale_relevantie": "string - relevant voor {{plaatsnaam}}?",
      "maatschappelijke_discussie": "string|null",
      "relevantie_preek": "string"
    }
  ],
  "kerkelijk_nieuws": [
    {
      "titel": "string",
      "bron": "string",
      "samenvatting": "string",
      "relevantie": "string"
    }
  ],
  "suggesties_predikant": {
    "in_de_preek": ["string - concrete suggesties hoe te verwerken"],
    "in_voorbeden": ["string - specifieke gebedspunten"],
    "mededelingen_collecte": ["string|null"]
  },
  "valkuilen": [
    {
      "valkuil": "string - bijv. 'te politiek worden'",
      "risico": "string",
      "advies": "string"
    }
  ]
}
```

**BELANGRIJK:** Retourneer ALLEEN valide JSON, geen markdown of toelichting.
