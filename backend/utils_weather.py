import requests
from fastapi import HTTPException

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def geocode_location(location: str):
    geo = requests.get(GEOCODE_URL, params={"name": location, "count": 1}, timeout=10).json()
    results = geo.get("results")
    if not results:
        raise HTTPException(status_code=404, detail="Location not found")
    return results[0]["latitude"], results[0]["longitude"]


def fetch_current_weather(location: str):
    lat, lon = geocode_location(location)
    data = requests.get(FORECAST_URL, params={
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
    }, timeout=10).json()
    current = data.get("current", {})
    return {
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "rainfall": current.get("precipitation"),
        "wind_speed": current.get("wind_speed_10m"),
    }
