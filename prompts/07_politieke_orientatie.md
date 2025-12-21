# Politieke Oriëntatie-analyse

Breng het politieke landschap en stemgedrag in kaart voor {{plaatsnaam}}.

## 0. Context & Recente Verkiezingen (BELANGRIJK)

De meest recente **Tweede Kamerverkiezingen in Nederland zijn gehouden op 29 oktober 2025**. Gebruik de uitslagen van deze verkiezingen als basis voor de analyse van het landelijk stemgedrag. Negeer oudere data uit 2023 voor de actuele status, tenzij je trends over langere tijd beschrijft.

Zoek expliciet naar:
- **Tweede Kamerverkiezingen (29 oktober 2025)**: Gebruik de uitslag voor {{plaatsnaam}}.
- **Gemeenteraadsverkiezingen**: Wanneer waren de laatste in {{plaatsnaam}} (meestal 2022 of 2026)?
- **Europees Parlementsverkiezingen (juni 2024)**.
- **Provinciale Statenverkiezingen (maart 2023)**.

## 1. Landelijk stemgedrag (Uitslag 29 oktober 2025)

Analyseer de uitslagen van de Tweede Kamerverkiezingen van 29 oktober 2025 in {{plaatsnaam}}:
- Welke partijen behaalden de meeste stemmen?
- Hoe verhoudt dit zich tot het landelijk gemiddelde van 2025?
- Welke verschuivingen zijn er t.o.v. de verkiezingen van 2023?

## 2. Europees stemgedrag (2024)

Bekijk de uitslagen van de Europees Parlementsverkiezingen van juni 2024 in {{plaatsnaam}}:
- Geeft dit een andere trend weer dan de TK-verkiezingen van 2025?

## 3. Provinciaal stemgedrag (2023)

Bekijk de Provinciale Statenverkiezingen van maart 2023 in de provincie van {{plaatsnaam}}:
- Dominante partijen en regionale bewegingen.

## 4. Gemeentelijk stemgedrag

Analyseer de meest recente gemeenteraadsverkiezingen (2022 of 2026):
- Lokale partijen en hun positie in de coalitie/oppositie.
- Belangrijke lokale politieke thema's.

## 5. Politieke cultuur

Beschrijf de bredere politieke cultuur in {{plaatsnaam}}:
- Progressief versus conservatief.
- Vertrouwen in overheid en instituties.
- Proteststemmen of anti-establishment sentiment.

## 6. Spanningsvelden

Welke politieke onderwerpen zorgen voor verdeeldheid in {{plaatsnaam}}?
- Lokale kwesties (bouwprojecten, windmolens, asielopvang).
- Hoe uit zich dit in het dagelijks leven?

## 7. Relevantie voor de prediking

Reflecteer op wat dit betekent voor de gemeente {{gemeente}}:
- Gevoeligheden en aansluitingspunten voor de preek.

## Bronnen

Gebruik verkiezingsuitslagen van kiesraad.nl, gemeente.nl en lokale nieuwsmedia. Wees concreet en feitelijk over {{plaatsnaam}}.

## JSON Output Schema

Retourneer UITSLUITEND een JSON object volgens onderstaand schema:

```json
{
  "verkiezingsdata": {
    "tweede_kamer": {
      "datum": "29 oktober 2025",
      "opmerking": "string|null"
    },
    "europees_parlement": {
      "datum": "juni 2024"
    },
    "provinciale_staten": {
      "datum": "maart 2023"
    },
    "gemeenteraad": {
      "datum": "string"
    }
  },
  "landelijk_stemgedrag": {
    "verkiezingsdatum": "29 oktober 2025",
    "top_partijen": [
      {
        "partij": "string",
        "percentage_lokaal": "number",
        "percentage_landelijk": "number",
        "verschil_tov_2023": "string"
      }
    ],
    "verschuivingen": ["string"],
    "opkomst": "string",
    "analyse": "string"
  },
  "europees_stemgedrag": {
    "verkiezingsdatum": "juni 2024",
    "top_partijen": [
      {
        "partij": "string",
        "percentage_lokaal": "number"
      }
    ]
  },
  "provinciaal_stemgedrag": {
    "verkiezingsdatum": "maart 2023",
    "dominante_partijen": ["string"],
    "regionale_partijen": ["string"]
  },
  "gemeentelijk_stemgedrag": {
    "verkiezingsdatum": "string",
    "coalitie": ["string"],
    "belangrijke_themas": ["string"]
  },
  "politieke_cultuur": {
    "progressief_conservatief": "string",
    "vertrouwen_overheid": "string",
    "anti_establishment": "string"
  },
  "spanningsvelden": [
    {
      "onderwerp": "string",
      "type": "string",
      "standpunten": "string"
    }
  ],
  "relevantie_prediking": {
    "gevoeligheden": ["string"],
    "aansluiting_mogelijkheden": ["string"]
  }
}
```

**BELANGRIJK:** Retourneer ALLEEN valide JSON, geen markdown of toelichting. Begin direct met `{`.
