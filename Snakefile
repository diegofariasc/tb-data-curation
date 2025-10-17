# Snakefile

DATASETS = [
    ("https://api.worldbank.org/v2/en/indicator/SH.TBS.INCD?downloadformat=csv", "worldbank_tb"),
]

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
QUALITY_DIR = "data/quality"

URLS = {prefix: url for url, prefix in DATASETS}

rule all:
    input:
        expand(f"{PROCESSED_DIR}/{{prefix}}_long.csv", prefix=[p for _, p in DATASETS]),
        expand(f"{QUALITY_DIR}/quality_report_{{prefix}}.txt", prefix=[p for _, p in DATASETS])

rule acquire_data:
    output:
        zip_file = f"{RAW_DIR}/{{prefix}}.zip",
        csv_file = f"{RAW_DIR}/{{prefix}}.csv"
    params:
        url=lambda wildcards: URLS[wildcards.prefix]
    shell:
        """
        python src/acquire_data.py {params.url} {RAW_DIR} {wildcards.prefix}
        """

rule quality_assessment:
    input:
        f"{RAW_DIR}/{{prefix}}.csv"
    output:
        f"{QUALITY_DIR}/quality_report_{{prefix}}.txt"
    shell:
        """
        python src/quality_assessment.py {input} {QUALITY_DIR}
        """

rule clean_transform:
    input:
        f"{RAW_DIR}/{{prefix}}.csv"
    output:
        f"{PROCESSED_DIR}/{{prefix}}_long.csv"
    shell:
        """
        python src/clean_transform.py {input} {PROCESSED_DIR}
        """
