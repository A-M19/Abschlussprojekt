import streamlit as st
import json
import os
import bcrypt
from source import person  # Hier war der Fehler! Jetzt richtig aus source geladen.

AUTH_FILE = "data/auth_db.json"

def load_auth_data():
    if not os.path.exists(AUTH_FILE):
        # Falls die Datei nicht existiert, erstellen wir sie mit Standard-Usern
        os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)
        initial_data = {}
        # Wir hashen das Standard-Passwort "geheim123" für die Test-Nutzer
        pwd_hash = bcrypt.hashpw("geheim123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        for i in range(1, 9):
            initial_data[str(i)] = pwd_hash
        with open(AUTH_FILE, "w", encoding="utf-8") as file:
            json.dump(initial_data, file, indent=4)
        return initial_data
        
    with open(AUTH_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_auth_data(data):
    with open(AUTH_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def login_user(username, password):
    # Erst prüfen wir, ob der Athlet überhaupt in der person_db.json existiert
    try:
        alle_athleten = person.get_person_data()
        athlet_existiert = False
        
        # Abfangen, ob die ID als Zahl oder String in der Liste ist
        for ath in alle_athleten:
            if str(ath.id) == str(username):
                athlet_existiert = True
                break
                
        if not athlet_existiert:
            return False
            
    except Exception:
        # Falls beim Lesen der JSON irgendetwas schiefgeht, blockieren wir sicherheitshalber
        return False

    # Wenn der Athlet existiert, prüfen wir das Passwort
    auth_data = load_auth_data()
    if username in auth_data:
        stored_hash = auth_data[username].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    return False

def register_user(username, password):
    auth_data = load_auth_data()
    if username in auth_data:
        return False  # User existiert bereits
        
    # Passwort hashen und speichern
    pwd_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    auth_data[username] = pwd_hash
    save_auth_data(auth_data)
    return True