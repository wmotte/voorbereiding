# Sociaal-Maatschappelijke Contextanalyse

Breng in kaart wie de hoorders zijn en in welke werkelijkheid zij leven.

## 1. Demografische gegevens van {{plaatsnaam}}
- Bevolkingsomvang en -dichtheid
- Leeftijdsopbouw (vergrijzing, gezinnen, jongeren)
- Huishoudensamenstelling
- Opleidingsniveaus
- Herkomst en diversiteit

## 2. Economische situatie
- Belangrijkste sectoren en werkgevers
- Werkloosheidscijfers en inkomensniveaus
- Economische vooruitzichten of problemen
- Recente bedrijfssluitingen of -openingen

## 3. Sociale structuur
- Verenigingsleven en sociale cohesie
- Voorzieningen (scholen, zorg, winkels)
- Krimp of groei van voorzieningen
- Woningmarkt en woonsituatie

## 4. Recente lokale gebeurtenissen
- Lokaal nieuws van de afgelopen maanden
- Ingrijpende gebeurtenissen (ongelukken, rampen, successen)
- Politieke ontwikkelingen
- Veranderingen in sociale veiligheid

## 5. Kerkelijke context
- Kerkelijke kaart van de regio (welke denominaties)
- Geschiedenis en positie van {{gemeente}}
- Recente ontwikkelingen in kerkelijk leven
- Verhouding tot andere kerken

## Bronnen
Gebruik CBS, AlleCijfers.nl en lokale nieuwsbronnen. Wees specifiek voor {{plaatsnaam}}.

## JSON Output Schema

Retourneer UITSLUITEND een JSON object volgens onderstaand schema:

```json
{
  "demografisch": {
    "bevolkingsomvang": "number",
    "bevolkingsdichtheid": "string - bijv. 'X inwoners per km²'",
    "leeftijdsopbouw": {
      "jongeren_0_18": "string - percentage of aantal",
      "werkenden_18_65": "string",
      "ouderen_65_plus": "string",
      "vergrijzingsgraad": "string",
      "toelichting": "string"
    },
    "huishoudens": {
      "eenpersoonshuishoudens": "string",
      "gezinnen_met_kinderen": "string",
      "samenstelling_toelichting": "string"
    },
    "opleidingsniveaus": {
      "laag": "string",
      "midden": "string",
      "hoog": "string",
      "vergelijking_landelijk": "string"
    },
    "herkomst_diversiteit": {
      "westers": "string",
      "niet_westers": "string",
      "grootste_groepen": ["string"],
      "toelichting": "string"
    }
  },
  "economisch": {
    "belangrijkste_sectoren": ["string"],
    "grote_werkgevers": ["string"],
    "werkloosheidspercentage": "string",
    "gemiddeld_inkomen": "string",
    "vergelijking_landelijk": "string",
    "economische_vooruitzichten": "string",
    "recente_ontwikkelingen": ["string - sluitingen, openingen, etc."]
  },
  "sociale_structuur": {
    "verenigingsleven": {
      "actief": "boolean",
      "belangrijke_verenigingen": ["string"],
      "toelichting": "string"
    },
    "sociale_cohesie": "string - beschrijving van gemeenschapsgevoel",
    "voorzieningen": {
      "scholen": ["string"],
      "zorg": ["string"],
      "winkels": "string - niveau voorzieningenniveau",
      "krimp_of_groei": "string"
    },
    "woningmarkt": {
      "type_woningen": "string",
      "prijsniveau": "string",
      "beschikbaarheid": "string"
    }
  },
  "recente_gebeurtenissen": [
    {
      "datum": "string - maand/jaar",
      "gebeurtenis": "string",
      "type": "string - ongeluk|politiek|economisch|sociaal|succes|anders",
      "impact": "string"
    }
  ],
  "kerkelijke_context": {
    "denominaties_aanwezig": [
      {
        "naam": "string",
        "type": "string - PKN|RKK|Evangelisch|Gereformeerd Vrijgemaakt|Anders",
        "geschatte_omvang": "string|null"
      }
    ],
    "positie_gemeente": {
      "naam": "string - {{gemeente}}",
      "type": "string - wijkgemeente|zelfstandige gemeente|etc.",
      "geschatte_leden": "string|null",
      "karakter": "string - beschrijving traditie/kleur"
    },
    "recente_kerkelijke_ontwikkelingen": ["string"],
    "oecumenische_samenwerking": "string|null"
  },
  "bronnen_gebruikt": ["string - CBS, AlleCijfers, lokale kranten, etc."]
}
```

**BELANGRIJK:** Retourneer ALLEEN valide JSON, geen markdown of toelichting.
