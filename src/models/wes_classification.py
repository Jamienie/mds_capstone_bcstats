# wes_classification.py
# Author: Aaron Quinton
# Date: 2019-06-06

# This script wraps the keras Model into simple functions to train or predict.

###############################################################################
# Import Modules and functions used in text classification                    #
###############################################################################
import pickle
import pandas as pd
import numpy as np

# Custom functions for preprocessing, data preparation, and evaluation
from src.data.preprocessing_text import preprocess_for_embed
import sklearn.metrics as metrics

# Training Word embeddings and pre-trained embeddings
from gensim.models import KeyedVectors

# Keras Deep learning functions for LSTM
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, Embedding
from keras.layers import Bidirectional, Conv1D
from keras.layers import GlobalMaxPooling1D, GlobalAveragePooling1D
from keras.layers import GRU, concatenate
from keras.models import Model
from keras.models import load_model


###############################################################################
# Define final model functions to train and predict on WES comments           #
###############################################################################
default_embed_fname = './references/pretrained_embeddings.nosync/glove/' + \
    'glove.840B.300d.w2v.txt'
default_embed_name = 'glove_crawl'
default_save_model_fname = 'models/keras_model_glove_crawl.h5'
default_save_tokenizer_fname = 'models/tokenizer_glove_crawl.pickle'


def model_theme_train(comments, labels, embedding_filepath=default_embed_fname,
                      embedding_name=default_embed_name,
                      save_model_filepath=default_save_model_fname,
                      save_tokenizer_filepath=default_save_tokenizer_fname):
    '''Train Deep Learning Model on WES Survey Comment data to classify into
    12 main themes. Model is returned as a Keras Object and saved in the
    specified filepath.

    Parameters
    ----------
    comments : Pandas Series object
        An iteratable of str data with the open ended survey response in each
        element

    labels : Numpy Array of Shape (n_observations, 12)
        An array of 1's and 0's indicating which themes have been labeled on
        each comment

    embedding_filepath : str
        A file path with the pretrained embedding to be used for the model.
        Default is set to use the glove_crawl embedding in the
        references/pretrained_embeddings/glove directory.

    embedding_name : str
        The name of the pretrained embedding used. Accpeted embeddings are
        'glove_crawl', 'glove_wiki', 'w2v_google_news', 'fasttext_crawl'. The
        default is set to 'glove_crawl'

    save_model_filepath : str
        The file path location and name to save the trained Keras Model.
        Default is set to 'models/keras_model_glove_crawl.h5'

    save_tokenizer_filepath : str
        The file path to save the tokenizer used in training the model. The
        default is set to 'models/tokenizer_glove_crawl.pickle'

    Returns
    -------
    model_keras : Keras Model
        This object contains the trained keras model which is also saved in the
        specified file path to be used for later predictions.
    '''

    X_train = comments
    Y_train = labels

    # Load pretrained embeddings
    embedding = KeyedVectors.load_word2vec_format(embedding_filepath,
                                                  unicode_errors='ignore')

    ###########################################################################
    # Build Embedding Matrix and prepare data for deep learning Model
    max_words = 12000
    maxlen = 700
    embed_size = 300

    # Preprocess text data based on embedding
    X_train_pp = np.array(preprocess_for_embed(X_train, embedding_name,
                                               split=False))

    # Build Tokenizer and save it for use in prediction
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(X_train_pp)
    with open(save_tokenizer_filepath, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Convert X_train comments to numbers and pad it for model
    tokenized_train = tokenizer.texts_to_sequences(X_train_pp)
    X_train_model = pad_sequences(tokenized_train, maxlen=maxlen)

    # Create embedding Matrix with the embeddings for each word
    word_index = tokenizer.word_index
    num_words = min(max_words, len(word_index) + 1)
    embedding_matrix = np.zeros((num_words, embed_size), dtype='float32')

    for word, i in word_index.items():

        if i >= max_words:
            continue

        try:
            embedding_vector = embedding[word]

            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector
        except:
            continue

    ###########################################################################
    # Set up Deep learning Architecture and train Model
    inp = Input(shape=(maxlen, ))

    x = Embedding(max_words, embed_size,
                  weights=[embedding_matrix],
                  trainable=False)(inp)

    x = Bidirectional(GRU(128, return_sequences=True, dropout=0.1,
                          recurrent_dropout=0.1))(x)

    x = Conv1D(64, kernel_size=3, padding="valid",
               kernel_initializer="glorot_uniform")(x)

    avg_pool = GlobalAveragePooling1D()(x)
    max_pool = GlobalMaxPooling1D()(x)

    x = concatenate([avg_pool, max_pool])

    preds = Dense(12, activation="sigmoid")(x)

    model = Model(inp, preds)

    model.compile(loss='binary_crossentropy', optimizer='adam',
                  metrics=['accuracy'])

    # Train Model
    batch_size = 128
    epochs = 16
    model.fit(X_train_model, Y_train, batch_size=batch_size,
              epochs=epochs, validation_split=0.15)

    # Save and return Keras Model
    model_keras = model
    model_keras.save(save_model_filepath)

    return model_keras


def model_theme_predict(comments, embedding_name=default_embed_name,
                        load_model_filepath=default_save_model_fname,
                        load_tokenizer_filepath=default_save_tokenizer_fname):
    '''Predict themes for the WES Survey Comment data based on the trained
    Keras Model.

    Parameters
    ----------
    comments : Pandas Series object
        An iteratable of str data with the open ended survey response in each
        element

    embedding_name : str
        The name of the pretrained embedding used. Accepted embeddings are
        'glove_crawl', 'glove_wiki', 'w2v_google_news', 'fasttext_crawl'. The
        default is set to 'glove_crawl'

    load_model_filepath : str
        The file path location and name of the trained Keras Model.
        Default is set to 'models/keras_model_glove_crawl.h5'

    load_tokenizer_filepath : str
        The file path to load the tokenizer used in training the model. The
        default is set to 'models/tokenizer_glove_crawl.pickle'

    Returns
    -------
    Y_pred : Numpy Array of Shape (n_observations, 12)
        An array of numbers between 0 and 1 indicating the probabilities for
        each theme to be labeled on each comment
    '''
    # load tokenizer and prepare comments for prediction
    X_predict = comments
    X_predict_pp = np.array(preprocess_for_embed(X_predict, embedding_name,
                                                 split=False))

    with open(load_tokenizer_filepath, 'rb') as handle:
        tokenizer = pickle.load(handle)

    tokenized_predict = tokenizer.texts_to_sequences(X_predict_pp)
    X_predict_model = pad_sequences(tokenized_predict, maxlen=700)

    # Load Keras Model and predict probabilities for each theme
    model_keras = load_model(load_model_filepath)

    Y_pred = model_keras.predict(X_predict_model)

    return Y_pred
