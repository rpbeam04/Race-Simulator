# Main Architecture

# Imports
#import gui
from sim import SimRace
import setup
import matplotlib.pyplot as plt
from pprint import pprint
from fastf1 import plotting as f1p

# Setup
"""
To run a race, you need a metadata file for basic information and then a
drivers csv file which will contain the sim info. Drivers files can be
different depending on the metadata file, ex: F1 specifies 3 tire compounds
versus other series having 1 or 2. Also, need a track file to change certain
parameters in the sim.
"""

f1p.setup_mpl()

#gui.launch()
drivers = setup.load_drivers("dev")
track = setup.load_track("dev")
rules = setup.load_rules("dev")

# Race Simulation
overtakes = 0
sims = 1000
driver_dict = {}
for driver in drivers:
    driver_dict[driver.Name] = [0]*(len(drivers)+1)
for i in range(sims):
    drivers = setup.load_drivers("dev")
    num_laps = 50
    race = SimRace(drivers, track, rules, num_laps)
    race.qualify()
    for _ in range(race.Laps):
        race.simulate_lap()
    overtakes += len(race.Overtakes)
    for k,driver in enumerate(race.drivers_racing()):
        driver_dict[driver.Name][k] += 1
    for driver in [driver for driver in race.Drivers if driver.DNF]:
        driver_dict[driver.Name][len(drivers)] += 1
    if i == 0:
        print("save race init")
        save_race = race
    elif len(race.Overtakes) > len(save_race.Overtakes):
        save_race = race
    if i % 50 == 0:
        print(i)
    
for key, val in driver_dict.items():
    assert sum(val) == sims

def race_overview_plot(race):
    # Create a figure and two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), gridspec_kw={'height_ratios': [2, 1]})

    # Plot for Gap to Mean
    for driver in race.Drivers:
        laps = range(1, len(driver.LapTimes) + 1)
        ax1.plot(laps, race.times_to_mean(driver))
    ax1.set_title("Intervals by Lap")
    ax1.legend([driver.Name for driver in race.Drivers], loc='upper left', bbox_to_anchor=(1, 1))
    ax1.set_xlabel("Lap")
    ax1.set_ylabel("Gap to Mean Laptime (sec)")

    # Plot for Position
    for driver in race.Drivers:
        laps = range(0, len(driver.LapPositions))
        ax2.plot(laps, driver.LapPositions)
    ax2.set_title("Race Position by Lap")
    ax2.set_xlabel("Lap")
    ax2.set_ylabel("Position")

    # Set axis limits
    xmin, xmax = ax2.get_xlim()
    ax1.set_xlim(xmin, xmax) 

    plt.tight_layout()
    plt.savefig("save_race.png")

race_overview_plot(save_race)

print(f"Save race: {len(save_race.Overtakes)} overtakes")
for overtake in save_race.Overtakes:
    overtake.print_overtake()

driver_dict = dict(sorted(driver_dict.items(), key=lambda x: x[1][0], reverse=True))
for key, val in driver_dict.items():
    print(f"{key}: ", val)

print(f"Avg Overtakes: {overtakes/sims}")