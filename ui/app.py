import streamlit as st

st.set_page_config(page_title="News Brief Generator", page_icon="📰", layout="centered")

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

from agents import run_scout, run_publisher, normalize_payload
from utils import get_location_context
from components import inject_css, page_header, tile

# ── Auth ─────────────────────────────────────────────────────────────────────
# APP_CREDENTIALS env var (Fly secret) holds a JSON blob with hashed credentials.
# If absent (local dev without docker-compose), auth is skipped entirely.
_creds_json = os.getenv("APP_CREDENTIALS")
if _creds_json:
    import bcrypt
    _cfg = json.loads(_creds_json)
    if not st.session_state.get("authenticated"):
        st.subheader("Login")
        _username = st.text_input("Username")
        _password = st.text_input("Password", type="password")
        if st.button("Login"):
            _usernames = _cfg.get("credentials", {}).get("usernames", {})
            _user = _usernames.get(_username)
            if _user and bcrypt.checkpw(_password.encode(), _user["password"].encode()):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect username or password.")
        st.stop()
# ─────────────────────────────────────────────────────────────────────────────

inject_css()
page_header()

st.markdown("### 🔍 Enter your topic")
st.markdown("Get comprehensive news reports with live context, weather, and financial data")
topic = st.text_input("topic", "Semiconductor factory opening in Japan", label_visibility="collapsed", placeholder="Enter any news topic...")

# Metadata toggle in sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")
    show_metadata = st.checkbox("🔍 Show metadata", value=False)
    st.markdown("---")
    st.markdown("### 💡 About")
    st.markdown("""
    This app uses AI agents to:
    - 🔎 Gather news headlines
    - 🌍 Fetch weather data
    - 💱 Get exchange rates
    - 🖼️ Find related images
    - ✍️ Generate articles
    """)
    st.markdown("---")
    st.markdown("**Version:** 0.1.0")
    st.markdown("**Powered by:** FastMCP + OpenAI")

if st.button("Generate Report", width="stretch"):
    with st.spinner("Detecting location..."):
        city = get_location_context(topic)['capital']
    with st.spinner("Running Scout..."):
        scout_data = run_scout(topic, city)
    scout_data = normalize_payload(scout_data)

    with st.spinner("Running Publisher..."):
        publisher_data = run_publisher(scout_data)

    # Context snapshot tiles
    context = scout_data.get("context", {})
    fx = context.get("financial_context", {})
    weather_str = context.get("location", {}).get("weather", "N/A")
    currency = fx.get("currency_code", "")
    rate = fx.get("rate", "")
    fx_str = f"1 {currency} = {rate} USD" if rate else "N/A"

    st.markdown("---")
    st.markdown("### 📊 Context Overview")
    st.write("")
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown(tile("📍", "Location", scout_data.get("location", "N/A")), unsafe_allow_html=True)
    with col2:
        st.markdown(tile("🌤", "Weather", weather_str), unsafe_allow_html=True)
    with col3:
        st.markdown(tile("💱", "Exchange Rate", fx_str), unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Render Article in an expander to reduce scrolling
    st.markdown("### 📄 Generated Article")
    with st.expander("▼ Read full article", expanded=True):
        st.markdown(publisher_data.get("article", "No output"), unsafe_allow_html=True)

    # Display related image
    st.write("")
    try:
        image_url = scout_data["media"]["images"][0]["src"]["url"]
        if image_url:
            st.markdown("### 🖼️ Related Imagery")
            st.image(image_url, caption="AI-selected contextual image", width="stretch")
    except Exception:
        pass

    # Metadata section — hidden by default
    if show_metadata:
        st.markdown("---")
        st.markdown("### 🔧 Debug Information")

        with st.expander("📦 Payload Data", expanded=False):
            st.json(publisher_data.get("payload"))

        signal = publisher_data.get("signal")
        if isinstance(signal, dict) and "ERROR" not in signal:
            with st.expander("📡 Signal Data", expanded=False):
                st.json(signal)
