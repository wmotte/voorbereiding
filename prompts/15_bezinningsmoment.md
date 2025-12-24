# Moment van Bezinning (Bijzondere Diensten)

Creëer een **moment van bezinning** aangepast aan de doelgroep ({{dienst_type}}) dat past bij de lezingen en het thema van de dienst.

**DOEL:** Een kort moment (3-5 minuten) van reflectie, betrokkenheid of troost dat mensen helpt de boodschap te voelen en beleven, niet alleen te horen.
Genereer **vijf totaal verschillende** opties voor dit moment.

**DIT VERVANGT HET KINDERMOMENT** - Dit is bestemd voor volwassenen in bijzondere situaties (bijv. verpleeghuis, doven, verstandelijke beperking, ziekenhuis). Behandel hen met waardigheid; vermijd kinderachtig taalgebruik, maar zoek wel naar eenvoud en zintuiglijkheid.

## Instructies per optie
Elke optie moet een unieke invalshoek hebben, afgestemd op een volwassen belevingswereld met specifieke behoeften:

1.  **Optie 1: De Symbolische Verdieping:** Een rustig, klassiek moment rondom een sterk, herkenbaar symbool (geen 'lesje', maar een ervaring).
2.  **Optie 2: Het Gezamenlijke Gebaar:** Een interactief moment waarbij iedereen iets doet (kaars aansteken, hand opsteken, iets doorgeven). Focust op verbondenheid.
3.  **Optie 3: De Zintuiglijke Ervaring:** Een benadering die focust op zien, ruiken of voelen (bijv. geur van brood, voelen van een steen, visuele projectie). Cruciaal voor mensen met cognitieve of auditieve beperkingen.
4.  **Optie 4: De Muzikale/Poëtische Verstilling:** Een moment van rust, gedragen door muziek, stilte of een korte, krachtige tekst (gedicht/mantra).
5.  **Optie 5: Het Korte Verhaal:** Een narratieve benadering met een 'volwassen' metafoor of mini-verhaal dat direct raakt aan de levenservaring van de doelgroep (vroeger, werk, pijn, hoop).

## Algemene eisen
- **Object/Handeling:** Kies voor elk moment een *ander* concreet element.
- **Inclusiviteit & Sensitiviteit:** Voorkom vervreemding van mensen met een zintuiglijke beperking. Gebruik voor doven geen momenten die uitsluitend op geluid/muziek leunen. Gebruik voor blinden geen momenten die uitsluitend visueel zijn. Gebruik inclusieve werkwoorden: liever 'ervaren', 'voelen' of 'ontvangen' dan uitsluitend 'kijken' of 'luisteren'.
- **Focus:** Leg uit welk specifiek element uit de lezingen centraal staat.
- **Toon:** Respectvol, warm, niet betuttelend. Eenvoudig van taal, maar diep van inhoud.
- **Doelgroep:** Volwassenen (pas de nuance aan op basis van `{{dienst_type}}` indien bekend, anders algemeen toepasbaar voor zorg/bijzondere setting).

## Output Formaat
Geef de output **uitsluitend** in de volgende JSON structuur (dezelfde structuur als het kindermoment voor technische compatibiliteit, maar inhoudelijk anders).
**LET OP:** Gebruik de key `kindermoment_opties` zoals hieronder aangegeven, ook al is het geen kindermoment.

```json
{
  "kindermoment_opties": [
    {
      "type": "Symbolisch",
      "titel": "Titel van optie 1",
      "object": {
        "naam": "Naam van het symbool/voorwerp",
        "uitleg": "Waarom dit symbool?"
      },
      "focus_schriftlezing": "Link naar de Bijbeltekst",
      "verhaal_script": "Volledig uitgeschreven tekst/instructie met regie-aanwijzingen voor de voorganger.",
      "afbeelding_idee": "Beschrijving voor een beamer-plaatje of visuele ondersteuning"
    },
    {
      "type": "Interactief",
      "titel": "Titel van optie 2",
      "object": {
        "naam": "Naam van het voorwerp/handeling",
        "uitleg": "Waarom deze handeling?"
      },
      "focus_schriftlezing": "Link naar de Bijbeltekst",
      "verhaal_script": "Volledig uitgeschreven tekst/instructie met regie-aanwijzingen.",
      "afbeelding_idee": "Beschrijving voor visuele ondersteuning"
    },
    {
      "type": "Zintuiglijk",
      "titel": "Titel van optie 3",
      "object": {
        "naam": "Naam van het zintuiglijke object",
        "uitleg": "Waarom dit zintuig?"
      },
      "focus_schriftlezing": "Link naar de Bijbeltekst",
      "verhaal_script": "Volledig uitgeschreven tekst/instructie met regie-aanwijzingen.",
      "afbeelding_idee": "Beschrijving voor visuele ondersteuning"
    },
    {
      "type": "Verstillend",
      "titel": "Titel van optie 4",
      "object": {
        "naam": "Naam van focuspunt (muziek/stilte/tekst)",
        "uitleg": "Waarom deze vorm?"
      },
      "focus_schriftlezing": "Link naar de Bijbeltekst",
      "verhaal_script": "Volledig uitgeschreven tekst/instructie met regie-aanwijzingen.",
      "afbeelding_idee": "Beschrijving voor visuele ondersteuning"
    },
    {
      "type": "Verhalend",
      "titel": "Titel van optie 5",
      "object": {
        "naam": "Naam van de metafoor/object",
        "uitleg": "Waarom dit verhaal?"
      },
      "focus_schriftlezing": "Link naar de Bijbeltekst",
      "verhaal_script": "Volledig uitgeschreven tekst/instructie met regie-aanwijzingen.",
      "afbeelding_idee": "Beschrijving voor visuele ondersteuning"
    }
  ]
}
```