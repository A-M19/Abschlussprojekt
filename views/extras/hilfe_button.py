import streamlit as st

def zeige_hilfe_bereich(is_hauptseite=False):
    aktuelle_seite = st.session_state.get("page", "login")

    if not is_hauptseite and aktuelle_seite == "hauptseite":
        return

    support_daten = {
        "E-Mail": "support@beatfaster.at",
        "Telefon": "+43 123 456789",
        "Erreichbarkeit": "24/7 für dich erreichbar!"
    }

    button_key = "help_btn_top" if is_hauptseite else "help_btn_bottom"

    # help= -> Tooltip beim Hovern ueber das Fragezeichen
    if st.button("❓", key=button_key, help="Hilfe & Support"):
        st.toast(
            f"ℹ️ **Support:**\n"
            f"📧 {support_daten['E-Mail']}\n"
            f"📞 {support_daten['Telefon']}\n"
            f"🕒 {support_daten['Erreichbarkeit']}"
        )