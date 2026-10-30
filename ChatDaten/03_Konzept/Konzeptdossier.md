# Konzeptdossier: Automatisierte Magazinlogistik bei Aumovio

Stand: 29.10.2026 · Universitätsgruppenprojekt · Werk Regensburg laut Startunterlagen.

[Zentraler Einstieg](../README.md) · [Bildkatalog](../01_Bildkatalog/Bildkatalog.md) · [Datenanalyse](../02_Analysen/Analysebericht.md) · [Fragen an Aumovio](../00_Projektstand/Offene_Fragen_Aumovio.md)

## 1. Vorschlag und Entscheidungsstand

**Eine stationäre Hub- und Verschiebeübergabe mit vorhandenen Magazinwagen sollte zuerst auf Machbarkeit geprüft werden.** Sie adressiert die heute manuelle Verbindung zwischen Linienaufnahme und Wagentransport und passt zum Ziel, Wagen und AGILOX bevorzugt weiterzuverwenden. Ein entsprechendes Modul muss auch am Ziel automatisch entladen beziehungsweise an die Eingabestation übergeben. Losreste, teilgefüllte Magazine, Teilwagen und Leergut gehören von Anfang an zum Ablauf.

Diese Priorisierung ist **bedingt**: Rollenauflagen sind auf den Fotos sichtbar, ihre sichere automatisierte Nutzung ist jedoch nicht nachgewiesen. Wagenstopps, Rollrichtung, Zugänglichkeit, Höhen, Kräfte, Toleranzen und Platz müssen überprüft werden. Scheitert dieser Ansatz daran, bietet die stationäre Roboter-/Portalhandhabung eine zweite Variante. Ein angepasstes Wagen-/Übergabesystem bildet die freiere Alternative, deren Standardisierungsnutzen gegen den Aufwand am tatsächlich betroffenen Wagenbestand abzuwägen ist.

Eine finale Stationszahl, Fahrzeugzahl, Pufferkapazität oder Investitionssumme ist mit den vorhandenen Unterlagen noch nicht belastbar. Das Dossier legt dafür die Nachweise und Rechenbasis offen. Es liegt keine Beschaffungsempfehlung für einen Anbieter vor.

## 2. Ausgangslage und Zielkreislauf

Die Unterlagen beschreiben Magazine mit bestückten Panels an SMT-Linien. Beschäftigte übernehmen die Magazine auf Wagen, während der AGILOX den längeren Weg fährt. Am Ziel entsteht erneut manueller Übergabeaufwand. Die Quellen nennen maximal vier Magazine auf zwei Ebenen sowie etwa 4.000 vorhandene Wagen. Diese Angaben sind in den Notizen/Startfolien belegt, aber noch nicht durch einen freigegebenen Betriebsmittelkatalog bestätigt.

Der Zielkreislauf umfasst Linienausschleusung, automatische Wagenbeladung, Wagentransport, automatische Übergabe zur nächsten Station oder zum Puffer sowie Rückführung passender leerer Magazine und freier Wagen. Bei beidseitiger Bestückung muss ein Magazin gegebenenfalls erneut in einen SMT-Prozess; ein fehlendes Zwischenziel in der Tabelle bedeutet nicht automatisch Backend-Abgang.

Die [Anforderungsliste A01–A16](../00_Projektstand/Istprozess_und_Anforderungen.md) enthält Quellenstellen und erforderliche Nachweise. Die genannten etwa 5 mm müssen einer konkreten Schnittstelle/Toleranzkette zugeordnet werden. Die Schadensspanne 1.500–10.000 EUR je Magazin/Einheit bleibt in ihrer Bedeutung offen und wird nicht als pauschale Einsparung angesetzt.

## 3. Was die Fotos beitragen

17 Fotos wurden unverändert kopiert, benannt und vier Hauptthemen zugeordnet. Jede Kopie ist über Bild-ID, Quell-ID und Prüfsumme zum Original rückverfolgbar. Der [Kontaktbogen](../01_Bildkatalog/Kontaktbogen.jpg) erlaubt einen schnellen Überblick.

- B002/B005/B006/B017 zeigen drei nummerierte Magazinplätze mit unterschiedlichen Auflagen und sichtbarer Sensorik. Ein-/Ausgaberichtung und Schnittstellen sind dadurch nicht vollständig geklärt.
- B015/B016 zeigen Rollen, Rahmen, Räder und zwei Wagenebenen. Daraus entsteht der Ansatz für V1; Maße, Reibung und Verriegelungen folgen daraus nicht.
- B010–B012 dokumentieren die relevante Wagenaufnahme des grünen AGILOX. Die konkrete technische Ausführung bleibt offen.
- B008/B009/B013/B014 zeigen Lagerreihen, Wagen und stationäre Übergabebahnen. Sie belegen keine freie oder automatisch nutzbare Lagerkapazität.

Ähnliche Ansichten und dieselben in Folien eingebetteten Fotos werden nicht als unabhängige Bestätigung gezählt.

## 4. Ergebnisse der Produktionsdatenanalyse

Quelle: Q018, vollständig beschriebene Berechnung im [Analysebericht](../02_Analysen/Analysebericht.md) und [Datenwörterbuch](../02_Analysen/Datenwoerterbuch.md).

| Befund | Bedeutung für das Konzept |
|---|---|
| 51.714 eindeutige LOTID, 01.07.2024–30.06.2026 | Zwei Jahre dokumentierte Losstarts; keine vollständige Magazintransporthistorie |
| 24 SMT-Linien, 559 BOARDTYPE | Werkweite Übertragbarkeit verlangt ein Stations-/Produktspektrum; ein Pilot allein ist keine Flottenauslegung |
| 20.175.629 bekannte Panel-Bearbeitungsvorgänge | Keine eindeutige physische Stückzahl über beide Seiten; zwei Lose haben keine Menge |
| Median 399, 95. Perzentil 875 Panels je mengenbekanntem Los | Variable Losgrößen und Restmagazine sind relevant; daraus folgen ohne Belegung keine Magazinzahlen |
| 19.631 Datensätze mit Zwischenzielmarkierung; davon 10.590 mit gleicher Quell-/Ziellinie | Routingsemantik bestätigen; nicht pauschal als Fahrt zwischen Linien zählen |
| Exakter Backend-Stammdatenmatch für 406 von 559 BOARDTYPE, 85,9 % der Lose | Fehlende Abdeckung und tatsächliche Zielwahl bleiben sichtbar |
| 154 BOARDTYPE mit mehreren möglichen Backend-Linien | Kein beliebiges erstes Ziel auswählen und keine Mengen durch Mehrfachzuordnung vervielfachen |
| Backend enthält Stammzeiten, keine tatsächlichen Abnahmen | Produktionsentkopplung noch nicht aus historischen Bestandsbilanzen dimensionierbar |

Die nachgerechneten Zeitumwandlungen und Auswahlregeln stimmen mit den gespeicherten Quellwerten überein. Das bestätigt die technische Verarbeitung, nicht die betriebliche Definition der Zeiten. Losmengen sind in Diagrammen nach Losstart zugeordnet; sie sind keine Fertigstellungs- oder Transportspitzen.

## 5. Lösungsvarianten

| Variante | Grundidee | Entscheidender Nachweis |
|---|---|---|
| V1: Hub-/Verschiebestation | Ganze Magazine unterstützt zwischen Linienaufnahme und den vier Wagenpositionen übertragen; Wagen gesichert andocken | Rollen-/Stoppsystem, Zugänglichkeit und Toleranzen ohne unverhältnismäßige Bestandsänderung beherrschen |
| V2: Stationärer Roboter/Portal | Magazine an tragenden Flächen aufnehmen und zwischen Station und Wagen bewegen | Sicheres Greifen/Unterstützen bei Vollgewicht; Arbeits-/Schutzraum und Variantenabdeckung |
| V3: Angepasstes Wagen-/Übergabesystem | Definierte Dockflächen, automatisch lösbare Sicherungen und standardisierte Auflagen | Umfang und Nutzen der Wagenänderung gegenüber Stationseinsparung und zuverlässigerer Übergabe |

Der [vollständige Variantenvergleich](Variantenvergleich.md) bewertet bei gleichem Leistungsumfang Durchsatz, Fläche, Bestandsänderungen, Integration, Beschädigungsrisiko und Aufwand. Es gibt keine erfundenen gewichteten Scores. Die [Herstellerreferenzen](Herstellerreferenzen.md) von ASYS/NUTEK zeigen Automatisierungsansätze an Magazinplattformen; sie bestätigen weder unsere Wagenkompatibilität noch einen schlüsselfertigen Gesamttransfer.

Die [Schnittstellen und Betriebsfälle](Schnittstellen_und_Betriebsfaelle.md) beschreiben Identität, Ziel/Belegung, Reservierung, Verriegelung, Übernahmebestätigung, AGV-Freigabe und geordneten Wiederanlauf. Ein vollständiger Zyklus enthält auch Andocken, Prüfen, Wechseln und Freigeben; veröffentlichte PCB-Zykluszeiten werden nicht als Magazinwechselzeiten verwendet.

## 6. Puffer und Dimensionierung

Das [Pufferkonzept](Pufferkonzept.md) trennt die kurzfristige Linienreserve von der längerfristigen Entkopplung bis zum nächsten Produktionsschritt. Als Basisszenario wird kurzfristige wagenweise Bereitstellung untersucht. Einzelmagazin-Puffer werden dort vertieft, wo echte Verweilzeiten, Zugriffsmuster oder Wagen-/Flächenbindung ihren Zusatzaufwand rechtfertigen.

Das vorbereitete [Bedarfsmodell](../02_Analysen/Bedarfsmodelle.md) rundet Magazinbedarf je Los auf und erfasst Losreste und teilweise belegte Wagen. Die wirksame Kapazität ist für 1.000 Produkt-/Seiten-/Revisionsschlüssel als leere Eingabe vorbereitet. Aktuell entstehen daraus keine behaupteten historischen Magazinzahlen. Die Rechenbeispiele sind ausdrücklich hypothetisch.

Für absolute Pufferbelegung sind Anfangsbestand und tatsächliche Zu-/Abgänge erforderlich. Backend-Stammzeiten und Losstarts ersetzen diese Ereignisse nicht. Eine mögliche 24-Stunden-Regel muss zunächst bestätigt werden. Übergabe-/Sperr-/Wechselplätze kommen zur berechneten Nettobelegung hinzu.

## 7. Investition rechtfertigen

V1/V2/V3 sind nur bei vollständigem, vergleichbarem Leistungsumfang wirtschaftlich zu bewerten. Höhere Kosten können sich durch weniger verbleibende Handhabung, weniger produktionswirksames Warten, geringere Wagen-/Flächenbindung oder nachgewiesene Qualitätsvorteile begründen. Keiner dieser Nutzen ist derzeit beziffert.

Die [Wirtschaftlichkeitsmethodik](Wirtschaftlichkeit.md) trennt frei werdende Arbeitskapazität von zahlungswirksamer Einsparung und betrachtet die Amortisation zusätzlicher Investitionen anhand des zusätzlichen Netto-Nutzens. Das Erhebungsblatt hält benötigte Parameter offen. Verbindliche Preise und Angebotsvergleiche stehen aus.

## 8. Nächster belastbarer Entscheidungsschritt

1. **Mechanikpaket:** Wagen-/Magazinzeichnungen, Gewichte, Verriegelungen und Stationstypen beschaffen (F01/F03/F13).
2. **Datenpaket:** wirksame Kapazitäten und bestätigte Los-/Routensemantik ergänzen (F02/F05/F06).
3. **Ereignispaket:** reale Magazinwechsel, Transporte und Backend-Abnahmen mit Anfangsbestand bereitstellen (F07/F08).
4. **Pilotvergleich:** kritische Last-/Geometriefälle von V1 gegen V2/V3 prüfen; reale Zykluszeiten und Layoutzugang nachweisen.
5. **Nutzenpaket:** Bedienzeiten und vergleichbare Pilotangebote erheben (F10/F11/F14); danach Empfehlung und Dimensionierung aktualisieren.

Abgeschlossen ist damit ein nachvollziehbarer Konzeptstand mit geordneten Befunden, geprüfter Datenauswertung und einer bedingten Priorisierung. Die technische und quantitative Freigabe erfolgt erst anhand der genannten Nachweise.
