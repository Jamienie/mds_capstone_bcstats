# -*- coding: utf-8 -*-
# Author: Fan Nie
# Date: May 2019
# This script file is for splitting the comment datasets into a train and test
# to ensure dataset test data is untouched during our analysis


import pandas as pd

# file paths to read the qualitative data
input_path_2015 = "data/interim/desensitized_qualitative-data2015.csv"
input_path_2018 = "data/interim/desensitized_qualitative-data2018.csv"

# file paths to write the csv files
output_path_test_2015 = "data/interim/test_2015-qualitative-data.csv"
output_path_test_2018 = "data/interim/test_2018-qualitative-data.csv"
output_path_train_2015 = "data/interim/train_2015-qualitative-data.csv"
output_path_train_2018 = "data/interim/train_2018-qualitative-data.csv"

# Read in qualitative data
# 2015
df_raw_2015 = pd.read_csv(input_path_2015)
# 2018
df_raw_2018 = pd.read_csv(input_path_2018)

# Put 10% of the data aside for testing and the remaining 90% for training
# 2015
df_test_2015 = df_raw_2015.sample(frac=0.1, random_state=2019)
df_train_2015 = df_raw_2015.drop(index=df_test_2015.index)
# 2018
df_test_2018 = df_raw_2018.sample(frac=0.1, random_state=2019)
df_train_2018 = df_raw_2018.drop(index=df_test_2018.index)

# Writing dataframes to csv files
# 2015
df_test_2015.to_csv(path_or_buf=output_path_test_2015, index=False)
df_train_2015.to_csv(path_or_buf=output_path_train_2015, index=False)
# 2018
df_test_2018.to_csv(path_or_buf=output_path_test_2018, index=False)
df_train_2018.to_csv(path_or_buf=output_path_train_2018, index=False)
