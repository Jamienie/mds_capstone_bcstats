# bow.py
# Author: Fan Nie
# Date: June 2019
# This script file is for building bag of words

# set the system directory
import sys
sys.path.insert(1, '.')

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from src.data.preprocessing_text import preprocess_for_bow
import scipy.sparse


# file paths to read the qualitative data
df_X_train_path = "data/interim/X_train_2018-qualitative-data.csv"
df_X_valid_path = "data/interim/X_valid_2018-qualitative-data.csv"

# file paths to write the csv files
output_path_X_train_bow = "data/interim/X_train_bow.npz"
output_path_X_valid_bow = "data/interim/X_valid_bow.npz"

################################################################
# Use Count Vectorizer to build bag of word arrays to train on
################################################################

# read in csv files as Series files
df_X_train = pd.read_csv(df_X_train_path,squeeze=True)
df_X_valid = pd.read_csv(df_X_valid_path,squeeze=True)

vectorizer = CountVectorizer(stop_words= 'english',
                             ngram_range=(1,5), 
                             min_df=2)   

X_train_bow = vectorizer.fit_transform(preprocess_for_bow(df_X_train))
X_valid_bow = vectorizer.transform(preprocess_for_bow(df_X_valid))


# Writing sparse matrices to npz files
scipy.sparse.save_npz(output_path_X_train_bow,X_train_bow, compressed=False)
scipy.sparse.save_npz(output_path_X_valid_bow,X_valid_bow, compressed=False)

