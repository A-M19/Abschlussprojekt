import streamlit as st
import os
import pandas as pd

from source import person
from views.extras.profil_bearbeiten import zeige_profil_bearbeiten
from views.diagramme.herzfrequenz_diagramm import zeige_herzfrequenz_diagramm
from views.diagramme.aktivitaets_diagramm import zeige_aktivitaets_diagramm
from views.extras.training_hinzufuegen import zeige_training_hinzufuegen, hole_alle_sportarten
from views.diagramme.leistungsvergleich import zeige_leistungsvergleich, hole_kombinierte_daten
from views.extras.hilfe_button import zeige_hilfe_bereich
from views.styles_theme import apply_dark_theme

INTENSITAET_DE = {"Low": "Niedrig", "Medium": "Moderat", "High": "Hoch"}


def standard_bildpfad(aktueller):
    """Kanonischer Speicherpfad für ein neu hochgeladenes Profilbild."""
    return os.path.join("data", "pictures", f"Athlete_{aktueller.id}.png")


def aktuelles_bild_pfad(aktueller):
    """
    Ermittelt den Pfad zum aktuell anzuzeigenden Profilbild.

    1. Wurde bereits ein Bild über die ID-Konvention gespeichert
       (data/pictures/Athlete_<id>.png), wird dieses bevorzugt.
    2. Andernfalls wird auf den in der JSON hinterlegten 'picture_path'
       zurückgegriffen.

    Gibt None zurück, wenn keiner der beiden Pfade existiert.
    """
    if not aktueller:
        return None

    id_pfad = standard_bildpfad(aktueller)
    if os.path.exists(id_pfad):
        return id_pfad

    hinterlegter_pfad = getattr(aktueller, "picture_path", None)
    if hinterlegter_pfad:
        hinterlegter_pfad = os.path.normpath(hinterlegter_pfad)
        if os.path.exists(hinterlegter_pfad):
            return hinterlegter_pfad

    return None


def render_hauptseite():
    apply_dark_theme()

    akktuelle_id = st.session_state.eingeloggt_als
    such_id = int(akktuelle_id) if akktuelle_id and str(akktuelle_id).isdigit() else akktuelle_id
    aktueller = person.get_person_by_id(such_id)

    if aktueller is None and such_id is not None:
        if hasattr(person, "create_new_athlete"):
            person.create_new_athlete(
                id=such_id,
                firstname="Neuer",
                lastname="Athlet",
                gender="Female",
                date_of_birth="2000",
            )
            aktueller = person.get_person_by_id(such_id)

    st.markdown(
        "<div style='font-size: 40px; font-weight: 800; letter-spacing: -1px; "
        "color: #FC4C02; margin-bottom: 30px;'>Beat faster!</div>",
        unsafe_allow_html=True,
    )

    links, rechts = st.columns([4.5, 0.7])

    with links:
        bild_col, text_col = st.columns([1, 3.5])

        with bild_col:
            try:
                bild_pfad = aktuelles_bild_pfad(aktueller)
                if bild_pfad:
                    st.image(bild_pfad, width=140)
                else:
                    st.markdown(
                        "<div style='font-size: 70px; line-height: 1;'>👤</div>",
                        unsafe_allow_html=True,
                    )
            except Exception:
                st.markdown(
                    "<div style='font-size: 70px; line-height: 1;'>👤</div>",
                    unsafe_allow_html=True,
                )

        with text_col:
            if aktueller:
                st.markdown(
                    f"""
                    <div style="font-size: 30px; font-weight: 800; color: #FFFFFF; 
                                margin-top: 10px; line-height: 1.1; letter-spacing: -0.5px;">
                        {aktueller.firstname} {getattr(aktueller, 'lastname', '')}
                    </div>
                    <div style="font-size: 15px; color: #9A9A9A; margin-top: 15px; font-weight: 500;">
                        ID: {aktueller.id} &nbsp;•&nbsp; Alter: {aktueller.calc_age()} &nbsp;•&nbsp; Geschlecht: {aktueller.gender}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("<div style='height: 2.4em;'></div>", unsafe_allow_html=True)
                zeige_training_hinzufuegen(aktueller)

    with rechts:
        if st.button("🚪", key="logout_btn", help="Abmelden"):
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
        _render_dashboard(aktueller)
    elif st.session_state.ansicht == "bearbeiten":
        zeige_profil_bearbeiten()


def _render_dashboard(aktueller):
    """Rendert das Dashboard mit Metriken und Diagrammen."""
    if "vergleich_aktiv" not in st.session_state:
        st.session_state.vergleich_aktiv = False

    # Vergleichs-Ansicht
    if st.session_state.vergleich_aktiv and aktueller:
        if st.button("← Zurück zum Dashboard", type="primary", key="vergleich_close_btn"):
            st.session_state.vergleich_aktiv = False
            st.rerun()
        zeige_leistungsvergleich(aktueller)
        return

    # Filter-Zeile
    st.markdown("<hr>", unsafe_allow_html=True)
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
        st.info(
            "👋 Willkommen! Füge über das '+' Symbol dein erstes Training hinzu "
            "oder vervollständige dein Profil über das '👤' Symbol."
        )
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

    # Aktivitäts-Zusammenfassung
    st.markdown(
        "<div style='font-size:22px; font-weight:800; text-transform:uppercase; "
        "letter-spacing:-0.3px; color:#FC4C02; margin-bottom:20px;'>"
        "Aktivitäts-Zusammenfassung</div>",
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)
    hr_val = daten["Heart_Rate"].mean() if "Heart_Rate" in daten.columns else 0
    o2_val = daten["Oxygen_Saturation"].mean() if "Oxygen_Saturation" in daten.columns else 0
    mu_val = daten["Muscle_Activity"].mean() if "Muscle_Activity" in daten.columns else 0

    with m1:
        st.metric(label="❤️ Ø Herzfrequenz", value=f"{hr_val:.0f} bpm")
    with m2:
        st.metric(label="🫁 O₂-Sättigung", value=f"{o2_val:.1f} %")
    with m3:
        st.metric(label="⚡ Muskel-Aktivität", value=f"{mu_val:.1f} µV")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Aktivitäts-Diagramm
    st.markdown(
        "<div style='font-size:22px; font-weight:800; text-transform:uppercase; "
        "letter-spacing:-0.3px; color:#FC4C02; margin-bottom:20px;'>Aktivität</div>",
        unsafe_allow_html=True,
    )

    zeit_col, legende_col = st.columns([2, 1])
    with zeit_col:
        zeitraum = (
            st.segmented_control(
                "Zeitraum",
                ["Letzte 6 Monate", "Letzter Monat", "Letzte Woche"],
                default="Letzte 6 Monate",
                label_visibility="collapsed",
            )
            or "Letzte 6 Monate"
        )
    with legende_col:
        st.markdown(
            """
            <div style="text-align: right; font-size: 14px; font-weight: 600; 
                        color: #9A9A9A; padding-top: 8px;">
                🟢 Niedrig &nbsp; 🟡 Moderat &nbsp; 🔴 Hoch
            </div>
            """,
            unsafe_allow_html=True,
        )

    zeige_aktivitaets_diagramm(aktueller, sportart, intensitaet_wahl, zeitraum, anker, daten=daten)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Herzfrequenz-Diagramm
    st.markdown(
        "<div style='font-size:22px; font-weight:800; text-transform:uppercase; "
        "letter-spacing:-0.3px; color:#FC4C02; margin-bottom:20px;'>Herzfrequenz</div>",
        unsafe_allow_html=True,
    )
    zeige_herzfrequenz_diagramm(daten, zeitraum, anker)

    # Leistungsvergleich-Button
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("Leistung vergleichen", type="primary", key="leistungsvergleich_toggle_btn"):
        st.session_state.vergleich_aktiv = True
        st.rerun()
