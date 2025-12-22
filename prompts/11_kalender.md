# Kalender: Gedenkdagen en Bijzondere Momenten

Maak een overzicht van alle relevante kalendergegevens voor de week die begint op {{datum}} en zich uitstrekt tot en met 6 dagen later.

## Context

De datum van de preek is {{datum}}. De gemeente is {{gemeente}} in {{plaatsnaam}}.

## Te onderzoeken en rapporteren

### 1. Kerkelijke gedenkdagen en heiligen

- **Heiligenkalender:** Welke heiligen worden deze week herdacht? Geef korte biografische informatie.

- **Protestantse gedenkdagen:** Relevante herdenkingen in de protestantse traditie (Reformatiedag, etc.)

- **Oecumenische gedenkdagen:** Wereldgebedsdag, Week van Gebed voor Eenheid, etc.

- **Martelaren en getuigen:** Moderne martelaren of geloofsgetuigen die deze week herdacht worden

### 2. Joodse kalender

- **Joodse feestdagen:** Valt er een Joods feest in deze periode? (Pesach, Soekkot, Jom Kippoer, Chanoeka, Rosj Hasjana, Sjawoeot, Poerim, etc.)

- **Sabbat en parasja:** Welke Tora-portie wordt gelezen in de synagoge?

- **Joodse gedenkdagen:** Jom HaSjoa, Jom Ha'atsmaoet, etc.

### 3. Internationale en VN-dagen

Welke internationale dagen vallen in deze week? Voorbeelden:

- Internationale Dag van de Leraar

- Wereldvoedseldag

- Internationale Dag van de Vrede

- Werelddag tegen Kinderarbeid

- Internationale Vrouwendag

- Wereldwaterdag

- Dag van de Mensenrechten

### 4. Nationale feest- en gedenkdagen (Nederland en België)

- **Nederlandse feestdagen:** Koningsdag, Bevrijdingsdag, Dodenherdenking, Prinsjesdag, etc.

- **Belgische feestdagen:** Nationale feestdag, Wapenstilstand, etc.

- **Regionale gedenkdagen:** Relevante lokale herdenkingen

### 5. Seizoensgebonden en culturele momenten

- **Schoolvakanties:** Welke regio's hebben vakantie? (Herfstvakantie, Kerstvakantie, Voorjaarsvakantie, Meivakantie, Zomervakantie)

- **Carnaval:** Indien relevant voor de periode

- **Sinterklaas:** Intocht en pakjesavond

- **Moederdag/Vaderdag:** Indien in deze periode

- **Seizoenswisselingen:** Eerste lentedag, langste dag, herfst-equinox, etc.

### 6. Astronomische gebeurtenissen (alleen bij zondag)

- **Maanfasen:** Nieuwe maan, volle maan

- **Zons- en maansverduisteringen:** Indien relevant

- **Bijzondere sterrenkundige gebeurtenissen:** Meteorenzwermen, planetaire conjuncties

- **Zonsopgang en zonsondergang:** Tijden voor de betreffende zondag

### 7. Weersverwachting (alleen bij zondag)

Geef een korte weersverwachting voor de komende week:

- Temperatuur (dag/nacht)

- Neerslag

- Wind

- Bijzonderheden (eerste vorst, hittegolf, storm)

*Let op: als de preekdatum meer dan 7 dagen in de toekomst ligt, vermeld dan: "Weersverwachting nog niet beschikbaar (huidige datum: [datum])."*

### 8. Overige relevante momenten

- **Sportevenementen:** WK, EK, Olympische Spelen, Tour de France, etc.

- **Culturele evenementen:** Boekenweek, Week van de Smaak, Open Monumentendag, etc.

- **Historische herdenkingen:** Belangrijke historische gebeurtenissen op deze datum

- **Actuele maatschappelijke campagnes:** Alzheimerweek, Werelddierendag, etc.

- **Lokale evenementen:** Kermis, jaarmarkt, stadfeest in {{plaatsnaam}}

## Gewenste output

Lever een overzichtelijke kalender die:

1. **Chronologisch geordend** is per dag van de week

2. Per dag de relevante **gedenkdagen en momenten** noemt

3. Bij elk item een **korte toelichting** geeft

**BELANGRIJK:** Toon ALLEEN wat relevant is:

- Geen "Geen bijzonderheden" of "Geen specifieke feestdag" vermelden

- Kopjes waar niets te melden valt, WEGLATEN

- Als een dag geen bijzonderheden heeft, die dag WEGLATEN

- Alleen concrete, feitelijke informatie opnemen

- **Weer** en **Astronomie** alleen bij de eerste dag (zondag) vermelden

## Bronnen

Gebruik betrouwbare bronnen zoals:

- heiligen.net (heiligenkalender)

- chabad.org (Joodse kalender)

- un.org/observances (VN-dagen)

- rijksoverheid.nl (Nederlandse feestdagen en vakanties)

- knmi.nl (weer)

- timeanddate.com (astronomie)

## Markdown formatting

**BELANGRIJK:** Zorg voor correcte markdown formatting:

- Plaats ALTIJD een lege regel VOOR en NA elke kop (##, ###)

- Plaats ALTIJD een lege regel VOOR een lijst met bullet points

- Plaats ALTIJD een lege regel tussen verschillende secties

- Elke bullet point moet op een eigen regel staan

## Voorbeeld format

```markdown
### Zondag 4 januari 2026 (preken op deze datum)

**Kerkelijk:**

- Epifanie - Openbaring van de Heer

- Gedachtenis H. Hendrikka van Delft (vrouwenheilige, mystica, †1260)

**Joods:**

- 15 Tevet 5786 - Fast of the Tenth of Tevet

**Weer:**

- Overwegend bewolkt, 4°C, kans op lichte sneeuw

**Astronomie:**

- Zonsopgang 08:32, zonsondergang 16:35

---

### Maandag 5 januari 2026

**Kerkelijk:**

- Ochtend na Epifanie - de Heer openbaart zich aan de wereld

**Joods:**

- 16 Tevet 5786

---

### Dinsdag 6 januari 2026

**Kerkelijk:**

- Heilig Drie-eenheid (in sommige kerken)

**Internationaal:**

- Internationale Dag van de Gezondheidswaakhond
```

Toon alleen dagen waarop iets te melden valt.

**BELANGRIJK:** Vermijd clichématige afsluitingen. Stop bij de inhoud.

## JSON Output Schema

Retourneer UITSLUITEND een JSON object volgens onderstaand schema:

```json
{
  "week_van": "string - bijv. '4-9 januari 2026'",
  "dagen": [
    {
      "datum": "string - bijv. 'Zondag 4 januari 2026'",
      "dag": "string - zondag|maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag",
      "is_preekzondag": "boolean",
      "kerkelijk": [
        {
          "naam": "string - bijv. '3e Advent (Gaudete)'",
          "type": "string - zondag|heilige|martelaar|herdenking",
          "toelichting": "string|null"
        }
      ],
      "joods": {
        "hebreeuwse_datum": "string|null - bijv. '16 Kislev 5785'",
        "feestdag": "string|null",
        "parasja": "string|null - welke Tora-portie?",
        "toelichting": "string|null"
      },
      "internationaal": [
        {
          "naam": "string - bijv. 'Internationale Theedag'",
          "organisatie": "string - VN|UNESCO|Anders",
          "relevantie": "string|null"
        }
      ],
      "nationaal": [
        {
          "naam": "string",
          "land": "string - NL|BE",
          "type": "string - feestdag|herdenking|traditie"
        }
      ],
      "vakantie": {
        "schoolvakantie": "string|null - bijv. 'Kerstvakantie Noord'",
        "regio": "string|null"
      },
      "weer": {
        "verwachting": "string|null - alleen op zondag invullen",
        "temperatuur": "string|null",
        "neerslag": "string|null",
        "bijzonderheden": "string|null"
      },
      "astronomie": {
        "zonsopgang": "string|null - alleen op zondag",
        "zonsondergang": "string|null",
        "maanfase": "string|null",
        "bijzonderheden": "string|null"
      },
      "overig": [
        {
          "categorie": "string - sport|cultuur|historisch|maatschappelijk|lokaal",
          "naam": "string",
          "toelichting": "string|null"
        }
      ]
    }
  ],
  "aandachtspunten_predikant": [
    "string - relevante momenten om te noemen of rekening mee te houden"
  ]
}
```

**BELANGRIJK:**
- Retourneer ALLEEN valide JSON, geen markdown of toelichting.
- Laat lege arrays `[]` of `null` voor dagen/categorieën zonder inhoud.
- Weer en astronomie ALLEEN op de zondag.
