import pandas as pd
import os
import sys
from resource_cleaners import cleaners

def detect_metadata_rows(csv_path: str, keyword: str = "Country", max_rows: int = 20) -> int:
    """
    Detect the number of initial metadata rows to skip.
    Args:
        csv_path: Path to CSV file
        keyword: Column keyword to detect header
        max_rows: Maximum rows to scan
    Returns:
        Number of rows to skip
    """
    with open(csv_path, "r", encoding="utf-8") as f:
        for i in range(max_rows):
            if keyword in f.readline():
                return i
    return 0

def clean_and_transform(csv_path: str, output_dir: str = "data/processed", resource_name: str = None, pivot = False) -> pd.DataFrame:
    """
    Clean and transform a dataset to long format.
    Applies resource-specific cleaning if available.

    Args:
        csv_path: Path to CSV file
        output_dir: Directory to save processed CSV
        resource_name: Optional resource key to apply custom cleaning

    Returns:
        Pandas DataFrame in long format
    """
    os.makedirs(output_dir, exist_ok=True)
    skiprows = detect_metadata_rows(csv_path)
    
    # Load CSV
    df = pd.read_csv(csv_path, skiprows=skiprows, engine="python", on_bad_lines="skip")
    df.columns = [col.strip() if col.strip() != "" else f"column_{i}" for i, col in enumerate(df.columns)]
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]

    if resource_name in cleaners:
        df = cleaners[resource_name](df)
   
    # Save output
    output_path = os.path.join(output_dir, os.path.basename(csv_path).replace(".csv", "_long.csv"))
    df.to_csv(output_path, index=False)
    print(f"Processed CSV saved to: {output_path}")
    return df

if __name__ == "__main__":
    csv_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/processed"
    resource_name = sys.argv[3] if len(sys.argv) > 3 else None
    clean_and_transform(csv_path, output_dir, resource_name)