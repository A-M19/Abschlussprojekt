import streamlit as st
from views.login_view import render_login_page
from source import person # Importiert die Datei deiner Kollegin

# Streamlit Konfiguration (MUSS das allererste in der Datei sein!)
st.set_page_config(page_title="Beat faster!", layout="wide")

# Session State Variablen anlegen, damit Streamlit den Zustand nicht vergisst
if "page" not in st.session_state:
    st.session_state.page = "login"
if "eingeloggt_als" not in st.session_state:
    st.session_state.eingeloggt_als = None

# Seiten-Steuerung (Routing)
if st.session_state.page in ["login", "registrieren", "erfolg"]:
    render_login_page()

elif st.session_state.page == "hauptseite":
    # Hol dir die eingegebene ID aus dem Session State
    aktuelle_id = st.session_state.eingeloggt_als
    
    # Sicherstellen, dass wir nach einer Zahl suchen, wenn die ID rein numerisch ist
    if aktuelle_id.isdigit():
        such_id = int(aktuelle_id)
    else:
        such_id = aktuelle_id

    # Alle Personen laden und den passenden Athleten anhand der ID suchen
    alle_athleten = person.get_person_data()
    aktueller_athlet = None
    
    for ath in alle_athleten:
        if ath.id == such_id:
            aktueller_athlet = ath
            break

    # Wenn der Athlet existiert, laden wir das Profil
    if aktueller_athlet is not None:
        st.title(f"Beat faster!")
        st.subheader(f"Hallo! {aktueller_athlet.firstname} {aktueller_athlet.lastname}")
        st.write(f"**ID:** {aktueller_athlet.id} | **Alter:** {aktueller_athlet.calc_age()} Jahre | **Geschlecht:** {aktueller_athlet.gender}")
        
        # Profilbild anzeigen
        try:
            bild = aktueller_athlet.get_image()
            st.image(bild, width=150)
        except Exception:
            st.warning("Kein Profilbild unter dem Pfad gefunden.")
            
    else:
        # Sicherheits-Fallback für neu registrierte Accounts
        st.title(f"Beat faster!")
        st.subheader(f"Hallo! {aktuelle_id}")
        st.info("Profil wird geladen... (Da dies ein neuer Account ist, wurden noch keine Profildaten in der JSON hinterlegt).")

    # Abmelde-Button
    st.write("---")
    if st.button("Abmelden"):
        st.session_state.page = "login"
        st.session_state.eingeloggt_als = None
        st.rerun()