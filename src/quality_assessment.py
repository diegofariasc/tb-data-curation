import pandas as pd
import os
import sys


def detect_metadata_rows(
    csv_path: str, max_rows: int = 20, keyword: str = "Country Name"
) -> int:
    with open(csv_path, "r", encoding="utf-8") as f:
        for i in range(max_rows):
            line = f.readline()
            if keyword in line:
                return i
    return 0


def assess_data_quality(csv_path: str, output_dir: str = "data/quality") -> dict:
    os.makedirs(output_dir, exist_ok=True)
    skiprows = detect_metadata_rows(csv_path)
    df = pd.read_csv(csv_path, skiprows=skiprows, engine="python", on_bad_lines="skip")
    df.columns = [
        col.strip() if col.strip() != "" else f"column_{i}"
        for i, col in enumerate(df.columns)
    ]
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]

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

    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    report_path = os.path.join(output_dir, f"quality_report_{base_name}.txt")

    with open(report_path, "w", encoding="utf-8") as f:
        for key, val in report.items():
            f.write(f"{key}: {val}\n")

    print(f"Quality report saved to {report_path}")
    return report


if __name__ == "__main__":
    csv_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/quality"
    assess_data_quality(csv_path, output_dir)
