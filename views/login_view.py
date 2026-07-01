import streamlit as st
import json
import os
from auth import login_user, register_user

from views.extras.hilfe_button import zeige_hilfe_bereich

DARK_CSS = """
<style>
.stApp { background-color:#1A1A1A !important; color:#E6E6E6 !important; }

p, span, label, li {
    color:#E6E6E6 !important;
    font-family:"Maison Neue", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Überschriften orange */
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3 {
    color:#FC4C02 !important; text-transform:uppercase;
    letter-spacing:-0.3px !important; font-weight:800 !important;
}

/* Textfelder dunkel */
div[data-testid="stTextInput"] input {
    background-color:#242424 !important; color:#E6E6E6 !important;
    border:1px solid #333333 !important; border-radius:8px !important;
}
div[data-testid="stTextInput"] label p { color:#E6E6E6 !important; font-weight:600 !important; }

/* Aktions-Buttons: schwarz mit oranger Schrift + orangem Rand */
div[data-testid="stButton"] button[kind="primary"] {
    background-color:#242424 !important; border:1px solid #FC4C02 !important;
    border-radius:30px !important; padding:10px 24px !important; box-shadow:none !important;
}
div[data-testid="stButton"] button[kind="primary"] p {
    color:#FC4C02 !important; font-weight:800 !important;
    text-transform:uppercase; letter-spacing:0.3px; font-size:15px !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover { border-color:#E34402 !important; }
div[data-testid="stButton"] button[kind="primary"]:hover p { color:#E34402 !important; }

/* Hilfe-Fragezeichen: ohne Rand, größer, orange (egal ob Popover oder Button) */
div[data-testid="stPopover"] button,
div[data-testid="stButton"] button:not([kind="primary"]) {
    background:transparent !important; border:none !important; box-shadow:none !important;
    padding:0 !important; color:#FC4C02 !important; min-height:auto !important;
}
div[data-testid="stPopover"] button p,
div[data-testid="stButton"] button:not([kind="primary"]) p {
    font-size:44px !important; color:#FC4C02 !important; line-height:1 !important;
}

/* Toast & Tooltip: schwarze Schrift auf hellem Hintergrund */
div[data-testid="stToast"], div[data-testid="stToast"] * { color:#1A1A1A !important; }
div[data-testid="stTooltipContent"], div[data-testid="stTooltipContent"] *,
div[role="tooltip"], div[role="tooltip"] * { color:#1A1A1A !important; }
</style>
"""


def ueberpruefe_ob_benutzer_existiert(username):
    """Überprüft in der person_db.json, ob der Name bereits vergeben ist."""
    json_pfad = os.path.join("data", "person_db.json")
    if os.path.exists(json_pfad):
        try:
            with open(json_pfad, "r", encoding="utf-8") as f:
                daten_liste = json.load(f)
                for nutzer in daten_liste:
                    existierender_name = nutzer.get("username") or nutzer.get("firstname")
                    if existierender_name and str(existierender_name).strip().lower() == str(username).strip().lower():
                        return True
        except Exception:
            pass
    return False


def render_login_page():
    st.markdown(DARK_CSS, unsafe_allow_html=True)

    # ----------------------------- LOGIN -----------------------------
    if st.session_state.page == "login":
        st.markdown("<div style='font-size:40px; font-weight:800; letter-spacing:-1px; color:#FC4C02; margin-bottom:30px;'>Beat faster!</div>", unsafe_allow_html=True)

        login_id = st.text_input("ID", placeholder="z. B. 12345")
        password = st.text_input("Passwort", type="password")

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Anmelden", type="primary", use_container_width=True):
                if login_id == "" or password == "":
                    st.error("Bitte alle Felder ausfüllen!")
                elif login_user(login_id, password):
                    st.session_state.eingeloggt_als = login_id
                    st.session_state.page = "hauptseite"
                    st.rerun()
                else:
                    st.error("Falsche ID oder Passwort!")

        with col2:
            if st.button("neuen Account erstellen", type="primary"):
                st.session_state.page = "registrieren"
                st.rerun()

    # -------------------------- REGISTRIEREN --------------------------
    elif st.session_state.page == "registrieren":
        st.markdown("<div style='font-size:40px; font-weight:800; letter-spacing:-1px; color:#FC4C02; margin-bottom:30px;'>Registrieren</div>", unsafe_allow_html=True)

        name = st.text_input("Name")
        pw1 = st.text_input("Passwort", type="password")
        pw2 = st.text_input("Passwort wiederholen", type="password")

        if st.button("Account erstellen", type="primary"):
            if name.strip() == "" or pw1 == "":
                st.error("Felder dürfen nicht leer sein!")
            elif pw1 != pw2:
                st.error("Passwörter stimmen nicht überein!")
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
        st.markdown("<div style='font-size:40px; font-weight:800; letter-spacing:-1px; color:#FC4C02; margin-bottom:30px;'>Beat faster!</div>", unsafe_allow_html=True)
        st.success("Account erstellt!")
        st.subheader(f"Deine ID lautet: {st.session_state.get('neue_id', '—')}")
        st.info("Merke dir diese ID – damit meldest du dich an.")

        if st.button("Zum Login", type="primary"):
            st.session_state.page = "login"
            st.rerun()

    # Hilfe-Button ganz unten
    st.markdown("<br><br>", unsafe_allow_html=True)
    zeige_hilfe_bereich()