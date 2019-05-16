# prepare_qualitative_data.py
# Author: Aaron Quinton
# Date: 2019-05-19

import sys
import pandas as pd

sys.path.append('src/data')
import sensitive_text

# File paths to Read the Qualitative Data
filepath_2015 = "data/raw/WES2015_Final_Qual_Results.xlsx"
filepath_2018 = "data/raw/2018 WES Qual Coded - Final Comments and Codes.xlsx"

# File Paths to Write the train and test .csv
filepath_test2015 = "data/interim/test_2015-qaulitative-data.csv"
filepath_train2015 = "data/interim/train_2015-qaulitative-data.csv"
filepath_test2018 = "data/interim/test_2018-qaulitative-data.csv"
filepath_train2018 = "data/interim/train_2018-qaulitative-data.csv"


###############################################################################
# Read in 2015 and 2018 raw qualitative data, remove sensitive comments, and  #
# prepare it into test and train .csv                                         #
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


# Put 10% of the data aside for testing and the remaining 90% for training
# 2015
df_test_2015 = df_raw_2015.sample(frac=0.1, random_state=2019)
df_train_2015 = df_raw_2015.drop(index=df_test_2015.index)
# 2018
df_test_2018 = df_raw_2018.sample(frac=0.1, random_state=2019)
df_train_2018 = df_raw_2018.drop(index=df_test_2018.index)


# Write raw train and test dataframes to csv with the sensitive rows removed
# 2015
df_test_2015.to_csv(filepath_test2015)
df_train_2015.to_csv(filepath_train2015)
# 2018
df_test_2018.to_csv(filepath_test2018)
df_train_2018.to_csv(filepath_train2018)
