# Snakefile

DATASETS = [
    {
        "url": "https://api.worldbank.org/v2/en/indicator/SH.TBS.INCD?downloadformat=csv",
        "prefix": "worldbank_tb_incidence",
        "method": "zip"
    },
    {
        "url": "https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=csv",
        "prefix": "worldbank_gdp_per_capita_usd",
        "method": "zip"
    },
    {
        "url": "https://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv",
        "prefix": "worldbank_population",
        "method": "zip"
    },
    {
        "url": "https://api.worldbank.org/v2/en/indicator/SH.XPD.CHEX.PC.CD?downloadformat=csv",
        "prefix": "worldbank_health_expenditure_usd",
        "method": "zip"
    },
        {
        "url": "https://api.worldbank.org/v2/en/indicator/SH.XPD.CHEX.GD.ZS?downloadformat=csv",
        "prefix": "worldbank_health_expenditure_gdp_percent",
        "method": "zip"
    },
    {
        "url": "https://extranet.who.int/tme/generateCSV.asp?ds=outcomes",
        "prefix": "who_treatment_outcomes",
        "method": "csvdirect"
    },
    {   "url": "undp_hdi_api", 
        "prefix": "undp_hdi", 
        "method": "api"
    },
    
]

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
QUALITY_DIR = "data/quality"

URLS = {d["prefix"]: d for d in DATASETS}


rule all:
    input:
        expand(
            f"{PROCESSED_DIR}/{{prefix}}_long.csv",
            prefix=[d["prefix"] for d in DATASETS],
        ),
        expand(
            f"{QUALITY_DIR}/quality_report_{{prefix}}.txt",
            prefix=[d["prefix"] for d in DATASETS],
        ),


rule acquire_data:
    output:
        zip_file=f"{RAW_DIR}/{{prefix}}.zip",
        csv_file=f"{RAW_DIR}/{{prefix}}.csv",
    run:
        import os, subprocess, glob, requests

        info = URLS[wildcards.prefix]
        url = info["url"]
        method = info["method"]
        prefix = wildcards.prefix
        os.makedirs(RAW_DIR, exist_ok=True)

        if method == "api":
            subprocess.run(["python", "src/acquire_undp_hdi.py"], check=True)
            csv_path = os.path.join(RAW_DIR, "undp_hdi.csv")
            import src.utils.io_utils as io_utils

            io_utils.read_csv_metadata(csv_path, skiprows=0, source_name="undp_hdi")
            if not os.path.exists(output.zip_file):
                open(output.zip_file, "wb").close()
            if csv_path != output.csv_file:
                os.replace(csv_path, output.csv_file)

        elif method == "zip":
            subprocess.run(
                ["python", "src/acquire_open_data.py", url, RAW_DIR, prefix], check=True
            )
            extracted = glob.glob(os.path.join(RAW_DIR, f"{prefix}*"))
            if extracted:
                csv_matches = [p for p in extracted if p.lower().endswith(".csv")]
                src_csv = csv_matches[0] if csv_matches else extracted[0]
                if src_csv != output.csv_file:
                    os.replace(src_csv, output.csv_file)

        elif method == "csvdirect":
            resp = requests.get(url)
            resp.raise_for_status()
            with open(output.csv_file, "wb") as f:
                f.write(resp.content)
            if not os.path.exists(output.zip_file):
                open(output.zip_file, "wb").close()

            import src.utils.io_utils as io_utils
            io_utils.read_csv_metadata(output.csv_file, skiprows=0, source_name=wildcards.prefix)

rule quality_assessment:
    input:
        f"{RAW_DIR}/{{prefix}}.csv",
    output:
        f"{QUALITY_DIR}/quality_report_{{prefix}}.txt",
    shell:
        "python src/quality_assessment.py {input} {QUALITY_DIR}"


rule clean_transform:
    input:
        f"{RAW_DIR}/{{prefix}}.csv",
    output:
        f"{PROCESSED_DIR}/{{prefix}}_long.csv",
    run:
        import subprocess

        info = URLS[wildcards.prefix]
        pivot_flag = info.get("pivot", "true")

        subprocess.run([
            "python",
            "src/clean_transform.py",
            input[0],
            PROCESSED_DIR,
            wildcards.prefix,
            pivot_flag
        ], check=True)