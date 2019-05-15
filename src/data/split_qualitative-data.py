import pandas as pd


df_raw = pd.read_excel("data/raw/2018 WES Qual Coded - Final Comments and Codes.xlsx",
                       skiprows = 1)

# Put 10% of the data aside for testing and the remaining 90% for training
df_test = df_raw.sample(frac = 0.1, random_state = 2019)
df_train = df_raw.drop(index = df_test.index)

df_test.to_csv(path_or_buf = "data/interim/test_2018-qaulitative-data.csv")
df_train.to_csv(path_or_buf = "data/interim/train_2018-qaulitative-data.csv")
