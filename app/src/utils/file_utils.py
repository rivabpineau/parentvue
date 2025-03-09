import os
import json
import pandas as pd
from typing import Any, Optional, List, Dict, Literal


def save_data(
        data: List[Dict[str, Any]],
        the_run_date: str,
        output_data_format: Literal["json", "csv", "both"] = "json",
        filename: Optional[str] = None,
        directory: Optional[str] = None
) -> None:
    """
    Saves data to disk in JSON, CSV, or both formats.

    Args:
        data (List[Dict[str, Any]]): The structured data to save.
        the_run_date (str): Date used for naming files.
        output_data_format (str): The format to save the data in. Options: 'json', 'csv', 'both'. Default is 'json'.
        filename (Optional[str]): Base filename (without extension). Defaults to environment variable or 'grades'.
        directory (Optional[str]): Directory to save files. Defaults to environment variable or current directory.

    Returns:
        None
    """
    try:
        # Set defaults from environment variables if not provided
        filename = filename or os.getenv("GRADES_FILE_NAME")
        directory = directory or os.getenv("OUTPUT_DIR")

        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Generate filenames
        json_filepath = os.path.join(directory, f"{filename}_{the_run_date}.json")
        csv_filepath = os.path.join(directory, f"{filename}_{the_run_date}.csv")

        # Save as JSON
        if output_data_format in ["json", "both"]:
            with open(json_filepath, mode="w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)
            print(f"[INFO] Successfully saved JSON to: {json_filepath}")

        # Save as CSV
        if output_data_format in ["csv", "both"]:
            df = pd.DataFrame(data)
            df.to_csv(csv_filepath, index=False, encoding="utf-8", quoting=1)
            print(f"[INFO] Successfully saved CSV to: {csv_filepath}")

    except (IOError, OSError, ValueError) as e:
        print(f"[ERROR] Failed to save data: {e}")

def get_all_files_in_output_dir(the_file_type: Literal["csv", "json"] ) -> tuple[list[str], str | None] | None:

    folder_path = os.getenv("OUTPUT_DIR")

    files = None

    if the_file_type == "csv":
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
    elif the_file_type == "json":
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

    if not files:
        print(f"No {the_file_type} files found in the directory.")
        return None


    return files, folder_path
