# avg_embeddings.py
# Authors: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-05-22

# Functions to get the word embeddings from the pretrained Google News model.
# Functions inspired by the DSCI 573 course Lab 1 by Varada Kolhatkar
# USAGE: Need to have GoogleNews-vectors-negative300.bin in the reference dir


# Import Modules
import numpy as np


def get_average_embeddings(sentences, embeddings_index, n_features=300):
    """
    Returns the average embedding of the given text containing n_features
    using the given trained model (e.g., word2vev, FastText).

    Keyword arguments
    text -- (str) input text
    model -- (gensim.models) model to use to get embeddings
    n_features -- (int) size of the embedding vector

    Returns:
    feat_vect -- (np.array) the average embedding vector of the given text
    """

    feat_vect = np.zeros(n_features, dtype='float64')

    nwords = 0

    for word in sentences:
        try:
            nwords += 1
            feat_vect = np.add(feat_vect, embeddings_index[word])
        except:
            continue

    if nwords == 0:
        nwords = 1
    feat_vect = np.divide(feat_vect, nwords)
    return feat_vect
