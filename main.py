import streamlit as st
import pandas as pd
import altair as alt
from views.login_view import render_login_page
from source import person
from views.hilfe_button import zeige_hilfe_bereich

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
            st.title(f"Hallo! {aktuelle_id}")
    with rechts:
        if st.button("Abmelden"):
            st.session_state.page = "login"
            st.session_state.eingeloggt_als = None
            st.rerun()

    if aktueller is None:
        st.info("Für diesen Account sind noch keine Profildaten hinterlegt.")
        st.stop()

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

    # ---------- Herzfrequenz als Punkte-Diagramm ----------
    st.subheader("Herzfrequenz")

    daten = daten.reset_index(drop=True)
    daten["Messung"] = daten.index  # gleichmäßiger Abstand auf der x-Achse

    chart = (
        alt.Chart(daten)
        .mark_circle(size=60)
        .encode(
            # x-Achse ohne Beschriftung, Punkte gleichmäßig verteilt
            x=alt.X("Messung:Q", axis=None),
            y=alt.Y("Heart_Rate:Q", title="Herzfrequenz (bpm)",
                    scale=alt.Scale(zero=False)),
            tooltip=[
                alt.Tooltip("Heart_Rate:Q", title="Herzfrequenz", format=".0f"),
                alt.Tooltip("Training_Intensity:N", title="Intensität"),
            ],
        )
    )
    st.altair_chart(chart, use_container_width=True)


zeige_hilfe_bereich()