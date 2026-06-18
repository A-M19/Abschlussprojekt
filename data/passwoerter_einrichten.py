"""
Legt für jede Person aus person_db.json ein Login-Passwort an und speichert
die bcrypt-Hashes in auth_db.json.

Standard-Passwort für ALLE: geheim123   (kannst du unten ändern)

Aufruf:  python passwoerter_einrichten.py   (nach daten_generieren.py ausführen!)
"""

import json
import bcrypt

PERSON_DB_PATH = "data/person_db.json"
AUTH_DB_PATH = "data/auth_db.json"
STANDARD_PASSWORT = "geheim123"


def main():
    with open(PERSON_DB_PATH, "r", encoding="utf-8") as f:
        personen = json.load(f)

    auth_db = {}
    for p in personen:
        hashed = bcrypt.hashpw(STANDARD_PASSWORT.encode("utf-8"), bcrypt.gensalt())
        auth_db[str(p["id"])] = hashed.decode("utf-8")

    with open(AUTH_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(auth_db, f, indent=2)

    print(f"{len(auth_db)} Passwörter gesetzt -> {AUTH_DB_PATH}")
    print(f"Passwort für alle: {STANDARD_PASSWORT}\n")
    print("Login-IDs:")
    for p in personen:
        print(f"  {p['id']}  ({p['firstname']} {p['lastname']})")


if __name__ == "__main__":
    main()