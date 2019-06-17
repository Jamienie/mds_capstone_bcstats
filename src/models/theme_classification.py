# theme_classification.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-09

# This script predicts the theme on the test data for every model

# Makefile USAGE:

'''
python src/models/theme_classification.py
'''

import sys
sys.path.insert(1, '.')
import pickle
import numpy as np
import pandas as pd
import scipy.sparse


##############################################################################
# Predict test data themes with Baseline BOW and Linear SVC Model
# Load Vectorized comments
X_text_bow = scipy.sparse.load_npz('./data/processed/X_test_bow.npz')

# Load Linear SVC Model
with open('./models/linearsvc_model.pickle', 'rb') as handle:
    linearsvc_model = pickle.load(handle)

# Predict themes
Y_bow = linearsvc_model.predict(X_text_bow)


###############################################################################
# Predict test data labels with Conv1d and biGRU Models
# Load Encoded Comments
with open('./data/processed/X_test_encoded.pickle', 'rb') as handle:
    X_test_encoded = pickle.load(handle)

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
    Y_conv1d[embed] = conv1d_models[embed].predict(X_test_encoded[embed])
    Y_biGRU[embed] = biGRU_models[embed].predict(X_test_encoded[embed])

###############################################################################
# Save test data predictions
Y_pred = {}
Y_pred['BOW'] = Y_bow
Y_pred['conv1d'] = Y_conv1d
Y_pred['biGRU'] = Y_biGRU
Y_pred['ensemble'] = (Y_conv1d['glove_wiki'] + Y_biGRU['glove_wiki']
                      + Y_biGRU['glove_crawl'] + Y_biGRU['fasttext_crawl'])/4

with open('./data/output/test_predictions.pickle', 'wb') as handle:
    pickle.dump(Y_pred, handle, protocol=pickle.HIGHEST_PROTOCOL)
