import fastf1 as f1
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from pprint import * 
import fetch as fetch

year = 2024
gp = "Australia"
sessions = ["FP1","FP2","FP3","Q","R"]

test_session = fetch.get_session_data(year, gp, sessions)
fp1 = test_session[0]