import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

HDRO_API_KEY = os.getenv("HDRO_API_KEY")
BASE_URL = "https://hdrdata.org/api/CompositeIndices/query"


def get_countries():
    url = f"https://hdrdata.org/api/Metadata/Countries?apikey={HDRO_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    countries = [c["code"] for c in response.json()]
    return countries


def get_hdi_indicator_code():
    url = f"https://hdrdata.org/api/Metadata/Indicators?apikey={HDRO_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    indicators = response.json()
    for ind in indicators:
        if "Human Development Index" in ind["name"]:
            return ind["code"]
    raise ValueError("HDI indicator code not found in metadata.")


def generate_years_string(start_year: int = 2000, end_year: int = 2024) -> str:
    return ",".join(str(year) for year in range(start_year, end_year + 1))


def acquire_undp_hdi(
    years: str = generate_years_string(1990, 2024),
    dest_dir: str = "data/raw",
    prefix: str = "undp_hdi",
) -> str:
    os.makedirs(dest_dir, exist_ok=True)

    countries = get_countries()
    indicator_code = get_hdi_indicator_code()

    all_data = []
    batch_size = 20

    for i in range(0, len(countries), batch_size):
        batch_countries = countries[i : i + batch_size]
        params = {
            "apikey": HDRO_API_KEY,
            "countryOrAggregation": ",".join(batch_countries),
            "year": years,
            "indicator": indicator_code,
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            all_data.extend(data)

    if not all_data:
        raise ValueError(
            "No data returned from the API. Check indicator and countries."
        )

    df = pd.DataFrame(all_data)
    csv_path = os.path.join(dest_dir, f"{prefix}.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"UNDP HDI dataset saved to {csv_path}")
    return csv_path


if __name__ == "__main__":
    acquire_undp_hdi()
