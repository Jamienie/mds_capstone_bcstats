# biGRU.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-10

# This script defines a function that trains a Bidirectional GRU neural net for
# each embedding and saves it in the models folder.

# Makefile USAGE:
'''
python src/models/biGRU.py
'''

# Import Modules
import pickle
import pandas as pd
import numpy as np
from keras.layers import Dense, Input, Embedding
from keras.layers import Bidirectional, Conv1D
from keras.layers import GlobalMaxPooling1D, GlobalAveragePooling1D
from keras.layers import GRU, concatenate
from keras.models import Model


def train_biGRU(X_train, Y_train, embed_name, embed_matrix=False):

    # Define parameters for Neural Net Architecture
    max_features = 12000
    maxlen = 700
    batch_size = 128
    filters = 64
    kernel_size = 3
    epochs = 12
    if embed_name == 'glove_twitter':
        embed_size = 200
    else:
        embed_size = 300

    # Neural Net Architecture
    inp = Input(shape=(maxlen, ))

    if embed_matrix is False:
        x = Embedding(max_features, embed_size)(inp)
    else:
        x = Embedding(max_features, embed_size, weights=[embed_matrix],
                      trainable=False)(inp)

    x = Bidirectional(GRU(128, return_sequences=True, dropout=0.1,
                          recurrent_dropout=0.1))(x)
    x = Conv1D(filters, kernel_size=kernel_size, padding="valid",
               kernel_initializer="glorot_uniform")(x)

    avg_pool = GlobalAveragePooling1D()(x)
    max_pool = GlobalMaxPooling1D()(x)

    x = concatenate([avg_pool, max_pool])

    preds = Dense(12, activation="sigmoid")(x)

    model = Model(inp, preds)

    model.compile(loss='binary_crossentropy', optimizer='adam',
                  metrics=['accuracy'])

    # Train Model
    model.fit(X_train, Y_train, batch_size=batch_size,
              epochs=epochs, validation_split=0.15)

    return model


###############################################################################
if __name__ == "__main__":

    embed_names = ['base', 'glove_crawl', 'glove_twitter', 'glove_wiki',
                   'fasttext_crawl', 'fasttext_wiki', 'w2v_google_news']

    # Get labels
    df = pd.read_csv('./data/interim/train_2018-qualitative-data.csv')
    Y_train = np.array(df.loc[:, "CPD":"OTH"])

    # Load embedding matrices
    with open('./models/embed_matrices.pickle', 'rb') as handle:
        embed_matrices = pickle.load(handle)

    # Load training data
    with open('./data/processed/X_train_encoded.pickle', 'rb') as handle:
        X_train_encoded = pickle.load(handle)

    # Train biGRU models and save in the models folder
    biGRU_models = {}
    for embed in embed_names:
        print('Training biGRU on', embed, 'embedding')
        if embed == 'base':
            biGRU_models[embed] = train_biGRU(X_train_encoded[embed],
                                              Y_train, embed, False)
        else:
            biGRU_models[embed] = train_biGRU(X_train_encoded[embed],
                                              Y_train, embed,
                                              embed_matrices[embed])

    with open('./models/biGRU_models.pickle', 'wb') as handle:
        pickle.dump(biGRU_models, handle, protocol=pickle.HIGHEST_PROTOCOL)
