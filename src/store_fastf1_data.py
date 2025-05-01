import fastf1
import pandas as pd


fastf1.Cache.enable_cache('data/cache')

def store_race_data(year, gp_name):
    try:
        race = fastf1.get_session(year, gp_name, 'R')
        race.load()

        race_info = race.event
        race_name = race_info.EventName
        race_country = race_info.Country
        race_round = race_info.RoundNumber


        laps = race.laps
        if not laps.empty:
            laps["RaceName"] = race_name
            laps["Country"] = race_country
            laps["Round"] = race_round

            laps.to_csv(f"data/races/laps/{year}_{gp_name}_laps.csv", index=False)

        results = race.results
        if results is not None and not results.empty:
            results["RaceName"] = race_name
            results["Country"] = race_country
            results["Round"] = race_round

            results.to_csv(f"data/races/results/{year}_{gp_name}_results.csv", index=False)


        print(f"Saved {gp_name} {year} race data successfully.")
    except Exception as e:
        print(f"❌ Failed {year} - {gp_name}: {e}")


store_race_data(2025,'Pre-Season Testing')
