# Datenwörterbuch und Auswertungsregeln

Stand: 29.10.2026. Quelle Q018. Feldnamen und Formelauswahl sind überprüfbar; die betriebliche Bedeutung muss Aumovio mit F05/F06 freigeben. Die Tabelle trennt ausdrücklich technische Beobachtung und fachliche Interpretation.

## SMD Lots

Eine Zeile entspricht einem eindeutigen dokumentierten LOTID-Datensatz. Es ist nicht belegt, dass eine LOTID ein physisches Panel über beide Seiten oder einen Magazintransport identifiziert. 51.714 Datenzeilen, 23 Quellspalten, keine doppelte LOTID.

| Spalte | Feld | Inhalt / Einheit / Behandlung |
|---|---|---|
| A | LOTID | Eindeutige Kennung im Auszug; als Textschlüssel exportiert, nicht summieren |
| B | LINE | Dokumentierte SMT-Linie; 24 Werte SMT01–SMT24 |
| C | REALAMOUNT | Menge gemäß Quelle; bei vorhandenen Werten exakt D × E. Ob abgeschlossene Iststückzahl oder andere Mengenbasis: F05. Zwei Werte fehlen |
| D | NUMBERPERPANEL | Stückzahl je Panel gemäß Feldname; Werte ganzzahlig, Bedeutung mit Nutzenaufbau bestätigen |
| E | NUMBEROFPANELSINLOT | Dokumentierte Panelmenge je Los; zwei Werte fehlen. Auswertung nennt Summen Panel-Bearbeitungsvorgänge |
| F | REALSTART | Textzeit `TT.MM.JJ hh:mm:ss,fffffffff`, bis zu neun Nachkommastellen. Zeitzone und genaue Ereignisbedeutung offen |
| G | Stunde | Gespeichertes Formelergebnis `INT(F×24)/24`, auf Stunde abgerundete Zeit; stimmt mit aus F geparster Stunde überein |
| H | SIDE | Top oder Bottom; allein kein verlässlicher physischer Verknüpfungsschlüssel |
| I | REVISION | Revisionskennzeichen; Teil des Kapazitätsschlüssels, keine beliebige Auswahl der neuesten Revision |
| J | Order | TopFirst, BottomFirst oder NoOrder; Prozessreihenfolge laut Bezeichnung, tatsächliche Routingsemantik offen |
| K | BOARDTYPE | Produkt-/Baugruppenschlüssel, 559 Werte. Exakter Join auf Backend.SMDBOARDTYPE; keine Teilstring- oder Revisionsheuristik |
| L | OISNETTIMEPERPANEL | Ganzzahliger Zeitbasiswert oder leer. Physische Bedeutung von OIS offen |
| M | OISNETTIMEPERPANELSEC | Quellenformel: L leer → leer, sonst L / 10.000.000; beabsichtigte Sekunden laut Feldname |
| N | OIBCYCLETIME | Alternativer ganzzahliger Zeitbasiswert; ein Wert fehlt. OIB-Bedeutung offen |
| O | OIBCYCLETIMESEC | Quellenformel: N leer → leer, sonst N / 10.000.000 |
| P | RELEVANTNETTIMESEC | Quellenformel: M verwenden, falls vorhanden, sonst O. Kein nachgewiesener realer Losdurchlauf einschließlich Rüsten/Stillstand |
| Q | TARGETLINE | Mögliches SMT-Zwischenziel; bei 32.083 Zeilen leer. Nicht als Backend-Linie interpretieren |
| R | AVGTARGETOISNETTIMEPERPANEL | Zeitbasiswert eines Zielprozesses gemäß Bezeichnung; fehlende Werte erhalten |
| S | AVGTARGETOISNETTIMEPERPANELSEC | R / 10.000.000, falls R vorhanden |
| T | AVGTARGETOIBCYCLETIME | Alternativer Zielzeitbasiswert; Bedeutung mit F05 bestätigen |
| U | AVGTARGETOIBCYCLETIMESEC | T / 10.000.000, falls T vorhanden |
| V | RELEVANTTARGETNETTIMESEC | S verwenden, falls vorhanden, sonst U. Keine reale Backend-Abnahmezeit |
| W | INTERMEDIATETARGET | 0 oder 1. 19.631 Zeilen mit 1 und Zielangabe. 0 oder fehlendes Ziel beweist keinen Backend-Abgang |

Die Division durch 10.000.000 ist aus den tatsächlichen Quellenformeln belegt. Daraus wird die Rechenumwandlung übernommen; die zugrunde liegende Erfassungseinheit und Zeitdefinition bleiben Gegenstand von F05. In den Sekundenspalten werden fehlende Werte nicht zu null.

## Backend-Productdata

2.476 Quellzeilen, 15 benannte Felder in A:O; P ist unbenannt und leer. Zeilen bilden Produkt-/Linien-/SMT-Zuordnungen mit Zeiten, keine Produktions- oder Verbrauchsereignisse. Die vollständige Dublette in Excelzeile 1513 zu 1512 wird nur in der abgeleiteten Mappingtabelle entfernt; beide Quellzeilen bleiben im Original.

| Spalte | Feld | Inhalt / Einheit / Behandlung |
|---|---|---|
| A | BACKENDPRODUCTNUMBER | Backend-Produktschlüssel, nicht mit BOARDTYPE gleichsetzen |
| B | DESCRIPTION | Produktbeschreibung; vier Werte fehlen |
| C | LINE | Mögliche Backend-Linie; 53 verschiedene Werte |
| D | LINEID | Linienkennung; ID statt Mengenwert |
| E | ISDEFAULT | 0/1. Auch unter 1 existieren mehrere mögliche Linien für manche BOARDTYPE |
| F | MANUALNETTIMEPERPANEL | Manuell hinterlegter Nettozeitbasiswert; höchste Priorität der Quellenformel |
| G | DEFAULTNETTIMEPERPANEL | Standard-Nettozeitbasiswert; letzte Rückfallebene |
| H | PDBNETTIMEPERPANEL | PDB-Nettozeitbasiswert; Vorrang vor G, aber nicht vor F |
| I | RELEVANTNETTIMESEC | Erste vorhandene Größe aus F, H, G geteilt durch 10.000.000 |
| J | MANUALGROSSTIMEPERPANEL | Manuell hinterlegter Bruttozeitbasiswert; höchste Priorität |
| K | DEFAULTGROSSTIMEPERPANEL | Standard-Bruttozeitbasiswert; letzte Rückfallebene |
| L | PDBGROSSTIMEPERPANEL | PDB-Bruttozeitbasiswert; Vorrang vor K, aber nicht vor J |
| M | RELEVANTGROSSTIMESEC | Erste vorhandene Größe aus J, L, K geteilt durch 10.000.000 |
| N | SMDBOARDTYPE | Exakter Verknüpfungsschlüssel zu SMD Lots.BOARDTYPE |
| O | SMDQUANTITY | Werte 1 und 2. Vermutete Mengenbeziehung zwischen SMT- und Backend-Produkt; vor Verwendung bestätigen. Nicht ungeprüft als Magazinbelegung verwenden |

Die Bezeichnung „PERPANEL“ allein beweist keine gemeinsame Zeit-/Mengeneinheit von SMT und Backend. Ohne bestätigte Stück-/Panel-/Produktbeziehung werden diese Zeiten nicht zu einem scheinbar präzisen Produktionsbilanzmodell kombiniert.

## Abgeleitete Felder und Tabellen

- `QUELLZEILE`: Original-Excelzeile einschließlich Kopfzeile. Nach Sortierungen weiterhin zur Quelle rückverfolgbar.
- `REALSTART_ISO`: normalisierte Textzeit ohne erfundene Zeitzone. F bleibt als Originaltext erhalten. `LOSSTART_STUNDE/TAG/MONAT` sind Aggregationsschlüssel.
- `MENGE_FEHLT`: kenntlich gemachte Lücke. `IDEALE_NETTO_DAUER_S = E × P` ist ausschließlich ein rechnerischer Nettozeitbedarf gemäß Quellenfeldern, keine tatsächliche Losdauer oder Endzeit.
- `BACKEND_LINIEN_ANZAHL`, `BACKEND_DEFAULT_LINIEN_ANZAHL` und `BACKEND_MAPPING_STATUS`: beschreiben die Stammdatenabdeckung, keine beobachtete Route. Mengen werden nicht über Zielalternativen vervielfacht.
- `panels_bearbeitungsvorgaenge`: bekannte Panelmengen summiert. Der separate Zähler `mengenlose_lose` zeigt die Vollständigkeit. Eine Gruppe mit ausschließlich fehlenden Mengen erhält eine leere Summe.
- `Magazinmodell_Lose.csv`: losreines Szenario mit offenem Kapazitätsparameter. Status und Quellenangabe begleiten jedes Ergebnis. Reale Fahrten, benötigte Fahrzeuge und Flottenauslastung werden nicht behauptet.
- Kalenderwochen beginnen montags. Die letzte Randwoche ist wegen des Datenendes am Dienstag unvollständig; nicht als vollständige Vergleichswoche behandeln. Keine Feiertage oder Schichten wurden ergänzt.

## Nicht aus der Datei bestimmbar

Effektive Magazinkapazität, tatsächlich verwendetes Magazinformat, Magazin-/Wagen-IDs, reale End-/Abhol-/Ankunftszeiten, Transportwege, Gesamtbestand, absolute Pufferbelegung, Backend-Abnahmehistorie und eindeutige physische Stückzahl über beide Seiten. Die Originalarbeitsmappe ist die Rohquelle; CSV sind aufbereitete Ableitungen mit gespeicherten Zellwerten, keine Kopie sämtlicher Excel-Formeln oder Formate.
