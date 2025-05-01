import pandas as pd
import os

def merge_season_data(year, data_type_folder, output_filename):
    folder_path = f"data/races/{data_type_folder}/"
    all_files = [f for f in os.listdir(folder_path) if f.startswith(str(year))]

    df_list = []

    for file in all_files:
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_csv(file_path)
            df_list.append(df)
        except Exception as e:
            print(f"❌ Failed to read {file_path}: {e}")

    if df_list:
        merged_df = pd.concat(df_list, ignore_index=True)
        merged_df.to_csv(f"data/merged/{output_filename}", index=False)
        print(f"✅ Merged {data_type_folder} for {year} into {output_filename}")
    else:
        print(f"⚠️ No files merged for {year} in {data_type_folder}")

if __name__ == "__main__":
    for year in range(2018, 2026):
        merge_season_data(year, "laps", f"laps_{year}.csv")
        merge_season_data(year, "results", f"results_{year}.csv")
