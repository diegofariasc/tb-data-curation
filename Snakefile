# Snakefile

RAW_DIR = "data/raw"
QUALITY_DIR = "data/quality"
PROCESSED_DIR = "data/processed"

RAW_CSV = f"{RAW_DIR}/API_SH.TBS.INCD_DS2_en_csv_v2_9205.csv"
LONG_CSV = f"{PROCESSED_DIR}/API_SH.TBS.INCD_DS2_en_csv_v2_9205_long.csv"
QUALITY_REPORT = f"{QUALITY_DIR}/quality_report.txt"

rule all:
    input:
        LONG_CSV,
        QUALITY_REPORT

# Rule 1: Download data
rule acquire_data:
    output:
        RAW_CSV
    shell:
        """
        python src/acquire_data.py
        """

# Rule 2: evaluate quality
rule quality_assessment:
    input:
        RAW_CSV
    output:
        QUALITY_REPORT
    shell:
        """
        python src/quality_assessment.py
        """

# Rule 3: format and clean
rule clean_transform:
    input:
        RAW_CSV
    output:
        LONG_CSV
    shell:
        """
        python src/clean_transform.py
        """
