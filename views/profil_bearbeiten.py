import streamlit as st
import json
import os
from PIL import Image

IMAGE_DIR = "data/pictures"
os.makedirs(IMAGE_DIR, exist_ok=True)


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


def standard_bildpfad(user_id_str: str):
    return os.path.join(IMAGE_DIR, f"Athlete_{user_id_str}.png")


def zeige_profil_bearbeiten():
    st.markdown("### Meine persönlichen Daten bearbeiten")

    if st.session_state.get("profil_gespeichert", False):
        st.success("Änderungen erfolgreich gespeichert")
        st.session_state.profil_gespeichert = False

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

        if aktueller_athlet is None and str(aktuelle_id).isdigit():
            idx = int(aktuelle_id)
            if 0 <= idx < len(alle_athleten):
                aktueller_athlet = alle_athleten[idx]
                index_oder_key = idx
    else:
        if user_id_str in alle_athleten:
            aktueller_athlet = alle_athleten[user_id_str]
            index_oder_key = user_id_str
        elif str(aktuelle_id).isdigit() and int(aktuelle_id) in alle_athleten:
            aktueller_athlet = alle_athleten[int(aktuelle_id)]
            index_oder_key = int(aktuelle_id)

    if aktueller_athlet is None:
        st.error(f"Fehler: Athlet mit der ID '{aktuelle_id}' wurde nicht gefunden.")
        return

    bildpfad = standard_bildpfad(user_id_str)

    if os.path.exists(bildpfad):
        st.image(bildpfad, width=110)

    with st.form("profil_edit_form"):
        neuer_vorname = st.text_input("Vorname", value=aktueller_athlet.get("firstname", ""))
        neuer_nachname = st.text_input("Nachname", value=aktueller_athlet.get("lastname", ""))
        neue_email = st.text_input("E-Mail-Adresse", value=aktueller_athlet.get("email", ""))
        neues_telefon = st.text_input("Telefonnummer", value=aktueller_athlet.get("phone", ""))

        st.write("---")
        st.markdown("#### Profilbild bearbeiten")

        hochgeladenes_bild = st.file_uploader(
            "Neues Profilbild auswählen",
            type=["png", "jpg", "jpeg"]
        )

        speichern_gedrueckt = st.form_submit_button("Änderungen speichern")

        if speichern_gedrueckt:
            # Textdaten speichern
            if ist_liste:
                alle_athleten[index_oder_key]["firstname"] = neuer_vorname
                alle_athleten[index_oder_key]["lastname"] = neuer_nachname
                alle_athleten[index_oder_key]["email"] = neue_email
                alle_athleten[index_oder_key]["phone"] = neues_telefon
                ziel = alle_athleten[index_oder_key]
            else:
                alle_athleten[index_oder_key]["firstname"] = neuer_vorname
                alle_athleten[index_oder_key]["lastname"] = neuer_nachname
                alle_athleten[index_oder_key]["email"] = neue_email
                alle_athleten[index_oder_key]["phone"] = neues_telefon
                ziel = alle_athleten[index_oder_key]

            # Bild nur ersetzen, wenn wirklich ein neues hochgeladen wurde
            if hochgeladenes_bild is not None:
                # Alte Varianten loeschen
                for ext in ["png", "jpg", "jpeg"]:
                    alter_pfad = os.path.join(IMAGE_DIR, f"Athlete_{user_id_str}.{ext}")
                    if os.path.exists(alter_pfad):
                        os.remove(alter_pfad)

                # Neues Bild IMMER unter demselben Pfad speichern
                bild = Image.open(hochgeladenes_bild).convert("RGB")
                bild.save(bildpfad, format="PNG")

                # Alle moeglichen Bildpfad-Felder synchron setzen
                ziel["profile_pic"] = bildpfad
                ziel["picture_path"] = bildpfad
                ziel["image_path"] = bildpfad
                ziel["image"] = bildpfad
                ziel["picture"] = bildpfad

            speichere_alle_athleten(alle_athleten)
            st.session_state.profil_gespeichert = True
            st.rerun()
