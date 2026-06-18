import bcrypt
import json

# Deine 10 Nutzer mit ihren Passwörtern (im echten Leben wählt das der User, hier für deine Test-User)
klartext_passwörter = {
    f"Nutzer_{i}": "geheim123" for i in range(1, 11)
}

datenbank = {}

for username, passwort in klartext_passwörter.items():
    # Passwort in Bytes umwandeln und salzen/hashing
    pass_bytes = passwort.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(pass_bytes, salt)
    
    # Als Text speichern, damit es in JSON geschrieben werden kann
    datenbank[username] = hashed_pass.decode('utf-8')

# In einer JSON-Datei als "Datenbank" abspeichern
with open("users_db.json", "w") as f:
    json.dump(datenbank, f, indent=4)

print("Nutzerdatenbank mit Bcrypt erfolgreich erstellt!")