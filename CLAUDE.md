# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

All components must be started in separate terminals. There is no single-command startup.

**1. Start MCP Servers** (in any order):
```bash
python mcp-servers/world-data/server.py        # Port 8001
python mcp-servers/finance-monitor/server.py   # Port 8002
python mcp-servers/media-engine/server.py      # Port 8003
```

**2. Start Agents** (after MCP servers are up):
```bash
python agents/contextualist_agent/main.py      # Port 8000
python agents/scout_agent/main.py              # Port 8004
python agents/publisher_agent/main.py          # Port 8005
```

**3. Start UI backend**:
```bash
python ui/backend/main.py             # Port 8006
```

**4. Start UI frontend** (first run: `cd ui/frontend && npm install`):
```bash
cd ui/frontend && npm run dev         # Port 5173 — proxies /api → 8006
```

Open `http://localhost:5173` in your browser.

No build step (for Python), linting config, or test suite exists in this project.

## Architecture

This is a **multi-agent pipeline** built on FastMCP. All components communicate over HTTP using the MCP protocol. There is also a file-based async message bus (`protocol/post_office.json`) for agent-to-agent coordination.

### Data Flow

```
ui/app.py
  → Scout Agent (8004)
      → Contextualist Agent (8000) via direct MCP call
          → World Data Server (8001): news + weather
          → Finance Monitor (8002): FX rates
          Publishes result to post_office.json
      ← Scout polls post_office.json for response
      → Media Engine (8003): images
      Publishes aggregated signal to post_office.json
  → Publisher Agent (8005)
      Reads signal, generates article via LLM
```

### Key Design Patterns

- **MCP servers** (`mcp-servers/`) expose tools via `@mcp.tool` decorators and run as independent HTTP services. Each wraps one or more external APIs.
- **Agents** (`agents/`) are also FastMCP servers that expose higher-level tools. They orchestrate MCP servers using `AsyncExitStack` + `stdio_client` for concurrent calls.
- **Post office** (`protocol/post_office.py`) is a simple JSON append-log used for async handoffs between agents. Agents poll it with `wait_for_response(task_id)`. It is cleared at the start of each Scout run.
- **UI backend** (`ui/backend/main.py`) is a FastAPI app (port 8006) that exposes `POST /api/generate` as an SSE stream. It calls agents via MCP and streams progress events to the browser as each pipeline step completes.
- **UI frontend** (`ui/frontend/`) is a Vite + React SPA (port 5173 in dev). It consumes the SSE stream and renders results progressively. Vite proxies `/api/*` to port 8006.

### Environment Variables

All API keys are loaded from `.env`. Required keys:
- `OPENAI_API_KEY` — article generation and location extraction
- `NEWSAPI_KEY` — news headlines
- `OPENWEATHERMAP_API_KEY` — weather
- `EXCHANGE_RATE_API_KEY` — FX rates
- `PEXELS_API_KEY` — stock images

No dependency manifest exists; install FastMCP, FastAPI, uvicorn, python-dotenv, httpx, and openai manually.
