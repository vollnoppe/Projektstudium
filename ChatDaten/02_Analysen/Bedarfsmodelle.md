# Offene Bedarfsmodelle

Stand: 29.10.2026. Die Modelle sind vorbereitet und an kleinen Fällen geprüft. Sie ersetzen fehlende betriebliche Eingaben nicht durch vermeintliche Istwerte. [Analysebericht](Analysebericht.md), [Fragenliste](../00_Projektstand/Offene_Fragen_Aumovio.md).

## 1. Von Panels zu Magazinen und Wagen

Für Los i gilt im ausdrücklich **losreinen Szenario**:

`Magazine_i = ceil(Panelmenge_i / wirksame Panels je Magazin_i)`

`beladene Wagenabgänge_i = ceil(Magazine_i / nutzbare Wagenplätze)`

`Restpanels_i = Panelmenge_i mod wirksame Panels je Magazin_i`

„Restpanels = 0“ bedeutet kein angebrochenes letztes Magazin, nicht ein leeres letztes Magazin. Der letzte Wagen kann dennoch teilweise belegt sein. Das Modell nimmt zunächst vier nutzbare Wagenplätze an (A04/M06). Nicht gefüllte Wagen müssen bei Losende beziehungsweise Freigabebedarf abfahren können; das reine Warten auf vier Magazine ist keine zulässige universelle Strategie.

**Bedeutung:** Das Ergebnis zählt eine modellierte Abgangsrichtung je Los. Es ist keine Anzahl physischer Fahrzeuge und kein vollständiger Rundfahrtbedarf. Leergut, Umlagerungen, Wiederverwendung eines Wagens, Fahrtzeiten, Rückläufe und gemischte Wagenaufträge benötigen zusätzliche Modellierung. Auch eine Kapazität mit Status „bestaetigt“ macht aus Produktionslosdaten keine beobachteten Fahrten.

### Kapazitätstabelle

Die Datei [Eingaben/Magazinkapazitaeten.csv](Eingaben/Magazinkapazitaeten.csv) enthält die 1.000 im Original vorhandenen Schlüssel aus BOARDTYPE, SIDE und REVISION. `panels_pro_magazin` ist zunächst leer. Mit `status=Annahme` und einer expliziten Szenarioquelle kann eine Sensitivität gerechnet werden. `status=bestaetigt` setzt einen betriebsbezogenen Nachweis voraus. Null, negative oder gebrochene Kapazitäten und doppelte Schlüssel werden abgewiesen.

Wenn für denselben Schlüssel mehrere Magazinbauformen oder Linienbedingungen unterschiedliche Kapazitäten erzeugen, muss der Schlüssel vor einer solchen Rechnung entsprechend erweitert werden. Es wird kein beliebiges Format ausgewählt. Eine Quellenangabe ist bei jedem eingetragenen Kapazitätswert erforderlich. Nach neuer Quelle/Produktschlüssel wird die Vorlage um neue Schlüssel ergänzt; bestehende Eingaben bleiben erhalten.

### Rechenbeispiele, keine Aumovio-Kapazitäten

| Panelmenge | Hypothetische Panels je Magazin | Magazine | Losreine Wagenabgänge bei 4 Plätzen | Restpanels |
|---|---|---|---|---|
| 399 | 20 | 20 | 5 | 19 |
| 399 | 25 | 16 | 4 | 24 |
| 399 | 50 | 8 | 2 | 49 |
| 101 | 25 | 5 | 2 | 1 |
| 1 | 25 | 1 | 1 | 1 |

399 entspricht dem beobachteten Median der mengenbekannten Lose; **20/25/50 sind frei gewählte Demonstrationsparameter**. Diese Beispiele werden nicht auf den historischen Datensatz übertragen. Sie zeigen, warum Stück-/Panelmenge ohne wirksame Belegung keine belastbare Magazinzahl ergibt. Die numerischen Beispiele werden separat durch die Modellfunktion erzeugt.

## 2. Liniennaher Übergabepuffer

Er soll die Produktion während Wagenwechsel, Abholwartezeit und kurzer Störungen entkoppeln. Er ist vom Lager für mehrere Produktionsschritte zu unterscheiden.

Ein erster konservativer Szenarioansatz ist `freie Magazinplätze >= ceil(Spitzenankunftsrate_Magazine_pro_s × Überbrückungszeit_s)` plus explizit benötigte Übergabe-/Wechselplätze. Dabei sind **Spitzenrate, Überbrückungszeit und freie Plätze** Eingaben, keine aus Losstarts abgeleiteten Istwerte. Die Verfügbarkeit eines noch in Befüllung befindlichen Magazins darf nicht als freier Reserveplatz gezählt werden. Die drei sichtbaren Stationsplätze sagen daher nicht, wie lange die Linie ohne Abholung weiterlaufen kann.

Die Stationsbedienzeit je Wagenauftrag setzt sich aus Anfahren/Andocken, Identifikation, Positionieren/Verriegeln, den einzelnen Magazintransfers und Freigabe/Abfahrt zusammen. Nötige Wechsel- und Leergutzyklen zählen zusätzlich. Ein theoretischer Mittelwert unter der Kapazitätsgrenze belegt noch keine Beherrschung gleichzeitiger Anforderungen.

Für den Nachweis: echte Magazinwechsel einer Pilotlinie verwenden, Zeitraster/Ereignisse einschließlich Losresten abspielen und Blockierung bei verzögerter Abholung, vollem Zielpuffer und fehlendem Leergut prüfen. Keine globale Dimensionierung aus „15 Losstarts pro Stunde“ ableiten.

## 3. Puffer zwischen SMT und nächstem Prozess

Für jedes klar abgegrenzte Puffersegment und jede Zeit t gilt:

`Bestand(t) = belegter Anfangsbestand + kumulierte Zugänge(t) − kumulierte Abgänge(t)`

Die Funktion `pufferbestand` verlangt Anfangsbestand und Ereignisse in ganzen Magazinen. Sie sortiert Zeitpunkte, bilanziert gleiche Zeitpunkte gemeinsam und weist einen negativen Bestand als Daten-/Modellwiderspruch zurück. Explizite UTC-Offsets werden auf UTC normalisiert; bei offsetlosen Daten wird keine Zeitzone erfunden. Gemischte offsetlose/offsetbehaftete Eingaben werden zurückgewiesen. Nanosekunden bleiben erhalten. Das ist eine Netto-Konvention bei Gleichzeitigkeit; kurzfristige Übergabeplätze müssen separat berücksichtigt werden.

[Pufferereignisse_Vorlage.csv](Eingaben/Pufferereignisse_Vorlage.csv) enthält nur Spalten, keine erfundenen Bewegungen. Anfangsbestand muss separat je Puffer vorgegeben werden. Eine reale maximale Belegung kann erst mit F07/F08 bestimmt werden. Eine 24-Stunden-Regel aus der Mitschrift wird nicht pauschal als erforderliche Lagerdauer angesetzt.

Little's Law `mittlerer Bestand = mittlerer Durchsatz × mittlere Verweilzeit` kann nach Bestätigung der Grundlagen eine Plausibilisierung stationärer Mittelwerte liefern. Es ersetzt keine Spitzen-, Sperr- oder Wiederanlaufanalyse. Die vorhandenen Backend-Stammzeiten liefern weder Belegungsplan noch Schichtkalender oder tatsächliche Abnahme.

## 4. Sensitivitäten und Akzeptanz

Mit nachgereichten Daten getrennt prüfen: Produkt-/Seitenmix, Magazinkapazität, Wagenbündelung, Restlosfreigabe, Wechselzeit, Abholverzug, Backend-Abnahme, Sperrbestand und Störungen. Nur belegte Grenzen oder klar bezeichnete Szenariowerte verwenden. Ergebnisse benötigen jeweils Quellenumfang, fehlende Mengen, Anfangsbestand, Zeitbasis und Modellregeln.

Für die Freigabe müssen Los-/Panelmengen erhalten bleiben, Restmagazine vollständig erfasst sein, keine Mengen über Zielalternativen vervielfacht werden, das Pufferkonto stimmen und alle physisch nötigen Wechselplätze berücksichtigt sein. Aktuell bleiben verbindliche Magazin-/Wagenzahlen, Puffergröße, Stationszahl und Flottenbedarf offen.
