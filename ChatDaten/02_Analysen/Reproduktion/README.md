# Analyse erneut ausführen

Die Originalarbeitsmappe wird ausschließlich gelesen. Die Skripte finden den Projektstamm relativ zu ihrem Speicherort; sie dürfen mit ChatDaten zusammen verschoben werden, solange Bilder und Daten im selben Projektstamm bleiben.

## In dieser Umgebung

PowerShell im Projektstamm:

```powershell
& 'C:\Users\Arthur\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'ChatDaten/02_Analysen/Reproduktion/auswerten.py'
& 'C:\Users\Arthur\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s 'ChatDaten/02_Analysen/Reproduktion' -p 'test_modell.py'
& 'C:\Users\Arthur\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'ChatDaten/00_Projektstand/pruefen.py'
```

Die Auswertung nutzt openpyxl (lesend), pandas, numpy und ReportLab. Die Diagramme werden zusätzlich als SVG gespeichert und durch das gebündelte Node-/Sharp-Laufzeitsystem in PNG umgewandelt. Matplotlib ist hier nicht installiert. Auf einem anderen Rechner die Abhängigkeiten einschließlich des Sharp-Aufrufs in diagramme_erstellen.py bereitstellen oder anpassen. Die ursprünglichen Laufzeitversionen stehen in Kennzahlen_und_Pruefungen.json.

## Vor einer Aktualisierung

1. Neue Originale separat inventarisieren; die historischen Prüfsummen nicht still ersetzen. Datum und Anlass protokollieren.
2. Kapazitätsparameter nur mit Quelle oder ausdrücklich gekennzeichneter Szenarioannahme ergänzen. Die Auswertung erhält bestehende Eingaben und ergänzt neue Produktschlüssel. Quelle, Status und Kapazität müssen zusammenpassen.
3. Das Skript überschreibt ausschließlich abgeleitete Tabellen, Diagramme, Kennzahlen und den Analysebericht. Es rekonstruiert keinen neuen Quellenbestand und verändert keine Originalarbeitsmappe.
4. Nach einem erfolgreichen Lauf die Ergebnisse prüfen und Dossier, Projektstand und offene Fragen inhaltlich aktualisieren. Statische Dokumente und Datumsangaben werden nicht automatisch zu einem neuen freigegebenen Stand.

CSV-Dateien nutzen UTF-8 mit BOM, Komma als Feldtrenner und Dezimalpunkt. In deutschsprachigem Excel bei Bedarf über „Daten aus Text/CSV“ importieren und Kennungen als Text behandeln.

## Modellprüfungen

18 Prüfungen sichern die Reproduktion: neun fachliche Kerntests zu Losresten, fehlenden Werten, zulässigen Mengen/Kapazitäten, losreiner Bündelung und Pufferbilanz; drei Prüfungen zu Kapazitätseingaben; sechs Regressionen zu UTC-Offsets, gleicher absoluter Zeit, gemischten Zeitbasen, Nanosekunden, großen Losen und aktualisierten Quellenhinweisen. Die neun Kerntests und sechs Regressionen wurden jeweils vor ihrer Implementierung beziehungsweise Korrektur rot und danach grün ausgeführt. Der vollständige Abschlusscheck prüft außerdem Quelldateien, Bildkopien, Verknüpfungen und Analysesummen.
