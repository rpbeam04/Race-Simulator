import numpy as np
from setup import SimDriver
from itertools import accumulate

class SimRace():
    def __init__(self, drivers: list, track: dict, rules: dict, laps: int) -> None:
        self.Drivers = drivers
        self.Track = track
        self.Rules = rules
        self.Laps = laps

    def qualify(self, display = False):
        self.Drivers.sort(key = lambda x: x.QualiTime)
        for i,driver in enumerate(self.Drivers):
            driver.StartPos = i+1
            driver.LapPositions.append(i+1)
        if display:
            print("Grid Order:")
            for i,driver in enumerate(self.Drivers):
                print(f"{i+1}. {driver.Name}\t{driver.QualiTime}")

    def start(self):
        for i,driver in enumerate(self.Drivers):
            laptime = driver.MeanTime + np.random.normal(0, driver.StdDev) + 6 + i*0.25 # + fuel + tire
            driver.LapTimes.append(laptime)
        self.Drivers.sort(key= lambda x: sum(x.LapTimes))
        for i, driver in enumerate(self.Drivers):
            driver.LapPositions.append(i+1)
    
    def simulate_lap(self):
        for i,driver in enumerate(self.Drivers):
            laptime = driver.MeanTime + np.random.normal(0, driver.StdDev) # + fuel + tire
            driver.LapTimes.append(laptime)
        self.Drivers.sort(key= lambda x: sum(x.LapTimes))
        for i, driver in enumerate(self.Drivers):
            driver.LapPositions.append(i+1)

    def times_to_leader(self, driver: SimDriver):
        cumulative_time = list(accumulate(driver.LapTimes))
        cumulative_leader = list(accumulate(self.Drivers[0].LapTimes))
        return np.subtract(cumulative_time, cumulative_leader)