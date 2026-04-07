import streamlit as st
from backend import load_data
from frontend import (
    apply_glass_ui, login_ui, sidebar_menu,
    dashboard_ui, add_employee_ui, visualizations_ui, rankings_ui
)

st.set_page_config(
    page_title="PerformX — Employee Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_glass_ui()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_ui()
else:
    df = load_data()
    page = sidebar_menu(df)

    if page == "📊 Dashboard":
        dashboard_ui(df)
    elif page == "➕ Add Employee":
        add_employee_ui()
    elif page == "📈 Visualizations":
        visualizations_ui(df)
    elif page == "🏆 Rankings":
        rankings_ui(df)

    st.markdown('<div class="watermark">PerformX Analytics v2.0</div>', unsafe_allow_html=True)
