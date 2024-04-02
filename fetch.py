import fastf1 as f1
import pandas as pd
import os

def get_session_data(year: int, gp: str, sessions: list[str], save: bool = False):
    data_return: list = []
    for session in sessions:
        session_data = f1.get_session(year,gp,session)
        session_data.load()
        gp = session_data.session_info["Meeting"]["Circuit"]["ShortName"]
        session = session_data.session_info["Name"]
        if save:
            if not os.path.exists(fr"Data/{year}/{gp.replace(" ","-")}"):
                os.makedirs(fr"Data/{year}/{gp.replace(" ","-")}")
            session_data.results.to_csv(fr"Data/{year}/{gp.replace(" ","-")}/{session.replace(" ","-")}-results.csv")
            session_data.laps.to_csv(fr"Data/{year}/{gp.replace(" ","-")}/{session.replace(" ","-")}-laps.csv")
        data_return.append(session_data)
    return data_return

def get_practice_data(year: int, gp: str):
    data = get_session_data(year, gp, ["FP1","FP2","FP3"])

def get_qualifying_data(year: int, gp: str):
    return 0

def get_race_data():
    return 0