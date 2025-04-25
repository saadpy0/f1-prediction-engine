import fastf1
from fastf1 import plotting
import pandas as pd

# Enable FastF1 caching to avoid redownloading data
fastf1.Cache.enable_cache('data/cache')

# Load the 2023 Monza (Italian GP) Race session
race = fastf1.get_session(2023, 'Monza', 'R')
race.load()

# Also load the qualifying session (optional for now, useful later)
qualifying = fastf1.get_session(2023, 'Monza', 'Q')
qualifying.load()

# Get all lap data from the race
laps = race.laps

# Show a sample of lap data
print("\n=== Laps Sample ===")
print(laps[['Driver', 'Team', 'LapTime', 'Compound', 'TyreLife']].head())

# Filter out laps with missing lap times (important for clean analysis)
valid_laps = laps[laps['LapTime'].notnull()]

# Find the fastest lap for each driver
fastest_laps = valid_laps.groupby('Driver').apply(
    lambda d: d.loc[d['LapTime'].idxmin()]
).reset_index(drop=True)

print("\n=== Fastest Lap for Each Driver ===")
print(fastest_laps[['Driver', 'LapNumber', 'LapTime']])

# Final race classification (our eventual target for prediction)
results = race.results
print("\n=== Race Results ===")
print(results[['Position', 'DriverNumber', 'Abbreviation', 'Time', 'Status']])

