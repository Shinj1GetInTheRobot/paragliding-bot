import json
import requests
import time

MIN_CONSECUTIVE_PREDICTIONS = 3
KMH_TO_KNOTS_CONV = 0.539957
DIR_RANGE = {   #compass bearing in degrees
    "min": 75,
    "max": 180
}
SPEED_RANGE = { #knots
    "min": 5,
    "max": 12
}
HOUR_RANGE = {  # 24hr time
    "min": 8,
    "max": 20
}

def try_check_conditions(api_key, location_id, location_name, num_days):
    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))

    wind_payload = {
        "forecasts": ["wind"],
        "days": num_days,
        "startDate": date,
    }
    ww_wind_rq_header = {
        "Content-Type": "application/json",
        "x-payload": json.dumps(wind_payload)
    }
    ww_wind_ep = f"https://api.willyweather.com.au/v2/{api_key}/locations/{location_id}/weather.json"

    response = requests.get(ww_wind_ep, headers=ww_wind_rq_header)
    response.raise_for_status()
    data = response.json()
    if data['location']['name'] != location_name:
        raise Exception(f"{location_name} different location to {data['location']['name']}?")

    weekly_forecast = data['forecasts']['wind']['days']
    if len(weekly_forecast) != num_days:
        raise Exception(f"Received forecast data for {len(weekly_forecast)} days, not {num_days}?")

    days = [day['dateTime'][:-9] for day in weekly_forecast if check_day(day['entries'])]
    return days

def check_day(day_forecast):
    consecutive_preds = 0
    for hour_pred in day_forecast:
        if looks_good(hour_pred):
            consecutive_preds += 1
        elif consecutive_preds > 0:
            consecutive_preds -= 1
        if MIN_CONSECUTIVE_PREDICTIONS <= consecutive_preds:
            return True
    return False

def looks_good(pred):
    if not in_range(HOUR_RANGE, parse_hr(pred['dateTime'])):
        return False
    if not in_range(DIR_RANGE, pred['direction']):
        return False
    if not in_range(SPEED_RANGE, pred["speed"] * KMH_TO_KNOTS_CONV):
        return False
    return True


def in_range(range_t, val):
    return range_t["min"] <= val <= range_t["max"]

def parse_hr(datetime_str):
    return int(datetime_str[11:13])