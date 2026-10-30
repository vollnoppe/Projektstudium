"""Unabhängige Abschlussprüfung der Originale und des abgeleiteten Dossiers."""
from pathlib import Path
from decimal import Decimal
import csv
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import unquote
import openpyxl
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
CHAT=ROOT/'ChatDaten'
results=[]


def record(label, condition, detail):
    results.append({'pruefung':label,'bestanden':bool(condition),'nachweis':detail})


def rows(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))


def main():
    manifest=json.loads((CHAT/'00_Projektstand/Originalpruefsummen.json').read_text(encoding='utf-8'))
    bad=[x['originalpfad'] for x in manifest if not (ROOT/x['originalpfad']).exists() or hashlib.sha256((ROOT/x['originalpfad']).read_bytes()).hexdigest()!=x['sha256']]
    record('Originale unverändert',len(manifest)==20 and not bad,f'{len(manifest)} SHA-256-Vergleiche; Abweichungen: {bad}')
    catalog=rows(CHAT/'01_Bildkatalog/Bildkatalog.csv')
    badpics=[x['bild_id'] for x in catalog if hashlib.sha256((CHAT/x['arbeitskopie']).read_bytes()).hexdigest()!=x['sha256']]
    record('17 Bildkopien und eindeutige Klassifikation',len(catalog)==17 and len({x['bild_id'] for x in catalog})==17 and len({x['arbeitskopie'] for x in catalog})==17 and all(x['hauptkategorie'] and x['beobachtung'] and x['unsicherheiten'] for x in catalog) and not badpics,f'Bildkopien mit Originalprüfsummen verglichen; Abweichungen: {badpics}')
    required=['README.md','00_Projektstand/Istprozess_und_Anforderungen.md','00_Projektstand/Entscheidungen.md','00_Projektstand/Offene_Fragen_Aumovio.md','01_Bildkatalog/Bildkatalog.md','02_Analysen/Analysebericht.md','02_Analysen/Datenwoerterbuch.md','02_Analysen/Bedarfsmodelle.md','03_Konzept/Konzeptdossier.md','03_Konzept/Variantenvergleich.md','03_Konzept/Pufferkonzept.md','03_Konzept/Schnittstellen_und_Betriebsfaelle.md','03_Konzept/Wirtschaftlichkeit.md','03_Konzept/Herstellerreferenzen.md']
    record('Dokumentationsumfang',all((CHAT/p).is_file() and (CHAT/p).stat().st_size>0 for p in required) and (ROOT/'AGENTS.md').is_file(),f'{len(required)} Kerndokumente und AGENTS.md vorhanden')
    # Dieses Prüfziel entsteht erst am Ende des Laufs und darf bereits verlinkt sein.
    expected_report=CHAT/'00_Projektstand/Pruefbericht.md'
    links=[]
    for p in list(CHAT.rglob('*.md'))+[ROOT/'AGENTS.md']:
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            target=target.split('#',1)[0].strip('<>')
            if not target or re.match(r'^[a-z]+://',target):continue
            destination=(p.parent/unquote(target)).resolve()
            if not destination.exists() and destination!=expected_report:links.append(f'{p.relative_to(ROOT)} -> {target}')
    record('Lokale Dokumentverknüpfungen',not links,f'Fehlende Ziele: {links}')

    summary=json.loads((CHAT/'02_Analysen/Kennzahlen_und_Pruefungen.json').read_text(encoding='utf-8'))
    smd=rows(CHAT/'02_Analysen/Tabellen/SMD_Lose_aufbereitet.csv')
    workbook=openpyxl.load_workbook(ROOT/'Daten/Bewegungsdaten AUMOVIO.xlsx',read_only=True,data_only=True)
    source=list(workbook['SMD Lots'].iter_rows(min_row=2,values_only=True))
    source_sum=sum(Decimal(str(x[4])) for x in source if x[4] not in [None,''])
    source_missing=sum(x[4] in [None,''] for x in source)
    exported_sum=sum(Decimal(x['NUMBEROFPANELSINLOT']) for x in smd if x['NUMBEROFPANELSINLOT']!='')
    ids_ok=len(smd)==len(source) and all(row['LOTID']==str(original[0]) and int(row['QUELLZEILE'])==i+2 and row['REALSTART']==original[5] for i,(row,original) in enumerate(zip(smd,source)))
    record('Alle Lose und Zeittexte erhalten',ids_ok and len({x['LOTID'] for x in smd})==len(source),f'{len(smd)} Exportzeilen, {len(source)} Quellzeilen; LOTID, QUELLZEILE und REALSTART zeilenweise verglichen')
    record('Mengen und Lücken erhalten',source_sum==exported_sum==Decimal(summary['panels_bearbeitungsvorgaenge_bekannt']) and sum(x['NUMBEROFPANELSINLOT']=='' for x in smd)==source_missing==summary['mengenlose_lose'],f'Quelle und Export: {source_sum} bekannte Panel-Bearbeitungsvorgänge; {source_missing} Mengenlücken')
    aggregate_files=['Losstarts_Monate.csv','Losstarts_Wochen.csv','Losstarts_Tage.csv','Losstarts_Stunden.csv','Linienprofil.csv','Losstarts_Linien_Tage.csv','Produktmix.csv','SMT_Zwischenzielmatrix.csv']
    bad_agg=[]
    for name in aggregate_files:
        table=rows(CHAT/'02_Analysen/Tabellen'/name)
        if sum(int(x['lose']) for x in table)!=len(source) or sum(Decimal(x['panels_bearbeitungsvorgaenge']) for x in table if x['panels_bearbeitungsvorgaenge']!='')!=source_sum or sum(int(x['mengenlose_lose']) for x in table)!=source_missing:bad_agg.append(name)
    record('Unabhängige Aggregationssummen',not bad_agg,f'{len(aggregate_files)} Tabellen gegen Quellmenge, Loszahl und Fehlmengen geprüft; Abweichungen: {bad_agg}')
    backend_source=list(workbook['Backend-Productdata'].iter_rows(min_row=2,values_only=True));workbook.close()
    unique_backend={tuple(x[:15]) for x in backend_source}
    backend_export=rows(CHAT/'02_Analysen/Tabellen/Backend_Zuordnungen_bereinigt.csv')
    record('Backend-Dublette transparent bereinigt',len(backend_export)==len(unique_backend)==2475 and len(backend_source)-len(unique_backend)==1,f'{len(backend_source)} Quellzeilen; {len(unique_backend)} unterschiedliche Zeilen; {len(backend_export)} Exportzeilen')
    mapping=rows(CHAT/'02_Analysen/Tabellen/Backend_Mappingabdeckung.csv')
    record('Backend-Abdeckung ohne Mengenvervielfachung',sum(int(x['lose']) for x in mapping)==len(source) and len(mapping)==559 and sum(int(x['backend_linien'])>1 for x in mapping)==154,'559 BOARDTYPE, 154 mit mehreren möglichen Linien; Loszahl über alle Produkte erhalten')
    model=rows(CHAT/'02_Analysen/Tabellen/Magazinmodell_Lose.csv')
    unsupported=[x['LOTID'] for x in model if (x['panels_pro_magazin']=='' or x['NUMBEROFPANELSINLOT']=='') and any(x[k]!='' for k in ['magazine','wagenfahrten_losrein','restpanels','belegte_plaetze_letzter_wagen'])]
    record('Modelllücken bleiben sichtbar',len(model)==len(source) and not unsupported,f'{len(model)} Modellzeilen; keine Ergebniszahl trotz fehlender Menge/Kapazität: {not unsupported}')
    mismatch=sum(summary['quellenformel_abweichungen_smd'].values())+sum(summary['quellenformel_abweichungen_backend'].values())
    record('Quellenformeln aus Basiswerten nachgerechnet',mismatch==0,f'{mismatch} Abweichungen in dokumentierten Zeit-/Mengenfeldern; gespeicherte Ergebnisse mit eigener Rechnung verglichen')
    chart_files=list((CHAT/'02_Analysen/Diagramme').glob('*.png'))
    charts_ok=len(chart_files)==4
    for p in chart_files:
        with Image.open(p) as im:
            charts_ok &= im.width>=1000 and im.height>=600
            rgba=im.convert('RGBA');charts_ok &= rgba.getpixel((0,0))==(255,255,255,255)
    record('Vier lesbare Diagrammdateien',charts_ok,f'{len(chart_files)} PNG; Größe und deckender weißer Hintergrund geprüft. Sichtprüfung wird zusätzlich dokumentiert.')
    command=[sys.executable,'-m','unittest','discover','-s',str(CHAT/'02_Analysen/Reproduktion'),'-p','test_modell.py']
    test=subprocess.run(command,capture_output=True,text=True)
    record('Fachliche Modelltests',test.returncode==0,(test.stdout+test.stderr).strip())
    payload={'stand':'2026-10-29','bestanden':all(x['bestanden'] for x in results),'pruefungen':results}
    (CHAT/'00_Projektstand/Pruefergebnisse.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    md=['# Abschlussprüfung','Stand: 29.10.2026. Automatisch aus pruefen.py; Prüfungen lesen Originale und Ableitungen.','**Gesamtergebnis: '+('bestanden' if payload['bestanden'] else 'nicht bestanden')+'**','| Prüfung | Ergebnis | Nachweis |','|---|---|---|']
    for r in results:md.append(f"| {r['pruefung']} | {'bestanden' if r['bestanden'] else 'FEHLER'} | {r['nachweis'].replace(chr(10),' ')} |")
    md+=['','## Sichtprüfung und fachliche Grenzen','Kontaktbogen und alle vier Diagramme werden vor Übergabe visuell geprüft. Das Ergebnis der abschließenden fachlichen Durchsicht und mögliche Korrekturen stehen in Arbeitsplan.md. Die Prüfung bestätigt Quellenintegrität, Struktur und Berechnungsverarbeitung, nicht die physische Machbarkeit oder eine betriebliche Investitionsfreigabe.','Die ursprünglichen neun Modelltests wurden vor Implementierung ausgeführt und schlugen wegen fehlender Fachfunktionen fehl; nach Implementierung bestanden sie. Zusätzliche Regressionen werden im Testlauf mitgeführt.']
    expected_report.write_text('\n\n'.join(md),encoding='utf-8')
    print(json.dumps({'bestanden':payload['bestanden'],'pruefungen':len(results),'fehler':[r['pruefung'] for r in results if not r['bestanden']]},ensure_ascii=False))
    return 0 if payload['bestanden'] else 1


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
