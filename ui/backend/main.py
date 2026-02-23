import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Allow imports from ui/ and project root
ROOT = Path(__file__).resolve().parent.parent.parent
UI_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(UI_DIR))

load_dotenv(dotenv_path=ROOT / ".env")

from utils import get_location_context  # noqa: E402
from agents import call_tool, normalize_payload  # noqa: E402

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Leaf MCP servers — none of these make nested MCP calls, so they're safe
# to call directly from here without triggering FastMCP's nested-client bug.
WORLD_DATA_URL = os.getenv("WORLD_DATA_URL", "http://0.0.0.0:8001/mcp")
FINANCE_URL    = os.getenv("FINANCE_URL",    "http://0.0.0.0:8002/mcp")
MEDIA_URL      = os.getenv("MEDIA_ENGINE_URL", "http://0.0.0.0:8003/mcp")
PUBLISHER_URL  = os.getenv("PUBLISHER_URL",  "http://0.0.0.0:8005/mcp")


class GenerateRequest(BaseModel):
    topic: str


async def generate_stream(topic: str):
    try:
        # Step 1: location (sync LLM call — offload to thread pool)
        loop = asyncio.get_event_loop()
        location = await loop.run_in_executor(None, get_location_context, topic)
        city = location.get("capital", "Washington")
        yield f"data: {json.dumps({'step': 'location', **location})}\n\n"

        # Step 2: gather context + media in parallel from leaf MCP servers
        news_task    = asyncio.create_task(call_tool(WORLD_DATA_URL, "search_news",   {"query": topic}))
        weather_task = asyncio.create_task(call_tool(WORLD_DATA_URL, "get_weather",   {"city": city}))
        fx_task      = asyncio.create_task(call_tool(FINANCE_URL,    "get_fx_rate",   {"location": city}))
        media_task   = asyncio.create_task(call_tool(MEDIA_URL,      "search_images", {"query": topic, "per_page": 1}))

        news, weather, fx, media = await asyncio.gather(
            news_task, weather_task, fx_task, media_task
        )

        # Assemble in the same shape Scout + Contextualist used to produce
        weather_str = f"{weather.get('temperature')}{weather.get('units', '°C')}, {weather.get('description', '')}"
        context = {
            "topic": topic,
            "news_headline": news.get("headline"),
            "location": {"city": city, "weather": weather_str},
            "financial_context": fx,
        }
        scout_data = normalize_payload({
            "topic": topic,
            "location": city,
            "context": context,
            "media": media,
        })
        yield f"data: {json.dumps({'step': 'scout', 'data': scout_data})}\n\n"

        # Step 3: publisher
        publisher_data = await call_tool(
            PUBLISHER_URL, "publish_brief", {"payload": scout_data}
        )
        yield f"data: {json.dumps({'step': 'publisher', 'data': publisher_data})}\n\n"

        yield f"data: {json.dumps({'step': 'done'})}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'step': 'error', 'message': str(e)})}\n\n"


@app.post("/api/generate")
async def generate(req: GenerateRequest):
    return StreamingResponse(
        generate_stream(req.topic),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8006)
