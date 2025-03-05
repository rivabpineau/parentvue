import os
import json
from typing import Any, overload, Optional


@overload
def save_json_to_disk(data: Any, the_run_date: str, filename: str, directory: str) -> None: ...

@overload
def save_json_to_disk(data: Any, the_run_date: str) -> None: ...

@overload
def save_json_to_disk(data: Any, the_run_date: str) -> None: ...

def save_json_to_disk(data: Any, the_run_date: str, filename: Optional[str] = None, directory: Optional[str] = None) -> None:
    """
    Saves JSON data to disk.

    Args:
        the_run_date:
        data (Any): The JSON serializable data to save.
        filename (Optional[str]): The filename for the JSON file.
        directory (Optional[str]): The directory to save the file in.

    If `filename` and `directory` are not provided, they will be fetched from environment variables.
    """
    # Fetch defaults from environment variables if arguments are not provided
    filename = filename or os.getenv("GRADES_FILE_NAME", f"grades_{the_run_date}.json")
    final_filename = filename + "_" + the_run_date + ".json"

    directory = directory or os.getenv("OUTPUT_DIR", ".")

    filepath = os.path.join(directory, final_filename)
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists

    try:

        with open(filepath, mode="w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        print(f"[INFO] Successfully saved JSON to: {filepath}")

    except (IOError, OSError) as e:
        print(f"[ERROR] Failed to save JSON: {e}")

