# a quest to correlate the station id with station name
# because none of that data is in the csv file
# we will do this by trying to match known (1) number
# of samples and (2) first timestamp

import pandas as pd
import numpy as np

NUMSAMPLES = 250
FIRSTDAY = "2024-7-15"
# LASTDAY = "2025-06-25"
# we are looking for Cuyo EC-01 = 195790

#195795 = RL-01


df = pd.read_csv("data_full.csv")
df["event_time"] = pd.to_datetime(df["event_time"], utc=True, yearfirst=True, format="%Y-%m-%d %H:%M:%S UTC")

for station_id in df["station_id"].unique():
    station_data = df[df["station_id"] == station_id]
    if station_data["event_time"].min().strftime("%Y-%m-%d") == FIRSTDAY:
        print(f"Station ID: {station_id} matches {NUMSAMPLES} samples and first timestamp {FIRSTDAY}")
        print(station_data.head(1))  # Print the first row of the matching station data