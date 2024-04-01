import fetch
import os
import pandas as pd
import json

class SimDriver():
    def __init__(self, name: str, number: int) -> None:
        self.Name = name
        self.Number = number
        self.LapTimes: list = []
        self.LapPositions: list = []

    def RaceTime(self, i=0):
        if i > 0:
            return sum(self.LapTimes[:-i])
        return sum(self.LapTimes)

def load_presets(_type: str):
    return os.listdir(fr"{_type.capitalize()}")

def match_preset(ident: str, _type: str):
    preset_files = load_presets(_type)

def load_drivers(method: str, ident: str | None = None):
    """
    Methods: csv, preset, fetch, custom, dev
    """
    if method == "preset":
        return match_preset(ident)
    elif method == "dev":
        data = pd.read_csv("Drivers/drivertest.csv").loc[:9]
        drivers = []
        for _,row in data.iterrows():
            driver = SimDriver(row["Name"], row["Number"])
            for item in data.columns:
                setattr(driver, item, row[item])
            drivers.append(driver)
        minP = min([driver.PracticeTime for driver in drivers])
        minQ = min([driver.QualiTime for driver in drivers])
        for driver in drivers:
            driver.PracticeDelta = driver.PracticeTime - minP
            driver.QualiDelta = driver.QualiTime - minQ
            driver.MeanTime = driver.PracticeTime + 0.5*(driver.QualiDelta - driver.PracticeDelta)
        return drivers
    else:
        ValueError("Unable to load drivers.")

def load_track(method: str):
    return json.load(open("Tracks/Circuit.json","r"))

def load_rules(method: str):
    return json.load(open("Rules/Formula1.json","r"))