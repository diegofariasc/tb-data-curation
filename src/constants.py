# ---------------------------------------------------------------------------
# INCLUDED COUNTRY CODES
# ---------------------------------------------------------------------------
INCLUDED_COUNTRY_CODES = [
    # Central African countries
    "CAF",
    "TCD",
    "CMR",
    "COG",
    "COD",
    "GAB",
    "GNQ",
    # South and East Asian focus countries
    "IND",
    "CHN",
    "PHL",
    "PAK",
    # G20 countries
    "ARG",
    "AUS",
    "BRA",
    "CAN",
    "CHN",
    "FRA",
    "DEU",
    "IND",
    "IDN",
    "ITA",
    "JPN",
    "KOR",
    "MEX",
    "RUS",
    "SAU",
    "ZAF",
    "TUR",
    "GBR",
    "USA",
    "EUU",
]

# ---------------------------------------------------------------------------
# YEAR FILTERING CONSTANTS
# ---------------------------------------------------------------------------
# Define the temporal range for included data
EARLIEST_INCLUDED_START = 2014
LATEST_INCLUDED_YEAR = 2025

# ---------------------------------------------------------------------------
# TB TREATMENT OUTCOME FIELD RENAME MAP
# ---------------------------------------------------------------------------
# Provides user-friendly, descriptive names for WHO TB outcome variables.
# Used to clean and standardize WHO treatment outcomes datasets.
TB_TREATMENT_OUTCOME_FIELD_RENAME_MAP = {
    # New TB cases (all forms)
    "new_sp_coh": "new_tb_cases_cohort",
    "new_sp_cur": "new_tb_cases_current",
    "new_sp_cmplt": "new_tb_cases_completed",
    "new_sp_died": "new_tb_cases_died",
    "new_sp_fail": "new_tb_cases_failed",
    "new_sp_def": "new_tb_cases_defaulted",
    "c_new_sp_tsr": "new_tb_treatment_success_rate",
    # New TB cases (smear-negative/extra-pulmonary)
    "new_snep_coh": "new_tb_snep_cohort",
    "new_snep_cmplt": "new_tb_snep_completed",
    "new_snep_died": "new_tb_snep_died",
    "new_snep_fail": "new_tb_snep_failed",
    "new_snep_def": "new_tb_snep_defaulted",
    "c_new_snep_tsr": "new_tb_snep_treatment_success_rate",
    # Retreatment TB
    "ret_coh": "retreatment_cohort",
    "ret_cur": "retreatment_current",
    "ret_cmplt": "retreatment_completed",
    "ret_died": "retreatment_died",
    "ret_fail": "retreatment_failed",
    "ret_def": "retreatment_defaulted",
    "c_ret_tsr": "retreatment_success_rate",
    # HIV co-infected TB (new cases)
    "hiv_new_sp_coh": "hiv_new_tb_cases_cohort",
    "hiv_new_sp_cur": "hiv_new_tb_cases_current",
    "hiv_new_sp_cmplt": "hiv_new_tb_cases_completed",
    "hiv_new_sp_died": "hiv_new_tb_cases_died",
    "hiv_new_sp_fail": "hiv_new_tb_cases_failed",
    "hiv_new_sp_def": "hiv_new_tb_cases_defaulted",
    "hiv_new_snep_coh": "hiv_new_tb_snep_cohort",
    "hiv_new_snep_cmplt": "hiv_new_tb_snep_completed",
    "hiv_new_snep_died": "hiv_new_tb_snep_died",
    "hiv_new_snep_fail": "hiv_new_tb_snep_failed",
    "hiv_new_snep_def": "hiv_new_tb_snep_defaulted",
    # HIV co-infected TB (retreatment)
    "hiv_ret_coh": "hiv_retreatment_cohort",
    "hiv_ret_cur": "hiv_retreatment_current",
    "hiv_ret_cmplt": "hiv_retreatment_completed",
    "hiv_ret_died": "hiv_retreatment_died",
    "hiv_ret_fail": "hiv_retreatment_failed",
    "hiv_ret_def": "hiv_retreatment_defaulted",
    # New relapse cases
    "newrel_coh": "new_relapse_cohort",
    "newrel_succ": "new_relapse_success",
    "newrel_fail": "new_relapse_failed",
    "newrel_died": "new_relapse_died",
    "newrel_lost": "new_relapse_lost",
    "c_new_tsr": "new_relapse_treatment_success_rate",
    # Retreatment non-relapse cases
    "ret_nrel_coh": "retreatment_nonrelapse_cohort",
    "ret_nrel_succ": "retreatment_nonrelapse_success",
    "ret_nrel_fail": "retreatment_nonrelapse_failed",
    "ret_nrel_died": "retreatment_nonrelapse_died",
    "ret_nrel_lost": "retreatment_nonrelapse_lost",
    "c_ret_tsr": "retreatment_nonrelapse_success_rate",
    # TB-HIV combined treatment outcomes
    "tbhiv_coh": "tbhiv_cohort",
    "tbhiv_succ": "tbhiv_success",
    "tbhiv_fail": "tbhiv_failed",
    "tbhiv_died": "tbhiv_died",
    "tbhiv_lost": "tbhiv_lost",
    "c_tbhiv_tsr": "tbhiv_treatment_success_rate",
    # Drug-resistant TB (multidrug-resistant)
    "mdr_coh": "multidrug_resistant_tb_cohort",
    "mdr_succ": "multidrug_resistant_tb_success",
    "mdr_fail": "multidrug_resistant_tb_failed",
    "mdr_died": "multidrug_resistant_tb_died",
    "mdr_lost": "multidrug_resistant_tb_lost",
    # Drug-resistant TB (extensively drug-resistant)
    "xdr_coh": "extensively_drug_resistant_tb_cohort",
    "xdr_succ": "extensively_drug_resistant_tb_success",
    "xdr_fail": "extensively_drug_resistant_tb_failed",
    "xdr_died": "extensively_drug_resistant_tb_died",
    "xdr_lost": "extensively_drug_resistant_tb_lost",
}
