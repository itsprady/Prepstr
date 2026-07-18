# Prepstr Streamlit App

import streamlit as st
from pages import Login, Signup, Dashboard, Mock_Test, Result, Admin

st.set_page_config(page_title="Prepstr", layout="wide")

# Simple router: use sidebar to choose page
pages = {
    "Login": Login,
    "Signup": Signup,
    "Dashboard": Dashboard,
    "Mock Test": Mock_Test,
    "Result": Result,
    "Admin": Admin,
}

if 'user' not in st.session_state:
    st.session_state.user = None

if 'test_in_progress' not in st.session_state:
    st.session_state.test_in_progress = None

st.sidebar.title("Prepstr")
choice = st.sidebar.radio("Go to", list(pages.keys()))

page = pages[choice]
page.show()
