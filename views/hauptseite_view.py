import streamlit as st
import pandas as pd
import altair as alt
from source import person

# Deutsche Anzeige  <->  englische CSV-Werte
INTENSITAET_DE = {"Low": "Niedrig", "Medium": "Moderat", "High": "Hoch"}


def render_hauptseite():
    aktuelle_id = st.session_state.eingeloggt_als
    such_id = int(aktuelle_id) if aktuelle_id and str(aktuelle_id).isdigit() else aktuelle_id
    aktueller = person.get_person_by_id(such_id)

    _kopfzeile(aktueller, aktuelle_id)

    if aktueller is None:
        st.info("Für diesen Account sind noch keine Profildaten hinterlegt.")
        return

    # Auswahl: Sportart + Trainingsintensität
    sportart = st.selectbox("Sportart", aktueller.get_sportarten())
    intensitaet_wahl = st.selectbox(
        "Trainingsintensität", ["Alle", "Niedrig", "Moderat", "Hoch"]
    )

    daten = person.get_athlete_measurements(aktueller.get_athlete_id_for_sport(sportart))
    if daten.empty:
        st.warning("Keine Messdaten gefunden.")
        return

    # deutsche Intensitäts-Spalte + Filter (gilt jetzt für Tabelle UND Diagramm)
    daten = daten.copy()
    daten["Intensität"] = daten["Training_Intensity"].map(INTENSITAET_DE)
    if intensitaet_wahl != "Alle":
        daten = daten[daten["Intensität"] == intensitaet_wahl]

    if daten.empty:
        st.info(f"Keine Messwerte mit Intensität „{intensitaet_wahl}“.")
        return

    _tabelle(daten)
    _herzfrequenz_diagramm(daten)


def _kopfzeile(aktueller, aktuelle_id):
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


def _tabelle(daten):
    tabelle = pd.DataFrame(
        {
            "Messwert": ["Ø Herzfrequenz", "O₂-Sättigung", "Muskel-Aktivität"],
            "Wert": [
                f"{daten['Heart_Rate'].mean():.0f} bpm",
                f"{daten['Oxygen_Saturation'].mean():.1f} %",
                f"{daten['Muscle_Activity'].mean():.1f}",
            ],
        }
    )
    st.table(tabelle)


def _herzfrequenz_diagramm(daten):
    st.subheader("Herzfrequenz")

    d = daten.reset_index(drop=True)
    d["Messung"] = d.index  # gleichmäßiger Abstand auf der x-Achse

    farben = alt.Scale(
        domain=["Niedrig", "Moderat", "Hoch"],
        range=["#2ca02c", "#f1c40f", "#e74c3c"],  # grün / gelb / rot
    )
    basis = alt.Chart(d).encode(
        x=alt.X("Messung:Q", axis=None),
        y=alt.Y("Heart_Rate:Q", title="Herzfrequenz (bpm)", scale=alt.Scale(zero=False)),
    )
    linie = basis.mark_line(color="#cccccc", strokeWidth=1)
    punkte = basis.mark_circle(size=70, opacity=0.9).encode(
        color=alt.Color("Intensität:N", scale=farben, title="Intensität"),
        tooltip=[
            alt.Tooltip("Heart_Rate:Q", title="Herzfrequenz", format=".0f"),
            alt.Tooltip("Intensität:N", title="Intensität"),
        ],
    )
    st.altair_chart((linie + punkte).properties(height=420), use_container_width=True)