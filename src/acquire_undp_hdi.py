import os
import requests
from dotenv import load_dotenv

load_dotenv()

HDRO_API_KEY = os.getenv("HDRO_API_KEY")
BASE_URL = "https://hdrdata.org/api/CompositeIndices/query"


def acquire_undp_hdi(
    countries: str = "all",
    years: str = "2020,2021,2022",
    indicators: str = "HDI",
    dest_dir: str = "data/raw",
    prefix: str = "undp_hdi",
) -> str:
    os.makedirs(dest_dir, exist_ok=True)

    params = {
        "apikey": HDRO_API_KEY,
        "countryOrAggregation": countries,
        "year": years,
        "indicator": indicators,
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    csv_path = os.path.join(dest_dir, f"{prefix}.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"UNDP HDI dataset saved to {csv_path}")
    return csv_path


if __name__ == "__main__":
    acquire_undp_hdi()
