from dataclasses import dataclass
from dotenv import load_dotenv
import os

@dataclass
class Config:
    pvue_url: str
    username: str
    password: str
    data_output_format: str = "json"
    grades_file_name: str = "grades"
    output_dir: str = "."

def load_config(env_file: str | None = None) -> "Config":
    """Load configuration from environment variables or an optional dotenv file."""
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv(verbose=True)
    return Config(
        pvue_url=os.environ.get("PVUE_URL", ""),
        username=os.environ.get("PVUE_USERNAME", ""),
        password=os.environ.get("PVUE_PASS", ""),
        data_output_format=os.environ.get("DATA_OUTPUT_FORMAT", "json"),
        grades_file_name=os.environ.get("GRADES_FILE_NAME", "grades"),
        output_dir=os.environ.get("OUTPUT_DIR", "."),
    )
