# views/diagramme/aktivitaets_diagramm.py
import streamlit as st
import altair as alt
from source import person
from views.diagramme.zeit import aggregiere_nach_intensitaet

ZONE_DE = {"Low": "Niedrig", "Medium": "Moderat", "High": "Hoch"}
INTENSITAET_EN = {"Niedrig": "Low", "Moderat": "Medium", "Hoch": "High"}
FARBEN = alt.Scale(domain=["Low", "Medium", "High"],
                   range=["#2ca02c", "#f1c40f", "#e74c3c"])  # grün / gelb / rot
# High unten, dann Medium, dann Low -> von unten nach oben: rot, gelb, grün
STAPEL = {"High": 0, "Medium": 1, "Low": 2}


def zeige_aktivitaets_diagramm(aktueller, sportart, intensitaet_wahl, zeitraum, anker=None, daten=None):
    if daten is None:
        daten = person.get_athlete_measurements(aktueller.get_athlete_id_for_sport(sportart))
        if intensitaet_wahl != "Alle":
            daten = daten[daten["Training_Intensity"] == INTENSITAET_EN.get(intensitaet_wahl, intensitaet_wahl)]

    daten = daten.dropna(subset=["Date"]).copy()
    if daten.empty:
        st.info("Keine Verlaufsdaten für diese Auswahl.")
        return

    # Dauer oder Kilometer (nur wenn die Sportart km hat) – Label ausgeblendet
    hat_km = "Distance_km" in daten.columns and daten["Distance_km"].notna().any()
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
    df["Stapel"] = df["Training_Intensity"].map(STAPEL)

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Label:N", sort=reihenfolge, title=None,
                    scale=alt.Scale(domain=reihenfolge),
                    axis=alt.Axis(labelAngle=0, labelColor="#9A9A9A")),
            y=alt.Y("Wert:Q", title=f"{metrik} ({einheit})",
                    axis=alt.Axis(grid=True, gridColor="#333333",
                                  titleColor="#9A9A9A", labelColor="#9A9A9A")),
            color=alt.Color("Training_Intensity:N", scale=FARBEN, legend=None),
            # Stapel-Reihenfolge: kleinster Wert unten -> High(rot) unten, Low(grün) oben
            order=alt.Order("Stapel:Q"),
            tooltip=[
                alt.Tooltip("Label:N", title="Zeitraum"),
                alt.Tooltip("Zone:N", title="Intensität"),
                alt.Tooltip("Wert:Q", title=metrik, format=".1f"),
            ],
        )
        .properties(height=320, background="transparent")
        .configure_view(strokeOpacity=0)
    )
    st.altair_chart(chart, use_container_width=True, theme=None)