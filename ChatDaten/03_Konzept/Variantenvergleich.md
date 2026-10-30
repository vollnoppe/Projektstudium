# Variantenvergleich und bedingte Empfehlung

Stand: 29.10.2026. Dies ist eine technische Vorprüfung auf Konzeptebene. Maße, Lasten, Zykluszeiten, Lieferumfang und Kosten sind noch nicht nachgewiesen. Quellen: [Istprozess und Anforderungen](../00_Projektstand/Istprozess_und_Anforderungen.md), Bilder B002/B005/B006/B015/B016/B017 und [Herstellerreferenzen](Herstellerreferenzen.md).

## Gemeinsamer Leistungsumfang

Jede Variante muss ganze Magazine automatisch zwischen Linienaufnahme und Wagen übertragen, beide Wagenebenen sowie bis zu vier Plätze erreichen, belegte/leere Plätze erkennen und den Transfer in Gegenrichtung unterstützen. Der AGILOX übernimmt den Wagentransport. Zur vollständigen Lösung gehören geeignete Module an den tatsächlich angefahrenen Eingabestationen und Pufferübergaben. Eine nur am Linienende automatisierte Lösung lässt den zweiten manuellen Übergabeabschnitt bestehen.

Die Steuerung unterscheidet **Magazinzustand** (leer, teilgefüllt, voll, gesperrt) und **Wagenbelegung** (welche Plätze mit welchen Magazinen belegt sind). Ein teilgefülltes Magazin und ein teilweise belegter Wagen sind verschiedene Zustände. Auf Losende muss eine Freigabe auch mit weniger als vier Magazinen möglich sein. Zielreinheit oder erlaubte Mischbeladung, Reihenfolge und zeitliche Freigabe bleiben mit F12 zu bestätigen.

## V1 – Stationäre Hub- und Verschiebeübergabe

**Prinzip:** Eine neben der Linie angeordnete Transferstation positioniert sich horizontal zu den Magazinplätzen und vertikal zu den beiden Wagenebenen. Eine tragende Übergabefläche beziehungsweise Teleskop-/Schiebemechanik verbindet Maschinenaufnahme und Wagenplatz. Der Wagen wird reproduzierbar angedockt und gegen Bewegung gesichert. Ein Magazin bleibt während der gesamten Bewegung unterstützt; das mechanische Detail wird erst nach Vermessung festgelegt.

**Ablauf:** Das System liest Magazin/Los/Ziel und den freien Wagenplatz, prüft Wagenverriegelung und Magazinfreigabe, fährt den Transfer auf die Zielhöhe/-position, übernimmt das Magazin kraftüberwacht und bestätigt den Zielzustand. Vor Wagenfreigabe werden Übergabebrücke und bewegte Teile vollständig zurückgezogen sowie Magazinsicherung und Platzbelegung geprüft. In Gegenrichtung wird das passende Magazin zur freigegebenen Eingabestation übertragen. Ein leerer Wagen kann unabhängig vom nächsten befüllten Wagen bereitgestellt werden; erforderliche Wechselplätze sind Bestandteil der Auslegung.

**Warum näher untersuchen:** An Wagen und einigen Linienstationen sind Rollenbahnen sichtbar. Eine bestandsnahe Station könnte diese Auflageflächen verwenden, ohne sämtliche Wagen aktiv auszurüsten. Das ist eine konstruktive Hypothese aus B015–B017, keine bestätigte Umrüstbarkeit.

**Kritische Grenzen:** Rollen allein garantieren keinen sicheren Transfer. Offen sind seitliche Zugänglichkeit, tatsächliche Rollrichtung, Wagenanschläge/Stopps, automatische Entriegelbarkeit, Spaltüberbrückung, Radstellung, Kraft und Toleranzkette. Eine notwendige interne Wagenänderung wird offengelegt und gegen E02 bewertet. „5 mm“ wird nicht ungeprüft als zulässiger Gesamtpositionierfehler angesetzt.

**Aufwandstreiber:** Zahl der unterschiedlichen Linien-/Zielstationen, Hub-/Querwege, Dock-/Wechselplatz, Halte- und Identifikationsmodule, Schutzbereich, PLC/MES-Integration sowie Wartung der Transfermechanik. Eine werkweite Stationszahl folgt nicht automatisch aus 24 SMT-Linien.

## V2 – Stationärer Roboter oder Portal

**Prinzip:** Eine stationäre Handhabung erreicht Linienstationen und die vier Wagenplätze. Das ganze Magazin wird an freigegebenen tragenden Flächen unterstützt oder gegriffen. Die Auswahl zwischen Portal und Gelenkarm erfolgt anhand von Nutzlast, Reichweite, Freiraum und Zugriffsrichtungen; sie ist noch keine Produktentscheidung.

**Ablauf:** Wagen positionieren und sichern, Magazinidentität und Ziel prüfen, Maschine zur Entnahme freigeben, Magazin aufnehmen, sicher bewegen, auf dem Wagen absetzen und Belegung bestätigen. Rückrichtung und Leergut verwenden dieselben verifizierten Abläufe. Der AGILOX wird nach sicherer Wagenübergabe entlassen und wartet möglichst nicht während der laufenden Magazinbefüllung.

**Möglicher Vorteil:** Unterschiedliche Magazinpositionen und Zugriffsrichtungen könnten über eine gemeinsame Handhabung abgedeckt werden. Das kann bei uneinheitlichen Linien wertvoll sein, muss jedoch für jedes Ziel und jede Magazinvariante nachgewiesen werden.

**Kritische Grenzen:** Es fehlen bestätigte Greif-/Auflageflächen, Vollgewichte und Schwerpunktgrenzen. Bewegungen dürfen Magazine nicht verformen oder Panels verschieben. Nutzlast umfasst Magazin, Inhalt und Greifer. Eine Bezeichnung als kollaborativer Roboter ersetzt keinen Nachweis der sicheren Anwendung. Schutzraum, Bedien-/Wartungszugang und Wiederanlauf können den vermeintlichen Flexibilitätsvorteil aufzehren.

**Aufwandstreiber:** Roboter/Portal, Greifer, Werkzeugwechsel falls nötig, Sensorik, Schutzbereich, Programmierung aller Varianten, sichere Lastretention, Integration und Instandhaltung. Eine geteilte Zelle für mehrere Linien ist nur sinnvoll, wenn diese ohne neue manuelle Magazinwege tatsächlich erreichbar sind und der Gleichzeitigkeitsfall beherrscht wird.

## V3 – Angepasstes Wagen- und Übergabesystem

**Prinzip:** Ein standardisierter beziehungsweise umgerüsteter Wagen besitzt definierte Andockflächen, automatisch lösbare Magazinsicherungen und vereinheitlichte Übergabeauflagen je Platz. Antriebsenergie kann stationär an der Dockstelle eingebracht werden; eine Batterie oder aktive Steuerung auf jedem Wagen ist kein gesetzter Bestandteil. Die AGILOX-Aufnahmegeometrie bleibt möglichst kompatibel.

**Ablauf:** AGILOX bringt einen geeigneten Wagen zur Dockstelle; nach Identifikation und Verriegelung erfolgt der Austausch der einzelnen Magazine über die standardisierten Plätze. Hub-/Queranpassung bleibt stationär, sofern die Linie nicht bereits beide Ebenen und Positionen erreichen kann. Am Ziel wird derselbe standardisierte Wagen automatisch entladen und anschließend für Leergut beziehungsweise Folgeaufträge freigegeben.

**Möglicher Vorteil:** Eine einheitliche mechanische Schnittstelle könnte Störquellen der heterogenen Bestandswagen reduzieren und die stationäre Übergabe vereinfachen. Dadurch kann V3 bei hohem Rolloutumfang einen technischen Vorteil haben.

**Kritische Grenzen:** Die Unterlagen nennen ungefähr 4.000 Wagen. Schon kleine Änderungen pro Wagen können den Rolloutaufwand deutlich erhöhen; außerdem müssen Ersatzteile, Mischbetrieb, Wagenfreigaben und Rückverfolgbarkeit beherrscht werden. Zunächst nur einen Pilotbestand bewerten. Ein Volltausch wird weder als nötig noch als wirtschaftlich vorausgesetzt.

**Aufwandstreiber:** Konstruktion und Freigabe der Wagenanpassung, tatsächlicher betroffener Bestand, Umrüstung/Prüfung pro Wagen, Stationsmodule, Mischbetrieb und Logistik der Umstellung. Eventuelle Änderungen an AGILOX-Lastaufnahme separat ausweisen.

## Gemeinsame Bewertungsmatrix

Die Einträge sind begründete Erwartungen auf Konzeptebene. Es gibt keine gemessenen Leistungswerte, Angebote oder willkürlich gewichteten Punktescores.

| Kriterium | V1 Hub/Verschieben | V2 Roboter/Portal | V3 angepasstes System | Entscheidend für den Nachweis |
|---|---|---|---|---|
| Bestandswagen | Bevorzugt unverändert; externe Betätigung vorhandener Stopps nötig | Möglich, wenn sichere Aufnahme und Zugriff funktionieren | Gezielte Änderung/Standardisierung | F01/F03/F13 |
| AGILOX | Vorhandener Wagentransport vorgesehen | Vorhandener Wagentransport vorgesehen | Aufnahme möglichst erhalten, erneut prüfen | F09 |
| Ein-/Ausgabevarianten | Je Geometrie passendes Transfer-/Adaptermodul | Potenziell flexibler, aber Reichweite und Greifer entscheidend | Stationsseite muss weiter zu den Linien passen | F01/F03 |
| Magazinhandling | Unterstützter Transfer als Ziel | Sicheres Aufnehmen/Absetzen nachweisen | Geführte Standardübergabe als Ziel | Vollgewicht, Kräfte, Produktstabilität |
| Zwei Ebenen/vier Plätze | Hub und Querpositionierung erforderlich | Im verifizierten Arbeitsraum erreichen | Standardplätze; stationäre Höhenanpassung bleibt nötig | Vermessung und Lastfall |
| Durchsatz | Offen: Docken plus einzelne Transfers und Wechsel | Offen: Greifen, Wege, Absetzen, Wiederholungen | Offen: Docken und standardisierte Transfers | F07; gemessener Gesamtzyklus |
| Platz | Dock-, Transfer-, Wechsel- und Schutzfläche | Arbeits-/Schutzraum und Wagenwechsel | Dock-/Wechselraum plus angepasste Station | Bemaßtes Layout F09 |
| Teilfüllung/Losende | Software und Platzidentität erforderlich | Software und Platzidentität erforderlich | Software und Platzidentität erforderlich | F04/F12, keine Pflicht zu voller Belegung |
| Integrationsaufwand | Mechanische Schnittstellen im Vordergrund | Greifer, Bewegungsprogramme und Schutzraum | Wagenfreigabe plus standardisierte Schnittstellen | Inventar aller Stationstypen |
| Kostentreiber | Zahl/Varianz stationärer Module | Handhabung, Greifer, Schutzraum, Varianten | Wagenanzahl, Umbau, Mischbetrieb, Module | Vergleichbare Angebote F14 |
| Hauptunsicherheit | Stopps und Roll-/Übergabegeometrie | Sichere Lastaufnahme bei allen Varianten | Skalierter Aufwand gegenüber Zusatznutzen | Pilot und wirtschaftliche Gegenrechnung |

## Empfehlung mit Bedingungen

**V1 zuerst auf mechanische Machbarkeit prüfen.** Die sichtbaren Rollenauflagen und das Ziel, Wagen und AGILOX bevorzugt weiterzuverwenden, liefern dafür einen plausiblen Ansatz. Das ist die Empfehlung für den nächsten Nachweis, keine abschließende Investitionsfreigabe.

V1 bleibt bevorzugt, wenn sich Magazine ohne Eingriff in kritische Wagenstrukturen sicher entriegeln, unterstützen, übertragen und erneut sichern lassen; beide Ebenen/Ziele erreichbar sind; der gemessene Wechselbedarf mit Reserve bewältigt wird und das Modul im realen Layout Platz findet. Diese Bedingungen werden mit F01/F03/F07/F09/F13 geprüft.

**V2 wird zur ernsthaften Alternative**, wenn V1 an nicht überbrückbarer Geometrie oder uneinheitlichen Übergaberichtungen scheitert und ein belegbar sicherer Greifer mehrere Stationstypen wirtschaftlicher abdecken kann. **V3 wird vertieft**, wenn Wagenanpassungen ohnehin erforderlich sind oder standardisierte Schnittstellen die nachgewiesenen Lebenszykluskosten und Störungen ausreichend reduzieren. Ein höherer Preis allein ist kein Ausschlusskriterium; ein unbelegter Flexibilitätsvorteil rechtfertigt ihn nicht.

## Nächster Prüfaufbau

1. Repräsentative Wagen-/Magazin-/Stationstypen vermessen und Variantenanteile erfassen.
2. Für V1 einen Transferablauf mit kritischer Höhe, ungünstiger Belegung und realen Stopps auf Papier beziehungsweise mit einem einfachen mechanischen Versuch nachweisen; noch kein Eingriff in laufende Produktionssteuerungen.
3. Dieselben Last-/Zugriffsfälle für V2 und den konkreten Änderungsumfang von V3 prüfen.
4. Tatsächliche Anforderungen und Gesamtzykluszeiten gegen Losreste, gleichzeitig fällige Magazine und Abholverzug abgleichen.
5. Vergleichbare Pilotangebote auf denselben Leistungsumfang beziehen und die bedingte Empfehlung aktualisieren.
