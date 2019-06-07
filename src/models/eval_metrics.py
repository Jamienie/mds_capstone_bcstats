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
    Y_count = []
    pred_count = []
    error = []
    dummy_diff = []
    accuracies = []
    precision = []
    recall = []

    for i in np.arange(Ytrue.shape[1]):
        Y_count.append(np.sum(Ytrue[:, i] == 1))
        pred_count.append(np.sum(Ypred[:, i] == 1))
        error.append(1 - metrics.accuracy_score(Ytrue[:, i], Ypred[:, i]))
        dummy_diff.append((np.mean(Ytrue[:, i] == 1)) - error[i])
        accuracies.append(metrics.accuracy_score(Ytrue[:, i], Ypred[:, i]))
        precision.append(metrics.precision_score(Ytrue[:, i], Ypred[:, i]))
        recall.append(metrics.recall_score(Ytrue[:, i], Ypred[:, i]))

    results = pd.DataFrame({'Label': labels,
                            'Y_count': Y_count,
                            'Pred_count': pred_count,
                            'Error': error,
                            'Dummy_Diff': dummy_diff,
                            'Accuarcy': accuracies,
                            'Precision': precision,
                            'Recall': recall})

    return results


def subtheme_results(Ytrue, Ypred):
    '''Calculate accuracies for subtheme classification

    Parameters
    ----------
    Ytrue : array of shape (n_obeservations, n_labels)
        Correct labels for the 62 text classifications

    Ypred : array of shape (n_obeservations, n_labels)
        Predicted labels for the 62 text classifications

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
    labels = ['CPD_Improve_new_employee_orientation',
              'CPD_Improve_performance_management',
              'CPD_Improve_training',
              'CPD_Provide_opportunities_advancement',
              'CPD_other',
              'CB_Ensure_salary_parity_across_gov',
              'CB_Ensure_salary_parity_with_other_orgs',
              'CB_Improve_benefits',
              'CB_Increase_salary',
              'CB_Review_job_classifications',
              'CB_other',
              'EWC_Act_on_engagement',
              'EWC_Address_discrimination',
              'EWC_Improve_morale',
              'EWC_Treat_employees_better',
              'EWC_Value_diversity',
              'EWC - Other',
              'Exec_Improve_communication',
              'Exec_Improve_stability',
              'Exec_Strengthen_quality_of_executive_leadership',
              'Exec_other',
              'FWE_Leading_Workplace_Strategies',
              'FWE_Increase_flexibility_location',
              'FWE_Increase_flexibility_schedule',
              'FWE_other',
              'SP_Ensure_hiring_and_promotions_merit_based',
              'SP_Focus_on_HR_planning',
              'SP_Make_hiring_process_more_efficient',
              'SP_other',
              'RE_Enable_staff_to_make_decisions',
              'RE_Listen_to_staff_input',
              'RE_Make_better_use_of_skills',
              'RE_Provide_more_recognition',
              'RE_other',
              'Sup_Cultivate_effective_teamwork',
              'Sup_Hold_employees_accountable',
              'Sup_Strengthen_quality_of_supervisory_leadership',
              'Sup_Improve_communication_between_employees',
              'Sup_other',
              'SW_Hire_more_staff',
              'SW_Improve_productivity_and_efficiency',
              'SW_Review_workload_expectations',
              'SW_Support_a_healthy_workplace',
              'SW_other',
              'TEPE__Ensure_safety_and_security',
              'TEPE_Improve_facilities',
              'TEPE_Better_supplies_equipment',
              'TEPE_Better_furniture',
              'TEPE_Better_computer_hardware',
              'TEPE_Upgrade_improve_software',
              'TEPE_other',
              'VMG_Assess_plans_priorities',
              'VMG_Improve_collaboration',
              'VMG_Improve_program_implementation',
              'VMG_Public_interest_and_service_delivery',
              'VMG_Review_funding_or_budget',
              'VMG_Keep_politics_out_of_work',
              'VMG_other',
              'OTH_Other_related',
              'OTH_Positive_comments',
              'OTH_Survey_feedback',
              'Unrelated']

    Y_count = []
    pred_count = []
    error = []
    dummy_diff = []
    accuracies = []
    precision = []
    recall = []

    for i in np.arange(Ytrue.shape[1]):
        Y_count.append(np.sum(Ytrue[:, i] == 1))
        pred_count.append(np.sum(Ypred[:, i] == 1))
        error.append(1 - metrics.accuracy_score(Ytrue[:, i], Ypred[:, i]))
        dummy_diff.append(round(((np.mean(Ytrue[:, i] == 1)) - error[i]), 5))
        accuracies.append(metrics.accuracy_score(Ytrue[:, i], Ypred[:, i]))
        precision.append(metrics.precision_score(Ytrue[:, i], Ypred[:, i]))
        recall.append(metrics.recall_score(Ytrue[:, i], Ypred[:, i]))

    results = pd.DataFrame({'Label': labels,
                            'Y_count': Y_count,
                            'Pred_count': pred_count,
                            'Error': error,
                            'Dummy_Diff': dummy_diff,
                            'Accuarcy': accuracies,
                            'Precision': precision,
                            'Recall': recall})

    return results


def investigate_results(df, Y_true, Y_pred):
    '''Return a dataframe with the full comments and theme classifications
    compared to the predicted classifications

    Parameters
    ----------
    df: pandas Dataframe of with n_observations
        original validation or train data frame
    Y_train : array of shape (n_obeservations, n_labels)
        Correct labels for the 12 text classifications

    Y_pred : array of shape (n_obeservations, n_labels)
        Predicted labels for the 12 text classifications

    Returns
    -------
    df_results : a dataframe of the comments and classes
    '''

    wrong_index = df[np.sum(Y_pred != Y_true, axis=1) > 0].index

    themes = ['CPD', 'CB', 'EWC', 'Exec', 'FWE', 'SP',
              'RE', 'Sup', 'SW', 'TEPE', 'VMG', 'OTH']

    # Build dataframe with full comments, indices, and correct classes
    df_results1 = pd.DataFrame()
    df_results1['base_index'] = df.index
    df_results1['true'] = 1
    df_results1['comment'] = df.values

    for i, theme in enumerate(themes):
        df_results1[theme] = Y_true[:, i]

    # Build dataframe with full comments, indices, and predicted classes
    df_results2 = pd.DataFrame()
    df_results2['base_index'] = df.index
    df_results2['true'] = 0
    df_results2['comment'] = df.values

    for i, theme in enumerate(themes):
        df_results2[theme] = Y_pred[:, i]

    # Combine dataframes with true classes and predicted classees
    df_results = df_results1.append(df_results2, ignore_index=True) \
                            .sort_values(by=['base_index', 'true'])

    df_results['correct'] = [index not in wrong_index for
                             index in df_results.base_index]

    return df_results
