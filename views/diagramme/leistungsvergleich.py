import streamlit as st
import pandas as pd
import os
import json
from source import person
from views.extras.training_hinzufuegen import hole_alle_sportarten

INTENSITAET_DE = {"Low": "Niedrig", "Medium": "Moderat", "High": "Hoch"}
TRAINING_DB_PATH = "data/training_db.json"

def hole_kombinierte_daten(aktueller, sportart):
    """Lädt Sensordaten und manuelle JSON-Einträge für eine Sportart."""
    try:
        daten = person.get_athlete_measurements(aktueller.get_athlete_id_for_sport(sportart))
    except Exception:
        daten = pd.DataFrame()

    manual_rows = []
    if os.path.exists(TRAINING_DB_PATH):
        try:
            with open(TRAINING_DB_PATH, "r", encoding="utf-8") as f:
                trainings = json.load(f)

            for t in trainings:
                if str(t.get("athlet_id")) == str(aktueller.id) and t.get("sportart") == sportart:
                    hr = t.get("herzfrequenz_bpm", 130)
                    if hr > 150: intens = "High"
                    elif hr > 120: intens = "Medium"
                    else: intens = "Low"

                    manual_rows.append({
                        "Date": t.get("datum"),
                        "Heart_Rate": float(hr),
                        "Oxygen_Saturation": 98.0,
                        "Muscle_Activity": 150.0,
                        "Training_Intensity": intens
                    })
        except Exception:
            pass

    if manual_rows:
        df_manual = pd.DataFrame(manual_rows)
        daten = pd.concat([daten, df_manual], ignore_index=True) if not daten.empty else df_manual

    if not daten.empty:
        daten = daten.sort_values("Date", ascending=False).reset_index(drop=True)

    return daten

def zeige_leistungsvergleich(aktueller):
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:22px; font-weight:800; text-transform:uppercase; letter-spacing:-0.3px; color:#FC4C02; margin-bottom:20px;'>Leistungsvergleich</div>", unsafe_allow_html=True)

    sportarten_liste = hole_alle_sportarten(aktueller)
    v_col1, v_col2 = st.columns(2)

    # --- AKTIVITÄT 1 ---
    with v_col1:
        st.markdown("<div style='font-size: 16px; font-weight: 700; margin-bottom: 5px;'>Aktivität 1</div>", unsafe_allow_html=True)
        v_sport1 = st.selectbox("Sportart 1 wählen", sportarten_liste, key="v_sport1_select", label_visibility="collapsed")
        v_daten1 = hole_kombinierte_daten(aktueller, v_sport1)

        if not v_daten1.empty:
            v_daten1["Label"] = v_daten1.apply(lambda r: f"{r['Date']} — {r['Heart_Rate']:.0f} bpm ({INTENSITAET_DE.get(r['Training_Intensity'], r['Training_Intensity'])})", axis=1)
            optionen1 = ["Gesamter Durchschnitt"] + v_daten1["Label"].tolist()

            gewaehlt1 = st.selectbox("Einheit für Sportart 1 wählen", optionen1, key="einheit_v1")
            st.markdown(f"#### Statistik: {v_sport1}")

            if gewaehlt1 == "Gesamter Durchschnitt":
                st.metric(label="❤️ Ø Herzfrequenz", value=f"{v_daten1['Heart_Rate'].mean():.0f} bpm")
                st.metric(label="🫁 Ø O₂-Sättigung", value=f"{v_daten1['Oxygen_Saturation'].mean():.1f} %")
                st.metric(label="⚡ Ø Muskel-Aktivität", value=f"{v_daten1['Muscle_Activity'].mean():.1f} µV")
            else:
                s_row1 = v_daten1[v_daten1["Label"] == gewaehlt1].iloc[0]
                st.metric(label="❤️ Herzfrequenz", value=f"{s_row1['Heart_Rate']:.0f} bpm")
                st.metric(label="🫁 O₂-Sättigung", value=f"{s_row1['Oxygen_Saturation']:.1f} %")
                st.metric(label="⚡ Muskel-Aktivität", value=f"{s_row1['Muscle_Activity']:.1f} µV")
        else:
            st.info(f"Noch keine Daten für {v_sport1} erfasst.")

    # --- AKTIVITÄT 2 ---
    with v_col2:
        st.markdown("<div style='font-size: 16px; font-weight: 700; margin-bottom: 5px;'>Aktivität 2</div>", unsafe_allow_html=True)
        default_idx = 1 if len(sportarten_liste) > 1 else 0
        v_sport2 = st.selectbox("Sportart 2 wählen", sportarten_liste, index=default_idx, key="v_sport2_select", label_visibility="collapsed")
        v_daten2 = hole_kombinierte_daten(aktueller, v_sport2)

        if not v_daten2.empty:
            v_daten2["Label"] = v_daten2.apply(lambda r: f"{r['Date']} — {r['Heart_Rate']:.0f} bpm ({INTENSITAET_DE.get(r['Training_Intensity'], r['Training_Intensity'])})", axis=1)
            optionen2 = ["Gesamter Durchschnitt"] + v_daten2["Label"].tolist()

            gewaehlt2 = st.selectbox("Einheit für Sportart 2 wählen", optionen2, key="einheit_v2")
            st.markdown(f"#### Statistik: {v_sport2}")

            if gewaehlt2 == "Gesamter Durchschnitt":
                st.metric(label="❤️ Ø Herzfrequenz", value=f"{v_daten2['Heart_Rate'].mean():.0f} bpm")
                st.metric(label="🫁 Ø O₂-Sättigung", value=f"{v_daten2['Oxygen_Saturation'].mean():.1f} %")
                st.metric(label="⚡ Ø Muskel-Aktivität", value=f"{v_daten2['Muscle_Activity'].mean():.1f} µV")
            else:
                s_row2 = v_daten2[v_daten2["Label"] == gewaehlt2].iloc[0]
                st.metric(label="❤️ Herzfrequenz", value=f"{s_row2['Heart_Rate']:.0f} bpm")
                st.metric(label="🫁 O₂-Sättigung", value=f"{s_row2['Oxygen_Saturation']:.1f} %")
                st.metric(label="⚡ Muskel-Aktivität", value=f"{s_row2['Muscle_Activity']:.1f} µV")
        else:
            st.info(f"Noch keine Daten für {v_sport2} erfasst.")

    st.markdown("<hr>", unsafe_allow_html=True)