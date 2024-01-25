import fastf1 as f1
import pandas as pd

def get_session_data(year: int, gp: str, sessions: list[str]):
    data_return: list = []
    for session in sessions: 
        session_data = f1.get_session(year,gp,session)
        session_data.load()
        gp = session_data.session_info["Meeting"]["Circuit"]["ShortName"]
        session = session_data.session_info["Name"]
        session_data.results.to_csv(fr"Data/{year}/{gp.replace(" ","-")}/{session.replace(" ","-")}-results.csv")
        session_data.laps.to_csv(fr"Data/{year}/{gp.replace(" ","-")}/{session.replace(" ","-")}-laps.csv")
        data_return.append(session_data)
    return data_return