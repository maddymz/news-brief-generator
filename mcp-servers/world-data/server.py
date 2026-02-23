import os
import requests
from fastmcp import FastMCP
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

mcp = FastMCP("World Data server")

@mcp.tool
def search_news(query: str):
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {"error": "TAVILY_API_KEY not set"}

    client = TavilyClient(api_key=api_key)
    response = client.search(
        query=query,
        topic="news",
        search_depth="advanced",
        max_results=1,
    )
    results = response.get("results", [])
    if not results:
        return {"query": query, "headline": None}

    r = results[0]
    print(f"results of tavily search: {r}")
    return {
        "query":        query,
        "headline":     r.get("title"),
        "description":  r.get("content"),
        "source":       r.get("url"),
        "url":          r.get("url"),
        "published_at": r.get("published_date"),
    }
   
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

@mcp.tool
def get_weather(city: str, units: str = "metric") -> dict:
    weather_api_key = os.getenv("OPENWEATHER_API_KEY")
    if not weather_api_key:
        return {"error": "OPENWEATHER_API_KEY not set in environment"}

    params = {"q": city, "appid": weather_api_key, "units": units}

    try:
        response = requests.get(OPENWEATHER_API_URL, params=params, timeout=10)

        if response.status_code == 404:
            return {"error": f"City '{city}' not found."}
        elif response.status_code == 401:
            return {"error": "Invalid API Key."}

        response.raise_for_status()
        data = response.json()

        return {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "description": data.get("weather", [{}])[0].get("description"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "units": "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001)
    

