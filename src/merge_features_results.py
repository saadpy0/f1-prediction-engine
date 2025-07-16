import pandas as pd
import os

def merge_features_and_results(year, features_dir='data/merged', output_dir='data/merged'):
    results_file = os.path.join(features_dir, f'results_features_{year}.csv')
    lap_features_file = os.path.join(features_dir, f'lap_features_{year}.csv')
    if not os.path.exists(results_file) or not os.path.exists(lap_features_file):
        print(f"Missing file for {year}, skipping.")
        return None
    results = pd.read_csv(results_file)
    lap_features = pd.read_csv(lap_features_file)
    # Merge on RaceName and Abbreviation (driver key)
    merged = pd.merge(results, lap_features, how='left', left_on=['RaceName', 'Abbreviation'], right_on=['RaceName', 'Driver'])
    merged['Year'] = year
    merged.to_csv(os.path.join(output_dir, f'merged_{year}.csv'), index=False)
    print(f"Merged data saved to {output_dir}/merged_{year}.csv")
    return merged

def merge_all_years(start=2018, end=2025, features_dir='data/merged', output_file='data/merged/f1_model_data.csv'):
    all_years = []
    for year in range(start, end+1):
        merged = merge_features_and_results(year, features_dir, features_dir)
        if merged is not None:
            all_years.append(merged)
    if all_years:
        full = pd.concat(all_years, ignore_index=True)
        full.to_csv(output_file, index=False)
        print(f"All years merged and saved to {output_file}")
    else:
        print("No data to merge.")

if __name__ == "__main__":
    merge_all_years() 