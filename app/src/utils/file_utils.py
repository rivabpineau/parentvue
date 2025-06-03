import os
import json
from typing import Any, List, Dict, Literal

import pandas as pd


def save_data(
    data: List[Dict[str, Any]],
    the_run_date: str,
    output_data_format: Literal["json", "csv", "both"] = "json",
    filename: str = "grades",
    directory: str = ".",
) -> dict[str, str]:
    """Save structured data to disk.

    The function writes ``data`` to ``directory`` using ``filename`` and the
    provided ``the_run_date``. It returns a dictionary containing the paths to
    any files that were written so tests can easily assert on their existence.
    """

    os.makedirs(directory, exist_ok=True)

    json_filepath = os.path.join(directory, f"{filename}_{the_run_date}.json")
    csv_filepath = os.path.join(directory, f"{filename}_{the_run_date}.csv")

    paths: dict[str, str] = {}

    if output_data_format in ["json", "both"]:
        with open(json_filepath, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        paths["json"] = json_filepath

    if output_data_format in ["csv", "both"]:
        df = pd.DataFrame(data)
        df.to_csv(csv_filepath, index=False, encoding="utf-8", quoting=1)
        paths["csv"] = csv_filepath

    return paths

def get_all_files_in_output_dir(
    the_file_type: Literal["csv", "json"], folder_path: str
) -> list[str]:
    """Return a list of file paths for the requested type within ``folder_path``."""

    extension = f".{the_file_type}"
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(extension)]
    return files
