import pandas as pd
from typing import List, Dict, Any
from utils.file_utils import get_all_files_in_output_dir

def json_to_csv_pandas(json_data: List[Dict[str, Any]]) -> str | None:
    """
    Converts a list of dictionaries (JSON) to CSV format using pandas and prints the output.

    Args:
        json_data (List[Dict[str, Any]]): The JSON data to convert.

    Returns:
        None (prints CSV output)
    """
    if not json_data:
        print("[ERROR] No data provided to convert.")
        return None

    # Convert to pandas DataFrame
    df = pd.DataFrame(json_data)

    try:
        # Save to CSV with proper formatting
        csv_output = df.to_csv(index=False, encoding="utf-8", quoting=1)
        return csv_output
    except Exception as e:
        print(f"[ERROR] Failed to convert JSON to CSV: {e}")
        return None


def merge_csv_data_by_scrape_date():

    csv_files, output_file = get_all_files_in_output_dir("csv")

    # Load all CSVs into a list of dataframes
    dfs = [pd.read_csv(file) for file in csv_files]

    # Concatenate all dataframes into one
    merged_df = pd.concat(dfs, ignore_index=True)

    # Save the merged CSV file
    merged_df.to_csv(output_file, index=False)

    return merged_df