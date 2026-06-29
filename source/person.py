import json
import os
import pandas as pd
from PIL import Image

RAW_CSV = "data/athlete_physiological_dataset.csv"
SESSIONS_CSV = "data/training_sessions.csv"   # angereichert: + Date, Duration_min, Distance_km
PERSON_DB_PATH = "data/person_db.json"


def load_measurements():
    """
    Lädt die Messdaten. Bevorzugt die angereicherte Datei (mit Date/Duration_min/
    Distance_km); falls die noch nicht erzeugt wurde, fällt sie auf die Roh-CSV zurück.
    """
    if os.path.exists(SESSIONS_CSV):
        return pd.read_csv(SESSIONS_CSV, parse_dates=["Date"])
    return pd.read_csv(RAW_CSV)


def get_athlete_measurements(athlete_id):
    """Liefert die Messzeilen eines Athleten (z. B. 'Athlete_41')."""
    df = load_measurements()
    return df[df["Athlete_ID"] == athlete_id].reset_index(drop=True)


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


# NEUE FUNKTION: Erstellt den Athleten mit der richtigen Struktur direkt in der person_db.json
def create_new_athlete(id, firstname="Neuer", lastname="Athlet", gender="Male", date_of_birth="2000"):
    """
    Erstellt einen brandneuen Athleten, speichert ihn in der person_db.json
    und stellt sicher, dass alle für die Person-Klasse notwendigen Felder existieren.
    """
    daten_liste = []
    if os.path.exists(PERSON_DB_PATH):
        try:
            with open(PERSON_DB_PATH, "r", encoding="utf-8") as file:
                daten_liste = json.load(file)
        except Exception:
            daten_liste = []

    # Sicherheits-Check: ID darf nicht doppelt eingetragen werden
    if any(str(p.get("id")) == str(id) for p in daten_liste):
        return

    # Struktur exakt an get_person_data() angepasst
    neuer_eintrag = {
        "id": int(id),
        "date_of_birth": str(date_of_birth),
        "firstname": firstname,
        "lastname": lastname,
        "picture_path": f"data/pictures/Athlete_{id}.png",
        "sports": {}, # Startet leer, damit Sportarten später hinzugefügt werden können
        "gender": gender
    }
    
    daten_liste.append(neuer_eintrag)

    # Permanent in die JSON-Datei schreiben
    with open(PERSON_DB_PATH, "w", encoding="utf-8") as file:
        json.dump(daten_liste, file, indent=4, ensure_ascii=False)


class Person:

    def __init__(self, id, date_of_birth, firstname, lastname, picture_path, sports, gender="Male"):
        self.id = id
        self.date_of_birth = date_of_birth
        self.firstname = firstname
        self.lastname = lastname
        self.picture_path = picture_path
        self.sports = sports          # dict: { "Schwimmen": "Athlete_41", ... }
        self.gender = gender

    def calc_age(self):
        return 2026 - int(self.date_of_birth)

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