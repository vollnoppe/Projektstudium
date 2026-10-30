"""Lesende Auswertung der Aumovio-Arbeitsmappe. Start: python auswerten.py.

Keine Änderungen an Originalen. CSV sind UTF-8 mit BOM, Komma als Feldtrenner,
Dezimalpunkt und leeren Feldern für fehlende Werte. Alle Zeiten ohne bestätigte
Zeitzone. Eingabetabellen werden bei Wiederholung erhalten und nur um neue
Produktschlüssel ergänzt.
"""
from pathlib import Path
import collections
import csv
import hashlib
import json
import math
import platform
import sys

import reportlab
import numpy as np
import openpyxl
import pandas as pd
from modell import magazinbedarf
from diagramme_erstellen import diagramme, quellenhinweise

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'ChatDaten/02_Analysen'
TABLES = OUT/'Tabellen'
CHARTS = OUT/'Diagramme'
INPUTS = OUT/'Eingaben'
SOURCE = ROOT/'Daten/Bewegungsdaten AUMOVIO.xlsx'
KEY = ['BOARDTYPE','SIDE','REVISION']


def save(frame, name):
    frame.to_csv(TABLES/name,index=False,encoding='utf-8-sig')


def fmt(value, decimals=0):
    if value is None or pd.isna(value):return 'offen'
    return f'{value:,.{decimals}f}'.replace(',','X').replace('.',',').replace('X','.')


def md_table(frame):
    rows=[list(frame.columns)]+frame.fillna('offen').astype(str).values.tolist()
    return '\n'.join(['| '+' | '.join(rows[0])+' |','| '+' | '.join(['---']*len(rows[0]))+' |']+['| '+' | '.join(r)+' |' for r in rows[1:]])


def load_sheet(workbook, name):
    rows=list(workbook[name].iter_rows(values_only=True))
    headers=list(rows[0]); width=max(i for i,x in enumerate(headers) if x is not None)+1
    return pd.DataFrame([row[:width] for row in rows[1:]],columns=headers[:width]).assign(QUELLZEILE=np.arange(2,len(rows)+1))


def read_capacity_template(df):
    path=INPUTS/'Magazinkapazitaeten.csv'
    keys=df[KEY].drop_duplicates().sort_values(KEY).astype(str)
    if path.exists():
        capacity=pd.read_csv(path,dtype=str,keep_default_na=False)
        required=KEY+['magazintyp','panels_pro_magazin','status','quelle']
        if not set(required).issubset(capacity.columns):raise ValueError('Kapazitätstabelle: erforderliche Spalten fehlen')
        if capacity.duplicated(KEY).any():raise ValueError('Kapazitätstabelle: mehrdeutige Produktschlüssel; keine automatische Erstauswahl')
        missing=keys.merge(capacity[KEY],how='left',on=KEY,indicator=True)
        missing=missing[missing['_merge']=='left_only'][KEY]
        if len(missing):
            for name in ['magazintyp','panels_pro_magazin','quelle']:missing[name]=''
            missing['status']='offen'
            capacity=pd.concat([capacity,missing],ignore_index=True)
    else:
        capacity=keys.copy()
        for name in ['magazintyp','panels_pro_magazin','quelle']:capacity[name]=''
        capacity['status']='offen'
    for _,row in capacity.iterrows():
        if row['panels_pro_magazin']!='':
            n=float(row['panels_pro_magazin'])
            if not math.isfinite(n) or n<=0 or not n.is_integer():raise ValueError('Magazinkapazität muss eine positive ganze Zahl sein')
            if row['status'] not in ['Annahme','bestaetigt']:raise ValueError('Eingetragene Kapazität braucht status Annahme oder bestaetigt')
            if not row['quelle'].strip():raise ValueError('Eingetragene Kapazität braucht eine Quelle oder eine explizite Szenario-Begründung')
    capacity.to_csv(path,index=False,encoding='utf-8-sig')
    return capacity


def main():
    for p in [TABLES,CHARTS,INPUTS]:p.mkdir(parents=True,exist_ok=True)
    workbook=openpyxl.load_workbook(SOURCE,read_only=True,data_only=True)
    df=load_sheet(workbook,'SMD Lots');backend=load_sheet(workbook,'Backend-Productdata');workbook.close()
    original_columns=[c for c in df.columns if c!='QUELLZEILE']
    df['LOTID']=df['LOTID'].map(str)
    for c in ['REALAMOUNT','NUMBERPERPANEL','NUMBEROFPANELSINLOT','OISNETTIMEPERPANEL','OISNETTIMEPERPANELSEC','OIBCYCLETIME','OIBCYCLETIMESEC','RELEVANTNETTIMESEC','AVGTARGETOISNETTIMEPERPANEL','AVGTARGETOISNETTIMEPERPANELSEC','AVGTARGETOIBCYCLETIME','AVGTARGETOIBCYCLETIMESEC','RELEVANTTARGETNETTIMESEC']:
        df[c]=pd.to_numeric(df[c],errors='raise')
    stamps=pd.to_datetime(df['REALSTART'],format='%d.%m.%y %H:%M:%S,%f',errors='raise')
    df['REALSTART_ISO']=stamps.map(lambda x:x.isoformat())
    df['LOSSTART_STUNDE']=stamps.dt.floor('h')
    df['LOSSTART_TAG']=stamps.dt.floor('D')
    df['LOSSTART_MONAT']=stamps.dt.strftime('%Y-%m')
    df['MENGE_FEHLT']=df['NUMBEROFPANELSINLOT'].isna()
    df['IDEALE_NETTO_DAUER_S']=df['NUMBEROFPANELSINLOT']*df['RELEVANTNETTIMESEC']
    capacity=read_capacity_template(df)
    backend_columns=[c for c in backend.columns if c!='QUELLZEILE']
    duplicate_mask=backend.duplicated(backend_columns,keep='first')
    hints=quellenhinweise(stamps,int(df['MENGE_FEHLT'].sum()),int(duplicate_mask.sum()))
    clean_backend=backend[~duplicate_mask].copy()
    by_board={key:group for key,group in clean_backend.groupby('SMDBOARDTYPE')}
    coverage=[]
    for board,group in df.groupby('BOARDTYPE'):
        bg=by_board.get(board)
        lines=sorted(bg['LINE'].unique()) if bg is not None else []
        defaults=sorted(bg.loc[bg['ISDEFAULT']==1,'LINE'].unique()) if bg is not None else []
        coverage.append({'BOARDTYPE':board,'lose':len(group),'panels_bearbeitungsvorgaenge':group['NUMBEROFPANELSINLOT'].sum(min_count=1),'backend_zeilen':len(bg) if bg is not None else 0,'backend_linien':len(lines),'default_linien':len(defaults),'linien_liste':' / '.join(lines),'default_liste':' / '.join(defaults),'zuordnung_status':'keine Stammdatenzuordnung' if not lines else 'eine mögliche Linie' if len(lines)==1 else 'mehrere mögliche Linien'})
    coverage=pd.DataFrame(coverage).sort_values('lose',ascending=False)
    lookup=coverage.set_index('BOARDTYPE')
    df['BACKEND_LINIEN_ANZAHL']=df['BOARDTYPE'].map(lookup['backend_linien'])
    df['BACKEND_DEFAULT_LINIEN_ANZAHL']=df['BOARDTYPE'].map(lookup['default_linien'])
    df['BACKEND_MAPPING_STATUS']=df['BOARDTYPE'].map(lookup['zuordnung_status'])

    # Quellenformeln unabhängig aus Basiswerten nachrechnen, keine Excel-Speicherung.
    checks={}
    for raw,seconds in [('OISNETTIMEPERPANEL','OISNETTIMEPERPANELSEC'),('OIBCYCLETIME','OIBCYCLETIMESEC'),('AVGTARGETOISNETTIMEPERPANEL','AVGTARGETOISNETTIMEPERPANELSEC'),('AVGTARGETOIBCYCLETIME','AVGTARGETOIBCYCLETIMESEC')]:
        expected=df[raw]/10000000
        checks[seconds]=int((~np.isclose(expected,df[seconds],equal_nan=True,rtol=0,atol=1e-8)).sum())
    for output,first,second in [('RELEVANTNETTIMESEC','OISNETTIMEPERPANELSEC','OIBCYCLETIMESEC'),('RELEVANTTARGETNETTIMESEC','AVGTARGETOISNETTIMEPERPANELSEC','AVGTARGETOIBCYCLETIMESEC')]:
        expected=df[first].fillna(df[second]);checks[output]=int((~np.isclose(expected,df[output],equal_nan=True,rtol=0,atol=1e-8)).sum())
    checks['Stunde_vs_REALSTART']=int((pd.to_datetime(df['Stunde'])!=df['LOSSTART_STUNDE']).sum())
    quantity_ok=df[['REALAMOUNT','NUMBERPERPANEL','NUMBEROFPANELSINLOT']].notna().all(axis=1)
    checks['REALAMOUNT_vs_Panels_mal_Nutzen']=int((df.loc[quantity_ok,'REALAMOUNT']!=df.loc[quantity_ok,'NUMBERPERPANEL']*df.loc[quantity_ok,'NUMBEROFPANELSINLOT']).sum())
    backend_checks={}
    for label,cols,out in [('netto',['MANUALNETTIMEPERPANEL','PDBNETTIMEPERPANEL','DEFAULTNETTIMEPERPANEL'],'RELEVANTNETTIMESEC'),('brutto',['MANUALGROSSTIMEPERPANEL','PDBGROSSTIMEPERPANEL','DEFAULTGROSSTIMEPERPANEL'],'RELEVANTGROSSTIMESEC')]:
        inputs=backend[cols].apply(pd.to_numeric,errors='raise')
        expected=inputs.bfill(axis=1).iloc[:,0]/10000000
        actual=pd.to_numeric(backend[out],errors='raise')
        backend_checks[label]=int((~np.isclose(expected,actual,equal_nan=True,rtol=0,atol=1e-8)).sum())

    def aggregation(group):
        return group.agg(lose=('LOTID','size'),panels_bearbeitungsvorgaenge=('NUMBEROFPANELSINLOT',lambda s:s.sum(min_count=1)),mengenlose_lose=('MENGE_FEHLT','sum'))
    monthly=aggregation(df.groupby('LOSSTART_MONAT')).reset_index()
    daily=aggregation(df.groupby('LOSSTART_TAG')).reindex(pd.date_range(stamps.min().floor('D'),stamps.max().floor('D'),freq='D'))
    for c in ['lose','mengenlose_lose']:daily[c]=daily[c].fillna(0).astype(int)
    # Ein Tag ohne Datensätze hat null dokumentierte Losstartmenge, nicht null Produktion.
    daily.loc[daily['lose']==0,'panels_bearbeitungsvorgaenge']=0
    daily.index.name='losstart_tag';daily=daily.reset_index()
    hourly=aggregation(df.groupby('LOSSTART_STUNDE')).reindex(pd.date_range(stamps.min().floor('D'),stamps.max().ceil('D')-pd.Timedelta(hours=1),freq='h'))
    for c in ['lose','mengenlose_lose']:hourly[c]=hourly[c].fillna(0).astype(int)
    hourly.loc[hourly['lose']==0,'panels_bearbeitungsvorgaenge']=0
    hourly.index.name='losstart_stunde';hourly=hourly.reset_index()
    weekly=df.copy();weekly['wochenbeginn']=weekly['LOSSTART_TAG']-pd.to_timedelta(weekly['LOSSTART_TAG'].dt.dayofweek,unit='D')
    weekly=aggregation(weekly.groupby('wochenbeginn')).reset_index()
    lines=aggregation(df.groupby('LINE')).join(df.groupby('LINE')['NUMBEROFPANELSINLOT'].agg(panelmedian='median',panel_p95=lambda s:s.quantile(.95),panelmaximum='max')).sort_values('lose',ascending=False).reset_index()
    line_days=aggregation(df.groupby(['LINE','LOSSTART_TAG'])).reset_index()
    product=aggregation(df.groupby('BOARDTYPE')).join(df.groupby('BOARDTYPE').agg(linien=('LINE','nunique'),seiten=('SIDE',lambda s:' / '.join(sorted(s.unique()))),revisionen=('REVISION',lambda s:' / '.join(sorted(s.unique()))))).sort_values('lose',ascending=False).reset_index()
    routes=aggregation(df.groupby(['LINE','TARGETLINE'],dropna=False)).reset_index()
    side_order=df.groupby(['Order','SIDE','INTERMEDIATETARGET'],dropna=False).size().rename('lose').reset_index()
    save(df,'SMD_Lose_aufbereitet.csv');save(clean_backend,'Backend_Zuordnungen_bereinigt.csv')
    for frame,name in [(monthly,'Losstarts_Monate.csv'),(daily,'Losstarts_Tage.csv'),(hourly,'Losstarts_Stunden.csv'),(weekly,'Losstarts_Wochen.csv'),(lines,'Linienprofil.csv'),(line_days,'Losstarts_Linien_Tage.csv'),(product,'Produktmix.csv'),(routes,'SMT_Zwischenzielmatrix.csv'),(side_order,'Seite_Reihenfolge_Zwischenziel.csv'),(coverage,'Backend_Mappingabdeckung.csv')]:save(frame,name)
    issues=[]
    for _,row in df[df['MENGE_FEHLT']].iterrows():issues.append({'typ':'Menge fehlt','blatt':'SMD Lots','quellzeile':row['QUELLZEILE'],'schluessel':row['LOTID'],'hinweis':'REALAMOUNT und NUMBEROFPANELSINLOT leer; Datensatz erhalten, Mengensumme unvollständig'})
    for _,row in backend[duplicate_mask].iterrows():issues.append({'typ':'Exakte Dublette','blatt':'Backend-Productdata','quellzeile':row['QUELLZEILE'],'schluessel':row['BACKENDPRODUCTNUMBER'],'hinweis':'Alle 15 benannten Quellfelder identisch; nur abgeleitete Mappingtabelle dedupliziert'})
    save(pd.DataFrame(issues),'Einzelauffaelligkeiten.csv')

    cap=capacity.copy();cap['panels_pro_magazin']=pd.to_numeric(cap['panels_pro_magazin'],errors='raise')
    model=df[['LOTID','QUELLZEILE']+KEY+['NUMBEROFPANELSINLOT']].merge(cap,on=KEY,how='left',validate='many_to_one')
    values=[]
    for row in model.itertuples(index=False):
        quantity=None if pd.isna(row.NUMBEROFPANELSINLOT) else row.NUMBEROFPANELSINLOT
        cap_value=None if pd.isna(row.panels_pro_magazin) else row.panels_pro_magazin
        result=magazinbedarf(quantity,cap_value,4)
        state='Menge fehlt' if quantity is None else 'Magazinkapazität fehlt' if cap_value is None else 'Szenario mit bestätigter Kapazität' if row.status=='bestaetigt' else 'Szenario mit angenommener Kapazität'
        values.append({'modellstatus':state,**(result or {'magazine':None,'wagenfahrten_losrein':None,'restpanels':None,'belegte_plaetze_letzter_wagen':None})})
    model=pd.concat([model,pd.DataFrame(values)],axis=1);save(model,'Magazinmodell_Lose.csv')
    examples=[]
    for n,c in [(399,20),(399,25),(399,50),(101,25),(1,25)]:examples.append({'status':'Rechenbeispiel, keine Aumovio-Kapazität','panels':n,'angenommene_panels_pro_magazin':c,'angenommene_wagenplaetze':4,**magazinbedarf(n,c,4)})
    save(pd.DataFrame(examples),'Magazinmodell_Rechenbeispiele.csv')
    if not (INPUTS/'Pufferereignisse_Vorlage.csv').exists():
        pd.DataFrame(columns=['puffer_id','zeitpunkt_iso','zugang_magazine','abgang_magazine','quelle']).to_csv(INPUTS/'Pufferereignisse_Vorlage.csv',index=False,encoding='utf-8-sig')

    total_panels=int(df['NUMBEROFPANELSINLOT'].sum(min_count=1));mapped=df['BACKEND_LINIEN_ANZAHL']>0
    summary={
        'stand':'2026-10-29','original_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'smd_lose':len(df),'smd_spalten':len(original_columns),'backend_zeilen_roh':len(backend),'backend_zeilen_bereinigt':len(clean_backend),
        'zeitraum_von':stamps.min().isoformat(),'zeitraum_bis':stamps.max().isoformat(),'zeitzone':'nicht im Datensatz bestätigt',
        'linien':df['LINE'].nunique(),'boardtypes':df['BOARDTYPE'].nunique(),'backend_linien':backend['LINE'].nunique(),
        'panels_bearbeitungsvorgaenge_bekannt':total_panels,'mengenlose_lose':int(df['MENGE_FEHLT'].sum()),'lotid_dubletten':int(df['LOTID'].duplicated().sum()),
        'backend_exakte_dubletten':int(duplicate_mask.sum()),'panelmedian':float(df['NUMBEROFPANELSINLOT'].median()),'panel_p95':float(df['NUMBEROFPANELSINLOT'].quantile(.95)),'panelmaximum':float(df['NUMBEROFPANELSINLOT'].max()),
        'lose_mit_backend_mapping':int(mapped.sum()),'lose_ohne_backend_mapping':int((~mapped).sum()),'boardtypes_mit_backend_mapping':int((coverage['backend_linien']>0).sum()),'boardtypes_ohne_backend_mapping':int((coverage['backend_linien']==0).sum()),
        'boardtypes_mit_mehreren_backend_linien':int((coverage['backend_linien']>1).sum()),'boardtypes_mit_mehreren_default_linien':int((coverage['default_linien']>1).sum()),
        'zwischenziel_markiert':int((df['INTERMEDIATETARGET']==1).sum()),'zwischenziel_gleiche_linie':int(((df['INTERMEDIATETARGET']==1)&(df['LINE']==df['TARGETLINE'])).sum()),
        'quellenformel_abweichungen_smd':checks,'quellenformel_abweichungen_backend':backend_checks,
        'modell_berechenbare_lose':int(model['magazine'].notna().sum()),'kapazitaetsschluessel':len(capacity),'ausgabe_csv_trenner':',',
        'kontrollen':{'monat_lose':int(monthly['lose'].sum()),'tag_lose':int(daily['lose'].sum()),'stunde_lose':int(hourly['lose'].sum()),'linie_lose':int(lines['lose'].sum()),'produkt_lose':int(product['lose'].sum()),'monat_panels':int(monthly['panels_bearbeitungsvorgaenge'].sum()),'tag_panels':int(daily['panels_bearbeitungsvorgaenge'].sum()),'stunde_panels':int(hourly['panels_bearbeitungsvorgaenge'].sum())},
        'laufzeitumgebung':{'python':platform.python_version(),'pandas':pd.__version__,'openpyxl':openpyxl.__version__,'reportlab':reportlab.Version,'png_renderer':'Sharp im gebündelten Node-Runtime'}
    }
    (OUT/'Kennzahlen_und_Pruefungen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    assert len(df)==df['LOTID'].nunique()
    assert all(summary['kontrollen'][k]==len(df) for k in ['monat_lose','tag_lose','stunde_lose','linie_lose','produkt_lose'])
    assert all(summary['kontrollen'][k]==total_panels for k in ['monat_panels','tag_panels','stunde_panels'])
    assert sum(checks.values())==0 and sum(backend_checks.values())==0

    diagramme(df,monthly,lines,stamps,CHARTS)

    top=lines[['LINE','lose','panels_bearbeitungsvorgaenge']].head(8).copy();top.columns=['Linie','Lose','Bekannte Panel-Bearbeitungsvorgänge']
    for c in top.columns[1:]:top[c]=top[c].map(fmt)
    peak_day=daily.loc[daily['lose'].idxmax()];peak_hour=hourly.loc[hourly['lose'].idxmax()]
    report=f'''# Auswertung der Bewegungsdaten

Stand: 29.10.2026. Quelle Q018: `Daten/Bewegungsdaten AUMOVIO.xlsx`, Blätter `SMD Lots` und `Backend-Productdata`. [Zur Übersicht](../README.md).

## Ergebnis und Aussagegrenze

Die Datei umfasst **{fmt(len(df))} eindeutige LOTID** mit Losstarts von **{stamps.min().strftime('%d.%m.%Y')} bis {stamps.max().strftime('%d.%m.%Y')}**, {summary['linien']} SMT-Linien und {summary['boardtypes']} BOARDTYPE. Sie beschreibt Produktionslose und Stammdaten. **Ein Los ist kein einzelner Magazintransport.** Es fehlen Magazin-IDs, tatsächliche Übergabe-/Endzeitpunkte, eine verlässliche Verbindung physischer Panels über beide Seiten und tatsächliche Backend-Verbrauchsereignisse.

Die bekannte Summe beträgt **{fmt(total_panels)} Panel-Bearbeitungsvorgänge**. {hints['fehlmengen']} {hints['mengenstatus']} Zugleich ist sie keine Zahl eindeutiger physischer Panels: erneute Seitenbearbeitungen können dasselbe Material erneut enthalten.

## Losgrößen und Linien

- Median: {fmt(summary['panelmedian'])} Panels je mengenbekanntem Los.
- 95. Perzentil: {fmt(summary['panel_p95'],1)} Panels; Maximum: {fmt(summary['panelmaximum'])} Panels.
- Das Perzentil beschreibt Losgrößen, keine notwendige Förderleistung.

{md_table(top)}

![Linienprofil](Diagramme/Linienprofil.png)

![Losgrößen](Diagramme/Losgroessen.png)

## Zeitliche Verteilung

Die Mengen werden vollständig der Stunde/dem Tag/dem Monat des **Losstarts** zugeordnet. Ein großes Los ist über seine Laufzeit verteilt gefertigt worden; diese Auswertung verteilt es mangels belegter Laufzeitdaten nicht künstlich auf Produktionsstunden. Schichtauslastung, tatsächliche Fertigstellungsspitzen und Transportspitzen folgen daraus nicht.

Der größte beobachtete Tageswert sind **{fmt(peak_day['lose'])} Losstarts am {peak_day['losstart_tag'].strftime('%d.%m.%Y')}**. Der größte Stundenwert sind **{fmt(peak_hour['lose'])} Losstarts am {peak_hour['losstart_stunde'].strftime('%d.%m.%Y um %H:%M')}**. Das sind Losstart-Häufungen. Tages- und Stundentabellen umfassen auch Kalenderintervalle ohne Datensätze. Null bedeutet dort keine dokumentierten Losstarts; daraus folgt kein Stillstand.

![Monatsverlauf](Diagramme/Losstarts_Monate.png)

![Wochentag und Stunde](Diagramme/Losstarts_Wochentag_Stunde.png)

## Zwischenziele und Backend

**{fmt(summary['zwischenziel_markiert'])} Lose** tragen `INTERMEDIATETARGET=1`. Bei {fmt(summary['zwischenziel_gleiche_linie'])} davon sind LINE und TARGETLINE gleich. Das weist keine Fahrt zwischen verschiedenen Linien nach und darf nicht pauschal als solche gezählt werden. Bei fehlendem Zwischenziel wird ebenfalls kein sicherer Backend-Abgang unterstellt.

Das Backend-Blatt enthält {fmt(len(backend))} Zeilen, nach transparenter Bereinigung {fmt(len(clean_backend))} Zuordnungszeilen, verteilt auf {summary['backend_linien']} Linien. {hints['dubletten']} Für **{summary['boardtypes_mit_backend_mapping']} von {summary['boardtypes']} BOARDTYPE** existiert ein exakter Stammdatenmatch. Das betrifft **{fmt(summary['lose_mit_backend_mapping'])} von {fmt(len(df))} Losen ({fmt(100*mapped.mean(),1)} %)**. {summary['boardtypes_ohne_backend_mapping']} BOARDTYPE mit {fmt(summary['lose_ohne_backend_mapping'])} Losen haben keinen exakten Match.

**{summary['boardtypes_mit_mehreren_backend_linien']} BOARDTYPE** besitzen mehrere mögliche Backend-Linien. Selbst bei `ISDEFAULT=1` gibt es für {summary['boardtypes_mit_mehreren_default_linien']} BOARDTYPE mehrere Linien. Ein Stammdatenmatch beweist weder den tatsächlichen nächsten Prozess noch eine konkrete Verbrauchszeit. Mögliche Ziele werden daher listenweise erhalten. Es erfolgt keine vervielfachende Mengenaggregation durch einen 1:n-Join.

## Datenqualität und Nachrechnung

Einzelbefunde zu Mengenlücken und Dubletten stehen mit Quellzeilen in [Einzelauffaelligkeiten.csv](Tabellen/Einzelauffaelligkeiten.csv). Alle {fmt(len(df))} Lose bleiben in der aufbereiteten Tabelle erhalten. Keine LOTID-Dublette wurde gefunden. Bei vorhandenen Mengen gilt überall `REALAMOUNT = NUMBERPERPANEL × NUMBEROFPANELSINLOT`.

Die Sekundenumrechnung und Auswahlregeln der Quellenformeln wurden aus den Basiswerten unabhängig nachgerechnet. Ergebnis: {sum(checks.values())} Abweichungen in den geprüften SMT-Feldern und {sum(backend_checks.values())} in den Backend-Zeitfeldern. Dies prüft die Übereinstimmung mit gespeicherten Ergebnissen, nicht die physische Bedeutung der Zeiten. Keine Neuberechnung oder Speicherung der Originalarbeitsmappe.

`REALSTART` wird mit bis zu neun Nachkommastellen eingelesen und zusätzlich als ISO-Zeit exportiert; der Originaltext bleibt erhalten. Die Zeitzone ist nicht belegt. Keine Umrechnung nach UTC und keine erfundene Sommerzeitkorrektur. `Stunde` stimmt in allen Zeilen mit der abgerundeten lokalen Textzeit überein.

## Magazinbedarf und Puffer

Die Kapazitätsvorlage enthält **{len(capacity)} Produktschlüssel aus BOARDTYPE, SIDE und REVISION**. Aktuell sind **{summary['modell_berechenbare_lose']} Lose** im Magazinmodell berechenbar. Solange Kapazitäten fehlen, bleiben Ergebnisse leer und tragen einen konkreten Fehlgrund. Die vier Wagenplätze sind eine Arbeitsannahme aus Q019/Q020, keine vermessene Freigabe.

Die Formeln und Rechenbeispiele stehen in [Bedarfsmodelle.md](Bedarfsmodelle.md). Beispielkapazitäten sind ausdrücklich hypothetisch; sie werden nicht auf die historischen Lose übertragen. Reale Pufferkapazität und Fahrzeugzahl bleiben offen. Das Backend-Blatt liefert keine beobachtete Abnahmehistorie.

## Reproduktion und Tabellen

Auswertung: `Reproduktion/auswerten.py`. Benötigt werden Python, openpyxl, pandas, numpy und ReportLab sowie der gebündelte Sharp-Renderer. Die verwendeten Versionen sowie Quellprüfsumme und Kontrollsummen stehen in [Kennzahlen_und_Pruefungen.json](Kennzahlen_und_Pruefungen.json). Startanleitung: [Reproduktion/README.md](Reproduktion/README.md).

Tabellen: aufbereitete Lose, deduplizierte Backend-Zuordnungen, Monats-/Wochen-/Tages-/Stundenwerte, Linienprofil, beobachtete Linie-Tag-Kombinationen, Produktmix, Zwischenzielmatrix, Seite/Reihenfolge, Mappingabdeckung, Einzelauffälligkeiten und Magazinmodell. CSV: UTF-8 mit BOM, Komma als Feldtrenner, Dezimalpunkt. Leeres Zahlenfeld bedeutet fehlend, nicht null. `QUELLZEILE` verweist auf die Original-Excelzeile. Die Linie-Tag-Tabelle enthält nur beobachtete Kombinationen; die Gesamt-Tages-/Stundentabellen enthalten alle Kalenderintervalle der Periode.
'''
    (OUT/'Analysebericht.md').write_text(report,encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
