# -*- coding: utf-8 -*-
# Author: Fan Nie
# Date: May 2019
# This script file is for splitting the comment datasets into train and test dataset


import pandas as pd

# file paths to read the qualitative data
input_path_2015 = "data/interim/desensitized_qualitative-data2015.csv"
input_path_2018 = "data/interim/desensitized_qualitative-data2018.csv"

# file paths to write the csv files
output_path_test_2015 = "data/interim/test_2015-qualitative-data.csv"
output_path_test_2018 = "data/interim/test_2018-qualitative-data.csv"
output_path_train_2015 = "data/interim/train_2015-qualitative-data.csv"
output_path_train_2018 = "data/interim/train_2018-qualitative-data.csv"

# reading in 2015 qualitative data
df_raw_2015 = pd.read_excel(input_path_2015)

# reading in 2018 qualitative data
df_raw_2018 = pd.read_excel(input_path_2018,skiprows = 1)

# Put 10% of the data aside for testing and the remaining 90% for training
df_test_2018 = df_raw_2018.sample(frac = 0.1, random_state = 2019)
df_test_2015 = df_raw_2015.sample(frac = 0.1, random_state = 2019)
df_train_2015 = df_raw_2015.drop(index = df_test_2015.index)
df_train_2018 = df_raw_2018.drop(index = df_test_2018.index)

#writing split data to csv files
df_test_2015.to_csv(path_or_buf = output_path_test_2015)
df_test_2018.to_csv(path_or_buf = output_path_test_2018)

df_train_2015.to_csv(path_or_buf = output_path_train_2015)
df_train_2018.to_csv(path_or_buf = output_path_train_2018)
