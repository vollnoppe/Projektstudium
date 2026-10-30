"""Erstellt Quellenaufbereitung und Bildkopien; Originale werden ausschließlich gelesen."""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET
import zipfile
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
CHAT = ROOT / 'ChatDaten'
OUT = CHAT / '01_Bildkatalog'
META = [
 (1,'Linienstationen','Station_zwei_Foerderebenen','Linienstation mit zwei übereinander angeordneten schwarzen Förderflächen, vertikalem Aufbau und Signalgebern.','Möglicher Ein-/Ausgabebereich für Magazine; Funktion und Bewegungsablauf sind nicht belegt.','Höhenwechsel; Zugang; Linienintegration','Richtung, Hersteller, Modell und Übergabehöhen offen.'),
 (2,'Linienstationen','Drei_Magazinplaetze_bestueckt','Drei beschriftete Magazinplätze 1 bis 3. Schwarze Magazine stehen auf Förderflächen; zwei enthalten sichtbar Leiterplatten, eines wirkt leer.','Beispiel einer Linie mit gleichzeitig unterschiedlichen Füllständen.','Teilfüllung; drei Plätze; Losende; Identifikation','Ein-/Ausgabeseite und tatsächlich nutzbare Magazinslots aus dem Foto nicht sicher.'),
 (3,'Linienstationen','Station_zwei_Foerderebenen_Frontal','Frontalansicht eines vertikalen Stationsaufbaus mit zwei Förderflächen und Schutzverkleidung.','Ergänzende Ansicht zur Geometrie der Station aus B001.','Hub; Übergabeseite; Schutzbereich','Gleichheit des konkreten Stationsmodells zu B001 ist visuelle Zuordnung, keine Identnummer.'),
 (4,'Linienstationen','Station_mit_benachbartem_Wagen','Station mit zwei Förderflächen; links steht ein hoher rollbarer Träger mit zwei Ebenen.','Räumlicher Zusammenhang von Linie und Wagen, möglicher Übergabebereich.','Wagen; Andocken; Freiraum; Hub','Abstände und Höhen sind nicht vermessen; die gezeigte Aufstellung beweist keine automatische Übergabe.'),
 (5,'Linienstationen','Drei_leere_Magazinplaetze_Frontal','Drei nummerierte leere Magazinplätze mit seitlichen Führungen und Förderbändern.','Zugängliche Aufnahmebereiche als Ausgangspunkt für eine externe Handhabung.','Drei Plätze; Führung; Stationsübergabe','Antriebsrichtung, Entriegelung und vorhandene Maschinensignale sind offen.'),
 (6,'Linienstationen','Drei_leere_Magazinplaetze_Schraeg','Schrägansicht von drei leeren Magazinplätzen; Bodenmarkierungen und angrenzende Anlagen sind sichtbar.','Ergänzung von B005 zur räumlichen Integration und zu freizuhaltenden Flächen.','Platzbedarf; Bedienzugang; Bodenmarkierung','Bodenmarkierungen sind keine bemaßte oder freigegebene Layoutzeichnung.'),
 (7,'Transport_und_Andocken','Schmales_Transportfahrzeug_im_Fahrweg','Schmales dunkles Fahrzeug mit bodennahem Ausleger und Leuchten; daneben Fahrwegmarkierungen und bodennahe Führungen.','Möglicherweise der in den Notizen erwähnte Einzelmagazintransporter.','Fahrweg; alternative Fahrzeuge; Bodenführung','Zuordnung zu HVT, Traglast und Ein-Magazin-Beschränkung sind aus dem Bild nicht bestätigt.'),
 (8,'Lager_und_Puffer','Lagerbereich_Wagen_und_Uebergaben','Hohe Regalreihen, zahlreiche zweistöckige Wagen und mehrere stationäre Förderflächen im Vordergrund.','Bestehender Lager-/Bereitstellbereich und potenzielle Übergabeschnittstelle.','Puffer; Wagenbestand; stationäre Übergabe','Regalinhalte, belegte Plätze und freie Kapazität sind nicht vollständig erkennbar.'),
 (9,'Lager_und_Puffer','Lagerbereich_mit_AGILOX','Lagerbereich aus ähnlicher Perspektive wie B008; rechts steht ein grünes AGILOX-Fahrzeug neben einem Wagen.','Zusammenhang von Lager, Wagen und Fahrzeug.','Puffer; AGILOX; Andocken','Ähnliche Perspektive zu B008, aber keine identische Datei; reale Lagerkapazität nicht abzählbar.'),
 (10,'Transport_und_Andocken','AGILOX_Moritz_am_Wagen','Grünes Fahrzeug mit Schriftzug AGILOX und Namensschild Moritz vor einem Magazinwagen.','Dokumentiert die fahrzeugseitige Wagenaufnahme als relevanten Bestand.','AGILOX; Wagenaufnahme; Fahrweg','Exakte Baureihe und Ausführung nicht anhand des Schriftzugs freigegeben.'),
 (11,'Transport_und_Andocken','AGILOX_Moritz_Wagenposition','AGILOX Moritz in unmittelbarer Nähe eines zweistöckigen Magazinwagens; Übergabeflächen links.','Weitere Position innerhalb einer visuell zusammengehörigen Aufnahmeserie.','Andocken; Wagen; Pufferanbindung','Statische Bilder liefern keine Zykluszeit, Andockgenauigkeit oder Blockierungsquote.'),
 (12,'Transport_und_Andocken','AGILOX_Moritz_unter_Wagen','AGILOX mit bodennahem Lastaufnahmeteil unter dem Magazinwagen; Wagen und Magazine stehen dicht am Fahrzeug.','Belegt die relevante mechanische Wagenaufnahme im vorhandenen System.','Wagenaufnahme; Bestandskompatibilität; Unterfahrbereich','Hubzustand, zulässige Last und Fahrfreigabe sind nicht messbar.'),
 (13,'Lager_und_Puffer','Foerderuebergaben_vor_Lagerreihen','Vier nebeneinander liegende Förder-/Auflagebahnen vor Regalreihen und Magazinwagen.','Mögliche stationäre Bereitstellung von Magazinen.','Puffer; vier Übergabepositionen; Flächenbedarf','Funktion, Steuerung und Auslegung dieser Bahnen sind nicht dokumentiert.'),
 (14,'Lager_und_Puffer','Vier_stationaere_Uebergabebahnen','Frontansicht von vier stationären Bahnen mit unterschiedlichen Auflagehöhen und seitlichen Führungen.','Ansatzpunkt für Prüfung von Übergabemodulen und Zwischenpufferung.','Übergabemechanik; Puffer; Höhen','Sichtbare Auflagehöhen sind nicht als Wagenhöhen oder zulässige Schnittstellenmaße zu übernehmen.'),
 (15,'Magazinwagen_und_Uebergabemechanik','Wagen_Rollenbahn_Detail','Detail eines Wagens mit unterer Auflage, Rollen und Lenkrolle; weitere Wagen und Station im Hintergrund.','Rollenunterstützte Verschiebung ganzer Magazine könnte nutzbar sein.','Rollenbahn; Unterbau; Räder; Übergabe','Rollen sind sichtbar; Antrieb, Rollwiderstand, Anschläge und Verriegelungen bleiben offen.'),
 (16,'Magazinwagen_und_Uebergabemechanik','Wagen_zwei_Ebenen_Detail','Wagen mit zwei Ebenen, mehreren Magazinen, seitlichen Rahmenprofilen, Auflagerollen und Lenkrollen.','Zentrale Referenz für zwei horizontale Positionen je Ebene und die Höhenanpassung.','Zwei Ebenen; vier Plätze; Rollen; Magazinrahmen','Vier Plätze sind durch Notizen/Folien beschrieben. Zulässige Kräfte, Maße und Sicherungen müssen vermessen werden.'),
 (17,'Linienstationen','Drei_Magazinplaetze_mit_Sensorik','Drei nummerierte Magazinplätze auf Rollenbahnen; darüber Sensor-/Leseköpfe mit sichtbarem OMRON-Schriftzug.','Vorhandene Identifikations-/Überwachungskomponenten sind Ansatzpunkt für digitale Übergabe.','Rollenbahn; Identifikation; Sensorik; Füllstand','Lesefunktion, Protokoll und tatsächlicher Dateninhalt sind nicht aus dem Foto bewiesen.'),
]


def main():
    manifest = json.loads((CHAT/'00_Projektstand/Originalpruefsummen.json').read_text(encoding='utf-8'))
    for item in manifest:
        p = ROOT/item['originalpfad']
        if hashlib.sha256(p.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError(f'Original seit Inventarisierung verändert: {p}')
    pictures=[]
    for number, category, short, observation, interpretation, tags, uncertainty in META:
        prefix = 'WhatsApp Image ' if number==1 else f'WhatsApp Image{number} '
        matches = list((ROOT/'Bilder').glob(prefix+'*'))
        if len(matches)!=1: raise ValueError(f'Bild {number}: {matches}')
        original=matches[0]; image_id=f'B{number:03d}'
        folder=OUT/category; folder.mkdir(parents=True,exist_ok=True)
        copy=folder/f'{image_id}_{short}.jpeg'; shutil.copyfile(original,copy)
        source=next(x for x in manifest if x['originalpfad']==original.relative_to(ROOT).as_posix())
        pictures.append({'bild_id':image_id,'quellen_id':source['quellen_id'],'original':original.relative_to(ROOT).as_posix(),'arbeitskopie':copy.relative_to(CHAT).as_posix(),'hauptkategorie':category,'kurztitel':short.replace('_',' '),'beobachtung':observation,'interpretation':interpretation,'schlagwoerter':tags,'unsicherheiten':uncertainty,'sha256':source['sha256']})
    with (OUT/'Bildkatalog.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=pictures[0].keys());w.writeheader();w.writerows(pictures)
    md=['# Bildkatalog','Stand: 29.10.2026. Alle 17 Originale bleiben unverändert. B001 entspricht dem Dateinamen ohne angehängte Bildnummer. Die Datumsangabe im Dateinamen ist kein bestätigter Aufnahmezeitpunkt.','[Zur Übersicht](../README.md) · [Kontaktbogen](Kontaktbogen.jpg) · [Katalog als CSV](Bildkatalog.csv)','## Kategorien','| Hauptkategorie | Bilder |','|---|---|']
    for category in dict.fromkeys(x['hauptkategorie'] for x in pictures):
        md.append(f"| {category.replace('_',' ')} | {', '.join(x['bild_id'] for x in pictures if x['hauptkategorie']==category)} |")
    md += ['','Ähnliche Ansichten und die AGILOX-Bildserie sind keine unabhängigen Anlagen- oder Zeitmessungen. Es gibt keine bytegleichen Originalfotos. Bilder aus der Startpräsentation sind teilweise dieselben Dateien und kein zusätzlicher unabhängiger Beleg.','']
    for item in pictures:
        relative=Path(item['arbeitskopie']).relative_to('01_Bildkatalog').as_posix()
        md += [f"## {item['bild_id']} – {item['kurztitel']}",f"![{item['bild_id']}: {item['kurztitel']}]({relative})",f"**Hauptkategorie:** {item['hauptkategorie'].replace('_',' ')}. **Quelle:** {item['quellen_id']}; Original: `{item['original']}`.",f"**Sichtbar:** {item['beobachtung']}",f"**Einordnung:** {item['interpretation']}",f"**Offen:** {item['unsicherheiten']}",f"**Schlagwörter:** {item['schlagwoerter']}",'']
    (OUT/'Bildkatalog.md').write_text('\n\n'.join(md),encoding='utf-8')
    font=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',21)
    small=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',15)
    sheet=Image.new('RGB',(1350,6*390+70),'#f3f5f7');draw=ImageDraw.Draw(sheet)
    draw.text((22,16),'Aumovio – Bildübersicht B001 bis B017',font=font,fill='#17334a')
    for i,item in enumerate(pictures):
        x=(i%3)*450; y=70+(i//3)*390
        im=ImageOps.exif_transpose(Image.open(CHAT/item['arbeitskopie']));im.thumbnail((430,335))
        sheet.paste(im,(x+(450-im.width)//2,y))
        draw.text((x+12,y+338),item['bild_id']+' '+item['kurztitel'][:46],font=small,fill='#17334a')
        draw.text((x+12,y+359),item['hauptkategorie'].replace('_',' '),font=small,fill='#435d6d')
    sheet.save(OUT/'Kontaktbogen.jpg',quality=91)
    notes=(ROOT/'Daten/Notizen.txt').read_text(encoding='utf-8-sig')
    indexed='\n'.join(f'{i:03d}: {line}' for i,line in enumerate(notes.splitlines(),1))
    (CHAT/'00_Projektstand/Notizen_mit_Zeilennummern.txt').write_text(indexed,encoding='utf-8')
    ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
    slides=[]
    with zipfile.ZipFile(ROOT/'Daten/Projektstudium - Gruppe C .pptx') as z:
        for i in range(1,5):
            tree=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
            slides.append({'folie':i,'text':[x.text for x in tree.findall('.//a:t',ns) if x.text]})
    (CHAT/'00_Projektstand/Startfolien_Text.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# Quellenverzeichnis','Stand: 29.10.2026. Originalpfade beziehen sich auf den Projektstamm. SHA-256 und Dateigrößen stehen vollständig in Quellenverzeichnis.csv und Originalpruefsummen.json.','| ID | Original | Verwendung |','|---|---|---|']
    lines += [f"| {q['quellen_id']} | {q['originalpfad']} | {q['verwendung']} |" for q in manifest]
    lines += ['','## Quellenkritik','Notizen sind informelle Mitschriften mit ausdrücklich unsicheren Passagen. Die vier Startfolien verdichten denselben Kontext und bestätigen ihn nicht unabhängig. Fotos belegen sichtbare Merkmale, aber keine Abmessungen, Taktzeiten oder vollständigen Abläufe. Die Excel-Datei enthält Produktionslose und Backend-Stammdaten, keine lückenlose Transporthistorie. Nutzerentscheidungen aus dem Chat stehen in Entscheidungen.md. Herstellerquellen und ihre Grenzen stehen im Konzeptbereich.']
    (CHAT/'00_Projektstand/Quellenverzeichnis.md').write_text('\n\n'.join(lines),encoding='utf-8')
    print(json.dumps({'bilder':len(pictures),'originale_geprueft':len(manifest),'folien':len(slides)},ensure_ascii=False))


if __name__=='__main__':main()
