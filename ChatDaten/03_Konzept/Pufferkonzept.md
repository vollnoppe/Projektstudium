# Pufferkonzept für Magazinlogistik

Stand: 29.10.2026. Eine verbindliche Größe ist mangels F02/F07/F08/F12 nicht bestimmbar. Dieses Teilkonzept legt Struktur und Nachweismethode fest. Rechenregeln: [Bedarfsmodelle](../02_Analysen/Bedarfsmodelle.md).

## Zwei unterschiedliche Aufgaben

| Ebene | Zweck | Wesentliche Eingaben | Ergebnis nach Nachweis |
|---|---|---|---|
| Liniennaher Übergabepuffer | Wagenwechsel, Abholverzug und kurze Störung ohne unnötige Produktionsunterbrechung überbrücken | Magazinankunftsfolge, freie Plätze, Wechselzeit, Abholverzug und Leergut | Freie Reserveplätze, Wechsel-/Warteplätze, zulässige Überbrückungszeit |
| Produktionsentkopplung | Magazine bis zur nächsten SMT-Bearbeitung oder Backend-Abnahme verfügbar halten | Zu-/Abgangsereignisse, Anfangsbestand, Bedarfstermine, Sperrbestand und Dispositionsregeln | Kapazität und Zuordnung je Puffersegment, Verweilzeit und Abdeckungsgrenze |

In Arbeit befindliche Magazine, transportbereite Magazine, gesperrtes Material und Leergut werden getrennt geführt. Ein Wagen im Fahrweg ist kein zulässiger zusätzlicher Pufferplatz. Die 24-Stunden-Angabe in Q019 Z. 48 ist unklar und bleibt unbestätigt.

## Lagerung auf Wagen oder als Einzelmagazine

| Lösung | Möglicher Nutzen | Zu prüfender Nachteil |
|---|---|---|
| Wagenweise Bereitstellung im Bestand | Vorhandene Wagen und Transportaufnahme nutzen; nach Beladung wenig zusätzliche Magazinhandhabung | Wagen länger gebunden; teilbelegte Wagen und unterschiedliche Bedarfszeiten belegen Fläche; Zugriff auf einzelnes Magazin nötig |
| Einzelmagazin-Puffer mit automatischer Ein-/Ausgabe | Bedarfsgerechter Zugriff und Entkopplung von Wagenumlauf möglich | Zusätzliche Transfers und Anlage; mechanische Kompatibilität, Identifikation, Kapazität und Ausfallszenario offen |
| Kombination | Kurzfristige, zielreine Wagenbereitstellung und gezielte Einzelmagazin-Pufferung bei belegtem Bedarf | Mehr Schnittstellen und Dispositionsregeln, die ihren Nutzen nachweisen müssen |

**Arbeitsvorschlag:** Wagenweise kurzfristige Bereitstellung als Basisszenario untersuchen. Einen Einzelmagazin-Puffer dort vertiefen, wo gemessene Verweilzeiten, Zugriffsmuster oder Wagen-/Flächenbindung den zusätzlichen Transfer und Anlagenaufwand rechtfertigen. Die Fotos des Lagerbereichs belegen vorhandene Strukturen, aber weder freie Kapazität noch Eignung für automatische Einzelmagazinlagerung.

## Disposition auf Konzeptebene

Ein Auftrag benötigt ein konkretes nächstes Ziel. Vor Abfahrt muss ein geeigneter Zielplatz reserviert sein. Gleiches Los/Ziel kann gebündelt werden; ob verschiedene Lose oder Produkte denselben Wagen teilen dürfen, entscheidet die betriebliche Regel F12. Bei Losende oder zeitkritischem Folgeprozess darf eine Teilbelegung freigegeben werden. Ein fester Zeitschwellwert wird ohne Dispositionsnachweis nicht gesetzt.

Leergutversorgung ist ein eigener Bedarf. Freie Wagenplätze allein helfen nicht, wenn passende leere Magazine fehlen. Gesperrte Magazine brauchen eine identifizierbare, zulässige Abstellmöglichkeit und dürfen nicht als verfügbarer Bestand für den Folgeprozess zählen.

## Nachweis und Szenarien

1. Pro Puffer den Anfangsbestand sowie vollständige Zugänge und Abgänge mit einer gemeinsamen Zeit-/Mengeneinheit erfassen. Datenlücken und Sperrbestände markieren.
2. Verlauf und Maximum der Belegung aus der Bilanz berechnen. Nicht mit einer frei auf null gesetzten Anfangsbelegung starten.
3. Gemessene Verzögerungen, eine verspätete Backend-Abnahme, hohe Produktwechselzahl, Teilwagen und Wiederanlauf nach Störung prüfen. Annahmen neben jeder Szenariokurve nennen.
4. Nutzbare Plätze um Übergabe-, Wartungs- und Sperrbedarf ergänzen. Berechnete Nettobelegung ist nicht automatisch der gesamte bauliche Platzbedarf.
5. Wagenbasierte und Einzelmagazin-Lösung auf demselben Mengen-/Zeitumfang vergleichen. Ein Mittelwert genügt nicht für den Spitzenlastnachweis.

**Aktueller Stand:** Keine belastbare Zahl für Pufferplätze, Verweilzeit, Wagenumlauf oder AGV-Flottengröße. Die vorbereiteten Daten-/Modelltabellen erlauben eine gezielte Fortschreibung, sobald die genannten Nachweise vorliegen.
