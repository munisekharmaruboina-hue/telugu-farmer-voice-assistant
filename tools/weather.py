import requests


def rain_forecast(lat=14.4426, lon=79.9865, day_offset=1):
    """day_offset: 0 = today, 1 = tomorrow. Default location is about Nellore."""
    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "daily": "precipitation_sum,precipitation_probability_max",
            "timezone": "Asia/Kolkata",
            "forecast_days": 8,
        },
        timeout=15,
    )
    if not resp.ok:
        print("Weather error", resp.status_code, resp.text)
        return None
    daily = resp.json()["daily"]
    return {
        "date": daily["time"][day_offset],
        "rain_mm": daily["precipitation_sum"][day_offset],
        "rain_chance_pct": daily["precipitation_probability_max"][day_offset],
    }


if __name__ == "__main__":
    print(rain_forecast())