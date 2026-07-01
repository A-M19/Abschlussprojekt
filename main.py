import streamlit as st
from views.login_view import render_login_page
from views.hauptseite_view import render_hauptseite
from views.extras.hilfe_button import zeige_hilfe_bereich


st.set_page_config(page_title="Beat faster!", layout="wide")
if "page" not in st.session_state:
    st.session_state.page = "login"
if "eingeloggt_als" not in st.session_state:
    st.session_state.eingeloggt_als = None
# ZUSATZ: Start-Ansicht für das Dashboard festlegen
if "ansicht" not in st.session_state:
    st.session_state.ansicht = "dashboard"
# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------
if st.session_state.page in ["login", "registrieren", "erfolg"]:
    render_login_page()
    
elif st.session_state.page == "hauptseite":
    render_hauptseite()
    zeige_hilfe_bereich ()
    