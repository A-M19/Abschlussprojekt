import streamlit as st
import json
import os

IMAGE_DIR = "data/pictures"
os.makedirs(IMAGE_DIR, exist_ok=True)

VORDEFINIERTE_SPORTARTEN = ["Laufen", "Radfahren", "Schwimmen", "Krafttraining", "Wandern", "Yoga", "Inline-Skaten"]


def lade_alle_athleten():
    try:
        with open("data/person_db.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Datenbank 'person_db.json' nicht gefunden!")
        return None


def speichere_alle_athleten(daten):
    with open("data/person_db.json", "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=4, ensure_ascii=False)


def ermittle_bildpfad_fuer_id(user_id_str: str):
    """Nimmt IMMER das Bild aus data/pictures/Athlete_<ID>.<ext>, falls vorhanden."""
    moegliche_endungen = ["png", "jpg", "jpeg"]
    for ext in moegliche_endungen:
        pfad = os.path.join(IMAGE_DIR, f"Athlete_{user_id_str}.{ext}")
        if os.path.exists(pfad):
            return pfad
    # Wenn nichts existiert, geben wir den Standardpfad mit png zurück
    return os.path.join(IMAGE_DIR, f"Athlete_{user_id_str}.png")


def zeige_profil_bearbeiten():
    st.markdown("### Meine persönlichen Daten bearbeiten")

    if "eingeloggt_als" not in st.session_state or st.session_state.eingeloggt_als is None:
        st.warning("Bitte logge dich zuerst ein, um dein Profil zu bearbeiten.")
        return
        
    aktuelle_id = st.session_state.eingeloggt_als
    user_id_str = str(aktuelle_id)

    alle_athleten = lade_alle_athleten()
    if alle_athleten is None:
        return

    aktueller_athlet = None
    index_oder_key = None
    ist_liste = isinstance(alle_athleten, list)
    
    if ist_liste:
        for index, athlet in enumerate(alle_athleten):
            if isinstance(athlet, dict) and str(athlet.get("id")) == user_id_str:
                aktueller_athlet = athlet
                index_oder_key = index
                break
    else:
        if user_id_str in alle_athleten:
            aktueller_athlet = alle_athleten[user_id_str]
            index_oder_key = user_id_str

    if aktueller_athlet is None:
        st.error(f"Fehler: Athlet mit der ID '{aktuelle_id}' wurde nicht gefunden.")
        return

    # --- IMMER BILD AUS data/pictures FÜR DIESE ID NUTZEN ---
    bildpfad_anzeige = ermittle_bildpfad_fuer_id(user_id_str)

    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists(bildpfad_anzeige):
            st.image(bildpfad_anzeige, width=100)
        else:
            st.image(
                "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
                width=100
            )

    # --- FORMULAR ---
    with st.form("profil_edit_form"):
        neuer_vorname = st.text_input("Vorname", value=aktueller_athlet.get("firstname", ""))
        neuer_nachname = st.text_input("Nachname", value=aktueller_athlet.get("lastname", ""))
        neue_email = st.text_input("E-Mail-Adresse", value=aktueller_athlet.get("email", ""))
        neues_telefon = st.text_input("Telefonnummer", value=aktueller_athlet.get("phone", ""))

        st.write("---")
        st.markdown("#### 📷 Profilbild ändern")

        hochgeladenes_bild = st.file_uploader(
            "Wähle ein neues Bild aus (Ersetzt das alte Bild im selben Pfad)",
            type=["png", "jpg", "jpeg"]
        )

        speichern_gedrueckt = st.form_submit_button("Änderungen speichern")

        if speichern_gedrueckt:

            # --- IMMER DEN PFAD IN data/pictures/Athlete_<ID>.* NUTZEN ---
            # Wenn schon eine Datei existiert, wird sie überschrieben.
            # Wenn nicht, wird eine neue mit passender Endung angelegt.
            if hochgeladenes_bild is not None:
                # Dateiendung aus Upload
                dateiendung = hochgeladenes_bild.name.split(".")[-1]
                bild_pfad_speichern = os.path.join(IMAGE_DIR, f"Athlete_{user_id_str}.{dateiendung}")

                # Falls eine Datei mit anderer Endung existiert, kannst du sie optional löschen:
                for ext in ["png", "jpg", "jpeg"]:
                    alter_pfad = os.path.join(IMAGE_DIR, f"Athlete_{user_id_str}.{ext}")
                    if os.path.exists(alter_pfad) and alter_pfad != bild_pfad_speichern:
                        os.remove(alter_pfad)

                # Falls Datei mit gleicher Endung existiert → löschen
                if os.path.exists(bild_pfad_speichern):
                    os.remove(bild_pfad_speichern)

                # Neues Bild speichern
                with open(bild_pfad_speichern, "wb") as f:
                    f.write(hochgeladenes_bild.getbuffer())

                # Pfad in DB aktualisieren (optional, aber sauber)
                aktueller_athlet["profile_pic"] = bild_pfad_speichern

            # --- TEXTFELDER SPEICHERN ---
            aktueller_athlet["firstname"] = neuer_vorname
            aktueller_athlet["lastname"] = neuer_nachname
            aktueller_athlet["email"] = neue_email
            aktueller_athlet["phone"] = neues_telefon

            # Änderungen speichern
            if ist_liste:
                alle_athleten[index_oder_key] = aktueller_athlet
            else:
                alle_athleten[index_oder_key] = aktueller_athlet

            speichere_alle_athleten(alle_athleten)

            st.success("Änderungen erfolgreich übernommen!")
            st.rerun()
