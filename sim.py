import numpy as np
from setup import SimDriver
from itertools import accumulate

class SimRace():
    def __init__(self, drivers: list, track: dict, rules: dict, laps: int) -> None:
        self.Drivers: list['SimDriver'] = drivers
        self.Track: dict = track
        self.Rules: dict = rules
        self.Laps: int = laps
        self.Overtakes: int = 0

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
        for i,driver in enumerate(self.Drivers):
            check = True
            j = i+1
            while(check and j < len(self.Drivers)):
                if self.Drivers[j].RaceTime() + self.Rules["FollowTime"]*2 <= driver.RaceTime():
                    j += 1
                elif self.Drivers[j].RaceTime() <= driver.RaceTime() + self.Rules["FollowTime"]:
                    diff = driver.RaceTime() + self.Rules["FollowTime"] - self.Drivers[j].RaceTime()
                    self.Drivers[j].LapTimes[-1] += diff
                    j += 1
                else:
                    check = False
        self.Drivers.sort(key= lambda x: sum(x.LapTimes))
        for i, driver in enumerate(self.Drivers):
            driver.LapPositions.append(i+1)
    
    def simulate_lap(self):
        for i,driver in enumerate(self.Drivers):
            laptime = driver.MeanTime + np.random.normal(0, driver.StdDev) # + fuel + tire
            if self.Rules["Rules"]["DRS"]:
                if i > 0 and driver.RaceTime() <= self.Drivers[i-1].RaceTime(1) + 1:
                    laptime += 0.4
            driver.LapTimes.append(laptime)
        for i,driver in enumerate(self.Drivers):
            check = True
            j = i+1
            while(check and j < len(self.Drivers)):
                if self.Drivers[j].RaceTime() + self.Track["Attributes"]["OvertakingThreshold"] <= driver.RaceTime():
                    j += 1
                    self.Overtakes += 1
                elif self.Drivers[j].RaceTime() <= driver.RaceTime() + self.Rules["FollowTime"]:
                    diff = driver.RaceTime() + self.Rules["FollowTime"] - self.Drivers[j].RaceTime()
                    self.Drivers[j].LapTimes[-1] += diff
                    j += 1
                else:
                    check = False
        self.Drivers.sort(key= lambda x: sum(x.LapTimes))
        for i, driver in enumerate(self.Drivers):
            driver.LapPositions.append(i+1)

    def times_to_mean(self, driver: SimDriver):
        means = [0]*self.Laps
        for drive in self.Drivers:
            means = np.add(means, drive.LapTimes)
        means = np.true_divide(means, len(self.Drivers))
        cumulative_time = list(accumulate(driver.LapTimes))
        cumulative_mean = list(accumulate(means))
        return np.subtract(cumulative_time, cumulative_mean)