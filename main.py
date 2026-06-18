import json
import os
import pandas as pd

# Pfade zu deinen Datensätzen
JSON_PATH = "athletes.json"
CSV_PATH = "data/athlete_physiological_dataset.csv"

def load_athletes():
    """Lädt die Athleten aus der JSON-Datei."""
    if not os.path.exists(JSON_PATH):
        # Falls die Datei noch nicht existiert, starten wir mit einer leeren Liste
        return []
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def save_athletes(athletes):
    """Speichert die Athleten-Liste dauerhaft zurück in die JSON-Datei."""
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(athletes, file, indent=2, ensure_ascii=False)
    print("✓ Daten erfolgreich in athletes.json gespeichert.")

def update_athlete_personal_data(athlete_id, firstname=None, lastname=None, date_of_birth=None):
    """Überarbeitet die Personendaten eines bestehenden Athleten."""
    athletes = load_athletes()
    
    for athlete in athletes:
        if athlete["id"] == athlete_id:
            if firstname:
                athlete["firstname"] = firstname
            if lastname:
                athlete["lastname"] = lastname
            if date_of_birth:
                athlete["date_of_birth"] = date_of_birth
            
            save_athletes(athletes)
            print(f"✓ Personendaten für Athlet ID {athlete_id} wurden aktualisiert.")
            return True
            
    print(f"✗ Athlet mit ID {athlete_id} wurde nicht gefunden.")
    return False

def add_ekg_test(athlete_id, test_date, test_type, intensity_filter):
    """Fügt einer Person eine neue Leistungsaufnahme (EKG-Test) hinzu."""
    athletes = load_athletes()
    
    for athlete in athletes:
        if athlete["id"] == athlete_id:
            # Automatische ID-Vergabe für den neuen Test innerhalb des Athleten
            existing_ids = [test["id"] for test in athlete["ekg_tests"]] if "ekg_tests" in athlete else []
            new_test_id = max(existing_ids) + 1 if existing_ids else 1
            
            new_test = {
                "id": new_test_id,
                "date": test_date,
                "test_type": test_type,                     # z.B. "Ruhe" oder "Belastung"
                "result_link": "data/athlete_physiological_dataset.csv", # Verweis auf die CSV
                "athlete_id": f"Athlete_{athlete_id}",       # z.B. "Athlete_1" für den CSV-Filter
                "intensity_filter": intensity_filter         # z.B. "Low", "Medium" oder "High"
            }
            
            if "ekg_tests" not in athlete:
                athlete["ekg_tests"] = []
                
            athlete["ekg_tests"].append(new_test)
            save_athletes(athletes)
            print(f"✓ Neuer Test (Typ: {test_type}) zu Athlet ID {athlete_id} hinzugefügt.")
            return True
            
    print(f"✗ Athlet mit ID {athlete_id} wurde nicht gefunden.")
    return False

def main():
    # --- BEISPIEL FÜR DIE APP-LOGIK ---
    print("--- Sportler-Verwaltungs-App gestartet ---")
    
    # 1. Beispiel: Nutzer überarbeitet seine Personendaten (z.B. Tippfehler im Namen korrigieren)
    # Wir ändern den Nachnamen von ID 3 (Augustus Gloob -> Augustus Gloop)
    update_athlete_personal_data(athlete_id=3, lastname="Gloop")
    
    # 2. Beispiel: Eine neue Leistungsaufnahme / EKG-Test hinzufügen
    # Jenny Wells (ID 1) hat am 18.06.2026 einen neuen maximalen Belastungstest absolviert
    add_ekg_test(
        athlete_id=1, 
        test_date="18.06.2026", 
        test_type="Maximal-Belastung", 
        intensity_filter="High"
    )

if __name__ == "__main__":
    main()