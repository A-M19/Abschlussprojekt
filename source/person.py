import json
import numpy as np
import pandas as pd
from PIL import Image

CSV_PATH = "data/athlete_physiological_dataset.csv"
PERSON_DB_PATH = "data/person_db.json"


def load_measurements():
    """Lädt die komplette Mess-CSV als DataFrame."""
    return pd.read_csv(CSV_PATH)


def get_athlete_measurements(athlete_id):
    """
    Liefert die 100 Messzeilen eines Athleten (z. B. 'Athlete_41') und fügt
    zwei GEFAKTE, aber stabile Spalten hinzu:
      - Date         : über die letzten ~7 Monate verteilte Trainingstage
      - Distance_km  : plausible Distanz je Einheit, abhängig von der Sportart

    Stabil heißt: gleicher Athlet -> immer dieselben Fake-Werte (Seed = Nummer).
    """
    df = load_measurements()
    rows = df[df["Athlete_ID"] == athlete_id].copy().reset_index(drop=True)
    if rows.empty:
        return rows

    n = len(rows)
    nummer = int("".join(c for c in str(athlete_id) if c.isdigit()) or "0")
    rng = np.random.default_rng(nummer)

    # Datum: n Trainings über die letzten ~7 Monate, chronologisch sortiert
    start = pd.Timestamp("2025-12-01")
    tage = np.sort(rng.integers(0, 210, size=n))
    rows["Date"] = [start + pd.Timedelta(days=int(t)) for t in tage]

    # Distanz je Sportart (gefakt, aber sinnvoll skaliert)
    sport = rows["Sport"].iloc[0]
    basis = {"Swimming": 2.5, "Track": 9.0, "Soccer": 7.0,
             "Basketball": 5.0, "Tennis": 4.0}.get(sport, 5.0)
    rows["Distance_km"] = np.round(rng.uniform(0.6, 1.4, size=n) * basis, 1)

    return rows


def get_person_data():
    """Lädt alle Personen aus der JSON-Datenbank als Person-Objekte."""
    with open(PERSON_DB_PATH, "r", encoding="utf-8") as file:
        person_data = json.load(file)

    person_object_list = []
    for d in person_data:
        person_object_list.append(
            Person(
                d["id"],
                d["date_of_birth"],
                d["firstname"],
                d["lastname"],
                d["picture_path"],
                d["sports"],
                d.get("gender", "Male"),
            )
        )
    return person_object_list


def get_person_by_id(person_id):
    """Sucht eine Person anhand ihrer Login-ID. Gibt None zurück, wenn nicht gefunden."""
    for p in get_person_data():
        if p.id == person_id:
            return p
    return None


class Person:

    def __init__(self, id, date_of_birth, firstname, lastname, picture_path, sports, gender="Male"):
        self.id = id
        self.date_of_birth = date_of_birth
        self.firstname = firstname
        self.lastname = lastname
        self.picture_path = picture_path
        self.sports = sports          # dict: { "Schwimmen": "Athlete_41", ... }
        self.gender = gender
        self.hr_max = self.calc_max_heart_rate()

    def calc_age(self):
        return 2026 - int(self.date_of_birth)

    def calc_max_heart_rate(self):
        age = self.calc_age()
        if self.gender.lower() == "female":
            return 226 - age
        else:
            return 220 - age

    def get_full_name(self):
        return self.lastname + ", " + self.firstname

    def get_sportarten(self):
        """Liste der Sportarten dieser Person (deutsche Namen)."""
        return list(self.sports.keys())

    def get_athlete_id_for_sport(self, sportart):
        """Liefert die CSV-Athlete_ID für eine gewählte Sportart."""
        return self.sports.get(sportart)

    def get_image(self):
        return Image.open(self.picture_path)