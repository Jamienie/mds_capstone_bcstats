# preprocessing_text.py
# Authors: Aaron Quinton
# Date: 2019-05-22

# Many functions and the overall workflow have been built from Kaggle Kernel
# written by "Dieter"
# https://www.kaggle.com/christofhenkel/how-to-preprocessing-when-using-embeddings

# Import modules
import re
import numpy as np

###############################################################################
# Functions used for preprocessing punctuation, numbers, and misspellings and #
# bootstrapping comment data to balance comments per theme label              #
###############################################################################


def clean_text(x):

    x = str(x)
    for punct in "/-'":
        x = x.replace(punct, ' ')
    for punct in '&':
        x = x.replace(punct, f' {punct} ')
    for punct in '?!.,"#$%\'()*+-/:;<=>@[\\]^_`{|}~' + '“”’':
        x = x.replace(punct, '')

    return x


def clean_numbers(x):

    x = re.sub('[0-9]{5,}', '#####', x)
    x = re.sub('[0-9]{4}', '####', x)
    x = re.sub('[0-9]{3}', '###', x)
    x = re.sub('[0-9]{2}', '##', x)
    return x


def _get_mispell(mispell_dict):
    mispell_re = re.compile('(%s)' % '|'.join(mispell_dict.keys()))
    return mispell_dict, mispell_re


mispell_dict = {'colour': 'color',
                'centre': 'center',
                'didnt': 'did not',
                'doesnt': 'does not',
                'isnt': 'is not',
                'shouldnt': 'should not',
                'behaviour': 'behavior',
                'behaviours': 'behaviors',
                'behavioural': 'behavioral',
                'favourite': 'favorite',
                'favouritism': 'favoritism',
                'travelling': 'traveling',
                'counselling': 'counseling',
                'theatre': 'theater',
                'acknowledgement': 'acknowledgment',
                'cancelled': 'canceled',
                'labour': 'labor',
                'organisation': 'organization',
                'wwii': 'world war 2',
                'citicise': 'criticize',
                'counsellor': 'counselor',
                'favour': 'favor',
                'defence': 'defense',
                'practise': 'practice',
                'instagram': 'social medium',
                'whatsapp': 'social medium',
                'snapchat': 'social medium'
                }
mispellings, mispellings_re = _get_mispell(mispell_dict)


def replace_typical_misspell(text):
    def replace(match):
        return mispellings[match.group(0)]

    return mispellings_re.sub(replace, text)


def remove_stopwords(sentences):
    to_remove = ['a', 'to', 'of', 'and']

    sentences_re = [[word for word in sentence if word not in to_remove]
                    for sentence in sentences]

    return sentences_re


def balance_themes(X, Y):
    counts = np.sum(Y, axis=0)

    for i in range(Y.shape[1]):

        X_labeled = X[Y[:, i] == 1, :]
        Y_labeled = Y[Y[:, i] == 1, :]

        index = np.random.randint(low=0, high=counts[i],
                                  size=max(counts) - counts[i])
        X_array_to_append = X_labeled[index, :]
        Y_array_to_append = Y_labeled[index, :]

        if i == 0:
            X_balance = X
            Y_balance = Y

        X_balance = np.vstack((X_balance, X_array_to_append))
        Y_balance = np.vstack((Y_balance, Y_array_to_append))

    return X_balance, Y_balance
