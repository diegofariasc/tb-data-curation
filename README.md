# Data curation aimed at monitoring global progress towards ending TB

## Overview
This project implements a reproducible end-to-end data curation pipeline to monitor global progress toward ending tuberculosis (TB). It integrates data from WHO, the World Bank, and UNDP.

## Conda Environment

1. For reproducibility purposes an `environment.yml` file is provided. This allows to easily generate a Conda environment with all necessary dependencies for running this project. Create the environment with:
```conda env create -f environment.yml```f
2. Activate it with
```conda activate tb-curation```

## UNDP HDI API Key Setup
The UNDP Human Development Index (HDI) dataset requires an API key to access the HDRO Data API.

### Steps to obtain an API key:
1. Navigate to [HDR Data API Subscription](https://hdrdata.org).
2. Click **Subscribe for HDR Data API** and fill out the form.
3. Verify your email through the link sent by HDR.
4. After verification, you will receive your API key via email. Keep it secure.

### Using the API key:
1. Create a `.env` file in the root folder of this project.
2. Add your API key in the following format:
```HDRO_API_KEY=your_api_key_here```

## Workflow Execution

The entire data curation process is automated using **Snakemake**, which orchestrates data acquisition, quality assessment, cleaning, and transformation steps.

### Running the Workflow

1. Ensure that the `tb-curation` environment is active and your `.env` file is added
2. If you want a clean workflow execution from scratch, make sure to remove `data` and `docs` folders
```rm -rf data docs```
3. Execute the full pipeline using:
```snakemake --cores 4``` \
Replace 4 with the number of CPU cores available on your system.

#### Output structure 
After successful execution, you should see an output like the following:
```bash
Finished job 0.
10 of 10 steps (100%) done
Complete log: .snakemake\log\2025-10-27T115542.339447.snakemake.log
```

The workflow will generate the following key folders and files:
```bash
tb-data-curation/
│
├── data/               # All dataset-related files
│   ├── raw/            # Original downloaded datasets
│   ├── quality/        # Per-dataset data quality reports
│   ├── processed/      # Cleaned and harmonized datasets
│
├── docs/
│   └── metadata.json   # Metadata and provenance information
```