import streamlit as st
import os
from source import person
from views.profil_bearbeiten import zeige_profil_bearbeiten
from views.diagramme.herzfrequenz_diagramm import zeige_herzfrequenz_diagramm
from views.diagramme.aktivitaets_diagramm import zeige_aktivitaets_diagramm

# Wichtig: Importiert den Hilfe-Button aus deiner separaten Datei im views-Ordner
from views.hilfe_button import zeige_hilfe_bereich

# Deutsche Anzeige  <->  englische CSV-Werte
INTENSITAET_DE = {"Low": "Niedrig", "Medium": "Moderat", "High": "Hoch"}


def render_hauptseite():
    # CSS für das professionelle Premium-Dashboard (Optimiert)
    st.markdown("""
        <style>
        /* Hintergrund der gesamten App auf ein sauberes, professionelles Grau setzen */
        .stApp {
            background-color: #F3F4F6 !important;
            color: #1F1F23 !important;
        }

        /* Typografie-Optimierung */
        h1, h2, h3, h4, p, span, label, div {
            color: #1F1F23 !important;
            font-family: "Maison Neue", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Sektions-Überschriften */
        h3 {
            font-size: 22px !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
            margin-bottom: 20px !important;
        }

        /* Labels komplett SCHWARZ und GRÖSSER */
        div[data-testid="stSelectbox"] label p {
            font-size: 18px !important;
            font-weight: 700 !important;
            color: #000000 !important;
        }

        /* Premium Cards für die Leistungswerte (Metrics) */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            padding: 24px !important;
            border-radius: 6px !important;
            border: 1px solid #E6E6EC !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        }

        /* Dezente Beschriftung der Metrics */
        div[data-testid="stMetricLabel"] {
            color: #6D6D78 !important;
            font-size: 14px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            font-weight: 600 !important;
        }

        /* Fokus auf die Leistungszahlen */
        div[data-testid="stMetricValue"] {
            color: #1F1F23 !important;
            font-size: 32px !important;
            font-weight: 800 !important;
        }

        /* Absolut flaches, einfarbiges WEISS für die Dropdowns ohne Verläufe oder Ränder */
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

        /* Saubere Trennlinien */
        hr {
            border-color: #D1D5DB !important;
            margin: 35px 0 !important;
        }

        /* Cleane, rahmenlose Funktionstasten */
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

        /* Verhindert unschöne Abstände um die Buttons */
        div[data-testid="stButton"] {
            margin-bottom: 20px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }

        /* Hover-Effekt wechselt edel zum Akzent-Orange */
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

    aktuelle_id = st.session_state.eingeloggt_als
    such_id = int(aktuelle_id) if aktuelle_id and str(aktuelle_id).isdigit() else aktuelle_id
    aktueller = person.get_person_by_id(such_id)

    if aktueller is None:
        st.info("Für diesen Account sind noch keine Profildaten hinterlegt.")
        return

    # Titel
    st.markdown("<div style='font-size: 32px; font-weight: 800; letter-spacing: -1px; color: #1F1F23; margin-bottom: 30px;'>Beat faster!</div>", unsafe_allow_html=True)

    # ---------- KOPFZEILE ----------
    links, rechts = st.columns([4.5, 0.7])

    with links:
        bild_col, text_col = st.columns([1, 3.5])

        with bild_col:
            try:
                bild_pfad = aktueller.get_image()
                if isinstance(bild_pfad, str):
                    dateiname = os.path.basename(bild_pfad)
                    test_pfad = os.path.join("data", "pictures", dateiname)
                    if os.path.exists(test_pfad):
                        bild_pfad = test_pfad

                st.markdown(f"""
                    <style>
                    img {{
                        border-radius: 8px !important;
                        border: 1px solid #E6E6EC !important;
                    }}
                    </style>
                """, unsafe_allow_html=True)
                st.image(bild_pfad, width=110)

            except Exception:
                st.markdown("<div style='font-size: 70px; line-height: 1;'>👤</div>", unsafe_allow_html=True)

        with text_col:
            st.markdown(f"""
                <div style="font-size: 30px; font-weight: 800; color: #1F1F23; margin-top: 10px; line-height: 1.1; letter-spacing: -0.5px;">
                    {aktueller.firstname} {aktueller.lastname if hasattr(aktueller, 'lastname') else 'Ahrens'}
                </div>
                <div style="font-size: 15px; color: #6D6D78; margin-top: 15px; font-weight: 500;">
                    ID: {aktueller.id} &nbsp;•&nbsp; Alter: {aktueller.calc_age()} &nbsp;•&nbsp; Geschlecht: {aktueller.gender}
                </div>
            """, unsafe_allow_html=True)

    # Alle drei Buttons stehen nun direkt untereinander ganz rechts oben
    with rechts:
        if st.button("🚪"):
            st.session_state.page = "login"
            st.session_state.eingeloggt_als = None
            st.rerun()

        if st.session_state.ansicht == "dashboard":
            if st.button("👤"):
                st.session_state.ansicht = "bearbeiten"
                st.rerun()
        else:
            if st.button("📊"):
                st.session_state.ansicht = "dashboard"
                st.rerun()

        # Zeichnet das Fragezeichen oben rechts (Dashboard-Menü)
        zeige_hilfe_bereich(is_hauptseite=True)

    # ---------- ROUTING BEREICH ----------
    if st.session_state.ansicht == "dashboard":

        filter_links, filter_rechts = st.columns(2)
        with filter_links:
            sportart = st.selectbox("Aktivität wählen", aktueller.get_sportarten())
        with filter_rechts:
            intensitaet_wahl = st.selectbox("Intensitäts-Filter", ["Alle", "Niedrig", "Moderat", "Hoch"])

        daten = person.get_athlete_measurements(aktueller.get_athlete_id_for_sport(sportart))

        if daten.empty:
            st.warning("Keine Aktivitätsdaten für diese Sportart gefunden.")
            return

        # Anker = jüngstes Trainingsdatum (statt echtem "heute") -> immer Daten sichtbar
        anker = daten["Date"].max()

        daten = daten.copy()
        daten["Intensität"] = daten["Training_Intensity"].map(INTENSITAET_DE)
        if intensitaet_wahl != "Alle":
            daten = daten[daten["Intensität"] == intensitaet_wahl]

        if daten.empty:
            st.info(f"Keine Messwerte für die Intensität '{intensitaet_wahl}' vorhanden.")
            return

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------- AKTIVITÄTS-ZUSAMMENFASSUNG ----------
        st.markdown("<h3>Aktivitäts-Zusammenfassung</h3>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="❤️ Ø Herzfrequenz", value=f"{daten['Heart_Rate'].mean():.0f} bpm")
        with m2:
            st.metric(label="🫁 O₂-Sättigung", value=f"{daten['Oxygen_Saturation'].mean():.1f} %")
        with m3:
            st.metric(label="⚡ Muskel-Aktivität", value=f"{daten['Muscle_Activity'].mean():.1f} µV")

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------- AKTIVITÄT ----------
        st.markdown("<h3>Aktivität</h3>", unsafe_allow_html=True)

        # Zeitraum-Buttons links, Farb-Legende rechts auf gleicher Höhe
        zeit_col, legende_col = st.columns([2, 1])
        with zeit_col:
            # Bei Streamlit < 1.36: durch st.radio(..., horizontal=True, label_visibility="collapsed") ersetzen
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

        zeige_aktivitaets_diagramm(aktueller, sportart, intensitaet_wahl, zeitraum, anker)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------- HERZFREQUENZ ----------
        st.markdown("<h3>Herzfrequenz</h3>", unsafe_allow_html=True)
        zeige_herzfrequenz_diagramm(daten, zeitraum, anker)

    elif st.session_state.ansicht == "bearbeiten":
        zeige_profil_bearbeiten()