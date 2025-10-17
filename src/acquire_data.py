from utils.io_utils import download_file, extract_from_zip, read_csv_metadata
from utils.constants import WB_TB_URL


def acquire_worldbank_tb():
    _, zip_content = download_file(WB_TB_URL, filename="worldbank_tb.zip")
    extracted_files = extract_from_zip(
        zip_content, include=["API_SH.TBS.INCD"], exclude=["Metadata"]
    )
    if not extracted_files:
        raise Exception("No CSV extracted from ZIP")
    read_csv_metadata(extracted_files[0], skiprows=4, source_name="worldbank_tb")


if __name__ == "__main__":
    acquire_worldbank_tb()
