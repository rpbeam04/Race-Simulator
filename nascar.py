import csv
import random
import math
import os
import pandas as pd
from pprint import *

class Manufacturer:
    def __init__(self, name):
        self.Name = name

class Team:
    def __init__(self, name, manufacturer, crew_chief):
        self.Name = name
        self.Manufacturer = manufacturer
        self.Crew_Chief = crew_chief

class Driver:
    def __init__(self, name, car_number, team, skill_rating):
        self.Name = name
        self.Car_Number = car_number
        self.Team = team
        self.Skill_Rating = skill_rating

class Car:
    def __init__(self, driver, fuel, tire_wear):
        self.Driver = driver
        self.Fuel = fuel
        self.Tire_Wear = tire_wear

def read_csv(file_path):
    drivers = []
    teams = {}
    manufacturers = {}
    
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            manufacturer_name = row['manufacturer']
            if manufacturer_name not in manufacturers:
                manufacturers[manufacturer_name] = Manufacturer(manufacturer_name)

            team_name = row['team']
            if team_name not in teams:
                teams[team_name] = Team(team_name, manufacturers[manufacturer_name], row['crew_chief'])

            driver = Driver(row['driver'], int(row['car_number']), teams[team_name], float(row['skill_rating']))
            drivers.append(driver)

    return drivers

def simulate_lap(driver, quali_time, practice_time):
    consistency = random.normalvariate(0.2,0.3)  # Random consistency adjustment
    expected_time = 0.7 * quali_time + 0.3 * practice_time + consistency
    lap_time = expected_time # + driver.skill_rating * 0.1  # Adjust for skill

    return lap_time

def simulate_race(drivers, laps):
    race_results = []
    lap_times = []

    for lap in range(1, laps + 1):
        lap_results = []

        for i, driver in enumerate(drivers):
            if lap == 1:
                # Apply small time penalty for the start
                start_penalty = (i + 1) * 0.1
                lap_time = simulate_lap(driver, driver.Quali_Time, driver.Practice_Time) + start_penalty
            else:
                lap_time = simulate_lap(driver, driver.Quali_Time, driver.Practice_Time)

            lap_results.append((driver, lap_time))
            lap_times.append({'Driver': driver.Name, 'Lap': lap, 'LapTime': lap_time})
        
        standings = []
        for driver in drivers:
            standings.append((driver, sum([lap['LapTime'] for lap in lap_times])))
        standings = sorted(standings, key = lambda x: x[1])

        race_results.append([result[0] for result in standings])

    return race_results, lap_times

def print_race_results(race_results):
    print("Final Race Standings:")
    for i, driver in enumerate(race_results[-1]):
        print(f"{i + 1}. {driver.Name} - Car #{driver.Car_Number} - Team: {driver.Team.Name}")

def write_lap_times_to_csv(lap_times, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Driver', 'Lap', 'LapTime'])
        writer.writeheader()
        writer.writerows(lap_times)

test = True
if test:
    path = os.path.join("NASCAR Data", "driver_data.csv")
    drivers = read_csv(path)

    for driver in drivers:
        # Simulate qualifying and practice
        driver.Quali_Time = random.uniform(25, 30)
        driver.Practice_Time = random.uniform(26, 31)

    # Starting Order
    drivers = sorted(drivers, key=lambda x: x.Quali_Time)

    race_results, lap_times = simulate_race(drivers, laps=50)

    print_race_results(race_results)
    path = os.path.join("NASCAR Data", "lap_times.csv")
    write_lap_times_to_csv(lap_times, path)

    lap_data = pd.read_csv(path)

    pprint(lap_data.groupby("Driver")["LapTime"].agg(["sum","mean"]).sort_values("sum"))

    # Race_Results is bugged