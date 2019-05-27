# eval.py
# Author: Aaron Quinton
# Date: 2019-05-20

# Import `theme_results()` function to evaluate the accuracies and other
# metrics for the text theme classification problem

import numpy as np
import pandas as pd
import sklearn.metrics as metrics


def theme_results(Ytrue, Ypred):
    '''Calculate accuracies for theme classification

    Parameters
    ----------
    Ytrue : array of shape (n_obeservations, n_labels)
        Correct labels for the 12 text classifications

    Ypred : array of shape (n_obeservations, n_labels)
        Predicted labels for the 12 text classifications

    Returns
    -------
    results : a dataframe of evaluation metrics by class
    '''

    # Calculate overall accuarcies to print to screen
    overall_accuracy = metrics.accuracy_score(Ytrue, Ypred)
    hamming_loss = metrics.hamming_loss(Ytrue, Ypred)
    hamming_loss_zeros = metrics.hamming_loss(Ytrue,
                                              np.zeros((Ytrue.shape[0],
                                                        Ytrue.shape[1])))

    print('Overall Accuracy:', round(overall_accuracy, 4),
          '\nHamming Loss:', round(hamming_loss, 4),
          '\nHamming Loss (pred. zeros):', round(hamming_loss_zeros, 4))

    # Calculate individual accuracies and evaluation metrics for each class
    labels = ['CPD', 'CB', 'EWC', 'Exec', 'FWE', 'SP', 'RE', 'Sup', 'SW',
              'TEPE', 'VMG', 'OTH']
    Y_prop = []
    pred_prop = []
    error = []
    dummy_diff = []
    accuracies = []
    precision = []
    recall = []

    for i in np.arange(Ytrue.shape[1]):
        Y_prop.append(np.mean(Ytrue[:, i] == 1))
        pred_prop.append(np.mean(Ypred[:, i] == 1))
        error.append(1 - metrics.accuracy_score(Ytrue[:, i], Ypred[:, i]))
        dummy_diff.append(Y_prop[i] - error[i])
        accuracies.append(metrics.accuracy_score(Ytrue[:, i], Ypred[:, i]))
        precision.append(metrics.precision_score(Ytrue[:, i], Ypred[:, i]))
        recall.append(metrics.recall_score(Ytrue[:, i], Ypred[:, i]))

    results = pd.DataFrame({'Label': labels,
                            'Y_proportion': Y_prop,
                            'Pred_proportion': pred_prop,
                            'Error': error,
                            'Dummy_Diff': dummy_diff,
                            'Accuarcy': accuracies,
                            'Precision': precision,
                            'Recall': recall})

    return results
