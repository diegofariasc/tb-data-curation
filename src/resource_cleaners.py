import pandas as pd

from constants import EARLIEST_INCLUDED_START, INCLUDED_COUNTRY_CODES, LATEST_INCLUDED_YEAR, TB_TREATMENT_OUTCOME_FIELD_RENAME_MAP


def clean_undp_hdi(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean UNDP HDI dataset:
    - Extract ISO3 country code
    - Keep only 'country_code', 'year', and 'value' columns
    - Drop redundant columns for simplified, correlation-ready dataset
    """

    # Extract country code
    country_cols = [col for col in df.columns if "country" in col.lower()]
    if country_cols:
        col = country_cols[0]
        df["country_code"] = df[col].astype(str).str.split(" - ").str[0].str.strip()
        df.drop(columns=[col], inplace=True)

    # Keep only desired columns
    df = df[["country_code", "year", "value"]]
    df.insert(df.columns.get_loc("value"), "indicator", "hdi")

    # Ensure proper types
    df["year"] = df["year"].astype(int)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Filter countries and years
    df = df[
        (df["country_code"].isin(INCLUDED_COUNTRY_CODES))
        & (df["year"] >= EARLIEST_INCLUDED_START)
        & (df["year"] <= LATEST_INCLUDED_YEAR)
    ]

    return df

def clean_worldbank_dataset(df: pd.DataFrame, indicator_name) -> pd.DataFrame:
    """
    Clean World Bank dataset:
    - Keep only 'Country Code', year columns, and 'Indicator Name/Code'
    - Add 'indicator' column with given value
    - Rename columns to 'country_code', 'year', 'value'
    - Filter by INCLUDED_COUNTRY_CODES and years between EARLIEST_INCLUDED_START and LATEST_INCLUDED_YEAR
    """
        
    # Keep relevant columns
    year_cols = [col for col in df.columns if col.isdigit()]
    df = df[["Country Code"] + year_cols].copy()

    # Rename country column
    df = df.rename(columns={"Country Code": "country_code"})

    # Melt to long format
    df_long = df.melt(
        id_vars=["country_code"],
        value_vars=year_cols,
        var_name="year",
        value_name="value"
    )

    # Add indicator column before value
    df_long.insert(df_long.columns.get_loc("value"), "indicator", indicator_name)

    # Ensure proper types
    df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce").astype("Int64")
    df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")

    # Filter countries and years
    df_long = df_long[
        (df_long["country_code"].isin(INCLUDED_COUNTRY_CODES))
        & (df_long["year"] >= EARLIEST_INCLUDED_START)
        & (df_long["year"] <= LATEST_INCLUDED_YEAR)
    ]

    return df_long

def clean_worldbank_population(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = clean_worldbank_dataset(df, "population")
    df_clean["value"] = pd.to_numeric(df_clean["value"], errors="coerce").astype("Int64")
    return df_clean

def clean_worldbank_health_expenditure_gdp_percent(df: pd.DataFrame) -> pd.DataFrame:
    return clean_worldbank_dataset(df, "health_expenditure_gdp_percent")

def clean_worldbank_health_expenditure_usd(df: pd.DataFrame) -> pd.DataFrame:
    return clean_worldbank_dataset(df, "worldbank_health_expenditure_usd")

def clean_worldbank_tb_incidence(df: pd.DataFrame) -> pd.DataFrame:
    return clean_worldbank_dataset(df, "tb_incidence_per_hundred_thousand")

def clean_worldbank_gdp_per_capita_usd(df: pd.DataFrame) -> pd.DataFrame:
    return clean_worldbank_dataset(df, "gdp_per_capita_usd")

def clean_who_treatment_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean WHO treatment outcomes dataset:
    - Keep only relevant columns (country_code, year, treatment outcome metrics)
    - Rename columns to readable snake_case
    - Filter only included countries and years
    - Pivot to long format (country_code, year, indicator, value)
    """
    # Ensure consistent country code column
    if "iso3" in df.columns and "country_code" not in df.columns:
        df["country_code"] = df["iso3"]

    # Only keep columns that exist in the DataFrame
    existing_rename_keys = [col for col in TB_TREATMENT_OUTCOME_FIELD_RENAME_MAP.keys() if col in df.columns]
    if not existing_rename_keys:
        raise ValueError("No matching columns found between DataFrame and rename_map")

    cols_to_keep = ["country_code", "year"] + existing_rename_keys
    df_clean = df[cols_to_keep].copy()

    # Rename columns
    df_clean = df_clean.rename(columns=TB_TREATMENT_OUTCOME_FIELD_RENAME_MAP)

    # Convert year to numeric
    df_clean["year"] = pd.to_numeric(df_clean["year"], errors="coerce").astype("Int64")

    # Apply filters only if constants are defined
    if "INCLUDED_COUNTRY_CODES" in globals() and "EARLIEST_INCLUDED_START" in globals() and "LATEST_INCLUDED_YEAR" in globals():
        df_clean = df_clean[
            (df_clean["country_code"].isin(INCLUDED_COUNTRY_CODES))
            & (df_clean["year"] >= EARLIEST_INCLUDED_START)
            & (df_clean["year"] <= LATEST_INCLUDED_YEAR)
        ]

    # Pivot to long format
    id_vars = ["country_code", "year"]
    value_vars = [col for col in df_clean.columns if col not in id_vars]

    df_long = df_clean.melt(
        id_vars=id_vars,
        value_vars=value_vars,
        var_name="indicator",
        value_name="value"
    )

    # Drop missing or zero values
    df_long = df_long.dropna(subset=["value"])
    df_long = df_long[df_long["value"] != 0]

    return df_long

# Dictionary mapping resource name to cleaning function
cleaners = {
    "undp_hdi": clean_undp_hdi,
    "worldbank_tb_incidence": clean_worldbank_tb_incidence,
    "worldbank_population": clean_worldbank_population,
    "worldbank_gdp_per_capita_usd": clean_worldbank_gdp_per_capita_usd,
    "who_treatment_outcomes": clean_who_treatment_outcomes,
    "worldbank_health_expenditure_gdp_percent": clean_worldbank_health_expenditure_gdp_percent,
    "worldbank_health_expenditure_usd": clean_worldbank_health_expenditure_usd
}