# conv1d.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-09

# This script defines a function that trains a convulutional neural net for
# each embedding and saves it in the models folder.

# Makefile USAGE:
'''
python src/models/conv1d.py
'''

# Import Modules
import pickle
import pandas as pd
import numpy as np
from keras.layers import Dense, Embedding, Dropout, Activation
from keras.layers import GlobalMaxPooling1D, Conv1D
from keras.models import Sequential


def train_conv1d(X_train, Y_train, embed_name, max_features,embed_matrix=False):

    maxlen = 700
    batch_size = 128
    filters = 250
    kernel_size = 3
    hidden_dims = 250
    epochs = 7
    if embed_name == 'glove_twitter':
        embed_size = 200
    else:
        embed_size = 300

    # Neural Net Architecture
    model = Sequential()

    if embed_matrix is False:
        model.add(Embedding(max_features, embed_size, input_length=maxlen))
    else:
        model.add(Embedding(max_features, embed_size, weights=[embed_matrix],
                            trainable=False, input_length=maxlen))

    model.add(Dropout(0.2))
    model.add(Conv1D(filters, kernel_size, padding='valid', activation='relu',
                     strides=1))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(hidden_dims))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))
    model.add(Dense(12))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam',
                  metrics=['accuracy'])

    # Train Model
    model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs,
              validation_split=0.15)

    return model


###############################################################################
if __name__ == "__main__":

    embed_names = ['base', 'glove_crawl', 'glove_twitter', 'glove_wiki',
                   'fasttext_crawl', 'fasttext_wiki', 'w2v_google_news']

    # Get labels
    df = pd.read_csv('./data/interim/train_2018-qualitative-data.csv')
    Y_train = np.array(df.loc[:, "CPD":"OTH"])

    # Load embedding matrices
    with open('src/models/embed_matrices.pickle', 'rb') as handle:
        embed_matrices = pickle.load(handle)

    # Load training data
    with open('./data/processed/X_train_encoded.pickle', 'rb') as handle:
        X_train_encoded = pickle.load(handle)

    # Train Conv1d models and save in the models folder
    conv1d_models = {}
    for embed in embed_names:
        print('Training conv1d on', embed, 'embedding')
        if embed == 'base':
            embed_size = np.max(np.ravel(X_train_encoded[embed])) + 1
            conv1d_models[embed] = train_conv1d(X_train_encoded[embed],
                                                Y_train,
                                                embed,
                                                embed_size,
                                                False)
        else:
            conv1d_models[embed] = train_conv1d(X_train_encoded[embed],
                                                Y_train,
                                                embed,
                                                embed_matrices[embed].shape[0],
                                                embed_matrices[embed])

    with open('src/models/conv1d_models.pickle', 'wb') as handle:
        pickle.dump(conv1d_models, handle, protocol=pickle.HIGHEST_PROTOCOL)
