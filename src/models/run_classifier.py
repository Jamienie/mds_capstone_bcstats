# run_classifier.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-09

# This script predicts the labels and saves the output.

# Makefile USAGE:
'''
python src/models/run_classifier.py \
--input_csv predict/predict_input/predict_comments_in.csv \
--output_csv predict/predict_output/predict_comments_out.csv
'''

import sys
sys.path.insert(1, '.')
import pickle
import pandas as pd
import argparse
from src.features.encode_comments import get_encoded_comments
import numpy as np


# Default File paths:
filepath_in = 'predict/predict_input/predict_comments_in.csv'
filepath_out = 'predict/predict_output/predict_comments_out.csv'


def get_arguments():
    parser = argparse.ArgumentParser(description='Encode comments from csv to'
                                     'arrays with number representations')

    parser.add_argument('--input_csv', '-i', type=str, dest='input_csv',
                        action='store', default=filepath_in,
                        help='the input csv file with comments')

    parser.add_argument('--output_csv', '-o', type=str,
                        dest='output_csv', action='store',
                        default=filepath_out, help='the output csv file')

    args = parser.parse_args()
    return args


###############################################################################
if __name__ == "__main__":

    args = get_arguments()
    embed_names = ['glove_crawl', 'glove_wiki', 'fasttext_crawl']

    df = pd.read_csv(args.input_csv)
    comments = df.iloc[:, 1]

    # Load Embedding Tokenizers
    with open('./models/embed_tokenizers.pickle', 'rb') as handle:
        embed_tokenizers = pickle.load(handle)

    # Load Neural Net Classification Models
    with open('./models/conv1d_models.pickle', 'rb') as handle:
        conv1d_models = pickle.load(handle)

    with open('./models/biGRU_models.pickle', 'rb') as handle:
        biGRU_models = pickle.load(handle)

    # Make predictions
    encoded_comments = {}
    for embed in embed_names:
        encoded_comments[embed] = get_encoded_comments(comments,
                                                       embed_tokenizers[embed],
                                                       embed)

    Y_conv1d = {}
    Y_biGRU = {}
    Y_conv1d['glove_wiki'] = conv1d_models['glove_wiki'] \
                                .predict(encoded_comments['glove_wiki'])

    Y_biGRU['glove_wiki'] = biGRU_models['glove_wiki'] \
                                .predict(encoded_comments['glove_wiki'])

    Y_biGRU['glove_crawl'] = biGRU_models['glove_crawl'] \
                                .predict(encoded_comments['glove_crawl'])

    Y_biGRU['fasttext_crawl'] = biGRU_models['fasttext_crawl'] \
                                .predict(encoded_comments['fasttext_crawl'])

    ensemble = (Y_conv1d['glove_wiki'] + Y_biGRU['glove_wiki']
                + Y_biGRU['glove_crawl'] + Y_biGRU['fasttext_crawl'])/4

    # Format predictions and save to csv
    predictions = pd.DataFrame(np.round(ensemble-0.42))

    predictions['comments'] = comments
    predictions['user_id'] = df.iloc[:, 0]
    predictions.columns = ['CPD', 'CB', 'EWC', 'Exec', 'FWE', 'SP', 'RE', 'Sup',
                           'SW', 'TEPE', 'VMG', 'OTH', 'comments', 'user_id']

    df = predictions[['user_id', 'comments', 'CPD', 'CB', 'EWC', 'Exec', 'FWE',
                      'SP', 'RE', 'Sup', 'SW', 'TEPE', 'VMG', 'OTH']]

    df.to_csv(args.output_csv)
