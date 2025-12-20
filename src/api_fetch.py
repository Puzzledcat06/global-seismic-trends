import requests
import pandas as pd
import time
import calendar
from datetime import date


BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

START_YEAR = 2020
MIN_MAGNITUDE = 4.5

today = date.today()

all_records = []

for year in range(START_YEAR, today.year + 1):

    for month in range(1, 13):

        if year == today.year and month > today.month:
            break

        last_day = calendar.monthrange(year, month)[1]

        if year == today.year and month == today.month:
            end_day = today.day
        else:
            end_day = last_day

        start_date = str(year) + "-" + str(month).zfill(2) + "-01"
        end_date = str(year) + "-" + str(month).zfill(2) + "-" + str(end_day).zfill(2)

        print("Fetching:", start_date, "to", end_date)

        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": MIN_MAGNITUDE
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print("Request failed for:", start_date, end_date)
            continue

        events = response.json().get("features", [])

        for event in events:

            properties = event.get("properties", {})
            geometry = event.get("geometry", {}).get("coordinates", [None, None, None])

            record = {
                "id": event.get("id"),
                "time": properties.get("time"),
                "updated": properties.get("updated"),
                "latitude": geometry[1],
                "longitude": geometry[0],
                "depth_km": geometry[2],
                "mag": properties.get("mag"),
                "magType": properties.get("magType"),
                "place": properties.get("place"),
                "status": properties.get("status"),
                "tsunami": properties.get("tsunami"),
                "sig": properties.get("sig"),
                "net": properties.get("net"),
                "nst": properties.get("nst"),
                "dmin": properties.get("dmin"),
                "rms": properties.get("rms"),
                "gap": properties.get("gap"),
                "magError": properties.get("magError"),
                "depthError": properties.get("depthError"),
                "magNst": properties.get("magNst"),
                "locationSource": properties.get("locationSource"),
                "magSource": properties.get("magSource"),
                "types": properties.get("types"),
                "ids": properties.get("ids"),
                "sources": properties.get("sources"),
                "type": properties.get("type")
            }

            all_records.append(record)


        time.sleep(1)

df = pd.DataFrame(all_records)
df.to_csv("data/raw/earthquakes_raw.csv", index=False)

print("Data saved successfully")
print("Total records:", len(df))
 