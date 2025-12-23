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

**BELANGRIJK: Voorkom Hallucinaties**
Bij het noemen van specifieke namen van scholen, verenigingen, bedrijven of instellingen:
1. **Verifieer** of deze daadwerkelijk bestaan in {{plaatsnaam}} via Google Search.
2. Als je geen specifieke naam kunt vinden, gebruik dan een algemene omschrijving (bijv. "diverse basisscholen", "lokale voetbalvereniging") in plaats van een naam te verzinnen.
3. Het is beter om "niet specifiek gevonden" te rapporteren dan een foutieve naam.

**SPECIFIEK VOOR KERKELIJKE GEGEVENS (WEES UITERST VOORZICHTIG):**
1. **Verifieer** alle genoemde kerken, gemeenten en denominaties via officiële kerkelijke websites (bijv. pkn.nl, kerkzoeker.nl), kerkelijke jaarboeken of lokale bronnen.
2. **Kwaliteit boven kwantiteit:** Bij de minste twijfel: vermeld de informatie NIET. Het is cruciaal om foutieve of "half-ware" informatie te vermijden. Geen informatie is beter dan foutieve informatie.
3. **Maak scherp onderscheid** tussen een specifieke lokale *wijkgemeente* (bijv. "Hervormde Wijkgemeente Dorpskerk") en de overkoepelende *denominatie* (bijv. de "Protestantse Kerk in Nederland (PKN)"). Noem een wijkgemeente nooit bij de naam van de landelijke kerk alleen.
4. **Denominaties:** Noem alleen denominaties waarvan het bestaan in {{plaatsnaam}} onomstotelijk is vastgesteld. Verzin geen namen en gebruik geen verouderde termen (zoals "Hervormde Kerk" als men tegenwoordig PKN bedoelt, tenzij het een specifieke Hersteld Hervormde Gemeente betreft).
5. **Positie van {{gemeente}}:** Stel vast of {{gemeente}} een zelfstandige gemeente is, een wijkgemeente binnen een groter geheel, of een samenwerkingsgemeente. Wees hierin accuraat.
6. Als je een kerkgebouw vindt, verifieer dan welke gemeente daar daadwerkelijk kerkt voordat je een denominatie toekent.

**SPECIFIEK VOOR ANDERE INSTELLINGEN EN ORGANISATIES:**
1. **Verifieer** namen van scholen, bedrijven, verenigingen, zorginstellingen en winkelcentra via officiële websites of betrouwbare lokale bronnen.
2. Gebruik alleen specifieke namen als je deze kunt bevestigen in {{plaatsnaam}}.
3. Vermijd het noemen van bekende namen die waarschijnlijk elders gevestigd zijn (bijv. Albert Heijn, Jumbo, etc.) tenzij je zeker weet dat ze daadwerkelijk in {{plaatsnaam}} aanwezig zijn.
4. Geef voorzichtigheid bij het noemen van recente gebeurtenissen - verifieer data en details via lokale nieuwsbronnen.
5. Als je geen betrouwbare informatie kunt vinden, gebruik dan algemene termen i.p.v. specifieke namen.

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
      "nederlandse_achtergrond": "string - percentage zonder migratieachtergrond",
      "migratieachtergrond": {
        "totaal": "string - percentage met migratieachtergrond",
        "westers": "string - percentage met westerse migratieachtergrond (excl. Nederland)",
        "niet_westers": "string - percentage met niet-westerse migratieachtergrond"
      },
      "grootste_groepen": ["string"],
      "toelichting": "string"
    }
  },
  "economisch": {
    "belangrijkste_sectoren": ["string"],
    "grote_werkgevers": ["string - ALLEEN geverifieerde, bestaande bedrijven"],
    "werkloosheidspercentage": "string",
    "gemiddeld_inkomen": "string",
    "vergelijking_landelijk": "string",
    "economische_vooruitzichten": "string",
    "recente_ontwikkelingen": ["string - sluitingen, openingen, etc."]
  },
  "sociale_structuur": {
    "verenigingsleven": {
      "actief": "boolean",
      "belangrijke_verenigingen": ["string - ALLEEN geverifieerde namen van sport/cultuur verenigingen"],
      "toelichting": "string"
    },
    "sociale_cohesie": "string - beschrijving van gemeenschapsgevoel",
    "voorzieningen": {
      "scholen": ["string - ALLEEN geverifieerde namen"],
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
        "naam": "string - Volledige, geverifieerde naam van de lokale gemeente",
        "type": "string - PKN|RKK|Evangelisch|NGK|HHK|CGK|Gereformeerde Gemeenten|Anders",
        "geschatte_omvang": "string|null - Alleen invullen bij betrouwbare bron"
      }
    ],
    "positie_gemeente": {
      "naam": "string - {{gemeente}}",
      "type": "string - bijv. 'Hervormde wijkgemeente van bijzondere aard', 'Gereformeerde Kerk', etc.",
      "geschatte_leden": "string|null",
      "karakter": "string - Traditie (bijv. confessioneel, gereformeerde bond, evangelisch, open)"
    },
    "recente_kerkelijke_ontwikkelingen": ["string - Alleen feitelijke, geverifieerde gebeurtenissen"],
    "oecumenische_samenwerking": "string|null"
  },
  "bronnen_gebruikt": ["string - CBS, AlleCijfers, lokale kranten, etc."]
}
```

**BELANGRIJK:** Retourneer ALLEEN valide JSON, geen markdown of toelichting.
