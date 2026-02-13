import streamlit as st

from agents import run_scout, run_publisher, normalize_payload
from utils import get_location_context
from components import tile

# Topic input
st.title("Generate News Reports")
topic = st.text_input("Topic", "Semiconductor factory opening in Japan")

# Auto-fetch city using LLM
city = get_location_context(topic)['capital']

# Metadata toggle in sidebar
with st.sidebar:
    st.header("Options")
    show_metadata = st.checkbox("Show metadata", value=False)

if st.button("Generate Report"):
    st.write("Running Scout...")
    scout_data = run_scout(topic, city)

    # Normalize image src before sending to publisher
    scout_data = normalize_payload(scout_data)

    st.write("Running Publisher...")
    publisher_data = run_publisher(scout_data)

    # Context snapshot tiles
    context = scout_data.get("context", {})
    fx = context.get("financial_context", {})
    weather_str = context.get("location", {}).get("weather", "N/A")
    currency = fx.get("currency_code", "")
    rate = fx.get("rate", "")
    fx_str = f"1 {currency} = {rate} USD" if rate else "N/A"

    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(tile("📍", "Location", scout_data.get("location", "N/A")), unsafe_allow_html=True)
    with col2:
        st.markdown(tile("🌤", "Weather", weather_str), unsafe_allow_html=True)
    with col3:
        st.markdown(tile("💱", "Exchange Rate", fx_str), unsafe_allow_html=True)
    st.write("")

    # Render Article in an expander to reduce scrolling
    st.subheader("Final Article")
    with st.expander("Read full article"):
        st.markdown(publisher_data.get("article", "No output"), unsafe_allow_html=True)

    # Display related image
    try:
        image_url = scout_data["media"]["images"][0]["src"]["url"]
        if image_url:
            st.image(image_url, caption="Related Image", use_container_width=True)
    except Exception:
        pass

    # Metadata section — hidden by default
    if show_metadata:
        st.divider()
        st.subheader("Metadata")

        st.markdown("**Payload**")
        st.json(publisher_data.get("payload"))

        signal = publisher_data.get("signal")
        if isinstance(signal, dict) and "ERROR" not in signal:
            st.markdown("**Signal**")
            st.json(signal)
