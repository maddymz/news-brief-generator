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
# Create nginx/.htpasswd (or omit the nginx service for no auth)
cp .env.example .env  # fill in your keys

docker compose up --build
# → http://localhost
```

---

## Deployment (Fly.io)

Deploys automatically on every push to `main` via GitHub Actions.

### One-time setup

```bash
# Install flyctl and log in
brew install flyctl && flyctl auth login

# Create the app and persistent volume
flyctl apps create news-brief-generator --org personal
flyctl volumes create post_office --app news-brief-generator --region iad --size 1

# Generate a deploy token (add as FLY_API_TOKEN GitHub secret)
flyctl tokens create deploy -x 2160h --app news-brief-generator
```

### GitHub Actions secrets

| Secret | Description |
|---|---|
| `FLY_API_TOKEN` | Deploy token from step above |
| `OPENAI_API_KEY` | OpenAI |
| `NEWSAPI_KEY` | NewsAPI |
| `OPENWEATHERMAP_API_KEY` | OpenWeatherMap |
| `EXCHANGE_RATE_API_KEY` | ExchangeRate-API |
| `PEXELS_API_KEY` | Pexels |
| `APP_CREDENTIALS` | Login credentials JSON (see below) |

### Generating `APP_CREDENTIALS`

```bash
source .venv/bin/activate
python3 - <<'EOF'
import streamlit_authenticator as stauth, json, secrets

config = {
    "credentials": {
        "usernames": {
            "admin": {
                "name": "Admin",
                "password": stauth.Hasher().hash("your-password-here")
            }
        }
    },
    "cookie": {
        "name": "news_brief_auth",
        "key": secrets.token_hex(16),
        "expiry_days": 30
    }
}
print(json.dumps(config))
EOF
```

Paste the output as the `APP_CREDENTIALS` GitHub secret. Log in using the plain-text password you chose above.

To change the password later: regenerate and update the secret — **no redeploy required**.

---

## Environment variables

| Variable | Source |
|---|---|
| `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) |
| `NEWSAPI_KEY` | [newsapi.org](https://newsapi.org) |
| `OPENWEATHERMAP_API_KEY` | [openweathermap.org](https://openweathermap.org) |
| `EXCHANGE_RATE_API_KEY` | [exchangerate-api.com](https://exchangerate-api.com) |
| `PEXELS_API_KEY` | [pexels.com/api](https://www.pexels.com/api) |
