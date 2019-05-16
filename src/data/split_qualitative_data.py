import pandas as pd

# reading in 2018 qualitative data
df_raw_2018 = pd.read_excel("../data/raw/2018 WES Qual Coded - Final Comments and Codes.xlsx",
                       skiprows = 1)
# reading in 2015 qualitative data
df_raw_2015 = pd.read_excel("../data/raw/WES2015_Final_Qual_Results.xlsx")

# Put 10% of the data aside for testing and the remaining 90% for training
df_test_2018 = df_raw_2018.sample(frac = 0.1, random_state = 2019)
df_test_2015 = df_raw_2015.sample(frac = 0.1, random_state = 2019)
df_train_2015 = df_raw_2015.drop(index = df_test_2015.index)
df_train_2018 = df_raw_2018.drop(index = df_test_2018.index)

#writing split data to csv files
df_test_2015.to_csv(path_or_buf = "../data/interim/test_2015-qualitative-data.csv")
df_test_2018.to_csv(path_or_buf = "../data/interim/test_2018-qualitative-data.csv")

df_train_2015.to_csv(path_or_buf = "../data/interim/train_2015-qualitative-data.csv")
df_train_2018.to_csv(path_or_buf = "../data/interim/train_2018-qualitative-data.csv")
