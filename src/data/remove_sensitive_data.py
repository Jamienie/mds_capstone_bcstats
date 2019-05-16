# prepare_qualitative_data.py
# Author: Aaron Quinton
# Date: 2019-05-19

import pandas as pd
from src.data import sensitive_text

# File paths to Read the Qualitative Data
filepath_2015 = "data/raw/WES2015_Final_Qual_Results.xlsx"
filepath_2018 = "data/raw/2018 WES Qual Coded - Final Comments and Codes.xlsx"

# File Paths to Write the train and test .csv
filepath_2015 = "data/interim/desensitized_qualitative-data.csv"
filepath_2018 = "data/interim/desensitized_qualitative-data.csv"


###############################################################################
# Read in 2015 and 2018 raw qualitative data and remove sensitive comments    #
###############################################################################

# Read Raw data files from local data directory
# 2015
df_raw_2015 = pd.read_excel(filepath_2015)
# 2018
df_raw_2018 = pd.read_excel(filepath_2018, skiprows=1)


# Identify and drop the rows that contain sensitive information in the comments
# 2015
comments2015 = df_raw_2015['2015 Comments']
index2015 = sensitive_text.sensitive_index(comments2015)
df_raw_2015 = df_raw_2015.drop(index=index2015)
# 2018
comments2018 = df_raw_2018['2018 Comment']
index2018 = sensitive_text.sensitive_index(comments2018)
df_raw_2018 = df_raw_2018.drop(index=index2018)


# Write raw train and test dataframes to csv with the sensitive rows removed
# 2015
df_raw_2015.to_csv(filepath_2015)
# 2018
df_raw_2018.to_csv(filepath_2018)
