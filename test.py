import fastf1 as f1 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from pprint import * 
import fetch

year = 2023
gp = "Bahrain"
sessions = ["FP2"]

test_session = fetch.get_session_data(year, gp, sessions)

drivers = test_session[0].drivers
laps_df: pd.DataFrame = test_session[0].laps

driver_labels = []
speeds = []
for driver in drivers:
    driver_laps: pd.DataFrame = laps_df[laps_df["DriverNumber"] == driver]
    driver_laps.reset_index(inplace=True)
    driver_name = driver_laps.loc[0,"Driver"]
    driver_speed = max(driver_laps["SpeedST"])
    driver_labels.append(driver_name)
    speeds.append(driver_speed)

plt.bar(driver_labels, speeds)
plt.xlabel("Drivers")
plt.ylabel("Max Speed Trap (kmh)")
plt.title("Saudi Arabian GP FP2 Speed Traps")
plt.show()