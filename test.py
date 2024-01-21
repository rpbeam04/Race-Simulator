import fastf1 as f1 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from pprint import * 

year = 2023
gp = "Jeddah"
session = "Qualifying"

def get_session_results(year: int, gp, session):
    session_data = f1.get_session(year,gp,session)
    session_data.load()
    session_data.results.to_csv(fr"Data/{year}/{gp}/{session}-results.csv")
    return session_data.results

test_session = get_session_results(year, gp, session)
pprint(test_session.describe())