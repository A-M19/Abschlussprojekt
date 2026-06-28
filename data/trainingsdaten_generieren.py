"""
Reichert den Original-Datensatz um Date, Duration_min und Distance_km an,
OHNE die Roh-CSV zu verändern. Ergebnis: data/training_sessions.csv

Aufruf:  python data/trainingsdaten_generieren.py
"""

import numpy as np
import pandas as pd

RAW_CSV = "data/athlete_physiological_dataset.csv"   # bleibt unangetastet
OUTPUT_CSV = "data/training_sessions.csv"            # angereicherte Kopie

# Dauer je Intensität: (Mittelwert in Minuten, Schwankung)
DAUER = {"Low": (75, 15), "Medium": (50, 12), "High": (32, 10)}

# Geschwindigkeit (km/h) je Sportart & Intensität – nur für Distanz-Sportarten
TEMPO = {
    "Track":    {"Low": 8.5, "Medium": 11.0, "High": 13.5},   # Laufen
    "Swimming": {"Low": 2.2, "Medium": 2.8,  "High": 3.4},
}
DISTANZ_SPORTARTEN = {"Track", "Swimming"}

START = pd.Timestamp("2025-12-01")
ZEITRAUM_TAGE = 210  # ~7 Monate


def main():
    df = pd.read_csv(RAW_CSV).reset_index(drop=True)

    datum = [pd.NaT] * len(df)
    dauer = [np.nan] * len(df)
    distanz = [np.nan] * len(df)

    # pro Athlet: deterministischer Seed -> stabile Werte bei jedem Lauf
    for ath, positionen in df.groupby("Athlete_ID").groups.items():
        positionen = list(positionen)
        n = len(positionen)
        nummer = int("".join(c for c in str(ath) if c.isdigit()) or "0")
        rng = np.random.default_rng(nummer)

        tage = np.sort(rng.integers(0, ZEITRAUM_TAGE, size=n))

        for k, pos in enumerate(positionen):
            zeile = df.loc[pos]
            intensitaet = zeile["Training_Intensity"]
            sportart = zeile["Sport"]
            hr = zeile["Heart_Rate"]

            # 0..1: wie hoch liegt die Herzfrequenz dieser Einheit
            hr_faktor = float(np.clip((hr - 90) / (180 - 90), 0, 1))

            # Dauer: höhere HF -> etwas kürzer
            d_mid, d_swing = DAUER.get(intensitaet, (50, 12))
            d = d_mid - d_swing * (hr_faktor - 0.5) * 2 + rng.normal(0, 4)
            d = float(max(10, round(d)))

            datum[pos] = START + pd.Timedelta(days=int(tage[k]))
            dauer[pos] = d

            # Distanz nur für Laufen & Schwimmen
            if sportart in DISTANZ_SPORTARTEN:
                tempo_mid = TEMPO[sportart][intensitaet]
                # höhere HF -> etwas schneller
                tempo = tempo_mid * (0.9 + 0.2 * hr_faktor) + rng.normal(0, tempo_mid * 0.05)
                tempo = max(0.5, tempo)
                distanz[pos] = round(tempo * d / 60, 2)

    df["Date"] = datum
    df["Duration_min"] = dauer
    df["Distance_km"] = distanz

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Angereicherte Datei geschrieben -> {OUTPUT_CSV}  ({len(df)} Zeilen)")
    print("Neue Spalten: Date, Duration_min, Distance_km")


if __name__ == "__main__":
    main()