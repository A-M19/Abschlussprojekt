import streamlit as st
import pandas as pd
from views.login_view import render_login_page
from source import person
from views.hilfe_button import zeige_hilfe_bereich
from views.profil_bearbeiten import zeige_profil_bearbeiten

st.set_page_config(page_title="Beat faster!", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "login"
if "eingeloggt_als" not in st.session_state:
    st.session_state.eingeloggt_als = None

# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------
if st.session_state.page in ["login", "registrieren", "erfolg"]:
    render_login_page()

elif st.session_state.page == "hauptseite":
    aktuelle_id = st.session_state.eingeloggt_als
    such_id = int(aktuelle_id) if aktuelle_id and str(aktuelle_id).isdigit() else aktuelle_id

    aktueller = person.get_person_by_id(such_id)

    # ---------- Kopfzeile ----------
    links, rechts = st.columns([5, 1])
    with links:
        if aktueller is not None:
            bild_spalte, info_spalte = st.columns([1, 4])
            with bild_spalte:
                try:
                    st.image(aktueller.get_image(), width=120)
                except FileNotFoundError:
                    st.warning("Kein Bild gefunden")
            with info_spalte:
                st.caption(f"ID: {aktueller.id}")
                st.title(f"Hallo! {aktueller.firstname}")
                st.write(
                    f"**Geburtsjahr:** {aktueller.date_of_birth} &nbsp;&nbsp; "
                    f"**Alter:** {aktueller.calc_age()} &nbsp;&nbsp; "
                    f"**Geschlecht:** {aktueller.gender}"
                )
        else:
            st.title(f"Hallo! {aktueller.firstname}")
    with rechts:
        if st.button("Abmelden"):
            st.session_state.page = "login"
            st.session_state.eingeloggt_als = None
            st.rerun()

    if aktueller is None:
        st.info("Für diesen Account sind noch keine Profildaten hinterlegt.")
        st.stop()

    # ---------- Tabs für Dashboard und Bearbeiten ----------
    tab_dashboard, tab_bearbeiten = st.tabs(["📊 Dashboard", "📝 Profil bearbeiten"])

    with tab_dashboard:
        # ---------- Sportart wählen ----------
        sportart = st.selectbox("Sportart", aktueller.get_sportarten())
        athlete_id = aktueller.get_athlete_id_for_sport(sportart)
        daten = person.get_athlete_measurements(athlete_id)

        if daten.empty:
            st.warning("Keine Messdaten gefunden.")
            st.stop()

        # ---------- Tabelle mit Durchschnittswerten ----------
        tabelle = pd.DataFrame(
            {
                "Messwert": ["Ø Herzfrequenz", "O₂-Sättigung",
                             "Ø Trainings-Intensität", "Muskel-Aktivität"],
                "Wert": [
                    f"{daten['Heart_Rate'].mean():.0f} bpm",
                    f"{daten['Oxygen_Saturation'].mean():.1f} %",
                    daten["Training_Intensity"].mode()[0],
                    f"{daten['Muscle_Activity'].mean():.1f}",
                ],
            }
        )
        st.table(tabelle)

        # ---------- Strava-Style: Trainingsvolumen pro Monat ----------
        st.subheader(f"Die letzten Monate – {sportart}")
        pro_monat = (
            daten.set_index("Date")
            .resample("MS")["Distance_km"]
            .sum()
            .rename("Distanz (km)")
        )
        # Monatsnamen als Beschriftung
        pro_monat.index = pro_monat.index.strftime("%b %Y")
        st.bar_chart(pro_monat)

        # ---------- Herzfrequenz-Verlauf ----------
        st.subheader("Herzfrequenz-Verlauf")
        hr = daten.set_index("Date")["Heart_Rate"]
        st.line_chart(hr)

    with tab_bearbeiten:
        zeige_profil_bearbeiten()


zeige_hilfe_bereich()

