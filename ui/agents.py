import asyncio
import os
from fastmcp import Client

SCOUT_URL = os.getenv("SCOUT_URL", "http://0.0.0.0:8004/mcp")
PUBLISHER_URL = os.getenv("PUBLISHER_URL", "http://0.0.0.0:8005/mcp")


async def call_tool(url, tool, params):
    async with Client(url) as client:
        res = await client.call_tool(tool, params)
        return res.data


def run_scout(topic, city):
    return asyncio.run(call_tool(SCOUT_URL, "scout", {"topic": topic, "city": city}))


def run_publisher(payload):
    return asyncio.run(call_tool(PUBLISHER_URL, "publish_brief", {"payload": payload}))


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
