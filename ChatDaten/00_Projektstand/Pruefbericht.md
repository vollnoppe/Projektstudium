# Abschlussprüfung

Stand: 29.10.2026. Automatisch aus pruefen.py; Prüfungen lesen Originale und Ableitungen.

**Gesamtergebnis: bestanden**

| Prüfung | Ergebnis | Nachweis |

|---|---|---|

| Originale unverändert | bestanden | 20 SHA-256-Vergleiche; Abweichungen: [] |

| 17 Bildkopien und eindeutige Klassifikation | bestanden | Bildkopien mit Originalprüfsummen verglichen; Abweichungen: [] |

| Dokumentationsumfang | bestanden | 14 Kerndokumente und AGENTS.md vorhanden |

| Lokale Dokumentverknüpfungen | bestanden | Fehlende Ziele: [] |

| Alle Lose und Zeittexte erhalten | bestanden | 51714 Exportzeilen, 51714 Quellzeilen; LOTID, QUELLZEILE und REALSTART zeilenweise verglichen |

| Mengen und Lücken erhalten | bestanden | Quelle und Export: 20175629 bekannte Panel-Bearbeitungsvorgänge; 2 Mengenlücken |

| Unabhängige Aggregationssummen | bestanden | 8 Tabellen gegen Quellmenge, Loszahl und Fehlmengen geprüft; Abweichungen: [] |

| Backend-Dublette transparent bereinigt | bestanden | 2476 Quellzeilen; 2475 unterschiedliche Zeilen; 2475 Exportzeilen |

| Backend-Abdeckung ohne Mengenvervielfachung | bestanden | 559 BOARDTYPE, 154 mit mehreren möglichen Linien; Loszahl über alle Produkte erhalten |

| Modelllücken bleiben sichtbar | bestanden | 51714 Modellzeilen; keine Ergebniszahl trotz fehlender Menge/Kapazität: True |

| Quellenformeln aus Basiswerten nachgerechnet | bestanden | 0 Abweichungen in dokumentierten Zeit-/Mengenfeldern; gespeicherte Ergebnisse mit eigener Rechnung verglichen |

| Vier lesbare Diagrammdateien | bestanden | 4 PNG; Größe und deckender weißer Hintergrund geprüft. Sichtprüfung wird zusätzlich dokumentiert. |

| Fachliche Modelltests | bestanden | .................. ---------------------------------------------------------------------- Ran 18 tests in 0.079s  OK |



## Sichtprüfung und fachliche Grenzen

Kontaktbogen und alle vier Diagramme werden vor Übergabe visuell geprüft. Das Ergebnis der abschließenden fachlichen Durchsicht und mögliche Korrekturen stehen in Arbeitsplan.md. Die Prüfung bestätigt Quellenintegrität, Struktur und Berechnungsverarbeitung, nicht die physische Machbarkeit oder eine betriebliche Investitionsfreigabe.

Die ursprünglichen neun Modelltests wurden vor Implementierung ausgeführt und schlugen wegen fehlender Fachfunktionen fehl; nach Implementierung bestanden sie. Zusätzliche Regressionen werden im Testlauf mitgeführt.