# Geloofsoriëntatie-analyse

Begrijp hoe hoorders geloofsmatig in het leven staan en of zij "God-talk" hebben.

## 1. Zes Ervaringsgebieden

### Schepping en het goede leven
- Hoe beleeft men natuur en seizoenen in {{plaatsnaam}}?
- Welke feesten en vieringen zijn er?
- Hoe uit zich dankbaarheid?

### Eindigheid en zingeving
- Hoe gaat men om met vergankelijkheid?
- Welke rituelen rond sterven zijn er?
- Hoe spreekt men over de dood?

### Menselijk tekort
- Hoe gaat men om met falen en schuld?
- Welke taboes zijn er?
- Hoe wordt vergeving beleefd?

### Lijden en het kwaad
- Recente ervaringen met lijden in de gemeenschap?
- Hoe duidt men onrecht en kwaad?
- Welke theodicee-vragen leven er?

### Wijsheid der volken
- Welke andere religieuze of levensbeschouwelijke stromingen zijn aanwezig?
- Hoe zijn de interreligieuze verhoudingen?
- Welke "spirituele markt" is er?

### Humaniteit en gemeenschap
- Hoe uit zich solidariteit?
- Welke vormen van naastenliefde zijn er?
- Hoe sterk is het gemeenschapsgevoel?

## 2. Geloofstaal-analyse

- In hoeverre is christelijke geloofstaal nog gangbaar in {{plaatsnaam}}?
- Welke woorden/concepten zijn versleten of onbekend?
- Welke "seculiere" taal wordt gebruikt voor religieuze ervaringen?
- Hoe is de vertrouwdheid met liturgie en kerkelijke rituelen?

## 3. Spirituele trends in de regio

Zoek naar informatie over:
- Kerkbezoek en kerkverlating
- Nieuwe vormen van spiritualiteit
- Pioniersplekken of kliederkerken
- Oecumenische initiatieven

## JSON Output Schema

Retourneer UITSLUITEND een JSON object volgens onderstaand schema:

```json
{
  "ervaringsgebieden": {
    "schepping_goede_leven": {
      "natuurbeleving": "string - hoe beleeft men natuur en seizoenen?",
      "feesten_vieringen": ["string"],
      "uitingen_dankbaarheid": "string"
    },
    "eindigheid_zingeving": {
      "omgang_vergankelijkheid": "string",
      "rituelen_sterven": ["string"],
      "taal_over_dood": "string - hoe spreekt men over de dood?"
    },
    "menselijk_tekort": {
      "omgang_falen_schuld": "string",
      "taboes": ["string"],
      "beleving_vergeving": "string"
    },
    "lijden_kwaad": {
      "recente_ervaringen": ["string - concrete voorbeelden van lijden in de gemeenschap"],
      "duiding_onrecht": "string - hoe duidt men onrecht en kwaad?",
      "theodicee_vragen": ["string - welke waarom-vragen leven er?"]
    },
    "wijsheid_volken": {
      "andere_stromingen": ["string - welke religies/levensbeschouwingen zijn aanwezig?"],
      "interreligieuze_verhoudingen": "string",
      "spirituele_markt": "string - yoga, mindfulness, new age, etc."
    },
    "humaniteit_gemeenschap": {
      "uitingen_solidariteit": ["string"],
      "vormen_naastenliefde": ["string"],
      "gemeenschapsgevoel": "string - hoe sterk is het?"
    }
  },
  "geloofstaal_analyse": {
    "gangbaarheid_christelijke_taal": "string - in hoeverre is geloofstaal nog gangbaar?",
    "versleten_woorden": ["string - begrippen die niet meer begrepen worden"],
    "onbekende_concepten": ["string - theologische termen die uitleg nodig hebben"],
    "seculiere_equivalenten": [
      {
        "religieus_concept": "string - bijv. 'genade'",
        "seculiere_taal": "string - bijv. 'tweede kans'"
      }
    ],
    "vertrouwdheid_liturgie": "string - hoe bekend zijn mensen met kerkelijke rituelen?"
  },
  "spirituele_trends_regio": {
    "kerkbezoek": {
      "trend": "string - stijgend|dalend|stabiel",
      "percentage": "string|null",
      "toelichting": "string"
    },
    "kerkverlating": {
      "omvang": "string",
      "redenen": ["string"]
    },
    "nieuwe_vormen": [
      {
        "naam": "string - bijv. 'kliederkerken', 'pioniersplek'",
        "beschrijving": "string",
        "doelgroep": "string"
      }
    ],
    "oecumenische_initiatieven": ["string"]
  },
  "homiletische_implicaties": {
    "geloofstaal_advies": "string - welke taal wel/niet gebruiken?",
    "aanknopingspunten": ["string - waar kan de preek bij aansluiten?"],
    "te_vermijden_aannames": ["string - wat niet zomaar veronderstellen?"]
  }
}
```

**BELANGRIJK:** Retourneer ALLEEN valide JSON, geen markdown of toelichting.
