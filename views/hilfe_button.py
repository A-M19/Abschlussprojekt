# views/hilfe_button.py
import streamlit as st

def zeige_hilfe_bereich(is_hauptseite=False):
    # Holt den aktuellen Status der Seite (z.B. "login", "registrieren" oder "hauptseite")
    aktuelle_seite = st.session_state.get("page", "login")

    # WICHTIGER LOGIK-CHECK:
    # Wenn der Aufruf vom Ende der main.py kommt (is_hauptseite ist False), 
    # aber der Nutzer schon auf der Hauptseite ist, brechen wir ab (verhindert den doppelten Button unten).
    if not is_hauptseite and aktuelle_seite == "hauptseite":
        return

    # Die Kontaktdaten des technischen Supports
    support_daten = {
        "E-Mail": "support@beatfaster.at",
        "Telefon": "+43 123 456789",
        "Erreichbarkeit": "24/7 für dich erreichbar!"
    }

    # Eindeutiger Key je nach Position, damit Streamlit nicht abstürzt
    button_key = "help_btn_top" if is_hauptseite else "help_btn_bottom"

    if st.button("❓", key=button_key):
        st.toast(
            f"ℹ️ **Support:**\n"
            f"📧 {support_daten['E-Mail']}\n"
            f"📞 {support_daten['Telefon']}\n"
            f"🕒 {support_daten['Erreichbarkeit']}"
        )