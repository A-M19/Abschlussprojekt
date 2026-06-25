# hilfe_button.py
import streamlit as st

def zeige_hilfe_bereich():
    # Die Kontaktdaten des technischen Supports
    support_daten = {
        "E-Mail": "support@beatfaster.at",
        "Telefon": "+43 123 456789",
        "Erreichbarkeit": "24/7 für dich erreichbar!"
    }

    st.divider() # Zieht eine saubere Trennlinie vor dem Hilfebereich

    # Der Hilfe-Button aus Streamlit
    if st.button("ℹ️ Hilfe / Support"):
        st.info(
            f"**So kannst du uns kontaktieren:**\n\n"
            f"📧 E-Mail: {support_daten['E-Mail']}\n\n"
            f"📞 Telefon: {support_daten['Telefon']}\n\n"
            f"🕒 Erreichbar: {support_daten['Erreichbarkeit']}"
        )