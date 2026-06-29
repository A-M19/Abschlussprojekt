# views/diagramme/zeit.py  -- gemeinsame Zeitraum-Logik fuer beide Diagramme
import pandas as pd

WOCHENTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
MONATE = {1: "Jan", 2: "Feb", 3: "Mär", 4: "Apr", 5: "Mai", 6: "Jun",
          7: "Jul", 8: "Aug", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Dez"}


def heute():
    return pd.Timestamp.today().normalize()


def zeitfenster(zeitraum, today=None):
    """Gibt (start, ende) zurueck - ende ist exklusiv. Anker ist das heutige Datum."""
    t = today if today is not None else heute()
    if zeitraum == "Letzte Woche":
        start = t - pd.Timedelta(days=t.weekday())          # Montag dieser Woche
        ende = start + pd.Timedelta(days=7)
    elif zeitraum == "Letzter Monat":
        montag = t - pd.Timedelta(days=t.weekday())
        start = montag - pd.Timedelta(weeks=4)              # 5 Wochen-Fenster
        ende = montag + pd.Timedelta(days=7)
    else:  # Letzte 6 Monate
        start = t.replace(day=1) - pd.DateOffset(months=5)
        ende = t.replace(day=1) + pd.DateOffset(months=1)
    return start, ende


def im_fenster(daten, zeitraum, today=None):
    start, ende = zeitfenster(zeitraum, today)
    return daten[(daten["Date"] >= start) & (daten["Date"] < ende)]


def aggregiere(daten, spalte, zeitraum, today=None):
    """Summe je Bucket mit VOLLSTAENDIGER fester Kategorienliste (keine Stretch-Balken)."""
    start, ende = zeitfenster(zeitraum, today)
    sub = daten[(daten["Date"] >= start) & (daten["Date"] < ende)].copy()

    if zeitraum == "Letzte Woche":
        idx = pd.date_range(start, periods=7, freq="D")
        schluessel = sub["Date"].dt.normalize()
        werte = sub.groupby(schluessel)[spalte].sum().reindex(idx, fill_value=0)
        labels = [WOCHENTAGE[d.weekday()] for d in idx]
    elif zeitraum == "Letzter Monat":
        idx = pd.date_range(start, periods=5, freq="W-MON")
        wk = (sub["Date"] - pd.to_timedelta(sub["Date"].dt.weekday, unit="D")).dt.normalize()
        werte = sub.groupby(wk)[spalte].sum().reindex(idx, fill_value=0)
        labels = [d.strftime("%d.%m") for d in idx]
    else:
        idx = pd.date_range(start, periods=6, freq="MS")
        mk = sub["Date"].dt.to_period("M").dt.to_timestamp()
        werte = sub.groupby(mk)[spalte].sum().reindex(idx, fill_value=0)
        labels = [f"{MONATE[d.month]} {d.year % 100:02d}" for d in idx]

    df = pd.DataFrame({"Label": labels, "Wert": werte.round(1).values})
    return df, labels


def _anker(daten, today=None):
    if today is not None and pd.notna(today):
        return pd.Timestamp(today).normalize()
    if "Date" in daten and daten["Date"].notna().any():
        return daten["Date"].max().normalize()
    return heute()


def _bucket_info(zeitraum, start):
    """Liefert (bucket_index, label_map, reihenfolge) je Zeitraum."""
    if zeitraum == "Letzte Woche":
        idx = pd.date_range(start, periods=7, freq="D")
        labelmap = {d: WOCHENTAGE[d.weekday()] for d in idx}
    elif zeitraum == "Letzter Monat":
        idx = pd.date_range(start, periods=5, freq="W-MON")
        labelmap = {d: d.strftime("%d.%m") for d in idx}
    else:
        idx = pd.date_range(start, periods=6, freq="MS")
        labelmap = {d: f"{MONATE[d.month]} {d.year % 100:02d}" for d in idx}
    return idx, labelmap, [labelmap[d] for d in idx]


def _bucket_key(reihen, zeitraum):
    if zeitraum == "Letzte Woche":
        return reihen["Date"].dt.normalize()
    if zeitraum == "Letzter Monat":
        return (reihen["Date"] - pd.to_timedelta(reihen["Date"].dt.weekday, unit="D")).dt.normalize()
    return reihen["Date"].dt.to_period("M").dt.to_timestamp()


def aggregiere_nach_intensitaet(daten, spalte, zeitraum, today=None):
    """Summe je (Bucket, Intensität) -> langes DataFrame für gestapelte Balken."""
    t = _anker(daten, today)
    start, ende = zeitfenster(zeitraum, t)
    sub = daten[(daten["Date"] >= start) & (daten["Date"] < ende)].copy()
    idx, labelmap, reihenfolge = _bucket_info(zeitraum, start)

    if sub.empty:
        return pd.DataFrame(columns=["Label", "Training_Intensity", "Wert"]), reihenfolge

    # KORREKTUR: Bereinigt die Intensitätsspalte für manuelle Einträge
    if "Training_Intensity" in sub.columns:
        # Falls deutsche Begriffe aus dem Formular reingeschrieben wurden, übersetzen wir sie live
        de_zu_en = {"Niedrig": "Low", "Moderat": "Medium", "Hoch": "High"}
        sub["Training_Intensity"] = sub["Training_Intensity"].replace(de_zu_en).fillna("Medium")
    else:
        sub["Training_Intensity"] = "Medium"

    # Bucket berechnen und Typen-Gleichheit für das Mapping erzwingen
    sub["bucket"] = _bucket_key(sub, zeitraum)
    sub["bucket"] = pd.to_datetime(sub["bucket"]).dt.normalize()

    # Aggregation ausführen
    g = sub.groupby(["bucket", "Training_Intensity"])[spalte].sum().reset_index()
    
    # Mapping auf die lesbaren Labels (z.B. "29.06")
    g["Label"] = g["bucket"].map(labelmap)
    g = g.dropna(subset=["Label"])
    g["Wert"] = g[spalte].round(1)
    
    return g[["Label", "Training_Intensity", "Wert"]], reihenfolge