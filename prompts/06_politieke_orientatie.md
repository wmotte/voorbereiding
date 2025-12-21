# Politieke Oriëntatie-analyse

Breng het politieke landschap en stemgedrag in kaart voor {{plaatsnaam}}.

## 0. Verkiezingsdata opzoeken (VERPLICHTE EERSTE STAP)

**Zoek EERST op wanneer de meest recente verkiezingen hebben plaatsgevonden.**
Let goed op de datum van de preek (`{{datum}}`). Als deze datum in de toekomst ligt (bijv. eind 2026), controleer dan of er in de tussenliggende periode (2024, 2025) verkiezingen zijn geweest (bijv. **Europees Parlement juni 2024** of vervroegde **Tweede Kamerverkiezingen in 2025**).

Zoek expliciet naar:
- **Tweede Kamerverkiezingen**: Meest recente verkiezingen waren in november 2025. (Zoek op "Tweede Kamerverkiezingen uitslag [jaartal van preek]" en "[jaartal van preek - 1]")
- **Europees Parlementsverkiezingen**: Meest recente (bijv. juni 2024). Dit geeft vaak een recenter beeld dan TK2023.
- **Provinciale Statenverkiezingen**: Wanneer waren de laatste?
- **Gemeenteraadsverkiezingen**: Wanneer waren de laatste in {{plaatsnaam}}?
- **Waterschapsverkiezingen**: Wanneer waren de laatste?

**Let op bij simulatie/toekomst:**
Als de preekdatum (`{{datum}}`) suggereert dat er verkiezingen zijn geweest (bijv. mrt 2026) waarvan nog geen *echte* uitslagen op internet staan (omdat het in werkelijkheid nog geen mrt 2026 is), vermeld dan:
1. Dat de verkiezingen volgens de tijdlijn net zijn geweest.
2. Wat de verwachting/peiling was of de context (bijv. val kabinet).
3. Gebruik de *Europees Parlementsverkiezingen (2024)* als meest recente *harde* data-indicator.

## 1. Landelijk stemgedrag

Analyseer de uitslagen van de meest recente Tweede Kamerverkiezingen in {{plaatsnaam}}:
- **Datum van deze verkiezingen** (expliciet vermelden!)
- *Check:* Zijn dit de verkiezingen van nov 2025 of recenter (2026)?
- Welke partijen behaalden de meeste stemmen?
- Hoe verhoudt dit zich tot het landelijk gemiddelde?
- Welke verschuivingen zijn er t.o.v. eerdere verkiezingen?

## 2. Europees stemgedrag (Recent & Relevant)

Bekijk de uitslagen van de meest recente Europees Parlementsverkiezingen (bijv. 2024) in {{plaatsnaam}}:
- **Datum:** (meestal juni 2024)
- Geeft dit een andere trend weer dan de TK-verkiezingen? (bijv. opkomst radicaal rechts of juist pro-Europees)
- Dit is vaak de meest actuele graadmeter voor de politieke stemming.

## 3. Provinciaal stemgedrag

Bekijk de meest recente Provinciale Statenverkiezingen:
- **Datum van deze verkiezingen** (expliciet vermelden)
- Dominante partijen in de provincie
- Regionale partijen of bewegingen
- Verschil tussen stad en platteland in de regio

## 4. Gemeentelijk stemgedrag

Analyseer de meest recente gemeenteraadsverkiezingen:
- **Datum van deze verkiezingen** (expliciet vermelden)
- Lokale partijen en hun positie
- Coalitiesamenstelling in de gemeente
- Belangrijke lokale politieke thema's
- Politieke stabiliteit of turbulentie

## 5. Waterschapsverkiezingen

Indien relevant:
- **Datum van deze verkiezingen** (expliciet vermelden)
- Betrokkenheid bij waterschapsverkiezingen
- Dominante stromingen

## 6. Politieke cultuur

Beschrijf de bredere politieke cultuur in {{plaatsnaam}}:
- Progressief versus conservatief
- Individualistisch versus gemeenschapsgeoriënteerd
- Openheid voor verandering versus behoudendheid
- Vertrouwen in overheid en instituties
- Proteststemmen of anti-establishment sentiment

## 7. Spanningsvelden

Welke politieke onderwerpen zorgen voor verdeeldheid?
- Lokale kwesties (bouwprojecten, windmolens, asielopvang)
- Nationale thema's die lokaal resoneren
- Hoe uit zich dit in het dagelijks leven?

## 8. Relevantie voor de prediking

Reflecteer kort op wat dit betekent voor de gemeente {{gemeente}}:
- Hoe verhouden kerkelijke standpunten zich tot lokale politieke voorkeuren?
- Welke gevoeligheden zijn er?
- Waar kan de preek aansluiten of juist spanning oproepen?

## Bronnen

Gebruik verkiezingsuitslagen van kiesraad.nl, gemeente.nl en lokale nieuwsmedia. Wees concreet en feitelijk over {{plaatsnaam}}.

## JSON Output Schema

Retourneer UITSLUITEND een JSON object volgens onderstaand schema:

```json
{
  "verkiezingsdata": {
    "tweede_kamer": {
      "meest_recente_datum": "string - bijv. 'november 2023'",
      "is_actueel": "boolean - zijn er recentere verkiezingen?",
      "opmerking": "string|null"
    },
    "europees_parlement": {
      "datum": "string",
      "opmerking": "string|null"
    },
    "provinciale_staten": {
      "datum": "string"
    },
    "gemeenteraad": {
      "datum": "string"
    },
    "waterschap": {
      "datum": "string|null"
    }
  },
  "landelijk_stemgedrag": {
    "verkiezingsdatum": "string",
    "top_partijen": [
      {
        "partij": "string",
        "percentage_lokaal": "number",
        "percentage_landelijk": "number",
        "verschil": "string"
      }
    ],
    "verschuivingen": ["string - t.o.v. vorige verkiezingen"],
    "opkomst": "string",
    "analyse": "string"
  },
  "europees_stemgedrag": {
    "verkiezingsdatum": "string",
    "top_partijen": [
      {
        "partij": "string",
        "percentage_lokaal": "number"
      }
    ],
    "trend_tov_tk": "string - wijkt dit af van TK-stemgedrag?"
  },
  "provinciaal_stemgedrag": {
    "verkiezingsdatum": "string",
    "dominante_partijen": ["string"],
    "regionale_partijen": ["string"],
    "stad_platteland_verschil": "string|null"
  },
  "gemeentelijk_stemgedrag": {
    "verkiezingsdatum": "string",
    "lokale_partijen": [
      {
        "naam": "string",
        "positie": "string - coalitie|oppositie",
        "zetels": "number|null"
      }
    ],
    "coalitie": ["string - partijen in coalitie"],
    "belangrijke_themas": ["string"],
    "politieke_stabiliteit": "string"
  },
  "waterschap": {
    "verkiezingsdatum": "string|null",
    "betrokkenheid": "string",
    "dominante_stromingen": ["string"]
  },
  "politieke_cultuur": {
    "progressief_conservatief": "string - schaal of beschrijving",
    "individualistisch_gemeenschaps": "string",
    "veranderingsgezind_behoudend": "string",
    "vertrouwen_overheid": "string - hoog|gemiddeld|laag",
    "anti_establishment": "string - mate van proteststemmen"
  },
  "spanningsvelden": [
    {
      "onderwerp": "string - bijv. 'asielopvang', 'windmolens'",
      "type": "string - lokaal|nationaal",
      "standpunten": "string - beschrijving van de verdeeldheid",
      "uiting_dagelijks_leven": "string"
    }
  ],
  "relevantie_prediking": {
    "verhouding_kerk_politiek": "string - hoe verhouden kerkelijke standpunten zich tot lokale voorkeuren?",
    "gevoeligheden": ["string - waar op letten?"],
    "aansluiting_mogelijkheden": ["string - waar kan de preek aansluiten?"],
    "spanning_mogelijkheden": ["string - waar kan de preek spanning oproepen?"]
  }
}
```

**BELANGRIJK:** Retourneer ALLEEN valide JSON, geen markdown of toelichting.
