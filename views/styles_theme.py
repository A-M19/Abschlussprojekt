import streamlit as st


def apply_dark_theme():
    """Wendet das Strava-inspirierte Dark Theme an."""
    st.markdown(
        """
        <style>
        /* ---------- DARK / STRAVA THEME ---------- */
        .stApp { background-color:#1A1A1A !important; color:#E6E6E6 !important; }

        p, span, label, li {
            color:#E6E6E6 !important;
            font-family:"Maison Neue", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        h1, h2, h3, h4 {
            color:#FC4C02 !important;
            font-family:"Maison Neue", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            text-transform:uppercase;
            letter-spacing:-0.3px !important;
        }
        h3 { font-size:22px !important; font-weight:800 !important; margin-bottom:20px !important; }

        .stApp h1, .stApp h2, .stApp h3, .stApp h4,
        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stMarkdownContainer"] h4 {
            color:#FC4C02 !important;
        }

        div[data-testid="stButton"], div[data-testid="stPopover"] {
            display:flex !important; flex-direction:column !important;
            align-items:center !important; justify-content:center !important;
            margin-bottom:16px !important;
        }

        div[data-testid="stSelectbox"] label p {
            font-size:15px !important; font-weight:700 !important;
            color:#E6E6E6 !important; text-transform:uppercase;
        }

        div[data-testid="stMetric"] {
            background-color:#242424 !important; padding:24px !important;
            border-radius:10px !important; border:1px solid #333333 !important;
            box-shadow:0 2px 12px rgba(0,0,0,0.35) !important;
        }
        div[data-testid="stMetricLabel"] {
            color:#9A9A9A !important; font-size:13px !important;
            text-transform:uppercase; letter-spacing:0.5px !important; font-weight:600 !important;
        }
        div[data-testid="stMetricValue"] {
            color:#FFFFFF !important; font-size:30px !important; font-weight:800 !important;
        }

        div[data-testid="stSelectbox"] div[data-baseweb="select"],
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color:#242424 !important; background:#242424 !important;
            border:1px solid #333333 !important; box-shadow:none !important;
            border-radius:10px !important; color:#E6E6E6 !important;
            font-size:16px !important; font-weight:500 !important; height:48px !important;
        }

        hr { border-color:#333333 !important; margin:30px 0 !important; }

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
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color:#E34402 !important; transform:scale(1.03) !important;
        }

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

        img { border-radius:8px !important; border:1px solid #333333 !important; }

        /* ============ NEU ============ */

        /* Eingabefelder dunkel (Text / Zahl / Datum) */
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stDateInput"] input,
        div[data-testid="stTextInput"] div[data-baseweb="input"],
        div[data-testid="stNumberInput"] div[data-baseweb="input"],
        div[data-testid="stDateInput"] div[data-baseweb="input"] {
            background-color:#242424 !important; color:#E6E6E6 !important;
            border:1px solid #333333 !important; border-radius:8px !important;
        }
        div[data-testid="stTextInput"] label p,
        div[data-testid="stNumberInput"] label p,
        div[data-testid="stDateInput"] label p,
        div[data-testid="stFileUploader"] label p {
            color:#E6E6E6 !important; font-weight:600 !important;
        }
        /* Plus/Minus-Stepper der Zahlenfelder */
        div[data-testid="stNumberInput"] button {
            background-color:#333333 !important; border:none !important;
        }
        div[data-testid="stNumberInput"] button p { color:#E6E6E6 !important; font-size:18px !important; }

        /* Datei-Upload sichtbar */
        div[data-testid="stFileUploader"] section {
            background-color:#242424 !important; border:1px dashed #555555 !important;
        }
        div[data-testid="stFileUploader"] section * { color:#E6E6E6 !important; }
        div[data-testid="stFileUploader"] button {
            background-color:#FC4C02 !important; border:none !important; border-radius:8px !important;
        }
        div[data-testid="stFileUploader"] button p { color:#1A1A1A !important; font-weight:700 !important; }

        /* Formular-Submit-Buttons (Training hinzufügen / Änderungen speichern) orange */
        div[data-testid="stFormSubmitButton"] button {
            background-color:#FC4C02 !important; border:none !important; border-radius:30px !important;
            padding:10px 24px !important; width:auto !important;
        }
        div[data-testid="stFormSubmitButton"] button p {
            color:#1A1A1A !important; font-weight:800 !important;
            text-transform:uppercase; letter-spacing:0.3px; font-size:15px !important;
        }

        /* Toast & Tooltip: dunkle (schwarze) Schrift auf hellem Hintergrund */
        div[data-testid="stToast"], div[data-testid="stToast"] * { color:#1A1A1A !important; }
        div[data-testid="stTooltipContent"], div[data-testid="stTooltipContent"] *,
        div[role="tooltip"], div[role="tooltip"] * { color:#1A1A1A !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )