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
sims = 1
overtakes = 0
driver_dict = {}
for driver in drivers:
    driver_dict[driver.Name] = [0]*(len(drivers)+1)
for i in range(sims):
    drivers = setup.load_drivers("dev")
    num_laps = 5
    race = SimRace(drivers, track, rules, num_laps)
    race.qualify()
    for i in range(race.Laps):
        race.simulate_lap()
    for i,driver in enumerate(race.drivers_racing()):
        driver_dict[driver.Name][i] += 1
    for driver in [driver for driver in race.Drivers if driver.DNF]:
        driver_dict[driver.Name][len(drivers)] += 1
    if 'save_race' not in locals():
        save_race = race
    if race.leader().Name != "Mario":
        save_race = race
    overtakes += race.Overtakes
    
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

    plt.tight_layout()
    plt.show()

race_overview_plot(save_race)

driver_dict = dict(sorted(driver_dict.items(), key=lambda x: x[1][0], reverse=True))
for key, val in driver_dict.items():
    print(f"{key}: ", val)

print("Avg Overtakes: ", overtakes/sims)