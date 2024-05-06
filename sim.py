import numpy as np
from setup import SimDriver
from itertools import accumulate

class SimRace():
    def __init__(self, drivers: list, track: dict, rules: dict, laps: int) -> None:
        self.Drivers: list['SimDriver'] = drivers
        self.Track: dict = track
        self.Rules: dict = rules
        self.Laps: int = laps
        self.Overtakes: list['Overtake'] = []
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
                if not driver.DNF:
                    driver.LapTimes.append(laptime)
        
        drivers_racing = self.drivers_racing()
        overtakes: list['Overtake'] = []
        overtake_thresh = self.Track["Attributes"]["OvertakingThreshold"] if self.CurrentLap != 1 else self.Track["Attributes"]["OvertakingThreshold"]/3
        for i, driver in enumerate(drivers_racing):
            for j, opponent in enumerate(drivers_racing[:i]):
                if driver.RaceTime() + overtake_thresh <= opponent.RaceTime():
                    overtakes.append(Overtake(driver, opponent, self.CurrentLap))

        for i, driver in enumerate(drivers_racing):
            attacks = [overtake for overtake in overtakes if (overtake.Overtaker == driver and not overtake.Complete)]
            attacks.sort(key= lambda x: drivers_racing.index(x.Overtaken), reverse=True)
            prev = [i]
            for attack in attacks:
                ind = drivers_racing.index(driver)
                new_ind = drivers_racing.index(attack.Overtaken)
                if new_ind + 1 in prev:
                    d = drivers_racing.pop(ind)
                    drivers_racing.insert(new_ind, d)
                    prev.append(new_ind)
                    attack.Complete = True
                else:
                    break
           
        self.Overtakes += [overtake for overtake in overtakes if overtake.Complete]

        for i, driver in enumerate(drivers_racing[:-1]):
            if driver.RaceTime() + self.Rules["FollowTime"] > drivers_racing[i+1].RaceTime():
                drivers_racing[i+1].LapTimes[-1] += driver.RaceTime() + self.Rules["FollowTime"] - drivers_racing[i+1].RaceTime() + np.random.uniform(0, 0.5*drivers_racing[i+1].StdDev)

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
        drivers = self.drivers_racing()
        olen = len(self.Drivers)
        dnfs = self.dnf_list()
        self.Drivers = drivers + dnfs
        assert(len(self.Drivers) == olen), f"F {len(self.Drivers)}, {olen}"

class Overtake():
    def __init__(self, overtaker, overtaken, lap):
        self.Overtaker: SimDriver = overtaker
        self.Overtaken: SimDriver = overtaken
        self.Lap: int = lap
        self.Complete: bool = False

    def print_overtake(self, advanced = False):
        print(f"{self.Overtaker.Name} on {self.Overtaken.Name}, Lap {self.Lap}")