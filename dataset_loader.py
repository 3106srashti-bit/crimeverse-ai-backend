import pandas as pd
from pathlib import Path

DATASET_DIR = Path(__file__).parent / "data" / "datasets"


def load_dataset(filename):
    file_path = DATASET_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    return pd.read_csv(
        file_path,
        on_bad_lines="skip"
    )