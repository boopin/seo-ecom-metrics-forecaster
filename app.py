import streamlit as st

# App-wide configuration
st.set_page_config(
    page_title="EcomSEO Predictor - Forecast Your E-commerce SEO Performance",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add meta tags for title and description
st.markdown(
    """
    <head>
        <meta charset="UTF-8">
        <meta name="title" content="EcomSEO Predictor - Forecast Your E-commerce SEO Performance">
        <meta name="description" content="Forecast your e-commerce SEO performance with EcomSEO Predictor. Predict traffic, conversions, and revenue growth with precision.">
    </head>
    """,
    unsafe_allow_html=True
)

# Redirect to the Home page
st.switch_page("pages/Home.py")
