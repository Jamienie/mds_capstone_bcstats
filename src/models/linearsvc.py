# linearsvc.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-09

# This script file is for building the LinearSVC model

# Makefile USAGE:
'''
python src/models/linearsvc.py
'''

# Import Modules
import pandas as pd
import numpy as np
import scipy.sparse
from skmultilearn.problem_transform import BinaryRelevance
from sklearn.svm import LinearSVC
import pickle


def train_linearsvc(X_train, Y_train):

    model_bow = BinaryRelevance(
        classifier=LinearSVC(C=0.5, tol=0.2)
    )

    model_bow.fit(X_train, Y_train)

    return model_bow


###############################################################################
if __name__ == "__main__":

    # Get labels
    df = pd.read_csv('./data/interim/train_2018-qualitative-data.csv')
    Y_train = np.array(df.loc[:, "CPD":"OTH"])

    # read in npz file
    X_train = scipy.sparse.load_npz('./data/processed/X_train_bow.npz')

    linearsvc_model = train_linearsvc(X_train, Y_train)

    with open('src/models/linearsvc_model.pickle', 'wb') as handle:
        pickle.dump(linearsvc_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
