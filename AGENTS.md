# Projektregeln: Aumovio-Magazinlogistik

## Ziel und Einstieg

Dieses Universitätsgruppenprojekt entwickelt einen begründeten Vorschlag zur automatischen Übergabe ganzer Magazine zwischen Produktionsstationen und Magazinwagen. Pufferung, erneute SMT-Bereitstellung und Leergutrücklauf gehören zum Kreislauf. Es handelt sich um ein Konzeptprojekt auf Basis realer Unternehmensunterlagen.

Vor weiterer Arbeit lesen:

1. `ChatDaten/README.md` als zentralen Projektstand.
2. `ChatDaten/00_Projektstand/Entscheidungen.md` und die priorisierten offenen Fragen.
3. Bei Datenarbeit das Datenwörterbuch, bei Konzeptänderungen das Konzeptdossier und den Variantenvergleich.

## Verbindliche Arbeitsweise

- Auf Deutsch, sachlich und für Hochschule und Industrie nachvollziehbar schreiben. Keine unbelegten Leistungs-, Kosten- oder Einsparungsversprechen.
- Vorhandene Wagen und AGILOX bilden die bevorzugte Basis. Eine freiere Alternative ist erlaubt. Dies ist kein absolutes Umbauverbot.
- Aktuelles Ergebnisformat ist das Konzeptdossier. CAD, Prototyp, neue Präsentation oder Eingriffe in Produktionssteuerungen sind kein impliziter Folgeauftrag.
- Termine sind derzeit irrelevant. Es gibt kein festes Budget; teurere Vorschläge müssen durch nachweisbaren Zusatznutzen begründet werden.
- Autorisierte reversible Analyse-/Dokumentationsarbeit fortführen, ohne bereits entschiedene Fragen erneut zur Freigabe vorzulegen. Fehlende Messwerte als offene Nachweise behandeln und unabhängige Arbeit fortsetzen.

## Originalschutz und Ablage

- Originaldateien in `Bilder/` und `Daten/` nicht verändern, umbenennen, verschieben oder überschreiben. Sortierte Bildkopien und alle Ableitungen liegen in `ChatDaten/`.
- `ChatDaten/00_Projektstand/Originalpruefsummen.json` dokumentiert den ursprünglichen Bestand. Neue Quellen ergänzend inventarisieren; historische Prüfsummen nicht still ersetzen.
- Bild-IDs B001–B017, Quell-IDs Q001–Q020 sowie A-/F-/V-Referenzen stabil halten. Ein Foto hat eine Hauptkategorie; weitere Bedeutungen über Tags.
- Quellenstellen nennen. Sichtbare Beobachtung, Interpretation, Arbeitsannahme, Nutzerentscheidung und betriebliche Freigabe unterscheiden. Startfolien und zugrunde liegende Notizen sind keine unabhängigen Bestätigungen.
- Reale interne Bilder und Produktionsdaten lokal verarbeiten. Herstellerinformationen öffentlich recherchieren; keine Betriebsdaten oder Bilder an externe Dienste übermitteln und keine Ansprechpartner ohne ausdrücklichen Auftrag kontaktieren.

## Datenregeln

- Die Zeilen der Bewegungsdaten sind Produktionslose, keine einzelnen Magazintransporte. Lose, Panels, Einzelplatinen, Magazine, Wagenabgänge und Fahrzeuge nicht gleichsetzen.
- Mengen über beide Seiten nicht als eindeutige physische Stückzahl ausgeben. LOTID ist im Auszug eindeutig, verknüpft aber nicht nachweislich dasselbe Material über mehrere Bearbeitungen.
- Mengen nach Losstart nur als solche ausweisen. Keine tatsächlichen Fertigstellungs-, Transport- oder Abnahmespitzen daraus behaupten. Zeitzone nicht erfinden.
- Fehlende Menge/Kapazität bleibt fehlend. Keine pauschale Magazinkapazität unterstellen. Kapazitäten benötigen Produkt-/Seiten-/Revisionsbezug, Status und Quelle; weitere Variantenbedingungen bei Bedarf explizit ergänzen.
- Backend enthält Stammzeiten und mögliche Produkt-/Linienzuordnungen. Kein 1:n-Join darf Mengen vervielfachen; kein beliebiges erstes oder vermeintliches Default-Ziel auswählen.
- Fehlendes Zwischenziel beweist keinen Backend-Abgang; gleiches Quell-/Ziellinienfeld beweist keine Fahrt zwischen verschiedenen Linien. Routingsemantik offenhalten, bis F05/F06 geklärt sind.
- Absolute Pufferbelegung benötigt Anfangsbestand und echte Zu-/Abgänge. Fahrzeugzahl benötigt Umlauf-/Warte-/Ladezeiten. Hypothetische Beispiele unmittelbar als solche kennzeichnen.
- Originalarbeitsmappe ausschließlich lesend öffnen. Bereinigungen nur abgeleitet, mit Quellzeile und Begründung. Zahlen, Einheiten, Zeitbasis und Datenabdeckung dokumentieren.

## Reproduktion, Prüfung und Fortschreibung

- Reproduktionsanleitung: `ChatDaten/02_Analysen/Reproduktion/README.md`. Keine Abhängigkeitsverzeichnisse des gebündelten Laufzeitsystems verändern.
- Bei Änderungen an Rechenlogik die fachlichen Modelltests und unabhängigen Summen-/Quellenprüfungen ausführen. Diagramme visuell auf Achsen, Einheiten und Lesbarkeit prüfen.
- Abschlussprüfung: `ChatDaten/00_Projektstand/pruefen.py`; Ergebnis im Prüfbericht halten. Keine Abschlussbehauptung ohne tatsächlich gelaufene Prüfung.
- Neue Erkenntnisse in Fragenliste/Entscheidungslog eintragen und betroffene Analyse, Anforderungen, Varianten und Dossier aktualisieren. `ChatDaten/README.md` muss zum Dossier passen.
- Diese Datei enthält Arbeitsregeln, nicht alle aktuellen Kennzahlen. Fachliche Zahlen und offene Nachweise bleiben in den verlinkten Dokumenten maßgeblich.
