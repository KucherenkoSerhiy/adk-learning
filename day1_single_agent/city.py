import datetime
import random
from zoneinfo import ZoneInfo


CITIES = ["Tokyo", "Berlin", "Girona", "Beijing", "San Francisco"]
CITY_TIMEZONES = {
        "Tokyo": "Asia/Tokyo",
        "Berlin": "Europe/Berlin",
        "Girona": "Europe/Madrid",
        "Beijing": "Asia/Shanghai",
        "San Francisco": "America/Los_Angeles"
    }

def get_current_time(city: str) -> dict:
    if city not in CITIES:
        return {"status": "error", "message": f"no data for {city}"}

    tz = ZoneInfo(CITY_TIMEZONES[city])
    current_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")

    return {
        "status": "success",
        "city": city,
        "time": current_time
    }

def get_forecast(city: str) -> dict:
    """mock-returns a one-word weather condition for the same cities you used above."""
    if city not in CITIES:
        return {"status": "error", "message": f"no data for {city}"}

    variants = ["Sunny", "Clouds", "Raining", "Raining cows"]
    weather = variants[random.randint(0, 3)]

    return {
        "status": "success",
        "city": city,
        "forecast": weather
    }

def convert_timezone(city_from: str, city_to: str, time: str) -> dict:
    """accepts time parameter only in ISO format"""
    if not city_from in CITIES or not city_to in CITIES:
        return {
            "status": "error",
            "city_from": city_from,
            "city_to": city_to,
            "time": time
        }

    naive_dt = datetime.datetime.fromisoformat(time)

    tz_from = ZoneInfo(CITY_TIMEZONES[city_from])
    aware_dt_from = naive_dt.replace(tzinfo=tz_from)

    tz_to = ZoneInfo(CITY_TIMEZONES[city_to])
    aware_dt_to = aware_dt_from.astimezone(tz_to)

    return {
        "status": "success",
        "city_from": city_from,
        "city_to": city_to,
        "time": time,
        "converted_time": aware_dt_to.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "offset_hours": (aware_dt_to - aware_dt_from).total_seconds() / 3600
    }