import pandas as pd
import os

def engineer_results_features(results_file, output_file):
    df = pd.read_csv(results_file)
    # Positions gained: grid - finish (positive = gained places)
    df['positions_gained'] = df['GridPosition'] - df['Position']
    # is_winner: 1 if Position == 1 else 0
    df['is_winner'] = (df['Position'] == 1).astype(int)
    # podium: 1 if Position in [1,2,3] else 0
    df['podium'] = df['Position'].isin([1,2,3]).astype(int)
    # dnf: 1 if Status != 'Finished' else 0
    df['dnf'] = (df['Status'] != 'Finished').astype(int)
    # driver_team_combo: for encoding synergy
    df['driver_team_combo'] = df['Abbreviation'] + '_' + df['TeamName']
    # Save engineered features
    df.to_csv(output_file, index=False)
    print(f"Engineered results saved to {output_file}")

if __name__ == "__main__":
    for year in range(2018, 2026):
        results_file = f'data/merged/results_{year}.csv'
        output_file = f'data/merged/results_features_{year}.csv'
        if os.path.exists(results_file):
            engineer_results_features(results_file, output_file)
        else:
            print(f"Results file for {year} not found, skipping.") 