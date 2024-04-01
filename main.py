# Main Architecture

# Imports
#import gui
from sim import SimRace
import setup
import matplotlib.pyplot as plt

# Setup
"""
To run a race, you need a metadata file for basic information and then a
drivers csv file which will contain the sim info. Drivers files can be
different depending on the metadata file, ex: F1 specifies 3 tire compounds
versus other series having 1 or 2. Also, need a track file to change certain
parameters in the sim.
"""

#gui.launch()
drivers = setup.load_drivers("dev")
track = setup.load_track("dev")
rules = setup.load_rules("dev")

# Race Simulation
race = SimRace(drivers, track, rules, 50)
race.qualify()
for driver in race.Drivers:
    print(f"{driver.Name}\t{driver.MeanTime}")
race.start()
for i in range(race.Laps-1):
    race.simulate_lap()
print("Overtakes: ", race.Overtakes)

plt.figure(figsize=(12,7))
for driver in race.Drivers:
    plt.plot(race.times_to_mean(driver))
plt.title("Race Simulation")
plt.legend([driver.Name for driver in race.Drivers], loc='upper left', bbox_to_anchor=(1, 1))
plt.xlabel("Lap")
plt.ylabel("Gap to Mean (sec)")
plt.show()