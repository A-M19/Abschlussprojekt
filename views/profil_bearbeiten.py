# views/profil_bearbeiten.py
import streamlit as st
import json

def lade_alle_athleten():
    """Lädt die aktuelle Datenbank aus der JSON-Datei."""
    try:
        with open("data/person_db.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Datenbank 'person_db.json' nicht gefunden!")
        return None

def speichere_alle_athleten(daten):
    """Schreibt die aktualisierten Daten zurück in die JSON-Datei."""
    with open("data/person_db.json", "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=4, ensure_ascii=False)

def zeige_profil_bearbeiten():
    st.markdown("### Meine persönlichen Daten bearbeiten")
    
    if "eingeloggt_als" not in st.session_state or st.session_state.eingeloggt_als is None:
        st.warning("Bitte logge dich zuerst ein, um dein Profil zu bearbeiten.")
        return

    aktuelle_id = st.session_state.eingeloggt_als
    user_id_str = str(aktuelle_id)
    
    alle_athleten = lade_alle_athleten()
    if alle_athleten is None:
        return
    
    aktueller_athlet = None
    index_oder_key = None
    ist_liste = isinstance(alle_athleten, list)

    # --- DIE ALLES-FRESSER-SUCHE (Egal ob Liste oder Dictionary) ---
    if ist_liste:
        # Wenn es eine Liste ist, loopen wir durch
        for index, athlet in enumerate(alle_athleten):
            if isinstance(athlet, dict) and str(athlet.get("id")) == user_id_str:
                aktueller_athlet = athlet
                index_oder_key = index
                break
        # Sicherheits-Fallback falls IDs nicht im Objekt stehen, sondern der Index gemeint ist
        if aktueller_athlet is None and aktuelle_id.isdigit():
            idx = int(aktuelle_id)
            if 0 <= idx < len(alle_athleten):
                aktueller_athlet = alle_athleten[idx]
                index_oder_key = idx
    else:
        # Wenn es ein Dictionary ist, nutzen wir die Keys
        if user_id_str in alle_athleten:
            aktueller_athlet = alle_athleten[user_id_str]
            index_oder_key = user_id_str
        elif aktuelle_id.isdigit() and int(aktuelle_id) in alle_athleten:
            aktueller_athlet = alle_athleten[int(aktuelle_id)]
            index_oder_key = int(aktuelle_id)

    # --- PRÜFUNG ---
    if aktueller_athlet is None:
        st.error(f"Fehler: Athlet mit der ID '{aktuelle_id}' wurde nicht gefunden.")
        return
    
    # --- FORMULAR ---
    with st.form("profil_edit_form"):
        
        
        neuer_vorname = st.text_input("Vorname", value=aktueller_athlet.get("firstname", ""))
        neuer_nachname = st.text_input("Nachname", value=aktueller_athlet.get("lastname", ""))
        neue_email = st.text_input("E-Mail-Adresse", value=aktueller_athlet.get("email", ""))
        neues_telefon = st.text_input("Telefonnummer", value=aktueller_athlet.get("phone", ""))
        
        speichern_gedrueckt = st.form_submit_button("Änderungen speichern")
        
        if speichern_gedrueckt:
            # Daten im geladenen Objekt anpassen
            if ist_liste:
                alle_athleten[index_oder_key]["firstname"] = neuer_vorname
                alle_athleten[index_oder_key]["lastname"] = neuer_nachname
                alle_athleten[index_oder_key]["email"] = neue_email
                alle_athleten[index_oder_key]["phone"] = neues_telefon
            else:
                alle_athleten[index_oder_key]["firstname"] = neuer_vorname
                alle_athleten[index_oder_key]["lastname"] = neuer_nachname
                alle_athleten[index_oder_key]["email"] = neue_email
                alle_athleten[index_oder_key]["phone"] = neues_telefon
            
            speichere_alle_athleten(alle_athleten)
            st.success("Deine Daten wurden erfolgreich aktualisiert!")
            st.rerun()
