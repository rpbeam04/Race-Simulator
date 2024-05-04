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
        self.CurrentLap: int = 1 # Lap of race currently on, not last completed lap

    def drivers_racing(self):
        return [driver for driver in self.Drivers if not driver.DNF]

    def qualify(self, display = False):
        self.Drivers.sort(key = lambda x: x.QualiTime)
        for i,driver in enumerate(self.Drivers):
            driver.StartPos = i+1
            driver.LapPositions.append(i+1)
        if display:
            print("Grid Order:")
            for i,driver in enumerate(self.Drivers):
                print(f"{i+1}. {driver.Name}\t{driver.QualiTime}")
    
    def simulate_lap(self):
        if self.CurrentLap > self.Laps:
            print("WARNING: Current lap number greater than race length.")
        start = True if self.CurrentLap == 1 else False
        self.sort_drivers()
        for i,driver in enumerate(self.drivers_racing()):
            if not driver.DNF:
                start_coef = 6+i*self.Rules["Rules"]["RolloffTime"] if start else 0
                if np.random.random() < driver.DNFRate/self.Laps:
                    driver.DNF = True
                laptime = driver.MeanTime + np.random.normal(0, driver.StdDev) + start_coef # + fuel + tire
                if self.Rules["Rules"]["DRS"] and not start:
                    if i > 0 and driver.RaceTime() <= self.Drivers[i-1].RaceTime(1) + 1:
                        laptime -= 0.3
                driver.LapTimes.append(laptime)
        
        drivers_racing = self.drivers_racing()
        new_drivers = [drivers_racing[0]]
        for driver in drivers_racing[1:]:
            if driver.RaceTime() + self.Track["Attributes"]["OvertakingThreshold"]

        self.sort_drivers()
        for i, driver in enumerate(self.drivers_racing()):
            driver.LapPositions.append(i+1)
        self.CurrentLap += 1

    def times_to_mean(self, driver: SimDriver):
        means = [0]*self.Laps
        racing_lap = [0]*self.Laps
        for drive in self.Drivers:
            for i,laptime in enumerate(drive.LapTimes):
                means[i] += laptime
                racing_lap[i] += 1
        for i,time in enumerate(means):
            means[i] = time/racing_lap[i]
        cumulative_time = list(accumulate(driver.LapTimes))
        cumulative_mean = list(accumulate(means))[:len(driver.LapTimes)]
        return np.subtract(cumulative_time, cumulative_mean)
    
    def leader(self):
        return self.drivers_racing()[0]
    
    def dnf_list(self):
        dnfs = [driver for driver in self.Drivers if driver.DNF]
        dnfs.sort(key= lambda x: sum(x.LapTimes), reverse=True)
        return dnfs

    def sort_drivers(self):
        self.Drivers.sort(key= lambda x: sum(x.LapTimes))
        olen = len(self.Drivers)
        dnfs = []
        for i,driver in enumerate(self.Drivers):
            if driver.DNF:
                dnf_d = self.Drivers.pop(i)
                dnfs.append(dnf_d)
                assert(len(self.Drivers) == olen - len(dnfs)), f"{olen}, {len(self.Drivers)}"
        dnfs.sort(key= lambda x: sum(x.LapTimes), reverse=True)
        self.Drivers = self.Drivers + dnfs
        assert(len(self.Drivers) == olen), f"F {len(self.Drivers)}, {olen}"