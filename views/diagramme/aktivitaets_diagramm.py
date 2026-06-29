import streamlit as st
import altair as alt
import pandas as pd
from source import person
from views.diagramme.zeit import aggregiere_nach_intensitaet

INTENSITAET_EN = {"Niedrig": "Low", "Moderat": "Medium", "Hoch": "High"}
ZONE_DE = {"Low": "Niedrig", "Medium": "Moderat", "High": "Hoch"}

FARBEN = alt.Scale(domain=["Low", "Medium", "High"],
                   range=["#2ca02c", "#f1c40f", "#e74c3c"])  # grün / gelb / rot


def zeige_aktivitaets_diagramm(aktueller, sportart, intensitaet_wahl, zeitraum, anker=None, daten=None):
    # Falls keine Daten übergeben wurden, laden wir sie
    if daten is None:
        daten = person.get_athlete_measurements(aktueller.get_athlete_id_for_sport(sportart))
    
    daten = daten.dropna(subset=["Date"]).copy()
    
    # Sicherstellen, dass das Datum als echtes Datetime-Objekt vorliegt
    daten["Date"] = pd.to_datetime(daten["Date"])

    # KORREKTUR / TOLERANZ: Falls Spalten leicht abweichen, benennen wir sie um
    if "Duration" in daten.columns and "Duration_min" not in daten.columns:
        daten = daten.rename(columns={"Duration": "Duration_min"})
    if "Distance" in daten.columns and "Distance_km" not in daten.columns:
        daten = daten.rename(columns={"Distance": "Distance_km"})

    # Falls gar keine Dauer-Spalte existiert, legen wir eine Dummy-Spalte an (damit es nicht abstürzt)
    if "Duration_min" not in daten.columns:
        daten["Duration_min"] = 30.0  # Standard-Fallback, falls leer

    if intensitaet_wahl != "Alle":
        daten = daten[daten["Training_Intensity"] == INTENSITAET_EN.get(intensitaet_wahl, intensitaet_wahl)]

    if daten.empty:
        st.info("Keine Verlaufsdaten für diese Auswahl.")
        return

    # Dauer oder Kilometer (nur wenn die Sportart km hat)
    hat_km = daten["Distance_km"].notna().any() if "Distance_km" in daten.columns else False
    metrik = "Dauer"
    if hat_km:
        metrik = st.segmented_control(
            "Anzeige", ["Dauer", "Kilometer"], default="Dauer",
            label_visibility="collapsed",
        ) or "Dauer"

    spalte = "Distance_km" if metrik == "Kilometer" else "Duration_min"
    einheit = "km" if metrik == "Kilometer" else "min"

    df, reihenfolge = aggregiere_nach_intensitaet(daten, spalte, zeitraum, today=anker)
    if df.empty:
        st.info("Keine Daten im gewählten Zeitraum.")
        return

    df["Zone"] = df["Training_Intensity"].map(ZONE_DE)

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Label:N", sort=reihenfolge, title=None,
                    scale=alt.Scale(domain=reihenfolge),
                    axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Wert:Q", title=f"{metrik} ({einheit})"),
            color=alt.Color("Training_Intensity:N", scale=FARBEN, legend=None),
            order=alt.Order("Training_Intensity:N"),
            tooltip=[
                alt.Tooltip("Label:N", title="Zeitraum"),
                alt.Tooltip("Zone:N", title="Intensität"),
                alt.Tooltip("Wert:Q", title=metrik, format=".1f"),
            ],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, use_container_width=True, theme=None)