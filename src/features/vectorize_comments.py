# vectorize_comments.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-11

# This script vectorizes comments for later training

# Makefile USAGE:
# For the 2018 data:
'''
python src/features/vectorize_comments.py
'''
# For the 2018 test data:
'''
python src/features/vectorize_comments.py \
--input_csv data/interim/test_2018-qualitative-data.csv \
--output_npz data/processed/X_test_bow.npz
'''

# Import modules
import sys
sys.path.insert(1, '.')
import pandas as pd
from src.data.preprocessing_text import preprocess_for_bow
import pickle
import argparse
import scipy.sparse

# Default File paths:
filepath_in = './data/interim/train_2018-qualitative-data.csv'
filepath_out = './data/processed/X_train_bow.npz'


def get_arguments():
    parser = argparse.ArgumentParser(description='Encode comments from csv to'
                                     'arrays with number representations')

    parser.add_argument('--input_csv', '-i', type=str, dest='input_csv',
                        action='store', default=filepath_in,
                        help='the input csv file with comments')

    parser.add_argument('--output_npz', '-o', type=str,
                        dest='output_npz', action='store',
                        default=filepath_out, help='the output npz file')

    args = parser.parse_args()
    return args


def get_vectorized_comments(comments, vectorizer):

    comments = preprocess_for_bow(comments)
    X = vectorizer.transform(comments)

    return X


###############################################################################
if __name__ == "__main__":

    args = get_arguments()
    df = pd.read_csv(args.input_csv)
    comments = df.iloc[:, 1]

    # Load Vectorizer
    with open('src/models/bow_vectorizer.pickle', 'rb') as handle:
        bow_vectorizer = pickle.load(handle)

    # Get sparse document-term matrix and save
    X = get_vectorized_comments(comments, bow_vectorizer)
    scipy.sparse.save_npz(args.output_npz, X)
