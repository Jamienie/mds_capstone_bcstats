# preprocessing_data _preperation.py
# Author: Fan Nie
# Date: June 2019
# This script file is for splitting the 2019 comment datasets into a train and validation
# to ensure dataset test data is untouched during our analysis

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Input Filepath
fname_rawdata2018 = "data/interim/train_2018-qualitative-data.csv"

# file paths to write the csv files
output_path_X_train = "data/interim/X_train_2018-qualitative-data.csv"
output_path_X_valid = "data/interim/X_valid_2018-qualitative-data.csv"
output_path_Y_train = "data/interim/Y_train_2018-qualitative-data.csv"
output_path_Y_valid = "data/interim/Y_valid_2018-qualitative-data.csv"

################################################################
# Preparing Comment data
################################################################

# Read in raw data
df = pd.read_csv(fname_rawdata2018)
df_userid = df[['_telkey', '2018 Comment']]
df_userid = df_userid.rename(columns = {'_telkey':'USERID'})

df = df[['2018 Comment']].join(df.loc[:,'CPD':'OTH'])
df = df.rename(columns = {'2018 Comment' : 'comment'})

Y = np.array(df.loc[:,"CPD":"OTH"])
themes = df.loc[:,'CPD':'OTH'].columns.tolist()

# Split the data
df_X_train, df_X_valid, Y_train, Y_valid = train_test_split(
        df.comment, Y, test_size=0.25, random_state=2019)
Y_train = pd.DataFrame(Y_train)
Y_valid = pd.DataFrame(Y_valid)
 
# Writing dataframes to csv files
df_X_train.to_csv(output_path_X_train, index=False,header=True)
df_X_valid.to_csv(output_path_X_valid, index=False,header=True)
Y_train.to_csv(output_path_Y_train, index=False,header=True)
Y_valid.to_csv(output_path_Y_valid, index=False,header=True)

