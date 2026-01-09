# Q&A voor kritische lezers

## Maar de Heilige Geest dan?

Een begrijpelijke vraag. Toch is het gebruik van voorbereidend materiaal in de gereformeerde traditie eerder regel dan uitzondering. Leespreekbundels worden al eeuwenlang gebruikt in gemeenten zonder predikant — voorgedrukte teksten die hardop worden voorgelezen. Postilles (preekschetsen voor het kerkelijk jaar) zijn een vast genre in de theologische literatuur. En de voorbeelden van Ryle, Spurgeon of Tim Keller worden wereldwijd als inspiratiebron gebruikt. Preken is een ambacht waarbij sterk geput wordt uit eerdere teksten, structuren en inzichten.

De Geest werkt niet alleen in het moment van spreken, maar ook in de voorbereiding, in het doordenken van de tekst, in het selecteren van wat wel en niet gezegd wordt. Die geestelijke arbeid blijft volledig bij de voorganger liggen — dit hulpmiddel vervangt dat niet, maar ondersteunt het.

## En wat kost dat niet aan energie?

Taalmodellen, waaronder Gemini, kosten inderdaad energie. Maar voor een eerlijke vergelijking is inzicht in de *controleconditie* essentieel: wat zou je anders doen en verbruiken?

Een uur YouTube-streaming kost meer aan cloud computing, datacenters en netwerktransport dan een uur gebruik van een gemiddeld taalmodel. De eenmalige energie voor het trainen van het model moet bovendien gedeeld worden door (honderd) miljoenen gebruikers post-training.

Daarnaast: een predikant die uren besteedt aan het doorzoeken van commentaren (op papier of digitaal) draagt ook bij aan zijn of haar ecologisch voetafdruk. Het opzoeken van liederen via zoekmachines als Google en het inlezen over de gemeente zijn geen energieneutrale acitiviteiten. Dit alles kost energie — eigen energie, maar ook die van verwarming, verlichting, apparatuur en digitale hulpmiddelen. De vraag is niet óf er energie wordt gebruikt, maar of die efficiënt wordt ingezet.

## Hoe zit het met plagiaat?

De generatieve opzet van de tool genereert alle output *de novo* — vanaf nul. Elke preekschets, elk gebed, elke formulering wordt ter plekke gegenereerd op basis van instructies over theologie, structuur en taalgebruik.

Ook waar gevraagd wordt om te schrijven "in de stijl van" een bepaalde theoloog, gaat het om stijlkenmerken, niet om het kopiëren van bestaande teksten. Geen enkele output is ooit eerder zo verschenen. Het is vergelijkbaar met een student die leert schrijven in academische stijl: de stijl is herkenbaar, maar de tekst is eigen.

## Wie kan dit gebruiken?

Op dit moment kan het systeem niet publiek worden aangeboden. Daar zijn twee redenen voor:

1. **Copyright**: De liedsuggesties worden geselecteerd uit bundels als Liedboek 2013, Hemelhoog en Weerklank — uitgaven met auteursrechtelijke bescherming.
2. **Privédatabase**: De exegetische validatie gebeurt met behulp van een database met theologische commentaren die niet vrij beschikbaar zijn.

De hoop is om een *provider* te vinden die de logistiek van gebruikersregistratie, licenties en toegangsbeheer voor zijn rekening neemt. Tot die tijd blijft het een prototype.

[Het homiletische feedbacksysteem - zie hieronder - is wel volledig te downloaden en zelfstandig te gebruiken.]

## Gebruikt u dit systeem zelf ook?

Nog niet. Alle gepresenteerde voorbeelden zijn hypothetisch (maar wel represenatief en 100% gegenereerd). Het systeem is pas eind december 2025 geïmplementeerd. Bovendien vragen de diensten in het dovenpastoraat om een andere insteek — meer visueel, met gebaren, en aangepast aan een specifieke doelgroep. Taalmodellen zijn overigens ook in te zetten voor gebarentaal. Zie: [Nederlands naar NmG](https://github.com/wmotte/nederlands_naar_gebaar).

Wel lopen er pilots met collega-predikanten die een aantal onderdelen testen: het kindermoment, de gebeden, de liedsuggesties. Hun feedback helpt om het systeem te verbeteren voordat het breder wordt ingezet.

## Dit voelt allemaal erg PKN aan...

Dat klopt. Het liturgisch rooster, de uitgeschreven gebeden, het Liedboek 2013, Weerklank, theologen als Noordmans, Fleming Rutledge en Walter Brueggemann — dit systeem is opgezet met PKN-diensten in het achterhoofd. Dat is geen toeval: het is de traditie waarin ik zelf werk en waarvan ik de liturgische en theologische 'grammatica' het beste ken.

Dat betekent niet dat de onderliggende techniek niet breder toepasbaar zou zijn. Met andere liedbundels, andere commentaren en andere theologische accenten zou een vergelijkbaar systeem kunnen werken in genootschappen waar zowel exegese als hoorderscontext serieus mogen meedoen tijdens de voorbereiding. Die implementatie vraagt om andere expertise dan de mijne.

## Maar taalmodellen hallucineren toch?

Dat klopt — en dat blijft altijd mogelijk. Taalmodellen kunnen informatie verzinnen die niet bestaat, of theologische verbanden leggen die er niet zijn. Daarom zijn er meerdere veiligheidsmaatregelen ingebouwd.

Ten eerste: de modellen opereren op een *lage temperatuur*. Dat betekent dat ze bij elke stap de meest waarschijnlijke, voorspelbare keuze maken in plaats van creatief te improviseren. Hoge temperatuur leidt tot variatie en verrassingen (handig bij creatief schrijven), lage temperatuur leidt tot stabiliteit en betrouwbaarheid (essentieel bij theologische output).

Ten tweede: meerdere onderdelen worden gegrond in externe bronnen. Exegetische validatie gebeurt met behulp van databases met theologische commentaren. Liedsuggesties worden geselecteerd uit bestaande bundels. En waar contextuele informatie nodig is — over een gemeente, een gebeurtenis, een seizoen — gebeurt dat via internetzoekopdrachten, niet via modelverbeelding.

Ten derde: ook zonder een hulpmiddel als deze is het altijd spannend of een voorganger de hoorders en de tekst recht doet. Elke preek draagt het risico van misinterpretatie, projectie of een verkeerde inschatting van wat de gemeente nodig heeft en de Schrift 'wil' zeggen. 'Hallucineren' — in de zin van iets zien dat er niet is — is niet voorbehouden aan taalmodellen. Het verschil is dat dit systeem dwingt tot explicitering van keuzes, zodat deze keuzes geëvalueerd en bijgesteld kunnen worden.

## Maar dit maakt je toch afhankelijk van (Amerikaanse) tech-bedrijven?

Dat is een reële zorg. Op dit moment draait het systeem op Gemini, een commercieel model van Google. Die keuze is pragmatisch: Gemini biedt een zeer grote contextwindow (twee miljoen tokens), wat nodig is om tijdens één sessie exegetische commentaren, gemeenteprofiel, liturgische opties en theologische instructies tegelijk mee te geven.

Maar de afhankelijkheid is niet absoluut. De open-source community zit de proprietary modellen op de hielen — modellen die lokaal draaien, geen data naar externe servers sturen, en volledig transparant zijn in hun werking. In principe is elk taalmodel met voldoende contextcapaciteit én grounding via search/database tools geschikt om dit systeem mee te laten functioneren. De architectuur is modulair opgezet: het onderliggende model is vervangbaar zonder dat de logica of output fundamenteel verandert.

Zodra open-source alternatieven technisch vergelijkbaar worden, is een overstap mogelijk. Tot die tijd blijft de keuze voor een commercieel model een afweging tussen wat nu werkbaar is en wat ideologisch wenselijk zou zijn.

## Begrijp ik goed dat deze tool in feite een aaneenschakeling is van tientallen specialistische taalmodellen (elk met een eigen context en prompt). Hoe 'weten' deze modellen van elkaars inzichten en output?

Ja, die beschrijving klopt. Het systeem bestaat uit meerdere gespecialiseerde taalmodellen — elk met een eigen taak, prompt en context. Er is een model voor exegetische analyse, een voor liedsuggesties, een voor gebeden, een voor de preekschets, een voor het kindermoment, enzovoort.

Niet alle modellen krijgen alle output te zien. Een deel is parallel geschakeld en werkt onafhankelijk. Het model dat liederen selecteert hoeft bijvoorbeeld niet te weten wat het model voor de voorbeden schrijft.

Maar een groot deel is sequentieel geschakeld: latere modellen krijgen de output van eerdere modellen als input. Het model dat de preekschets schrijft, krijgt de exegetische analyse, het gemeenteprofiel en de gekozen theologische focus mee. Het model dat de gebeden formuleert, krijgt de preekschets en de thema's van de dienst te zien. Zo ontstaat theologische consistentie: niet omdat één enkel model alles doet, maar omdat de keten van modellen telkens voortbouwt op wat eerder is gegenereerd.

Die architectuur maakt het systeem flexibel — een enkel onderdeel kan worden vervangen of bijgesteld zonder dat de hele keten opnieuw moet — en transparant: elk model heeft een afgebakende verantwoordelijkheid die geëvalueerd kan worden.

## Leidt het gebruik van taalmodellen in de preekvoorbereiding niet tot vervreemding in plaats van resonantie? Hartmut Rosa zou dit toch bekritiseren?

Dat is een scherpe vraag. Hartmut Rosa (geb. 1965) beschrijft in zijn werk over versnelling en vervreemding hoe technologische ontwikkelingen kunnen leiden tot een wereldrelatie waarin de wereld stom, koud en onverschillig — zelfs vijandig — wordt. Resonantie is het tegenovergestelde: een responsieve relatie waarin subject en wereld elkaar wederzijds raken en transformeren, waarbij beide kanten met hun eigen stem spreken.

Het risico is reëel. Technologische versnelling kan leiden tot vervreemding, vooral als tools de wereld reduceren tot beheersbare, instrumentele objecten. Een preekvoorbereidingssysteem dat de tekst, de hoorders en de liturgie behandelt als variabelen in een productieproces zou precies doen wat Rosa bekritiseert: resonantie vervangen door efficiëntie.

Maar het hangt af van hoe het systeem wordt gebruikt. Resonantie is niet hetzelfde als spontaniteit of directheid — ze kan ook gefaciliteerd worden door structuur en voorbereiding. Een voorganger die uren besteedt aan administratieve zoektaken (welke liederen passen bij dit thema? waar staat die uitleg ook alweer? was er niet ergens een citaat over dit of dat?) kan juist minder ruimte ervaren voor de responsieve relatie met tekst en gemeente. Als het systeem tijdrovende taken versnelt, creëert het potentieel meer ruimte voor wat Rosa 'luisteren naar de eigen stem van de wereld' noemt.

Bovendien: het systeem dwingt tot explicitering van keuzes. Dat voorkomt dat de preekvoorbereiding (en voorbereiding van de gebeden!) een 'stomme' routine wordt — een herhaling van patronen zonder aandacht. De output is geen script dat gevolgd moet worden, maar materiaal dat gehoord, geëvalueerd en eventueel verworpen kan worden. De voorganger blijft degene die met eigen stem spreekt. Het verschil is dat die stem nu in gesprek kan met een gestructureerd aanbod van passend materiaal.

Rosa wijst in *Onbeschikbaarheid* (Boom, 2022) op het belang van ervaringen die zich niet laten beheersen of beschikbaar maken. Paradoxaal genoeg kan een goed ontworpen hulpmiddel ruimte creëren voor juist die onbeschikbaarheid — door administratieve lasten (waaronder zeker ook het zoeken naar tekstuele illustraties en beeldmateriaal voor de preek) te verminderen en zo contemplatieve ruimte te behouden. Zie ook *Leven in tijden van versnelling: een pleidooi voor resonantie* (Boom, 2016).

## Werkt dit geen 'luie' dienaren in de hand?

Het tegenovergestelde. In de gelijkenis van de talenten (Matteüs 25:14-30) wordt juist de knecht berispt die zijn talent begraaft — die niets doet met wat hem is toevertrouwd. De knechten die hun talenten vermeerderen, worden geprezen. Het Matteüseffect, zoals socioloog Robert K. Merton dit in 1968 beschreef, verwijst naar Matteüs 25:29: "Want wie heeft, zal nog meer krijgen, en wel in overvloed." Wie al succesvol is, presteert steeds beter — niet door luiheid, maar door slimmer gebruik van middelen en structuren.

Dit systeem beloont niet luiheid, maar ambachtelijke inzet. Een voorganger die theologisch onderlegd is, exegetisch scherp, contextueel gevoelig en liturgisch bewust, kan hiermee nóg beter worden. Wie daarentegen zonder nadenken output overneemt zonder kritische reflectie, zal oppervlakkig blijven — en dat zal (na verloop van tijd) hoorbaar zijn. Het systeem verhoogt de lat, het verlaagt hem niet.

Dit hulpmiddel neemt bovendien klassieke excuses weg. Er is nu geen gebrek meer aan toegang tot heldere homiletische structuurvormen, tot exegetische diepgang, tot inzicht in wat hoorders beweegt. Wat voorheen vaak ontbrak — tijd, bronnen, overzicht — is nu beschikbaar. De vraag verschuift daarmee van 'kon het beter?' naar 'heb je gedaan wat mogelijk was?' Middelmatigheid wordt niet gestimuleerd, maar juist zichtbaarder. En dat is een uitnodiging: het kan beter, en nu zijn de middelen er om dat ook te laten zien.

## Wat betekent dit voor de discussie rond HBO-predikanten?

Democratisering van het ambacht. Er is niets magisch of gnostisch aan de universitair geschoolde predikant — geen geheime kennis die alleen door jarenlange academische vorming wordt ontsloten. Wat universitair geschoolden doorgaans wél hebben, is een bepaalde manier van denken gecombineerd met toegang tot de juiste exegetische literatuur, theologische traditie en homiletische vormgeving. Dat is geen mysterie, maar vooral infrastructuur.

Dit systeem maakt diezelfde infrastructuur breder beschikbaar (inclusief het academische denken!). Het verlaagt de drempel tot ambachtelijke kwaliteit zonder de lat te verlagen. Een HBO-predikant met theologische nieuwsgierigheid en pastorale sensitiviteit kan met dit gereedschap uitstekende diensten voorbereiden met dezelfde complexe structuur en balancering (Moves & Structures, bijv.) — niet omdat het systeem het werk overneemt, maar omdat het de benodigde kennis en structuur aanreikt.

De verschillen tussen universitair en HBO worden hierdoor kleiner. Dat is winst voor de kerk. Het gaat niet om diploma's, maar om ambachtelijke kwaliteit — en kwaliteit kan ondersteund worden door goed gereedschap.

De discussie verschuift hiermee deels van opleidingsniveau naar ambachtelijke toewijding. Wie bereid is te leren en te groeien, krijgt de middelen om dat te doen. Dat maakt het speelveld rechtvaardiger, niet gemakkelijker.

## Waartoe dit alles?

Twee redenen.

Ten eerste: homiletiek is een wetenschappelijke discipline. Wie een dienst — oneerbiedig gesproken — uit elkaar en weer in elkaar kan zetten (deconstructie en reconstructie), is beter in staat om te zien waar het ambachtelijk goed dan wel minder goed gaat. Het bouwen van een generatief systeem dwingt tot explicitering van wat vaak impliciet blijft of soms zelfs genegeerd wordt.

Ten tweede: er is een chronisch gebrek aan *structurele* feedback op de output van voorgangers. Preken worden gehouden, soms gewaardeerd, zelden systematisch geëvalueerd. Deze voorbereiding is een hulpmiddel om uiteindelijk tot een integraal feedbacksysteem te komen (met o.a. representatieve 'virtuele' hoorders) — een manier om het ambacht te blijven ontwikkelen. Dit gebeurt in samenwerking met onderzoekers van de PThU (Utrecht).

Een eerste opzet van zo'n (open source) feedbacksysteem is te vinden op [Feedback](https://github.com/wmotte/homiletiek_feedback).
