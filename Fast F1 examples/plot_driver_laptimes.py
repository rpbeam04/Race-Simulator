"""Driver Laptimes Scatterplot
==============================

Plot a driver's lap times in a race, with color coding for the compounds.
"""

import seaborn as sns
from matplotlib import pyplot as plt

import fastf1
import fastf1.plotting


# The misc_mpl_mods option enables minor grid lines which clutter the plot
fastf1.plotting.setup_mpl(misc_mpl_mods=False)

###############################################################################
# Load the race session.

race = fastf1.get_session(2024, "Jeddah", 'Q')
race.load()

###############################################################################
# Get all the laps for a single driver.
# Filter out slow laps as they distort the graph axis.

drivers_plot = ["ALO","VER","PER","LEC","BEA"]
dp_laps = []
for driver in drivers_plot:
    data = race.laps.pick_driver(driver).pick_quicklaps(1.09).reset_index()
    dp_laps.append(data)

###############################################################################
# Make the scattterplot using lap number as x-axis and lap time as y-axis.
# Marker colors correspond to the compounds used.
# Note: as LapTime is represented by timedelta, calling setup_mpl earlier
# is required.

fig, ax = plt.subplots(figsize=(8, 8))

driver_colors = {abv: fastf1.plotting.DRIVER_COLORS[driver] for abv,
                 driver in fastf1.plotting.DRIVER_TRANSLATE.items()}
driver_colors["OCO"] = "#ff5bd7"
driver_colors["GAS"] = "#cd1b97"
driver_colors["ZHO"] = "#32B232"
driver_colors["BOT"] = "#62F262"

for laps in dp_laps:
    sns.scatterplot(data=laps,
                    x="LapNumber",
                    y="LapTime",
                    ax=ax,
                    hue="Driver",
                    palette=driver_colors,
                    s=50,
                    linewidth=0,
                    legend='auto')
# sphinx_gallery_defer_figures

###############################################################################
# Make the plot more aesthetic.
ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time")

# The y-axis increases from bottom to top by default
# Since we are plotting time, it makes sense to invert the axis
ax.invert_yaxis()
plt.suptitle("Bahrain 2024 FP2 Laptimes")

# Turn on major grid lines
plt.grid(color='w', which='major', axis='both')
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()