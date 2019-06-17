# run_classifier.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-09

# This script predicts the labels and saves the output.

# Makefile USAGE:
'''
python src/models/run_classifier.py
'''

import sys
sys.path.insert(1, '.')
import pickle
import pandas as pd
from src.features.encode_comments import get_encoded_comments


df = pd.read_csv("test.csv")
comments = df['comments']


###############################################################################
# Predict test data labels with Conv1d and biGRU Models                       #
###############################################################################
# Load Embedding Tokenizers
with open('./models/embed_tokenizers.pickle', 'rb') as handle:
    embed_tokenizers = pickle.load(handle)

# Load Neural Net Classification Models
with open('./models/conv1d_models.pickle', 'rb') as handle:
    conv1d_models = pickle.load(handle)

with open('./models/biGRU_models.pickle', 'rb') as handle:
    biGRU_models = pickle.load(handle)

# Predict on each embedding
embed_names = ['base', 'glove_crawl', 'glove_twitter', 'glove_wiki',
               'fasttext_crawl', 'fasttext_wiki', 'w2v_google_news']

Y_conv1d = {}
Y_biGRU = {}
for embed in embed_names:
    X = get_encoded_comments(comments, embed_tokenizers[embed], embed)
    Y_conv1d[embed] = conv1d_models[embed].predict(X)
    Y_biGRU[embed] = biGRU_models[embed].predict(X)
