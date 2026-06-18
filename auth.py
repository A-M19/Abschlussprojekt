import json
import os
import random
import bcrypt

AUTH_DB_PATH = "data/auth_db.json"


def _load_auth_db():
    if not os.path.exists(AUTH_DB_PATH):
        return {}
    with open(AUTH_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_auth_db(db):
    with open(AUTH_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def login_user(login_id, password):
    """Prüft ID + Passwort gegen die bcrypt-Hashes in auth_db.json."""
    db = _load_auth_db()
    gespeicherter_hash = db.get(str(login_id))
    if gespeicherter_hash is None:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), gespeicherter_hash.encode("utf-8"))


def register_user(password):
    """
    Legt einen neuen Account an, vergibt eine zufällige, freie 5-stellige ID
    und gibt diese ID zurück (oder None bei Fehler).
    """
    db = _load_auth_db()

    # freie 5-stellige ID finden
    while True:
        neue_id = random.randint(10000, 99999)
        if str(neue_id) not in db:
            break

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    db[str(neue_id)] = hashed.decode("utf-8")
    _save_auth_db(db)
    return neue_id