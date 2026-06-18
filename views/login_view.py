import streamlit as st
from source import person
from auth import login_user, register_user

def render_login_page():
    # Wir nutzen den session_state, um zwischen Login, Registrieren und Erfolg zu wechseln
    if st.session_state.page == "login":
        st.title("Beat faster!")
        
        # Eingabefelder laut Mockup
        username = st.text_input("ID / Benutzername", placeholder="Z.B. 1, 2, 3...")
        password = st.text_input("Passwort", type="password")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Anmelden", use_container_width=True):
                if username == "" or password == "":
                    st.error("Bitte alle Felder ausfüllen!")
                elif login_user(username, password):
                    st.session_state.eingeloggt_als = username
                    st.session_state.page = "hauptseite"
                    st.rerun()
                else:
                    st.error("Falsche ID oder Passwort!")
                    
        with col2:
            if st.button("neuen Account erstellen"):
                st.session_state.page = "registrieren"
                st.rerun()
                
        st.caption("Hilfe")

    elif st.session_state.page == "registrieren":
        st.title("Registrieren")
        
        neuer_user = st.text_input("Benutzername / Neue ID")
        pw1 = st.text_input("Passwort", type="password")
        pw2 = st.text_input("Passwort wiederholen", type="password")
        
        if st.button("Account erstellen"):
            if pw1 != pw2:
                st.error("Passwörter stimmen nicht überein!")
            elif neuer_user.strip() == "" or pw1 == "":
                st.error("Felder dürfen nicht leer sein!")
            else:
                # Registrierung in auth.py ausführen
                erfolg = register_user(neuer_user, pw1)
                if erfolg:
                    st.session_state.page = "erfolg"
                    st.rerun()
                else:
                    st.error("Benutzername existiert bereits!")

    elif st.session_state.page == "erfolg":
        st.title("Beat faster!")
        # Exakt die geforderte Schrift und Logik aus deiner Beschreibung:
        st.success("Account erstellt!")
        
        if st.button("Zum Login"):
            st.session_state.page = "login"
            st.rerun()