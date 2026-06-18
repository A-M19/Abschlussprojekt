"""
Erzeugt 10 "Personen" aus dem Athleten-Datensatz.

Jede Person besteht aus 5 Athleten GLEICHEN Geschlechts -- einer pro Sportart
(Schwimmen, Basketball, Leichtathletik, Fußball, Tennis). Jede Person bekommt
eine zufällige 5-stellige Login-ID und ein Profilbild (reihum aus data/pictures).

Aufruf:  python daten_generieren.py
Ergebnis: data/person_db.json
"""

import json
import os
import glob
import random
import pandas as pd

CSV_PATH = "data/athlete_physiological_dataset.csv"
OUTPUT_PATH = "data/person_db.json"
PICTURE_DIR = "data/pictures"

# Deutsche Sport-Bezeichnung  ->  Bezeichnung in der CSV
SPORT_MAP = {
    "Schwimmen": "Swimming",
    "Basketball": "Basketball",
    "Leichtathletik": "Track",
    "Fußball": "Soccer",
    "Tennis": "Tennis",
}

VORNAMEN_M = ["Lukas", "Jonas", "Felix", "Maximilian", "Paul",
              "Leon", "Finn", "Elias", "Noah", "Ben"]
VORNAMEN_W = ["Mia", "Emma", "Hannah", "Lea", "Lena",
              "Marie", "Sophie", "Lina", "Clara", "Anna"]
NACHNAMEN = ["Müller", "Schmidt", "Wagner", "Becker", "Hoffmann",
             "Koch", "Bauer", "Richter", "Klein", "Wolf"]

PERSONEN_PRO_GESCHLECHT = 5   # 5 + 5  ->  insgesamt 10 Personen


def main():
    random.seed(42)  # reproduzierbar: bei jedem Lauf dieselben Personen
    df = pd.read_csv(CSV_PATH)

    # Pro (Sportart, Geschlecht) eine gemischte Liste verfügbarer Athleten-IDs
    pools = {}
    for sport_csv in SPORT_MAP.values():
        for gender in ["Male", "Female"]:
            ids = df[(df["Sport"] == sport_csv) & (df["Gender"] == gender)]["Athlete_ID"].unique().tolist()
            random.shuffle(ids)
            pools[(sport_csv, gender)] = ids

    # Vorhandene Bilder einsammeln (reihum verteilt)
    bilder = sorted(glob.glob(os.path.join(PICTURE_DIR, "*.jpg")) +
                    glob.glob(os.path.join(PICTURE_DIR, "*.png")))
    if not bilder:
        bilder = ["data/pictures/placeholder.jpg"]

    benutzte_ids = set()
    personen = []
    bild_index = 0

    for gender in ["Male", "Female"]:
        vornamen = VORNAMEN_M if gender == "Male" else VORNAMEN_W
        for _ in range(PERSONEN_PRO_GESCHLECHT):
            # je einen Athleten pro Sportart aus dem passenden Pool ziehen
            sports = {}
            for sport_de, sport_csv in SPORT_MAP.items():
                sports[sport_de] = pools[(sport_csv, gender)].pop()

            # Alter aus einem der Athleten übernehmen
            referenz_athlet = sports["Leichtathletik"]
            age = int(df[df["Athlete_ID"] == referenz_athlet]["Age"].iloc[0])
            geburtsjahr = 2026 - age

            # eindeutige 5-stellige Login-ID
            while True:
                login_id = random.randint(10000, 99999)
                if login_id not in benutzte_ids:
                    benutzte_ids.add(login_id)
                    break

            bild = bilder[bild_index % len(bilder)].replace("\\", "/")
            bild_index += 1

            personen.append({
                "id": login_id,
                "firstname": random.choice(vornamen),
                "lastname": random.choice(NACHNAMEN),
                "gender": gender,
                "date_of_birth": geburtsjahr,
                "picture_path": bild,
                "sports": sports,
            })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(personen, f, indent=2, ensure_ascii=False)

    print(f"{len(personen)} Personen erzeugt -> {OUTPUT_PATH}\n")
    for p in personen:
        print(f"  ID {p['id']}  |  {p['firstname']} {p['lastname']}  ({p['gender']})")


if __name__ == "__main__":
    main()