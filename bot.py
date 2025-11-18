def try_check_conditions():
    # TO DO!
    return True

# stanwell_id = 3250
# wind_payload = {
#         "forecasts": ["wind"],
#         "days": 7,
#         "startDate": "2025-11-21"
# }
# ww_wind_rq_header = {
#     "Content-Type": "application/json",
#     "x-payload": json.dumps(wind_payload)
# }

# ww_wind_ep = f"https://api.willyweather.com.au/v2/{api_key}/locations/{stanwell_id}/weather.json"
#
# response = requests.get(ww_wind_ep, headers=ww_wind_rq_header)
#
# response.raise_for_status()
#
# print(response.json())