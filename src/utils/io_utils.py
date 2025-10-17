import os
import io
import zipfile
import requests
import pandas as pd
from .metadata_utils import hash_file, log_metadata


def download_file(url: str, dest_dir: str = "data/raw", filename: str | None = None):
    """
    Generic downloader for any file (CSV, ZIP, JSON, etc.).
    Returns the path to the saved file and the raw content.
    """
    os.makedirs(dest_dir, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    # Infer filename if not provided
    if not filename:
        filename = url.split("/")[-1] or "downloaded_file"
        if "?" in filename:
            filename = filename.split("?")[0]

    output_path = os.path.join(dest_dir, filename)
    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"File downloaded to {output_path}")
    return output_path, response.content


def extract_from_zip(
    zip_content: bytes,
    dest_dir: str = "data/raw",
    include: list[str] | None = None,
    exclude: list[str] | None = None,
):
    """
    Extract files from a ZIP with optional include/exclude filters.
    Returns list of extracted file paths.
    """
    os.makedirs(dest_dir, exist_ok=True)
    extracted_files = []

    with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
        for name in z.namelist():
            if include and not any(pat in name for pat in include):
                continue
            if exclude and any(pat in name for pat in exclude):
                continue

            dest_path = os.path.join(dest_dir, os.path.basename(name))
            with z.open(name) as src, open(dest_path, "wb") as tgt:
                tgt.write(src.read())
            extracted_files.append(dest_path)
            print(f"Extracted: {dest_path}")

    if not extracted_files:
        print("No files extracted. Check filters or ZIP contents")

    return extracted_files


def read_csv_metadata(csv_path: str, skiprows: int = 0, source_name: str = "generic"):
    """
    Reads a CSV file, counts rows, computes hash, and logs metadata.
    """
    df = pd.read_csv(csv_path, skiprows=skiprows)
    rows = len(df)
    file_hash = hash_file(csv_path)
    log_metadata(source_name, csv_path, rows, file_hash)
    print(f"Registered: {os.path.basename(csv_path)} | Rows={rows}, Hash={file_hash}")
    return df, file_hash, rows
