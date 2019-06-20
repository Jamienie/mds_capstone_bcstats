# bow_vectorizer.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-11

# This script file builds the bow vectorizer to be used later in the model

# Makefile USAGE:
# For the 2018 data:
'''
python src/features/bow_vectorizer.py
'''


# Import Modules
import sys
sys.path.insert(1, '.')
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from src.data.preprocessing_text import preprocess_for_bow
import scipy
import argparse
import pickle


# Default file paths
filepath_in = "data/interim/train_2018-qualitative-data.csv"


def get_arguments():
    parser = argparse.ArgumentParser(description='Build bow Vectorizer from'
                                     'csv')

    parser.add_argument('--input_csv', '-i', type=str, dest='input_csv',
                        action='store', default=filepath_in,
                        help='the input csv file with comments')

    args = parser.parse_args()
    return args


def get_bow_vectorizer(comments):

    vectorizer = CountVectorizer(stop_words='english', ngram_range=(1, 5),
                                 min_df=2)
    comments = preprocess_for_bow(comments)

    vectorizer.fit(comments)

    return vectorizer


###############################################################################
if __name__ == "__main__":

    args = get_arguments()
    df = pd.read_csv(args.input_csv)
    comments = df.iloc[:, 1]

    bow_vectorizer = get_bow_vectorizer(comments)

    with open("src/models/bow_vectorizer.pickle", 'wb') as handle:
        pickle.dump(bow_vectorizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
