# Fachliche Abschlussdurchsicht

Stand: 29.10.2026. Unabhängige agentische Durchsicht der Unterlagen, Datenableitungen und Rechenlogik; keine betriebliche Sicherheits-, Machbarkeits- oder Investitionsfreigabe.

## Bestätigte Stärken

- Die priorisierte Variante V1 umfasst ausdrücklich auch die automatische Übergabe an der Zielstation. Leergut, Losende, Teilbelegung und Störungen sind berücksichtigt.
- Die Empfehlung ist angemessen bedingt. Es wurden keine unbelegten definitiven Puffer-, Fahrzeug- oder Leistungsbemessungen gefunden.
- Losstarts, Panel-Bearbeitungsvorgänge, eindeutige physische Panels, Magazine, Wagenabgänge und Fahrzeuge werden getrennt behandelt.
- Die Durchsicht bestätigte zusätzlich lesend die 20 Originalprüfsummen, 17 Bildkopien, 51.714 eindeutigen Exportlose und die bekannte Mengensumme. LOTID und Panelmenge wurden für alle Quell-/Exportzeilen verglichen.

## Befunde und Korrekturen

| Befund | Auswirkung | Korrektur / Nachweis |
|---|---|---|
| Unterschiedliche UTC-Offsets wurden im vorbereiteten Puffermodell als Zeichenketten sortiert | Bei späteren offsetbehafteten Ereignisdaten, etwa Zeitumstellung, war eine falsche Reihenfolge/Unterdeckung möglich; aktuelle historische Kennzahlen nicht betroffen | Zeitobjekte verwenden, explizite Offsets auf UTC normalisieren, offsetlose Daten beibehalten und gemischte Zeitbasen ablehnen. Vier Regressionen einschließlich gleicher absoluter Zeit und Nanosekunden erst rot, dann grün |
| Histogramm hatte eine feste obere Klassengrenze | Neue Lose über 2.400 Panels konnten bei späteren Datenlieferungen aus dem Diagramm fallen; aktuelles Maximum 2.265 war enthalten | Obergrenze aus beobachtetem Maximum ableiten, Gesamtzählung prüfen. Regression mit 399/2.500/2.501 Panels erst rot, dann grün |
| Automatisch erzeugte Quellenhinweise enthielten feste Fehlmengen-/Dubletten-/Periodenangaben | Bei neuer Datengrundlage konnten frisch erzeugte Beschriftungen veraltet sein | Als relevanten Bestandteil desselben Aktualisierungswegs korrigiert: Werte aus dem jeweils eingelesenen Datensatz erzeugen. Regression mit neuem Zeitraum sowie null/sieben Mengenlücken und vier Dubletten erst rot, dann grün |

Die Korrekturen wurden in einem Durchgang umgesetzt. Anschließend wurden die vollständige 18er-Testsuite, die Datenauswertung und die unabhängige Abschlussprüfung erneut ausgeführt. Die zugehörigen aktuellen Resultate stehen im [Prüfbericht](Pruefbericht.md).

## Fachlich weiterhin offen

Physische Machbarkeit, Sicherheitsfreigabe, reale Zyklusleistung und tatsächliche Wirtschaftlichkeit benötigen die bereits benannten betrieblichen Nachweise. Sie wurden nicht als bewiesen behandelt. Die Durchsicht ersetzt keine Zeichnungen, Zeitaufnahmen, Anlagenfreigaben oder Angebote. Die Prüfungen, die Dateien erzeugen, hat der ausführende Agent vorgenommen; die unabhängige Durchsicht war lesend.
