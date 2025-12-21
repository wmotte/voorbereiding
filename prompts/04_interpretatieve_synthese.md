# Interpretatieve Synthese

Integreer de contextanalyse tot concrete homiletische adviezen voor de predikant.

## 1. Congruentie-analyse
- Wat zegt men in {{gemeente}} officieel te geloven versus hoe leeft men?
- Waar zijn spanningen tussen norm en praktijk?
- Welke onbewuste aannames leven er?

## 2. Verbindingspunten
- Waar kan de preek aansluiten bij geleefde ervaring?
- Welke beelden en metaforen zullen resoneren in {{plaatsnaam}}?
- Welke verhalen uit de gemeenschap kunnen bruggen slaan?

## 3. Confrontatiepunten
- Waar zou de bijbeltekst kunnen confronteren?
- Welke profetische kritiek zou relevant zijn?
- Waar zijn blinde vlekken?

## 4. De werkelijke versus veronderstelde hoorder
- Welke aannames moet de predikant loslaten?
- Welke diversiteit is er binnen de gemeente?
- Wie zijn de "onzichtbare" hoorders?

## 5. Specifiek voor {{datum}}
- Seizoen: welke associaties?
- Wat zou men verwachten te horen?
- Welke actualiteit speelt mee?

## 6. Concrete Homiletische Aanbevelingen

**Toon:** Welke toon past bij deze gemeente en dit moment?

**Taal:** Welke geloofstaal is toegankelijk? Waar moet worden uitgelegd?

**Beelden:** Welke beelden en metaforen zullen werken?

**Balans:** Verhouding pastoraal/profetisch, troost/vermaning

**Waarschuwingen:** Welke "heilige huisjes" kunnen ter sprake komen? Waar liggen gevoeligheden?

## 7. Implicaties voor de preek

Sluit af met een samenvattende sectie "Implicaties voor de preek" waarin je de belangrijkste inzichten uit alle voorgaande analyses bundelt tot concrete, praktische handvatten voor de predikant.

**BELANGRIJK:** Vermijd clichématige afsluitingen of samenvattende zinnen die de waarde van dit overzicht voor de predikant benadrukken.

## JSON Output Schema

Retourneer UITSLUITEND een JSON object volgens onderstaand schema:

```json
{
  "congruentie_analyse": {
    "officiele_geloofsopvatting": "string - wat zegt men te geloven?",
    "geleefde_praktijk": "string - hoe leeft men werkelijk?",
    "spanningen_norm_praktijk": ["string - waar wringen norm en praktijk?"],
    "onbewuste_aannames": ["string - wat neemt men stilzwijgend aan?"]
  },
  "verbindingspunten": {
    "aansluiting_geleefde_ervaring": ["string - waar kan de preek bij aansluiten?"],
    "resonerende_beelden": [
      {
        "beeld": "string",
        "waarom_resoneert": "string",
        "bijbelse_parallel": "string|null"
      }
    ],
    "brugverhalen": ["string - verhalen uit de gemeenschap die bruggen slaan"]
  },
  "confrontatiepunten": {
    "bijbeltekst_confronteert": ["string - waar zou de tekst kunnen confronteren?"],
    "profetische_kritiek": ["string - welke kritiek is relevant?"],
    "blinde_vlekken": ["string - waar kijkt men niet naar?"]
  },
  "hoordersanalyse": {
    "los_te_laten_aannames": ["string - aannames die de predikant moet loslaten"],
    "diversiteit_binnen_gemeente": ["string - beschrijving van verschillende groepen"],
    "onzichtbare_hoorders": ["string - wie zijn er maar worden niet gezien?"]
  },
  "specifiek_voor_datum": {
    "seizoens_associaties": ["string"],
    "verwachting_hoorders": "string - wat zou men verwachten te horen?",
    "actualiteit": ["string - welke actualiteit speelt mee?"]
  },
  "homiletische_aanbevelingen": {
    "toon": {
      "aanbevolen": "string - welke toon past?",
      "te_vermijden": "string"
    },
    "taal": {
      "toegankelijk": ["string - welke taal is toegankelijk?"],
      "uit_te_leggen": ["string - welke begrippen moeten uitgelegd worden?"]
    },
    "beelden": {
      "werkend": ["string - beelden en metaforen die werken"],
      "niet_werkend": ["string - beelden om te vermijden"]
    },
    "balans": {
      "pastoraal_profetisch": "string - aanbevolen verhouding",
      "troost_vermaning": "string - aanbevolen verhouding"
    },
    "waarschuwingen": [
      {
        "onderwerp": "string - heilig huisje of gevoeligheid",
        "risico": "string",
        "advies": "string"
      }
    ]
  },
  "kernimplicaties_preek": [
    "string - max 5 kernpunten voor de predikant"
  ]
}
```

**BELANGRIJK:** Retourneer ALLEEN valide JSON, geen markdown of toelichting.
