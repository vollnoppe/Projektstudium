# Priorisierte Fragen und benötigte Nachweise

Stand: 29.10.2026. Alle Fragen sind offen. Diese Liste kann das Team mit Aumovio durchgehen; es wurden keine externen Ansprechpartner kontaktiert. Antworten mit Datum und Quelle in der letzten Spalte beziehungsweise im Entscheidungslog ergänzen.

## Zuerst beschaffen

Für den nächsten belastbaren Konzeptentscheid sind vier Pakete am wichtigsten: **bemaßte Mechanik**, **wirksame Magazinkapazitäten**, **Bedeutung der Los-/Routendaten** und **echte Zu-/Abgangsereignisse**. Ein Pilot mit einer repräsentativen Linie genügt für den ersten Mechaniknachweis; eine werkweite Dimensionierung benötigt anschließend die vollständige Stations-/Mengenabdeckung.

| ID / Priorität | Konkrete Frage und gewünschtes Ergebnis | Zweck / betroffene Entscheidung | Geeignete Stelle | Antwort / Quelle |
|---|---|---|---|---|
| F01 / P0 | Welche Wagen- und Magazinbauformen werden tatsächlich eingesetzt? Benötigt: Zeichnungen oder Messblatt mit Außenmaßen, Auflagehöhen beider Ebenen, vier Platzkoordinaten, Unterfahrbereich, Leer-/Vollgewichten, Schwerpunkt und Toleranzen. | V1/V2/V3, A04/A07/A10: Hubweg, Zugriff und sichere Lastaufnahme | Betriebsmittel-/Anlagenplanung | offen |
| F02 / P0 | Wie viele Panels passen effektiv je BOARDTYPE, SIDE, REVISION und Magazinbauform in ein Magazin? Bitte Slotabstand, ausgelassene Slots, Bauteilhöhe, Mehrfachbelegung und Ausnahmen benennen. | Mengen in Magazine umrechnen; Transport- und Pufferbedarf. Vorlage: Magazinkapazitaeten.csv | Fertigung / Industrial Engineering | offen |
| F03 / P0 | Welche Ein-/Ausgabestationen gibt es je Linie und Backend? Benötigt: Hersteller/Typ, Übergabeseite/-richtung, freie Zugänge, Magazinverriegelung, Antriebe und aktueller Wechselablauf. Was bedeuten die 5 mm genau? | V1 kann nur bei beherrschbarer Übergabeschnittstelle bevorzugt werden; A01/A02/A07 | Anlagenbetreuung / Automation | offen |
| F04 / P0 | Welche Meldungen und Identitäten sind technisch verfügbar: Magazin-ID, LOTID, Belegung, Losende, Ziel, Übergabebereitschaft? Gibt es dokumentierte Schnittstellen und Testzugang? | Zustandsmodell und automatische Ziel-/Füllstandsprüfung; A11 | MES / IT / Steuerungstechnik | offen |
| F05 / P0 | Was bedeutet ein Datensatz in SMD Lots genau? Sind REALAMOUNT und NUMBEROFPANELSINLOT Ist-, Soll- oder abgeschlossene Mengen? Welche Bedeutung/Einheit haben OIS-, OIB-, Netto- und Backend-Zeiten sowie SMDQUANTITY? Welche Zeitzone gilt? | Keine falschen Stück-/Kapazitätsannahmen; Datenwörterbuch freigeben | Datenlieferant, laut Notizen Thomas Wölfl | offen |
| F06 / P0 | Wie sind die beiden Seiten desselben physischen Panels/Losverbunds verknüpft? Was bedeuten Order, INTERMEDIATETARGET und TARGETLINE, insbesondere gleiches Quell-/Ziellinienfeld und fehlende Ziele? | Physische Mengen, SMT-Rückläufe und tatsächliche Transportbeziehungen | MES / Fertigungsplanung | offen |
| F07 / P0 | Können tatsächliche Magazinwechsel und Transporte für repräsentative Hochlast- und Normalzeiträume bereitgestellt werden? Felder: Ereigniszeit, Magazin-/Wagen-ID, Lot/Produkt/Seite, Menge, Quelle, Ziel, Übergabe-/Abhol-/Ankunftszeit, Störung. Ideal: 2–4 Wochen plus bekannter Spitzenzeitraum. | Stationstakt, Wartezeit, AGV-Bedarf und Linienpuffer; Losstartdaten reichen dafür nicht | MES / AGV-Leitsystem / Fertigung | offen |
| F08 / P0 | Welche tatsächlichen Abnahmen ins Backend und welche Pufferbestände gab es? Benötigt: Anfangsbestand, Zu-/Abgänge mit Zeit/ID/Menge, Sperr-/Freigabestatus und Zuordnung zu Backend-Prozess. | Produktionsentkopplung dimensionieren und Bilanz prüfen; keine historischen Pufferzahlen ohne diese Basis | Backend / Logistik / Planung | offen |
| F09 / P1 | Welche AGILOX-Ausführung, Flotte und Wagenfreigaben bestehen? Wie lange dauern Fahrt, Docken, Warten und Laden? Bitte bemaßtes Layout mit Fahrwegen, Übergabe- und Warteflächen. | Bestandskompatibilität, Fahrzeugbelegung und Blockierungsanalyse | Intralogistik / AGV-Verantwortliche | offen |
| F10 / P1 | Wie viel aktive Bedienzeit fällt pro Magazin und pro Wagenwechsel an? Für eine erste Zeitaufnahme möglichst mindestens 20 vollständige Wechsel verschiedener Zustände erfassen; Geh-, Warte- und Handhabungszeit getrennt. | Automatisierbarer Arbeitsaufwand und wirtschaftlicher Zusatznutzen | Fertigung / Zeitwirtschaft | offen |
| F11 / P1 | Wie oft entstehen Schäden, Blockaden oder produktionswirksame Wartezeiten? Was umfasst die Angabe 1.500–10.000 EUR: Magazin, Inhalt, Nacharbeit oder Folgekosten? | Risikonutzen, Ausfallkosten und Vermeidung einer pauschalen Schadensersparnis | Qualität / Fertigung / Controlling | offen |
| F12 / P1 | Dürfen Lose/Produkte/Ziele einen Wagen teilen? Wann werden Restlose freigegeben? Wie laufen Leergutversorgung, Sperrware, Reihenfolge und die erwähnte 24-Stunden-Regel tatsächlich? | Wagenbelegung, Pufferstrategie, FIFO/Priorität und Rückführung | Disposition / SMT / Backend / Logistik | offen |
| F13 / P1 | Welche Freigaben gelten für ESD, kraftbegrenztes Schieben/Greifen, Ladungssicherung und Zugang zu bewegten Anlagen? Sind bestehende Wagenstopps extern automatisch betätigbar? | Sicherheit und Beschädigungsschutz; mögliches Ausschlusskriterium für V1 | Automation / Qualität / Arbeitssicherheit | offen |
| F14 / P2 | Welche Betriebsmittel-/Integrationsangebote und laufenden Kosten lassen sich für einen Pilot und für den Ausbau ermitteln? Welche Amortisations- oder Nutzenkriterien verwendet Aumovio? | Mehrinvestition gegenüber V1 sachlich begründen, ohne erfundene Preise | Einkauf / Engineering / Controlling | offen |

## Datenlieferungen effizient vorbereiten

- F01/F03: Zeichnungen oder ein gemeinsames Messblatt; Fotos mit Referenzmaß und Stations-ID als Ergänzung. Keine Maße aus Perspektivfotos schätzen.
- F02: Die vorbereitete Kapazitätstabelle ausfüllen. Bei mehreren zulässigen Magazinformaten je Schlüssel die Abgrenzung vor der Modellrechnung ergänzen.
- F05/F06: Felddefinitionen und wenige nachvollziehbare reale Ablaufbeispiele liefern, insbesondere über beide Seiten und mit gleichem Zwischenziel.
- F07/F08: CSV oder Excel mit eindeutigen IDs und Einheiten. Zeitbasis, Abdeckung, fehlende Ereignisse und Anfangsbestand mitliefern. Ein Ausschnitt ohne Anfangsbestand reicht nicht für absolute Pufferbelegung.
- F10/F11/F14: Gemessene Bedienzeit und wirtschaftlich bewertete Einsparung trennen. Frei werdende Kapazität ist nicht automatisch eine zahlungswirksame Personalkostenersparnis.

## Nachweise schließen

Eine beantwortete Frage wird mit Quelle, Stand, Geltungsbereich und betroffenen Anforderungen verknüpft. Bei geänderten Kapazitäten die Analyse erneut ausführen; bei neuer Mechanik V1/V2/V3 neu bewerten. Datenlücken dürfen als offene Nachweise bestehen bleiben, müssen aber unmittelbar bei der betroffenen Empfehlung stehen.
