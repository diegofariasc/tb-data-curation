import pandas as pd
import os
import sys


def detect_metadata_rows(
    csv_path: str, keyword: str = "Country", max_rows: int = 20
) -> int:
    with open(csv_path, "r", encoding="utf-8") as f:
        for i in range(max_rows):
            if keyword in f.readline():
                return i
    return 0


def clean_and_transform(
    csv_path: str, output_dir: str = "data/processed"
) -> pd.DataFrame:
    os.makedirs(output_dir, exist_ok=True)
    skiprows = detect_metadata_rows(csv_path)
    df = pd.read_csv(csv_path, skiprows=skiprows, engine="python", on_bad_lines="skip")
    df.columns = [
        col.strip() if col.strip() != "" else f"column_{i}"
        for i, col in enumerate(df.columns)
    ]
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    metadata_cols = [col for col in df.columns if col not in numeric_cols]

    df_long = df.melt(
        id_vars=metadata_cols,
        value_vars=numeric_cols,
        var_name="Variable",
        value_name="Value",
    )
    try:
        df_long["Variable"] = pd.to_numeric(df_long["Variable"], errors="coerce")
    except:
        pass
    df_long = df_long.dropna(subset=["Value"])

    output_path = os.path.join(
        output_dir, os.path.basename(csv_path).replace(".csv", "_long.csv")
    )
    df_long.to_csv(output_path, index=False)
    print(f"Processed CSV saved to: {output_path}")
    return df_long


if __name__ == "__main__":
    csv_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/processed"
    clean_and_transform(csv_path, output_dir)
