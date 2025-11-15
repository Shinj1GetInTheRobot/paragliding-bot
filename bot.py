import json
import requests
import os

stanwell_id = 3250

wind_payload = {
        "forecasts": ["wind"],
        "days": 7,
        "startDate": "2025-11-21"
}
ww_wind_rq_header = {
    "Content-Type": "application/json",
    "x-payload": json.dumps(wind_payload)
}

if __name__ == "__main__":
    # Read API Key from auth.txt
    with open("auth.txt") as f:
        api_key = f.read()[10:]
        if api_key == "" or api_key == "?":
            print("ERROR: Please input API_KEY in auth.txt")
            print("EXITING...")
            exit(0)

    data_st = os.stat("./.data")

    print(data_st.st_mtime)

    with open(".data") as data:
        pass

    # ww_wind_ep = f"https://api.willyweather.com.au/v2/{api_key}/locations/{stanwell_id}/weather.json"
    #
    # response = requests.get(ww_wind_ep, headers=ww_wind_rq_header)
    #
    # response.raise_for_status()
    #
    # print(response.json())
