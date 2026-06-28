# views/diagramme/herzfrequenz_diagramm.py
import streamlit as st
import altair as alt
from views.diagramme.zeit import im_fenster

ZONE_DE = {"Low": "Niedrig", "Medium": "Moderat", "High": "Hoch"}


def zeige_herzfrequenz_diagramm(daten, zeitraum, anker=None):
    d = im_fenster(daten, zeitraum, today=anker).reset_index(drop=True)
    if d.empty:
        st.info("Keine Herzfrequenz-Daten im gewählten Zeitraum.")
        return

    d["Messung"] = d.index
    d["Zone"] = d["Training_Intensity"].map(ZONE_DE)

    farben = alt.Scale(domain=["Low", "Medium", "High"],
                       range=["#2ca02c", "#f1c40f", "#e74c3c"])

    basis = alt.Chart(d).encode(
        x=alt.X("Messung:Q", axis=alt.Axis(title=None, labels=False, grid=False)),
        y=alt.Y("Heart_Rate:Q", title="Herzfrequenz (bpm)", scale=alt.Scale(zero=False),
                axis=alt.Axis(grid=True, gridColor="#E6E6EC", titleColor="#6D6D78",
                              labelColor="#6D6D78", titleFontSize=13, labelFontSize=11)),
    )

    linie = basis.mark_line(color="#9BB4CE", strokeWidth=2.5, opacity=0.9)
    punkte = basis.mark_circle(size=90, opacity=1.0).encode(
        color=alt.Color("Training_Intensity:N", scale=farben, legend=None),
        tooltip=[
            alt.Tooltip("Heart_Rate:Q", title="Herzfrequenz"),
            alt.Tooltip("Zone:N", title="Zone"),
        ],
    )

    chart = (linie + punkte).properties(height=400, background="transparent").configure_view(strokeOpacity=0)
    st.altair_chart(chart, use_container_width=True, theme=None)