import streamlit as st

# App-wide configuration
st.set_page_config(
    page_title="EcomSEO Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Redirect to the Home page
st.switch_page("pages/Home.py")
