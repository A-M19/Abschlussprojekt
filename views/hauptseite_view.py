import streamlit as st
import os
import pandas as pd
from source import person
from views.profil_bearbeiten import zeige_profil_bearbeiten
from views.diagramme.herzfrequenz_diagramm import zeige_herzfrequenz_diagramm
from views.diagramme.aktivitaets_diagramm import zeige_aktivitaets_diagramm
from views.training_hinzufuegen import zeige_training_hinzufuegen, hole_alle_sportarten

# Importiert den ausgelagerten Leistungsvergleich und die Daten-Pipeline
from views.leistungsvergleich import zeige_leistungsvergleich, hole_kombinierte_daten
from views.hilfe_button import zeige_hilfe_bereich

INTENSITAET_DE = {"Low": "Niedrig", "Medium": "Moderat", "High": "Hoch"}


def standard_bildpfad(aktueller):
    return os.path.join("data", "pictures", f"Athlete_{aktueller.id}.png")


def render_hauptseite():
    st.markdown("""
        <style>
        .stApp {
            background-color: #F3F4F6 !important;
            color: #1F1F23 !important;
        }

        h1, h2, h3, h4, p, span, label, div {
            color: #1F1F23 !important;
            font-family: "Maison Neue", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        h3 {
            font-size: 22px !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
            margin-bottom: 20px !important;
        }

        div[data-testid="stSelectbox"] label p {
            font-size: 18px !important;
            font-weight: 700 !important;
            color: #000000 !important;
        }

        div[data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            padding: 24px !important;
            border-radius: 6px !important;
            border: 1px solid #E6E6EC !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #6D6D78 !important;
            font-size: 14px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            font-weight: 600 !important;
        }

        div[data-testid="stMetricValue"] {
            color: #1F1F23 !important;
            font-size: 32px !important;
            font-weight: 800 !important;
        }

        div[data-testid="stSelectbox"] div[data-baseweb="select"],
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            border: none !important;
            box-shadow: none !important;
            border-radius: 12px !important;
            color: #1F1F23 !important;
            font-size: 17px !important;
            font-weight: 500 !important;
            height: 48px !important;
        }

        hr {
            border-color: #D1D5DB !important;
            margin: 35px 0 !important;
        }

        div[data-testid="stButton"] button,
        div[data-testid="stButton"] button p {
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
            font-size: 38px !important;
            line-height: 1 !important;
            box-shadow: none !important;
            transition: transform 0.15s ease-in-out, color 0.15s ease;
            min-height: auto !important;
            width: auto !important;
            color: #6D6D78 !important;
        }

        div[data-testid="stButton"] {
            margin-bottom: 20px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }

        div[data-testid="stButton"] button:hover p {
            color: #FC4C02 !important;
            transform: scale(1.08) !important;
        }
        
        div[data-testid="stButton"] button:focus,
        div[data-testid="stButton"] button:active {
            background-color: transparent !important;
            box-shadow: none !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    akktuelle_id = st.session_state.eingeloggt_als
    such_id = int(akktuelle_id) if akktuelle_id and str(akktuelle_id).isdigit() else akktuelle_id
    aktueller = person.get_person_by_id(such_id)

    # AUTOMATISCHE REGISTRIERUNG NEUER ACCOUNTS:
    # Wenn die ID in der JSON-Datei noch fehlt, legen wir sie hier live mit Standardwerten an
    if aktueller is None and such_id is not None:
        if hasattr(person, "create_new_athlete"):
            person.create_new_athlete(
                id=such_id,
                firstname="Neuer",
                lastname="Athlet",
                gender="Male",
                date_of_birth="2000"
            )
            # Direkt neu aus der person_db.json laden -> liefert jetzt ein echtes Person-Objekt
            aktueller = person.get_person_by_id(such_id)

    st.markdown(
        "<div style='font-size: 32px; font-weight: 800; letter-spacing: -1px; color: #1F1F23; margin-bottom: 30px;'>Beat faster!</div>",
        unsafe_allow_html=True
    )

    links, rechts = st.columns([4.5, 0.7])

    with links:
        bild_col, text_col = st.columns([1, 3.5])

        with bild_col:
            try:
                bild_pfad = standard_bildpfad(aktueller)

                st.markdown("""
                    <style>
                    img {
                        border-radius: 8px !important;
                        border: 1px solid #E6E6EC !important;
                    }
                    </style>
                """, unsafe_allow_html=True)

                if aktueller and os.path.exists(bild_pfad):
                    st.image(bild_pfad, width=110)
                else:
                    st.markdown("<div style='font-size: 70px; line-height: 1;'>👤</div>", unsafe_allow_html=True)

            except Exception:
                st.markdown("<div style='font-size: 70px; line-height: 1;'>👤</div>", unsafe_allow_html=True)

        with text_col:
            if aktueller:
                st.markdown(f"""
                    <div style="font-size: 30px; font-weight: 800; color: #1F1F23; margin-top: 10px; line-height: 1.1; letter-spacing: -0.5px;">
                        {aktueller.firstname} {aktueller.lastname if hasattr(aktueller, 'lastname') else ''}
                    </div>
                    <div style="font-size: 15px; color: #6D6D78; margin-top: 15px; font-weight: 500;">
                        ID: {aktueller.id} &nbsp;•&nbsp; Alter: {aktueller.calc_age()} &nbsp;•&nbsp; Geschlecht: {aktueller.gender}
                    </div>
                """, unsafe_allow_html=True)

    with rechts:
        if st.button("🚪", key="logout_btn"):
            st.session_state.page = "login"
            st.session_state.eingeloggt_als = None
            st.rerun()

        if st.session_state.ansicht == "dashboard":
            if st.button("👤", key="profil_edit_btn", help="Profil bearbeiten"):
                st.session_state.ansicht = "bearbeiten"
                st.rerun()
        else:
            if st.button("📊", key="dashboard_view_btn", help="Dashboard anzeigen"):
                st.session_state.ansicht = "dashboard"
                st.rerun()

        zeige_hilfe_bereich(is_hauptseite=True)

    if st.session_state.ansicht == "dashboard":

        if "vergleich_aktiv" not in st.session_state:
            st.session_state.vergleich_aktiv = False

        btn_col1, spacer, btn_col2, _ = st.columns([1.0, 0.5, 1.0, 7.5])
        
        with btn_col1:
            if aktueller:
                zeige_training_hinzufuegen(aktueller)

        with btn_col2:
            if st.button("⚖️", key="leistungsvergleich_toggle_btn", help="Leistungsvergleich öffnen / schließen"):
                st.session_state.vergleich_aktiv = not st.session_state.vergleich_aktiv
                st.rerun()

        if st.session_state.vergleich_aktiv and aktueller:
            zeige_leistungsvergleich(aktueller)
            return

        # --- REGULÄRES DASHBOARD ---
        filter_links, filter_rechts = st.columns(2)

        with filter_links:
            verfuegbare_sportarten = hole_alle_sportarten(aktueller) if aktueller else []
            if not verfuegbare_sportarten:
                verfuegbare_sportarten = ["Schwimmen", "Laufen", "Boxen", "Radfahren"]
            sportart = st.selectbox("Aktivität auswählen", verfuegbare_sportarten)

        with filter_rechts:
            intensitaet_wahl = st.selectbox("Intensitäts-Filter", ["Alle", "Niedrig", "Moderat", "Hoch"])

        # Daten laden
        daten = hole_kombinierte_daten(aktueller, sportart) if aktueller else pd.DataFrame()

        if daten.empty:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.info("👋 Willkommen! Füge über das '+' Symbol dein erstes Training hinzu oder vervollständige dein Profil über das '👤' Symbol.")
            return

        # Datetime konvertieren
        daten["Date"] = pd.to_datetime(daten["Date"])
        anker = daten["Date"].max()
        daten = daten.copy()
        
        if "Training_Intensity" in daten.columns:
            daten["Intensität"] = daten["Training_Intensity"].map(INTENSITAET_DE).fillna("Moderat")
        else:
            daten["Intensität"] = "Moderat"
            daten["Training_Intensity"] = "Medium"

        if intensitaet_wahl != "Alle":
            daten = daten[daten["Intensität"] == intensitaet_wahl]

        if daten.empty:
            st.info(f"Keine Messwerte für die Intensität '{intensitaet_wahl}' vorhanden.")
            return

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h3>Aktivitäts-Zusammenfassung</h3>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)

        hr_val = daten['Heart_Rate'].mean() if 'Heart_Rate' in daten.columns else 0
        o2_val = daten['Oxygen_Saturation'].mean() if 'Oxygen_Saturation' in daten.columns else 0
        mu_val = daten['Muscle_Activity'].mean() if 'Muscle_Activity' in daten.columns else 0

        with m1:
            st.metric(label="❤️ Ø Herzfrequenz", value=f"{hr_val:.0f} bpm")
        with m2:
            st.metric(label="🫁 O₂-Sättigung", value=f"{o2_val:.1f} %")
        with m3:
            st.metric(label="⚡ Muskel-Aktivität", value=f"{mu_val:.1f} µV")

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------- AKTIVITÄT ----------
        st.markdown("<h3>Aktivität</h3>", unsafe_allow_html=True)

        zeit_col, legende_col = st.columns([2, 1])
        with zeit_col:
            zeitraum = st.segmented_control(
                "Zeitraum",
                ["Letzte 6 Monate", "Letzter Monat", "Letzte Woche"],
                default="Letzte 6 Monate",
                label_visibility="collapsed",
            ) or "Letzte 6 Monate"
        with legende_col:
            st.markdown("""
                <div style="text-align: right; font-size: 14px; font-weight: 600; color: #6D6D78; padding-top: 8px;">
                    <span style="color: #2ca02c;">●</span> Niedrig &nbsp;
                    <span style="color: #f1c40f;">●</span> Moderat &nbsp;
                    <span style="color: #e74c3c;">●</span> Hoch
                </div>
            """, unsafe_allow_html=True)

        zeige_aktivitaets_diagramm(aktueller, sportart, intensitaet_wahl, zeitraum, anker, daten=daten)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------- HERZFREQUENZ ----------
        st.markdown("<h3>Herzfrequenz</h3>", unsafe_allow_html=True)
        zeige_herzfrequenz_diagramm(daten, zeitraum, anker)

    elif st.session_state.ansicht == "bearbeiten":
        zeige_profil_bearbeiten()