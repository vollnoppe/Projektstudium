"""Prüft die fachlich kritischen Rechenregeln mit kleinen, unabhängigen Fällen."""
import importlib.util
import pathlib
import types
import unittest
import uuid
import pandas as pd
import auswerten
import diagramme_erstellen

p = pathlib.Path(__file__).with_name('modell.py')
if p.exists():
    spec = importlib.util.spec_from_file_location('modell', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
else:
    m = types.SimpleNamespace()


class ModellTests(unittest.TestCase):
    def function(self, name):
        fn = getattr(m, name, None)
        self.assertTrue(callable(fn), f'Fachfunktion {name} fehlt noch')
        return fn

    def test_losrest_braucht_eigenes_magazin_und_wagenplatz(self):
        r = self.function('magazinbedarf')(101, 25, 4)
        self.assertEqual((r['magazine'], r['wagenfahrten_losrein'], r['restpanels']), (5, 2, 1))
        self.assertEqual(r['belegte_plaetze_letzter_wagen'], 1)

    def test_volles_magazin_hat_keinen_rest(self):
        r = self.function('magazinbedarf')(100, 25, 4)
        self.assertEqual((r['magazine'], r['wagenfahrten_losrein'], r['restpanels']), (4, 1, 0))

    def test_fehlende_menge_oder_kapazitaet_bleibt_unverfuegbar(self):
        f = self.function('magazinbedarf')
        self.assertIsNone(f(None, 25, 4))
        self.assertIsNone(f(100, None, 4))

    def test_echte_null_bleibt_null(self):
        r = self.function('magazinbedarf')(0, 25, 4)
        self.assertEqual((r['magazine'], r['wagenfahrten_losrein']), (0, 0))

    def test_unzulaessige_kapazitaeten_und_mengen_werden_abgewiesen(self):
        f = self.function('magazinbedarf')
        for args in [(100, 0, 4), (100, -1, 4), (100.5, 25, 4), (-1, 25, 4), (100, 25, 0)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                f(*args)

    def test_losreine_buendelung_ist_keine_beliebige_poolung(self):
        f = self.function('magazinbedarf')
        a, b = f(1, 25, 4), f(1, 25, 4)
        self.assertEqual(a['wagenfahrten_losrein'] + b['wagenfahrten_losrein'], 2)

    def test_puffer_braucht_anfangsbestand(self):
        f = self.function('pufferbestand')
        with self.assertRaises(ValueError):
            f([('2026-01-01T10:00:00', 2, 0)], None)

    def test_puffer_bilanziert_ereignisse_und_erkennt_unterdeckung(self):
        f = self.function('pufferbestand')
        r = f([('2026-01-01T11:00:00', 0, 2), ('2026-01-01T10:00:00', 3, 0)], 1)
        self.assertEqual([x['bestand_magazine'] for x in r], [4, 2])
        with self.assertRaises(ValueError):
            f([('2026-01-01T10:00:00', 0, 2)], 1)

    def test_mehrere_ereignisse_gleicher_zeit_werden_gemeinsam_bilanziert(self):
        r = self.function('pufferbestand')([('2026-01-01T10:00:00', 0, 1), ('2026-01-01T10:00:00', 2, 0)], 0)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]['bestand_magazine'], 1)

    def test_puffer_sortiert_explizite_offsets_nach_absoluter_zeit(self):
        f = self.function('pufferbestand')
        try:
            result = f([('2026-10-25T02:15:00+01:00',0,2),('2026-10-25T02:45:00+02:00',2,0)],0)
        except ValueError:
            result = None
        self.assertIsNotNone(result,'Zeitumstellung darf keine falsche Unterdeckung erzeugen')
        self.assertEqual([x['bestand_magazine'] for x in result],[2,0])

    def test_identische_absolute_zeitpunkte_werden_zusammengefasst(self):
        f = self.function('pufferbestand')
        try:
            result = f([('2026-10-25T10:00:00+02:00',2,0),('2026-10-25T08:00:00+00:00',0,1)],0)
        except ValueError:
            result = None
        self.assertIsNotNone(result)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['bestand_magazine'],1)

    def test_gemischte_offsetlose_und_offsetbehaftete_zeiten_werden_abgewiesen(self):
        with self.assertRaisesRegex(ValueError,'Zeitbasis'):
            self.function('pufferbestand')([('2026-01-01T10:00:00',1,0),('2026-01-01T10:00:00+00:00',1,0)],0)

    def test_nanosekunden_werden_nicht_als_gleichzeitig_zusammengelegt(self):
        result = self.function('pufferbestand')([('2026-01-01T10:00:00.000000002',2,0),('2026-01-01T10:00:00.000000003',0,2)],0)
        self.assertEqual(len(result),2)
        self.assertEqual([x['bestand_magazine'] for x in result],[2,0])


class AktualisierungsTests(unittest.TestCase):
    def test_histogramm_enthaelt_auch_grosse_neue_lose(self):
        fn = getattr(diagramme_erstellen,'losgroessen_histogramm',None)
        self.assertTrue(callable(fn),'Dynamische Histogrammfunktion fehlt')
        counts,edges = fn([399,2500,2501])
        self.assertEqual(int(counts.sum()),3)
        self.assertGreaterEqual(edges[-1],2501)

    def test_beschriftung_folgt_neuem_zeitraum_und_datenluecken(self):
        fn = getattr(diagramme_erstellen,'quellenhinweise',None)
        self.assertTrue(callable(fn),'Dynamische Quellenhinweise fehlen')
        times = pd.to_datetime(['2027-01-01','2027-02-03'])
        clean = fn(times,0,0)
        changed = fn(times,7,4)
        self.assertEqual(clean['zeitraum'],'01.01.2027 bis 03.02.2027')
        self.assertEqual(clean['fehlmengen'],'Keine Lose ohne Mengenangabe.')
        self.assertIn('7 Lose',changed['fehlmengen'])
        self.assertIn('4',changed['dubletten'])


class KapazitaetsEingabeTests(unittest.TestCase):
    def setUp(self):
        self.testdir = pathlib.Path(__file__).parent / ('_testkapazitaet_' + uuid.uuid4().hex)
        self.testdir.mkdir()
        self.previous = auswerten.INPUTS
        auswerten.INPUTS = self.testdir
        self.df = pd.DataFrame([{'BOARDTYPE':'A','SIDE':'Top','REVISION':'a'}])

    def tearDown(self):
        auswerten.INPUTS = self.previous
        self.assertTrue(self.testdir.resolve().is_relative_to(pathlib.Path(__file__).parent.resolve()))
        for p in self.testdir.iterdir():
            self.assertEqual(p.name,'Magazinkapazitaeten.csv')
            p.unlink()
        self.testdir.rmdir()

    def write(self, frame):
        frame.to_csv(auswerten.INPUTS/'Magazinkapazitaeten.csv',index=False,encoding='utf-8-sig')

    def test_eingabe_bleibt_bei_neuen_produkten_erhalten(self):
        initial = auswerten.read_capacity_template(self.df)
        initial.loc[0,['panels_pro_magazin','status','quelle']] = ['25','Annahme','Expliziter Testfall']
        self.write(initial)
        more = pd.concat([self.df,pd.DataFrame([{'BOARDTYPE':'B','SIDE':'Bottom','REVISION':'b'}])])
        result = auswerten.read_capacity_template(more)
        self.assertEqual(len(result),2)
        self.assertEqual(result.loc[result.BOARDTYPE=='A','panels_pro_magazin'].iloc[0],'25')
        self.assertEqual(result.loc[result.BOARDTYPE=='B','panels_pro_magazin'].iloc[0],'')

    def test_mehrdeutige_kapazitaetsschluessel_werden_abgewiesen(self):
        initial = auswerten.read_capacity_template(self.df)
        self.write(pd.concat([initial,initial]))
        with self.assertRaisesRegex(ValueError,'mehrdeutige'):
            auswerten.read_capacity_template(self.df)

    def test_kapazitaet_braucht_status_und_quelle(self):
        initial = auswerten.read_capacity_template(self.df)
        initial.loc[0,'panels_pro_magazin']='25'
        self.write(initial)
        with self.assertRaisesRegex(ValueError,'status'):
            auswerten.read_capacity_template(self.df)
        initial.loc[0,'status']='bestaetigt'
        self.write(initial)
        with self.assertRaisesRegex(ValueError,'Quelle'):
            auswerten.read_capacity_template(self.df)


if __name__ == '__main__':
    unittest.main(verbosity=2)
