# Pre-provided imports
from dotenv import load_dotenv
from openai import OpenAI
import json
import os

load_dotenv()  # Load environment variables

# MCP agent URLs
SCOUT_URL = "http://0.0.0.0:8004/mcp"
PUBLISHER_URL = "http://0.0.0.0:8005/mcp"

# Fetch OpenAI API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Async helper to call MCP tools
async def call_tool(url, tool, params):
    async with Client(url) as client:
        res = await client.call_tool(tool, params)
        return res.data

# Pre-provided OpenAI client
client = OpenAI(api_key=api_key)

# Pre-provided function to fetch city/country context from topic
def get_location_context(news_text: str) -> dict:
    """
    Extracts country and capital from a text string using an LLM.
    """
    prompt = f"""
    Given the news text below, identify the primary country it is about.
    Return only a JSON object with the keys 'country' and 'capital'.
    If no country is mentioned, return US and its capital for both.

    Text: "{news_text}"
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# Task 10: Build Streamlit Interface to Trigger Agents
import streamlit as st
import asyncio
from fastmcp import Client
# Call Scout agent
def run_scout(topic, city):
    return asyncio.run(call_tool(SCOUT_URL, "scout", {"topic": topic, "city": city}))

# Call Publisher agent
def run_publisher(payload):
    return asyncio.run(call_tool(PUBLISHER_URL, "publish_brief", {"payload": payload}))

# Normalize payload to ensure image src is a valid JSON object
def normalize_payload(payload):
    try:
        img = payload["media"]["images"][0]
        src = img.get("src")
        if isinstance(src, str):
            img["src"] = {"url": src, "type": "image"}
        if src is None:
            img["src"] = {"url": "", "type": "image"}
    except Exception:
        pass
    return payload

# Streamlit UI
st.title("Generate News Reports")

# Topic input
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

    def tile(icon, label, value):
        return f"""
        <div style="
            background:#f8f9fb;
            border:1px solid #e0e4ea;
            border-radius:12px;
            padding:16px 14px;
            text-align:center;
            min-height:90px;
        ">
            <div style="font-size:11px;color:#888;font-weight:600;
                        text-transform:uppercase;letter-spacing:0.8px;
                        margin-bottom:8px;">{icon} {label}</div>
            <div style="font-size:14px;font-weight:600;color:#1a1a2e;
                        word-wrap:break-word;line-height:1.5;">{value}</div>
        </div>"""

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