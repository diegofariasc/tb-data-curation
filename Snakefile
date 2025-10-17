# Snakefile

DATASETS = [
    ("https://api.worldbank.org/v2/en/indicator/SH.TBS.INCD?downloadformat=csv", "worldbank_tb"),
    ("undp_hdi_api", "undp_hdi")  # Handled via API key
]

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
QUALITY_DIR = "data/quality"

URLS = {prefix: url for url, prefix in DATASETS}

rule all:
    input:
        expand(f"{PROCESSED_DIR}/{{prefix}}_long.csv", prefix=[p for _, p in DATASETS]),
        expand(f"{QUALITY_DIR}/quality_report_{{prefix}}.txt", prefix=[p for _, p in DATASETS])


rule acquire_open_data:
    output:
        zip_file = f"{RAW_DIR}/{{prefix}}.zip",
        csv_file = f"{RAW_DIR}/{{prefix}}.csv"
    params:
        url=lambda wildcards: URLS[wildcards.prefix]
    run:
        import os, subprocess, glob
        url = params.url
        prefix = wildcards.prefix
        os.makedirs(RAW_DIR, exist_ok=True)

        if url == "undp_hdi_api":
            subprocess.run(["python", "src/acquire_undp_hdi.py"], check=True)
            
            import src.utils.io_utils as io_utils
            csv_path = os.path.join(RAW_DIR, "undp_hdi.csv")

            io_utils.read_csv_metadata(csv_path, skiprows=0, source_name="undp_hdi")

            zip_path = output.zip_file
            if not os.path.exists(zip_path):
                open(zip_path, "wb").close()
            
            if csv_path != output.csv_file:
                os.replace(csv_path, output.csv_file)
        else:
            subprocess.run(["python", "src/acquire_open_data.py", url, RAW_DIR, prefix], check=True)
            extracted = glob.glob(os.path.join(RAW_DIR, f"{prefix}*"))
            if extracted:
                # prefer files ending with .csv
                csv_matches = [p for p in extracted if p.lower().endswith(".csv")]
                if csv_matches:
                    src_csv = csv_matches[0]
                else:
                    src_csv = extracted[0]
                if src_csv != output.csv_file:
                    os.replace(src_csv, output.csv_file)


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
