# News Brief Generator

An AI-powered news brief tool. Enter a topic, get a structured article with live news, weather, FX rates, and a related image — all generated in one pipeline run.

**Live:** https://news-brief-generator.fly.dev

---

## How it works

The pipeline runs as 8 separate processes that communicate over HTTP (MCP protocol) and a shared JSON message bus.

```
UI (Streamlit)
  → Scout Agent          — orchestrates context gathering
      → Contextualist    — calls World Data + Finance Monitor in parallel
          → World Data   — news headlines + weather (NewsAPI, OpenWeatherMap)
          → Finance      — FX rates (ExchangeRate API)
      → Media Engine     — stock images (Pexels)
  → Publisher Agent      — reads signal, writes article via GPT-4o
```

---

## Local development

**Prerequisites:** Python 3.12

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -e .

# 3. Copy and fill in API keys
cp .env.example .env
```

Start each component in a separate terminal (MCP servers first, then agents, then UI):

```bash
# MCP servers
python mcp-servers/world-data/server.py       # :8001
python mcp-servers/finance-monitor/server.py  # :8002
python mcp-servers/media-engine/server.py     # :8003

# Agents
python agents/contextualist_agent/main.py     # :8000
python agents/scout_agent/main.py             # :8004
python agents/publisher_agent/main.py         # :8005

# UI
streamlit run ui/app.py
```

---

## Docker Compose (local)

```bash
cp .env.example .env  # fill in your keys
docker compose up --build
# → http://localhost
```
