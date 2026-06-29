import streamlit as st
import json
import os
from auth import login_user, register_user

# Absoluter Import aus dem Hauptverzeichnis
from views.hilfe_button import zeige_hilfe_bereich


def ueberpruefe_ob_benutzer_existiert(username):
    """
    Überprüft in der person_db.json, ob der Name bereits vergeben ist.
    """
    json_pfad = os.path.join("data", "person_db.json")
    if os.path.exists(json_pfad):
        try:
            with open(json_pfad, "r", encoding="utf-8") as f:
                daten_liste = json.load(f)
                for nutzer in daten_liste:
                    # Prüft sowohl 'username' als auch 'firstname' (case-insensitive)
                    existierender_name = nutzer.get("username") or nutzer.get("firstname")
                    if existierender_name and str(existierender_name).strip().lower() == str(username).strip().lower():
                        return True
        except Exception:
            pass
    return False


def render_login_page():
    # ----------------------------- LOGIN -----------------------------
    if st.session_state.page == "login":
        st.title("Beat faster!")

        login_id = st.text_input("ID", placeholder="z. B. 12345")
        password = st.text_input("Passwort", type="password")

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Anmelden", use_container_width=True):
                if login_id == "" or password == "":
                    st.error("Bitte alle Felder ausfüllen!")
                elif login_user(login_id, password):
                    st.session_state.eingeloggt_als = login_id
                    st.session_state.page = "hauptseite"
                    st.rerun()
                else:
                    st.error("Falsche ID oder Passwort!")

        with col2:
            if st.button("neuen Account erstellen"):
                st.session_state.page = "registrieren"
                st.rerun()

    # -------------------------- REGISTRIEREN --------------------------
    elif st.session_state.page == "registrieren":
        st.title("Registrieren")

        name = st.text_input("Name")
        pw1 = st.text_input("Passwort", type="password")
        pw2 = st.text_input("Passwort wiederholen", type="password")

        if st.button("Account erstellen"):
            if name.strip() == "" or pw1 == "":
                st.error("Felder dürfen nicht leer sein!")
            elif pw1 != pw2:
                st.error("Passwörter stimmen nicht überein!")
            # Die Duplikats-Überprüfung vor der Registrierung
            elif ueberpruefe_ob_benutzer_existiert(name):
                st.error("Benutzername und Passwort existiert schon, bitte neue Log in Daten wählen")
            else:
                neue_id = register_user(pw1)
                if neue_id is not None:
                    st.session_state.neue_id = neue_id
                    st.session_state.page = "erfolg"
                    st.rerun()
                else:
                    st.error("Account konnte nicht erstellt werden.")

    # ----------------------------- ERFOLG -----------------------------
    elif st.session_state.page == "erfolg":
        st.title("Beat faster!")
        st.success("Account erstellt!")
        st.subheader(f"Deine ID lautet: {st.session_state.get('neue_id', '—')}")
        st.info("Merke dir diese ID – damit meldest du dich an.")

        if st.button("Zum Login"):
            st.session_state.page = "login"
            st.rerun()

    # Rendert den Button beim Login ganz unten
    st.markdown("<br><br>", unsafe_allow_html=True)  
    zeige_hilfe_bereich()