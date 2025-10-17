import pandas as pd
import os


def detect_metadata_rows(
    csv_path: str, max_rows: int = 20, keyword: str = "Country Name"
) -> int:
    """
    Detects how many top rows are metadata by searching for the header keyword.
    Returns the number of rows to skip.
    """
    with open(csv_path, "r", encoding="utf-8") as f:
        for i in range(max_rows):
            line = f.readline()
            if keyword in line:
                return i
    return 0  # fallback if not found


def assess_data_quality(csv_path: str, output_dir: str = "data/quality") -> dict:
    os.makedirs(output_dir, exist_ok=True)

    skiprows = detect_metadata_rows(csv_path)

    # Read CSV with python engine, skip bad lines
    df = pd.read_csv(csv_path, skiprows=skiprows, engine="python", on_bad_lines="skip")

    # Strip column names
    df.columns = [
        col.strip() if col.strip() != "" else f"column_{i}"
        for i, col in enumerate(df.columns)
    ]
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]

    # Convert numeric columns automatically
    for col in df.columns[skiprows:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    report = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": df.isna().sum().sum(),
        "duplicate_rows": df.duplicated().sum(),
        "columns_with_missing": df.columns[df.isna().any()].tolist(),
        "column_types": df.dtypes.astype(str).to_dict(),
    }

    report_path = os.path.join(output_dir, "quality_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        for key, val in report.items():
            f.write(f"{key}: {val}\n")

    print(f"Quality report saved to {report_path}")
    return report


if __name__ == "__main__":
    csv_path = "data/raw/API_SH.TBS.INCD_DS2_en_csv_v2_9205.csv"
    assess_data_quality(csv_path)
