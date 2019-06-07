# linearsvc.py
# Author: Fan Nie
# Date: June 2019
# This script file is for building LinearSVC model


import pandas as pd
import scipy.sparse
from skmultilearn.problem_transform import BinaryRelevance
from sklearn.svm import LinearSVC


# file paths to read the qualitative data
df_X_train_path = "data/interim/X_train_bow.npz"
df_X_valid_path = "data/interim/X_valid_bow.npz"
Y_train_path = "data/interim/Y_train_2018-qualitative-data.csv"

# file paths to write the csv files
output_path_Y_pred_bow = "data/interim/Y_pred_bow.csv"

################################################################
# Use Count Vectorizer to build LinearSVC model
################################################################

# read in npz files
X_train_bow = scipy.sparse.load_npz(df_X_train_path)
X_valid_bow = scipy.sparse.load_npz(df_X_train_path)

# read in csv files
Y_train = pd.read_csv(Y_train_path)

model_bow = BinaryRelevance(
    classifier = LinearSVC(C = 0.5, tol = 0.2)
)

model_bow.fit(X_train_bow, Y_train)

Y_pred_bow = model_bow.predict(X_valid_bow).toarray()

# Writing dataframe to csv file
pd.DataFrame(Y_pred_bow).to_csv(output_path_Y_pred_bow,index=False)


