"""Offene Bedarfsmodelle: keine Aumovio-Kapazitäten oder Transportereignisse erfinden."""
from collections import defaultdict
from math import ceil, isfinite
import pandas as pd


def _ganzzahl(value, name, minimum=0):
    if isinstance(value, bool):
        raise ValueError(f'{name}: ganze Zahl erforderlich')
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f'{name}: ganze Zahl erforderlich') from None
    if not isfinite(number) or number != int(number) or number < minimum:
        raise ValueError(f'{name}: ganze Zahl >= {minimum} erforderlich')
    return int(number)


def magazinbedarf(panels, kapazitaet, wagenplaetze=4):
    """Losreines Szenario; keine Aussage über reale Fahrten oder Fahrzeuganzahl."""
    if panels is None or kapazitaet is None:
        return None
    n = _ganzzahl(panels, 'Panelmenge')
    c = _ganzzahl(kapazitaet, 'wirksame Magazinkapazität', 1)
    w = _ganzzahl(wagenplaetze, 'Wagenplätze', 1)
    magazines = ceil(n / c)
    trips = ceil(magazines / w)
    return {
        'magazine': magazines,
        'wagenfahrten_losrein': trips,
        'restpanels': n % c,
        'belegte_plaetze_letzter_wagen': ((magazines - 1) % w + 1) if magazines else 0,
    }


def pufferbestand(ereignisse, anfangsbestand):
    """Zeitpunkt, Zugang, Abgang in ganzen Magazinen; gleiche Zeiten netto bilanzieren.

    Die Gleichzeitigkeit ist eine Modellannahme. Platzbedarf während physischer
    Übergabe muss zusätzlich untersucht werden. Keine Prognose oder Imputation.
    """
    if anfangsbestand is None:
        raise ValueError('Anfangsbestand fehlt')
    stock = _ganzzahl(anfangsbestand, 'Anfangsbestand')
    grouped = defaultdict(lambda: [0, 0])
    time_basis = None
    for timestamp, arriving, leaving in ereignisse:
        stamp = pd.Timestamp(timestamp)
        if pd.isna(stamp):
            raise ValueError('Ungültiger Ereigniszeitpunkt')
        has_offset = stamp.tzinfo is not None
        if time_basis is not None and time_basis != has_offset:
            raise ValueError('Gemischte Zeitbasis: offsetlose und offsetbehaftete Zeitpunkte')
        time_basis = has_offset
        if has_offset:
            stamp = stamp.tz_convert('UTC')
        grouped[stamp][0] += _ganzzahl(arriving, 'Zugang')
        grouped[stamp][1] += _ganzzahl(leaving, 'Abgang')
    result = []
    for stamp, (arriving, leaving) in sorted(grouped.items()):
        stock += arriving - leaving
        if stock < 0:
            raise ValueError(f'Unterdeckung bei {stamp}: Daten/Anfangsbestand prüfen')
        result.append({'zeitpunkt': stamp.isoformat(), 'zugang_magazine': arriving,
                       'abgang_magazine': leaving, 'bestand_magazine': stock})
    return result
