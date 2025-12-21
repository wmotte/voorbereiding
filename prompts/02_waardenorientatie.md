# Waardenoriëntatie-analyse

Begrijp wat de hoorders belangrijk vinden en waar ze zich druk om maken.

## 1. De Vijf V's voor {{plaatsnaam}}

**Visioenen** - Welke toekomstbeelden leven in deze gemeenschap? Waar werkt men naartoe? Welke collectieve dromen zijn er?

**Verlangens** - Waar hunkert deze gemeenschap naar? Wat mist men? Welke behoeften zijn onvervuld?

**Vreugden** - Waar is men trots op? Wat viert men? Welke tradities worden gekoesterd?

**Verdriet** - Welke collectieve pijn is er? Wat is verloren gegaan? Welke zorgen leven er?

**Vragen** - Welke existentiële vragen spelen? Waar zoekt men antwoorden op? Welke onzekerheden zijn er?

## 2. Trendanalyse

### Mesotrends (5-15 jaar) die hier spelen:
- Impact van digitalisering
- Flexibilisering van werk
- Veranderingen in gezinsvormen
- Migratie en diversiteit
- Klimaat en duurzaamheid
- Zorg en vergrijzing

### Microtrends (1-5 jaar) actueel voor {{datum}}:
- Huidige maatschappelijke discussies
- Lokale issues in {{plaatsnaam}}
- Seizoensgebonden thema's
- Actualiteit rond de preekdatum

## 3. Motivaction Mentality-model

Analyseer welke sociale milieus waarschijnlijk vertegenwoordigd zijn in {{gemeente}}:

| Groep | Kenmerken |
|-------|-----------|
| Traditionele burgerij | Behoudend, rust, veiligheid |
| Gemaksgeoriënteerden | Impulsief, genieten |
| Moderne burgerij | Conformistisch, statusgevoelig |
| Nieuwe conservatieven | Verantwoordelijk, maatschappelijke orde |
| Kosmopolieten | Succesgericht, internationaal |
| Postmaterialisten | Idealistisch, duurzaamheid |
| Postmoderne hedonisten | Vrijheid, authenticiteit |
| Opwaarts mobielen | Carrièregericht, competitief |

Welke taal en beelden resoneren bij welke groepen? Waar liggen spanningen?

## JSON Output Schema

Retourneer UITSLUITEND een JSON object volgens onderstaand schema:

```json
{
  "vijf_vs": {
    "visioenen": {
      "beschrijving": "string - welke toekomstbeelden leven in deze gemeenschap?",
      "concrete_voorbeelden": ["string"],
      "collectieve_dromen": ["string"]
    },
    "verlangens": {
      "beschrijving": "string - waar hunkert deze gemeenschap naar?",
      "onvervulde_behoeften": ["string"],
      "concrete_voorbeelden": ["string"]
    },
    "vreugden": {
      "beschrijving": "string - waar is men trots op?",
      "tradities": ["string"],
      "vieringen": ["string"]
    },
    "verdriet": {
      "beschrijving": "string - welke collectieve pijn is er?",
      "verloren_gegaan": ["string"],
      "zorgen": ["string"]
    },
    "vragen": {
      "beschrijving": "string - welke existentiële vragen spelen?",
      "onzekerheden": ["string"],
      "zoektochten": ["string"]
    }
  },
  "trendanalyse": {
    "mesotrends_5_15_jaar": [
      {
        "trend": "string - bijv. 'digitalisering'",
        "impact_lokaal": "string - hoe speelt dit in {{plaatsnaam}}",
        "relevantie_preek": "string"
      }
    ],
    "microtrends_1_5_jaar": [
      {
        "trend": "string",
        "actueel_voor_datum": "string - specifiek voor {{datum}}",
        "lokale_uitwerking": "string"
      }
    ]
  },
  "motivaction_milieus": {
    "waarschijnlijk_aanwezig": [
      {
        "milieu": "string - Traditionele burgerij|Gemaksgeoriënteerden|Moderne burgerij|Nieuwe conservatieven|Kosmopolieten|Postmaterialisten|Postmoderne hedonisten|Opwaarts mobielen",
        "geschat_percentage": "string|null",
        "kenmerken_lokaal": "string",
        "taal_die_resoneert": ["string"],
        "beelden_die_werken": ["string"]
      }
    ],
    "spanningen_tussen_groepen": [
      {
        "groep_a": "string",
        "groep_b": "string",
        "spanningsveld": "string",
        "implicatie_preek": "string"
      }
    ]
  },
  "homiletische_implicaties": {
    "aanbevolen_taalveld": "string - welk taalregister werkt hier?",
    "te_vermijden": ["string - woorden/beelden die niet landen"],
    "kansrijke_beelden": ["string - metaforen die zullen resoneren"]
  }
}
```

**BELANGRIJK:** Retourneer ALLEEN valide JSON, geen markdown of toelichting.
