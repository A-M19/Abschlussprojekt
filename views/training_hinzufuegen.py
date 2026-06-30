import streamlit as st
import json
import os
from datetime import date

TRAINING_DB_PATH = "data/training_db.json"
SPORTARTEN_CUSTOM_PATH = "data/sportarten_custom.json"

SPORTARTEN_MIT_STRECKE = [
    "Laufen",
    "Radfahren",
    "Schwimmen",
    "Wandern",
    "Inline-Skaten"
]

NEUE_SPORTART_OPTION = "➕ Training hinzufügen"


def lade_trainings():
    if not os.path.exists(TRAINING_DB_PATH):
        return []

    try:
        with open(TRAINING_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def speichere_trainings(trainings):
    # Sicherheitshalber den Ordner erstellen, falls er noch nicht existiert
    os.makedirs(os.path.dirname(TRAINING_DB_PATH), exist_ok=True)
    with open(TRAINING_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(trainings, f, indent=4, ensure_ascii=False)


def lade_eigene_sportarten():
    """Lädt die vom Nutzer selbst hinzugefügten Sportarten (Name + ob sie eine Strecke haben).
    Einträge ohne gültigen "name"-Schlüssel werden hier herausgefiltert, damit fehlerhafte
    oder veraltete Daten in sportarten_custom.json die App nicht zum Absturz bringen."""
    if not os.path.exists(SPORTARTEN_CUSTOM_PATH):
        return []

    try:
        with open(SPORTARTEN_CUSTOM_PATH, "r", encoding="utf-8") as f:
            daten = json.load(f)
    except Exception:
        return []

    return [s for s in daten if isinstance(s, dict) and s.get("name")]


def speichere_eigene_sportart(name, hat_strecke):
    """Speichert eine neue, vom Nutzer angelegte Sportart dauerhaft ab, falls noch nicht vorhanden."""
    eigene_sportarten = lade_eigene_sportarten()

    if not any(s["name"] == name for s in eigene_sportarten):
        eigene_sportarten.append({"name": name, "hat_strecke": hat_strecke})

        os.makedirs(os.path.dirname(SPORTARTEN_CUSTOM_PATH), exist_ok=True)
        with open(SPORTARTEN_CUSTOM_PATH, "w", encoding="utf-8") as f:
            json.dump(eigene_sportarten, f, indent=4, ensure_ascii=False)


def hole_alle_sportarten(aktueller):
    """
    Zentrale Stelle, die IMMER die vollständige, aktuelle Liste aller
    Sportarten liefert: Standard-/Athleten-Sportarten + selbst hinzugefügte.
    """
    try:
        sportart_optionen = aktueller.get_sportarten()
    except Exception:
        sportart_optionen = []

    if not sportart_optionen:
        sportart_optionen = [
            "Laufen",
            "Radfahren",
            "Schwimmen",
            "Krafttraining",
            "Wandern",
            "Yoga",
            "Inline-Skaten"
        ]
    else:
        # falls aktueller.get_sportarten() eine eigene Liste zurückgibt,
        # diese nicht verändern, sondern eine Kopie verwenden
        sportart_optionen = list(sportart_optionen)

    eigene_sportarten = lade_eigene_sportarten()
    for s in eigene_sportarten:
        if s["name"] not in sportart_optionen:
            sportart_optionen.append(s["name"])

    return sportart_optionen


def hole_sportarten_mit_strecke():
    """
    Liefert alle Sportarten, bei denen eine Strecke erfasst wird/werden
    kann - die festen aus SPORTARTEN_MIT_STRECKE sowie die selbst
    angelegten, bei denen "hat_strecke" gesetzt wurde.
    """
    eigene_sportarten = lade_eigene_sportarten()
    eigene_mit_strecke = [s["name"] for s in eigene_sportarten if s.get("hat_strecke")]
    return SPORTARTEN_MIT_STRECKE + eigene_mit_strecke


def zeige_training_hinzufuegen(aktueller):
    # 1. PRÜFUNG: Hat der aktuelle Nutzer bereits Trainingsdaten?
    alle_trainings = lade_trainings()
    hat_daten = False
    if aktueller and hasattr(aktueller, 'id'):
        hat_daten = any(t.get("athlet_id") == aktueller.id for t in alle_trainings)

    # 2. DEFAULT EINSTELLUNG: Wenn keine Daten da sind, wird das Formular automatisch angezeigt (True)
    if "training_form_anzeigen" not in st.session_state:
        st.session_state.training_form_anzeigen = not hat_daten

    plus_col, leer_col = st.columns([0.2, 5])

    with plus_col:
        # KORRIGIERT: Expliziter und korrekter Tooltip, alter "Account"-Text ist weg
        if st.button("➕", key="training_plus_button", help="Training hinzufügen"):
            st.session_state.training_form_anzeigen = not st.session_state.training_form_anzeigen

    if st.session_state.training_form_anzeigen:
        st.markdown("### Neues Training hinzufügen")

        sportart_optionen = hole_alle_sportarten(aktueller)
        sportarten_mit_strecke = hole_sportarten_mit_strecke()

        # Option zum Anlegen einer komplett neuen Sportart anhängen
        sportart_optionen = sportart_optionen + [NEUE_SPORTART_OPTION]

        # WICHTIG: Selectbox außerhalb des st.form, damit neue Sportarten dynamisch aufpoppen 
        # und das Styling genau wie beim Dashboard-Filter ist.
        sportart = st.selectbox(
            "Aktivität auswählen",
            sportart_optionen,
            key="sportart_auswahl"
        )

        neue_sportart_name = None
        neue_sportart_hat_strecke = False

        if sportart == NEUE_SPORTART_OPTION:
            neue_sportart_name = st.text_input(
                "Name der neuen Sportart",
                key="neue_sportart_name_input"
            )
            neue_sportart_hat_strecke = st.checkbox(
                "Wird bei dieser Sportart eine Strecke zurückgelegt? (z. B. Laufen, Radfahren)",
                key="neue_sportart_hat_strecke_checkbox"
            )

        zeigt_strecke = (
            sportart in sportarten_mit_strecke
            or (sportart == NEUE_SPORTART_OPTION and neue_sportart_hat_strecke)
        )

        with st.form("training_hinzufuegen_form"):
            trainings_datum = st.date_input("Datum", value=date.today())

            dauer_minuten = st.number_input(
                "Dauer (Minuten)",
                min_value=1,
                max_value=1000,
                value=45,
                step=1
            )

            strecke_km = None
            if zeigt_strecke:
                strecke_km = st.number_input(
                    "Zurückgelegte Strecke (km)",
                    min_value=0.1,
                    max_value=500.0,
                    value=5.0,
                    step=0.1
                )

            herzfrequenz_bpm = st.number_input(
                "Durchschnittliche Herzfrequenz (bpm)",
                min_value=40,
                max_value=240,
                value=130,
                step=1
            )

            training_speichern = st.form_submit_button("Training hinzufügen")

            if training_speichern:
                finale_sportart = sportart

                if sportart == NEUE_SPORTART_OPTION:
                    if neue_sportart_name and neue_sportart_name.strip():
                        finale_sportart = neue_sportart_name.strip()
                        speichere_eigene_sportart(finale_sportart, neue_sportart_hat_strecke)
                    else:
                        st.warning("Bitte einen Namen für die neue Sportart eingeben.")
                        finale_sportart = None

                if finale_sportart:
                    trainings_liste = lade_trainings()

                    neuer_eintrag = {
                        "athlet_id": aktueller.id,
                        "datum": str(trainings_datum),
                        "sportart": finale_sportart,
                        "dauer_minuten": int(dauer_minuten),
                        "herzfrequenz_bpm": int(herzfrequenz_bpm)
                    }

                    if strecke_km is not None:
                        neuer_eintrag["strecke_km"] = float(strecke_km)

                    trainings_liste.append(neuer_eintrag)
                    speichere_trainings(trainings_liste)

                    st.session_state.training_form_anzeigen = False
                    st.session_state.training_gespeichert = True
                    st.rerun()

    if st.session_state.get("training_gespeichert", False):
        st.success("Training erfolgreich hinzugefügt.")
        st.session_state.training_gespeichert = False