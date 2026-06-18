import json
from PIL import Image

def get_person_data():
    """Lädt alle Personen aus der JSON-Datenbank"""
    with open("data/person_db.json", "r", encoding="utf-8") as file:
        person_data = json.load(file)

    person_object_list = []
    for person_dict in person_data:
        # Falls "gender" fehlt ODER als "unknown" in der JSON steht, 
        # setzen wir es hier im Code sicherheitshalber auf "male" (wie in der Angabe gewünscht)
        gender_value = person_dict.get("gender", "male")
        if gender_value.lower() == "unknown":
            gender_value = "male"

        person_object = Person(
            person_dict["id"],
            person_dict["date_of_birth"],
            person_dict["firstname"],
            person_dict["lastname"],
            person_dict["picture_path"],
            person_dict["ekg_tests"],
            gender_value  # Übergabe des bereinigten Werts
        )
        person_object_list.append(person_object)
    return person_object_list


def get_person_object_by_full_name(full_name):
    """Gibt ein Person-Objekt anhand des vollen Namens zurück"""
    persons = get_person_data()
    firstname = full_name.split(", ")[1]
    lastname = full_name.split(", ")[0]
    for person in persons:
        if person.firstname == firstname and person.lastname == lastname:
            return person
    return None  # Absicherung, falls kein Name matcht


class Person:

    def __init__(self, id, date_of_birth, firstname, lastname, picture_path, ekg_tests, gender="male"):
        self.id = id
        self.date_of_birth = date_of_birth
        self.firstname = firstname
        self.lastname = lastname
        self.picture_path = picture_path
        self.ekg_tests = ekg_tests
        self.gender = gender
        
        # Aufruf der geforderten Methode zur Berechnung der maximalen Herzfrequenz
        self.hr_max = self.calc_max_heart_rate()

    def calc_age(self):
        """Berechnet das Alter basierend auf dem Geburtsjahr (laut Aufgabenstellung gefordert)"""
        # Hinweis: 2025 ist super, alternativ 2026 für das aktuelle Jahr
        return 2026 - int(self.date_of_birth)

    def calc_max_heart_rate(self):
        """Berechnet die maximale Herzfrequenz basierend auf Alter und Geschlecht (laut Aufgabenstellung gefordert)"""
        age = self.calc_age()
        # Berücksichtigung des Geschlechts laut medizinischem Standard (Fox & Haskell)
        if self.gender.lower() == "female":
            return 226 - age
        else:
            return 220 - age

    def set_hr(self, hr):
        self.hr_max = hr

    def get_full_name(self):
        return self.lastname + ", " + self.firstname

    def get_image(self):
        image = Image.open(self.picture_path)
        return image