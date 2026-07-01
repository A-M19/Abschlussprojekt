# Beat faster! 

Ein Fitness-Dashboard, gebaut mit **Streamlit**. Nach dem Login sieht man pro Sportart seine Trainingsdaten als Diagramme im Strava-Stil (Aktivität pro Monat, Herzfrequenz), kann eigene Trainings hinzufügen, sein Profil bearbeiten und seine Leistung vergleichen.

Dieses Projekt ist im Rahmen der Programmierübung als Abschlussprojekt entstanden.

---

## Voraussetzungen

- **Python 3** (getestet mit 3.11+)
- Alle nötigen Pakete stehen in der `requirements.txt` 

---

## Installation & Start

1. **Alle benötigten Pakete installieren** 

   ```bash
   pip install -r requirements.txt
   ```

   Damit werden automatisch alle Abhängigkeiten heruntergeladen, die die App braucht.

2. **App starten**

   ```bash
   streamlit run main.py
   ```

   Danach öffnet sich die App automatisch im Browser 

---

## Login / Testzugang

Die App startet auf der Login-Seite. Man meldet sich mit einer **ID** und einem **Passwort** an.

Zum Ausprobieren gibt es 10 vorbereitete Beispiel-Personen. Zum Beispiel:

- **ID:** `63354`
- **Passwort:** `123`

Die **IDs aller 10 Beispiel-Personen** stehen in der Datei `data/auth_db.json` (das sind dort die Schlüssel). Alle Beispiel-Accounts nutzen dasselbe Passwort **`123`**.

Über *„neuen Account erstellen"* kann man sich außerdem selbst registrieren – dabei wird automatisch eine neue, zufällige ID vergeben.

---

## Funktionen

- **Login & Registrierung** mit bcrypt-gehashten Passwörtern
- **Dashboard** mit Filter nach Sportart und Trainingsintensität
- **Aktivitäts-Zusammenfassung**: Ø Herzfrequenz, O₂-Sättigung, Muskel-Aktivität
- **Aktivitäts-Diagramm** (gestapelte Balken nach Intensität, umschaltbar zwischen Dauer und Kilometern)
- **Herzfrequenz-Diagramm** mit farbcodierten Intensitätszonen
- **Zeitraum-Auswahl**: letzte 6 Monate / letzter Monat / letzte Woche
- **Training hinzufügen**: eigene Einheiten (inkl. selbst angelegter Sportarten) erfassen
- **Profil bearbeiten**: Name, Kontaktdaten und Profilbild ändern
- **Leistungsvergleich** zwischen den Sportarten
- Durchgängiges dunkles **Strava-inspiriertes Design**

---

## Hinweise zu den Daten

Die Beispiel-Personen und Login-Daten (`person_db.json`, `auth_db.json`, `training_sessions.csv`) sind bereits im Projekt enthalten – die App ist also direkt startklar.

Die Daten sind teilweise **synthetisch**: Aus dem physiologischen Datensatz werden je 5 Athleten (eine pro Sportart) zu einer Person gebündelt, und die Trainingsdaten werden mit erzeugten Datums-, Dauer- und Kilometerwerten angereichert, damit sich die Verläufe über die Monate sinnvoll darstellen lassen. Für ein Übungsprojekt ist das bewusst so gewählt.