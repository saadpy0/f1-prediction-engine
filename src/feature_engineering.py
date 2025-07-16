import pandas as pd
import numpy as np
import os

def aggregate_lap_features(lap_file, output_file):
    df = pd.read_csv(lap_file)
    if df['LapTime'].dtype == object:
        df['LapTime'] = pd.to_timedelta(df['LapTime'], errors='coerce')
    df = df[df['LapTime'].notnull() & (df['LapTime'] > pd.Timedelta(0))]
    agg = df.groupby(['RaceName', 'Driver']).agg({
        'LapTime': [
            ('avg_lap_time', lambda x: x.mean().total_seconds()),
            ('fastest_lap_time', lambda x: x.min().total_seconds()),
            ('lap_time_std', lambda x: x.std().total_seconds() if len(x) > 1 else 0)
        ],
        'LapNumber': [('num_laps', 'count')],
        'Stint': [('num_stints', lambda x: x.nunique())],
        'Compound': [('most_used_compound', lambda x: x.mode().iloc[0] if not x.mode().empty else None)],
        'TyreLife': [('avg_tyre_life', 'mean')],
        'IsPersonalBest': [('num_personal_bests', 'sum')],
        'PitInTime': [('num_pitstops', lambda x: x.notnull().sum())],
        'Sector1Time': [('best_sector1', lambda x: pd.to_timedelta(x, errors='coerce').min().total_seconds())],
        'Sector2Time': [('best_sector2', lambda x: pd.to_timedelta(x, errors='coerce').min().total_seconds())],
        'Sector3Time': [('best_sector3', lambda x: pd.to_timedelta(x, errors='coerce').min().total_seconds())],
    })
    agg.columns = [col[1] for col in agg.columns]
    agg = agg.reset_index()
    agg.to_csv(output_file, index=False)
    print(f"Aggregated features saved to {output_file}")

if __name__ == "__main__":
    for year in range(2018, 2026):
        lap_file = f'data/merged/laps_{year}.csv'
        output_file = f'data/merged/lap_features_{year}.csv'
        if os.path.exists(lap_file):
            aggregate_lap_features(lap_file, output_file)
        else:
            print(f"Lap file for {year} not found, skipping.") 