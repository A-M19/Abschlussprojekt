import streamlit as st
import os
import pandas as pd
from source import person
from views.profil_bearbeiten import zeige_profil_bearbeiten
from views.diagramme.herzfrequenz_diagramm import zeige_herzfrequenz_diagramm
from views.diagramme.aktivitaets_diagramm import zeige_aktivitaets_diagramm
from views.training_hinzufuegen import zeige_training_hinzufuegen, hole_alle_sportarten

from views.diagramme.leistungsvergleich import zeige_leistungsvergleich, hole_kombinierte_daten
from views.hilfe_button import zeige_hilfe_bereich

INTENSITAET_DE = {"Low": "Niedrig", "Medium": "Moderat", "High": "Hoch"}


def standard_bildpfad(aktueller):
    return os.path.join("data", "pictures", f"Athlete_{aktueller.id}.png")


def render_hauptseite():
    st.markdown("""
        <style>
        /* ---------- DARK / STRAVA THEME ---------- */
        .stApp { background-color:#1A1A1A !important; color:#E6E6E6 !important; }

        p, span, label, li {
            color:#E6E6E6 !important;
            font-family:"Maison Neue", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Überschriften im Strava-Orange */
        h1, h2, h3, h4 {
            color:#FC4C02 !important;
            font-family:"Maison Neue", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            text-transform:uppercase;
            letter-spacing:-0.3px !important;
        }
        h3 { font-size:22px !important; font-weight:800 !important; margin-bottom:20px !important; }

        /* Stärkerer Selektor: faengt auch Ueberschriften in anderen Views (z.B. Leistungsvergleich) */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4,
        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stMarkdownContainer"] h4 {
            color:#FC4C02 !important;
        }

        /* Icon-Buttons + Popover sauber zentriert untereinander */
        div[data-testid="stButton"], div[data-testid="stPopover"] {
            display:flex !important; flex-direction:column !important;
            align-items:center !important; justify-content:center !important;
            margin-bottom:16px !important;
        }

        div[data-testid="stSelectbox"] label p {
            font-size:15px !important; font-weight:700 !important;
            color:#E6E6E6 !important; text-transform:uppercase;
        }

        /* Metric-Cards dunkel */
        div[data-testid="stMetric"] {
            background-color:#242424 !important; padding:24px !important;
            border-radius:10px !important; border:1px solid #333333 !important;
            box-shadow:0 2px 12px rgba(0,0,0,0.35) !important;
        }
        div[data-testid="stMetricLabel"] {
            color:#9A9A9A !important; font-size:13px !important;
            text-transform:uppercase; letter-spacing:0.5px !important; font-weight:600 !important;
        }
        div[data-testid="stMetricValue"] { color:#FFFFFF !important; font-size:30px !important; font-weight:800 !important; }

        /* Dropdowns dunkel */
        div[data-testid="stSelectbox"] div[data-baseweb="select"],
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color:#242424 !important; background:#242424 !important;
            border:1px solid #333333 !important; box-shadow:none !important;
            border-radius:10px !important; color:#E6E6E6 !important;
            font-size:16px !important; font-weight:500 !important; height:48px !important;
        }

        hr { border-color:#333333 !important; margin:30px 0 !important; }

        /* Icon-Buttons (Emoji) bleiben transparent */
        div[data-testid="stButton"] button {
            background-color:transparent !important; border:none !important; padding:0 !important;
            font-size:38px !important; line-height:1 !important; box-shadow:none !important;
            min-height:auto !important; width:fit-content !important; color:#9A9A9A !important;
            margin-left:auto !important; margin-right:auto !important; display:block !important;
            transition: transform 0.15s ease, color 0.15s ease;
        }
        div[data-testid="stButton"] button p { font-size:38px !important; line-height:1 !important; }
        div[data-testid="stPopover"] button p { font-size:38px !important; line-height:1 !important; }
        div[data-testid="stButton"] button:hover p { color:#FC4C02 !important; transform:scale(1.08) !important; }

        /* Aktions-Buttons = orange Pille mit dunkler Schrift */
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] {
            background-color:#FC4C02 !important; border:none !important; border-radius:30px !important;
            padding:12px 26px !important; box-shadow:0 2px 10px rgba(252,76,2,0.30) !important;
            width:auto !important;
        }
        div[data-testid="stButton"] button[kind="primary"] p,
        div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] p {
            color:#1A1A1A !important; font-size:16px !important; font-weight:800 !important;
            text-transform:uppercase; letter-spacing:0.3px;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover { background-color:#E34402 !important; transform:scale(1.03) !important; }

        /* ---------- DROPDOWN-MENUE (offen): orange Schrift auf schwarz ---------- */
        ul[data-baseweb="menu"], div[data-baseweb="popover"] ul[role="listbox"] {
            background-color:#1A1A1A !important;
        }
        li[role="option"], ul[data-baseweb="menu"] li {
            color:#FC4C02 !important; background-color:#1A1A1A !important;
            font-weight:600 !important;
        }
        li[role="option"]:hover, ul[data-baseweb="menu"] li:hover,
        li[role="option"][aria-selected="true"] {
            background-color:#242424 !important; color:#FC4C02 !important;
        }

        /* ---------- SEGMENTED CONTROL (Zeitraum / Dauer-km): alle lesbar ---------- */
        div[data-testid="stSegmentedControl"] button p,
        div[data-testid="stSegmentedControl"] label p {
            color:#E6E6E6 !important; font-size:15px !important; font-weight:600 !important;
        }
        div[data-testid="stSegmentedControl"] button {
            background-color:#242424 !important; border:1px solid #333333 !important;
        }
        div[data-testid="stSegmentedControl"] button:hover {
            background-color:#333333 !important;
        }
        div[data-testid="stSegmentedControl"] button[aria-checked="true"],
        div[data-testid="stSegmentedControl"] button[data-selected="true"] {
            background-color:#FC4C02 !important; border-color:#FC4C02 !important;
        }
        div[data-testid="stSegmentedControl"] button[aria-checked="true"] p,
        div[data-testid="stSegmentedControl"] button[data-selected="true"] p {
            color:#1A1A1A !important;
        }
        button[kind="segmented_control"], button[kind="segmented_control"] *,
        button[kind="pills"], button[kind="pills"] * {
            background-color:#242424 !important; color:#E6E6E6 !important;
        }
        button[kind="segmented_controlActive"], button[kind="segmented_controlActive"] *,
        button[kind="pillsActive"], button[kind="pillsActive"] * {
            background-color:#FC4C02 !important; color:#1A1A1A !important; border-color:#FC4C02 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    akktuelle_id = st.session_state.eingeloggt_als
    such_id = int(akktuelle_id) if akktuelle_id and str(akktuelle_id).isdigit() else akktuelle_id
    aktueller = person.get_person_by_id(such_id)

    if aktueller is None and such_id is not None:
        if hasattr(person, "create_new_athlete"):
            person.create_new_athlete(
                id=such_id, firstname="Neuer", lastname="Athlet",
                gender="Female", date_of_birth="2000"
            )
            aktueller = person.get_person_by_id(such_id)

    st.markdown(
        "<div style='font-size: 40px; font-weight: 800; letter-spacing: -1px; color: #FC4C02; margin-bottom: 30px;'>Beat faster!</div>",
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
                    img { border-radius:8px !important; border:1px solid #333333 !important; }
                    </style>
                """, unsafe_allow_html=True)
                if aktueller and os.path.exists(bild_pfad):
                    st.image(bild_pfad, width=140)
                else:
                    st.markdown("<div style='font-size: 70px; line-height: 1;'>👤</div>", unsafe_allow_html=True)
            except Exception:
                st.markdown("<div style='font-size: 70px; line-height: 1;'>👤</div>", unsafe_allow_html=True)

        with text_col:
            if aktueller:
                st.markdown(f"""
                    <div style="font-size: 30px; font-weight: 800; color: #FFFFFF; margin-top: 10px; line-height: 1.1; letter-spacing: -0.5px;">
                        {aktueller.firstname} {aktueller.lastname if hasattr(aktueller, 'lastname') else ''}
                    </div>
                    <div style="font-size: 15px; color: #9A9A9A; margin-top: 15px; font-weight: 500;">
                        ID: {aktueller.id} &nbsp;•&nbsp; Alter: {aktueller.calc_age()} &nbsp;•&nbsp; Geschlecht: {aktueller.gender}
                    </div>
                """, unsafe_allow_html=True)
                # 2 Zeilen Abstand, dann Training hinzufügen
                st.markdown("<div style='height: 2.4em;'></div>", unsafe_allow_html=True)
                zeige_training_hinzufuegen(aktueller)

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

        # Vergleichs-Ansicht (mit eigenem Zurück-Button)
        if st.session_state.vergleich_aktiv and aktueller:
            if st.button("← Zurück zum Dashboard", type="primary", key="vergleich_close_btn"):
                st.session_state.vergleich_aktiv = False
                st.rerun()
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

        daten = hole_kombinierte_daten(aktueller, sportart) if aktueller else pd.DataFrame()

        if daten.empty:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.info("👋 Willkommen! Füge über das '+' Symbol dein erstes Training hinzu oder vervollständige dein Profil über das '👤' Symbol.")
            return

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

        st.markdown("<div style='font-size:22px; font-weight:800; text-transform:uppercase; letter-spacing:-0.3px; color:#FC4C02; margin-bottom:20px;'>Aktivitäts-Zusammenfassung</div>", unsafe_allow_html=True)
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
        st.markdown("<div style='font-size:22px; font-weight:800; text-transform:uppercase; letter-spacing:-0.3px; color:#FC4C02; margin-bottom:20px;'>Aktivität</div>", unsafe_allow_html=True)

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
                <div style="text-align: right; font-size: 14px; font-weight: 600; color: #9A9A9A; padding-top: 8px;">
                    🟢 Niedrig &nbsp; 🟡 Moderat &nbsp; 🔴 Hoch
                </div>
            """, unsafe_allow_html=True)

        zeige_aktivitaets_diagramm(aktueller, sportart, intensitaet_wahl, zeitraum, anker, daten=daten)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ---------- HERZFREQUENZ ----------
        st.markdown("<div style='font-size:22px; font-weight:800; text-transform:uppercase; letter-spacing:-0.3px; color:#FC4C02; margin-bottom:20px;'>Herzfrequenz</div>", unsafe_allow_html=True)
        zeige_herzfrequenz_diagramm(daten, zeitraum, anker)

        # ---------- LEISTUNG VERGLEICHEN (ganz unten) ----------
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("Leistung vergleichen", type="primary", key="leistungsvergleich_toggle_btn"):
            st.session_state.vergleich_aktiv = True
            st.rerun()

    elif st.session_state.ansicht == "bearbeiten":
        zeige_profil_bearbeiten()