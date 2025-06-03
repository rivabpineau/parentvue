import os
from typing import Any, Dict, List

import pandas as pd
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
        return None

    # Convert to pandas DataFrame
    df = pd.DataFrame(json_data)

    try:
        csv_output = df.to_csv(index=False, encoding="utf-8", quoting=1)
        return csv_output
    except Exception:
        return None


def merge_csv_data_by_scrape_date(output_dir: str, output_name: str = "merged.csv") -> pd.DataFrame:
    """Merge all CSV files in ``output_dir`` into a single DataFrame."""

    csv_files = get_all_files_in_output_dir("csv", output_dir)
    dfs = [pd.read_csv(file) for file in csv_files]

    merged_df = pd.concat(dfs, ignore_index=True)

    output_file = os.path.join(output_dir, output_name)
    merged_df.to_csv(output_file, index=False)

    return merged_df
