"""Cab Management App — Streamlit entry point.

Run with:
    streamlit run app.py
"""

import streamlit as st

from database.db import init_db

# Ensure tables exist on startup
init_db()

st.set_page_config(
    page_title="Cab Management",
    page_icon="🚕",
    layout="wide",
)

st.title("🚕 Cab Management App")
st.markdown(
    "Welcome! Use the sidebar to navigate between "
    "**Vehicles**, **Drivers**, **Ride Requests**, **Trips**, and the **Dashboard**."
)
