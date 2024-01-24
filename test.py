import fastf1 as f1 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from pprint import * 

year = 2023
gp = "Bahrain"
session = "FP2"

def get_session_results(year: int, gp, session):
    session_data = f1.get_session(year,gp,session)
    session_data.load()
    gp = session_data.session_info["Meeting"]["Circuit"]["ShortName"]
    session = session_data.session_info["Name"]
    session_data.results.to_csv(fr"Data/{year}/{gp.replace(" ","-")}/{session.replace(" ","-")}-results.csv")
    session_data.laps.to_csv(fr"Data/{year}/{gp.replace(" ","-")}/{session.replace(" ","-")}-laps.csv")
    return session_data

test_session = get_session_results(year, gp, session)
pprint(test_session.car_data.head())
pprint(test_session.total_laps)