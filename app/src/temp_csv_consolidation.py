import pandas as pd
import os

def consolidate_csvs(folder_path):
    """
    Reads all CSV files in the given folder, consolidates them,
    and saves the output as 'all_grades.csv' in the same folder.

    adding csv appender. takes a list of csvs and performs a append
    merge creating on csv with all of the data.
    Parameters:
        folder_path (str): The directory containing CSV files.

    Returns:
        pd.DataFrame: The consolidated DataFrame.
    """
    csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the directory.")
        return None

    df_list = []
    for file in csv_files:
        try:
            df = pd.read_csv(file, encoding="utf-8", dtype=str)  # Read as string to prevent conversion issues
            df_list.append(df)
        except pd.errors.EmptyDataError:
            print(f"Skipping empty file: {file}")
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not df_list:
        print("No valid CSV files to merge.")
        return None

    # Merge all CSVs and drop duplicates
    merged_df = pd.concat(df_list, ignore_index=True).drop_duplicates()

    # Save to 'all_grades.csv'
    output_file = os.path.join(folder_path, "03-03-2025_all_grades.csv")
    merged_df.to_csv(output_file, index=False)

    print(f" Consolidated file saved as: {output_file}")
    return merged_df



folder_path = "/Users/bp_home/PycharmProjects/parentvue/database/"
consolidate_csvs(folder_path)