from clean_transform import detect_metadata_rows
from utils.io_utils import download_file, extract_from_zip, read_csv_metadata
import sys
import os


def acquire_dataset(url: str, dest_dir: str, prefix: str) -> str:
    """
    Downloads a ZIP from `url`, extracts CSV files (excluding Metadata),
    stores them in `dest_dir`, and returns the path of the main CSV.
    """
    os.makedirs(dest_dir, exist_ok=True)

    # Download ZIP
    zip_name = f"{prefix}.zip"
    _, zip_content = download_file(url, dest_dir=dest_dir, filename=zip_name)

    # Extract CSVs from ZIP
    extracted_files = extract_from_zip(
        zip_content, include=["API"], exclude=["Metadata"], dest_dir=dest_dir
    )
    if not extracted_files:
        raise Exception("No CSV extracted from ZIP")

    # Pick the first extracted CSV as the main dataset
    main_csv = extracted_files[0]

    # Rename CSV to fixed name
    fixed_csv = os.path.join(dest_dir, f"{prefix}.csv")
    os.rename(main_csv, fixed_csv)

    # Read metadata
    skiprows = detect_metadata_rows(fixed_csv)
    read_csv_metadata(fixed_csv, skiprows=skiprows, source_name=prefix)

    return main_csv


if __name__ == "__main__":
    url = sys.argv[1]
    dest_dir = sys.argv[2]
    prefix = sys.argv[3]
    csv_path = acquire_dataset(url, dest_dir, prefix)
    print(f"Acquired dataset: {csv_path}")
