"""Statische wissenschaftliche Diagramme mit ReportLab, PNG-Rendering mit Sharp."""
from pathlib import Path
import subprocess
import sys
import numpy as np
import pandas as pd
from reportlab.graphics.shapes import Drawing, String, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
from reportlab.graphics import renderSVG
from reportlab.lib.colors import HexColor, Color, white

BLUE=HexColor('#237fa1');ORANGE=HexColor('#d59137');INK=HexColor('#17334a')


def title(d,title_text,subtitle):
    d.add(Rect(0,0,d.width,d.height,fillColor=white,strokeColor=None))
    d.add(String(24,d.height-27,title_text,fontName='Helvetica-Bold',fontSize=16,fillColor=INK))
    d.add(String(24,d.height-47,subtitle,fontName='Helvetica',fontSize=10,fillColor=INK))


def export(d,path):
    svg=path.with_suffix('.svg');renderSVG.drawToFile(d,str(svg))
    dependencies=Path(sys.executable).resolve().parents[1]
    node=dependencies/'node/bin/node.exe';sharp=dependencies/'node/node_modules/sharp'
    code="const sharp=require(process.argv[1]);sharp(process.argv[2],{density:160}).png().toFile(process.argv[3]).catch(e=>{console.error(e);process.exit(1)});"
    subprocess.run([str(node),'-e',code,str(sharp),str(svg),str(path)],check=True,capture_output=True,text=True)


def vertical(d,data,categories,x,y,width,height,color,angle=0):
    b=VerticalBarChart();b.x=x;b.y=y;b.width=width;b.height=height;b.data=[tuple(float(v) for v in data)]
    b.categoryAxis.categoryNames=list(categories);b.categoryAxis.labels.fontSize=8;b.categoryAxis.labels.angle=angle
    b.categoryAxis.labels.boxAnchor='ne' if angle else 'n';b.categoryAxis.labels.dx=-2 if angle else 0
    b.valueAxis.valueMin=0;b.valueAxis.labels.fontSize=9;b.valueAxis.maximumTicks=5
    b.bars[0].fillColor=color;b.bars.strokeColor=None;b.categoryAxis.strokeColor=INK;b.valueAxis.strokeColor=INK
    d.add(b);return b


def losgroessen_histogramm(quantities,klassenbreite=50):
    values=np.asarray(quantities,dtype=float)
    maximum=float(values.max()) if len(values) else 0
    upper=max(klassenbreite,int(np.ceil(maximum/klassenbreite))*klassenbreite)
    counts,edges=np.histogram(values,bins=np.arange(0,upper+klassenbreite,klassenbreite))
    if int(counts.sum())!=len(values):
        raise ValueError('Histogramm enthält nicht sämtliche mengenbekannten Lose')
    return counts,edges


def quellenhinweise(zeitpunkte,fehlmengen,dubletten=0):
    dates=pd.DatetimeIndex(zeitpunkte)
    missing=int(fehlmengen);duplicates=int(dubletten)
    return {
        'zeitraum':dates.min().strftime('%d.%m.%Y')+' bis '+dates.max().strftime('%d.%m.%Y'),
        'fehlmengen':'Keine Lose ohne Mengenangabe.' if missing==0 else f'{missing} Los ohne Mengenangabe.' if missing==1 else f'{missing} Lose ohne Mengenangabe.',
        'mengenstatus':'Die bekannte Mengensumme ist unvollständig.' if missing else 'Die Panelmengen sind für alle Lose vorhanden.',
        'dubletten':'Keine vollständig identische Backend-Dublette.' if duplicates==0 else '1 vollständig identische Backend-Dublette.' if duplicates==1 else f'{duplicates} vollständig identische Backend-Dubletten.',
    }


def diagramme(df,monthly,lines,stamps,folder):
    hints=quellenhinweise(stamps,int(df['NUMBEROFPANELSINLOT'].isna().sum()))
    d=Drawing(850,570);title(d,'Losstarts und zugeordnete Panelmengen nach Monat',hints['zeitraum']+'. Keine Fertigstellungs- oder Transportzeitreihe. '+hints['fehlmengen'])
    d.add(String(65,495,'Dokumentierte Losstarts',fontSize=10,fillColor=INK))
    labels=list(monthly['LOSSTART_MONAT']);short=[v if i%2==0 else '' for i,v in enumerate(labels)]
    vertical(d,monthly['lose'],short,65,315,750,165,BLUE,35)
    d.add(String(65,245,'Panel-Bearbeitungsvorgänge in Mio. (bekannte Mengen)',fontSize=10,fillColor=INK))
    vertical(d,monthly['panels_bearbeitungsvorgaenge']/1e6,short,65,65,750,165,ORANGE,35)
    export(d,folder/'Losstarts_Monate.png')

    d=Drawing(850,720);title(d,'Linienprofil nach dokumentierten Losstarts','Je Losstart zugeordnete Panel-Bearbeitungsvorgänge. Keine Magazinfahrten oder eindeutigen physischen Panels.')
    for i,(values,label,color) in enumerate([(lines['lose'],'Dokumentierte Losstarts',BLUE),(lines['panels_bearbeitungsvorgaenge']/1e6,'Panel-Bearbeitungsvorgänge in Mio.',ORANGE)]):
        b=HorizontalBarChart();b.x=80+i*400;b.y=65;b.width=310;b.height=570;b.data=[tuple(float(v) for v in values.iloc[::-1])]
        b.categoryAxis.categoryNames=list(lines['LINE'].iloc[::-1]);b.categoryAxis.labels.fontSize=9;b.valueAxis.valueMin=0;b.valueAxis.labels.fontSize=8;b.valueAxis.maximumTicks=5
        b.bars[0].fillColor=color;b.bars.strokeColor=None;d.add(b);d.add(String(b.x,655,label,fontSize=10,fillColor=INK))
    export(d,folder/'Linienprofil.png')

    quantities=df['NUMBEROFPANELSINLOT'].dropna();counts,edges=losgroessen_histogramm(quantities)
    labelstep=max(1,int(np.ceil(len(counts)/12)))
    labels=[str(int(x)) if i%labelstep==0 else '' for i,x in enumerate(edges[:-1])]
    d=Drawing(850,410);title(d,'Losgrößen nach dokumentierten Panelmengen',f'Median: {quantities.median():.0f} Panels je mengenbekanntem Los. '+hints['fehlmengen'])
    vertical(d,counts,labels,65,65,750,255,BLUE)
    d.add(String(300,22,'Panels je Los/Bearbeitungsvorgang; Klassenbreite 50 Panels',fontSize=10,fillColor=INK));d.add(String(65,335,'Anzahl Lose',fontSize=10,fillColor=INK))
    export(d,folder/'Losgroessen.png')

    heat=pd.crosstab(stamps.dt.dayofweek,stamps.dt.hour).reindex(index=range(7),columns=range(24),fill_value=0)
    d=Drawing(850,340);title(d,'Losstarts nach Wochentag und Stunde','Gesamte Datenperiode; Farbe zeigt die Anzahl Losstarts, keine Produktions- oder Transportleistung.')
    maximum=float(heat.to_numpy().max());x0=65;y0=90;cw=30;ch=23
    for day in range(7):
        y=y0+(6-day)*ch;d.add(String(32,y+7,['Mo','Di','Mi','Do','Fr','Sa','So'][day],fontSize=10,fillColor=INK))
        for hour in range(24):
            ratio=float(heat.iloc[day,hour])/maximum;color=Color(.94-.80*ratio,.97-.47*ratio,.99-.36*ratio)
            d.add(Rect(x0+hour*cw,y,cw-1,ch-1,fillColor=color,strokeColor=None))
    for h in range(0,24,2):d.add(String(x0+h*cw+8,67,str(h),fontSize=10,fillColor=INK))
    d.add(String(280,42,'Stunde des dokumentierten Losstarts',fontSize=10,fillColor=INK))
    d.add(String(65,20,f'Farbskala: hell = 0, dunkel = {int(maximum)} Losstarts. Zeitzone nicht bestätigt.',fontSize=9,fillColor=INK))
    export(d,folder/'Losstarts_Wochentag_Stunde.png')
