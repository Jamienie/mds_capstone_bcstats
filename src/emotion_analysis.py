# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 11:24:21 2019

@author: payla
"""

import spacy
from spacy.matcher import Matcher 
nlp = spacy.load('en_core_web_sm')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random


def create_emotion_matcher(emotion_lexicon):
    """
    Adds all the rules per emotion from a lexicon to the SpaCy Matcher 
    
    Parameters
    -----------
    emotion_lexicon: dataframe 
        Dataframe that has the words to be added to rules of the matcher 
        in a column named 'term'
        
    Returns
    -------
    Matcher: Spacy Object
        SpaCy matcher with all the words from the emotion lexicon added
        
    Example
    -------
    anger_matcher = create_emotion_matcher(anger)
    
    """
    matcher = Matcher(nlp.vocab)
    for word in emotion_lexicon['term']:
        dict_rule = {"LOWER" : word}  
        matcher.add(word, None, [dict_rule])
        
    
    if not len(matcher) == emotion_lexicon.shape[0]:
        raise TypeError("Not all words were added to matcher")
        
    return matcher


def emotion_strength(text, matcher, emotion_lexicon):
    """
    Gets the strength of the emotion
    
    Parameters
    -------
    text: SpaCy tokens 
        Give it the text to calculate emotion. This can be a word, sentence,
        comment or document level. All words must be lower case or they 
        won't match with the matcher rules properly.
    matcher: SpaCy Matcher
        Matcher with the rules already created
    emotion_lexicon: dataframe
        Name of the emotion lexicon to relate the rule to the 
        strength of the emotion (anger, fear, sad, joy). Must have 
        the words under 'term' column and scores under 'score' column. 
    
    Returns
    --------
    emotion_strength: sum
        Generates the strength of the emotion for the text 
    
    Example
    -------
    emotion_strength(docs, match_anger, anger)
    
    """
    emotion_strength = []
    for i in range(len(text)):
        phrase_matches = matcher(text[i])
        # only parse through the non-zero lists 
        if len(phrase_matches) != 0:   
            count = 0
            # get the words from matched phrase
            for match_id, start, end in phrase_matches:       
                words = []
                span = text[i][start:end] 
                
                if not str(span).islower() == True:
                    raise TypeError("Text is not lowercase")
                
                words.append(span.text)
                # sum of strength of words by cross referencing emotion lexicon
                for j in words:
                    value = emotion_lexicon[emotion_lexicon["term"] == j]['score'].tolist()[0]
                    count = value + count              
            emotion_strength.append(count)
        else:
            emotion_strength.append(0)
    return emotion_strength


def one_hot_emotions(data):
    """
    Removes all the emotionless comments, labels the emotion of the comment based on the
    maximum emotion score and then converts the data to be one-hot encoding for the labels.
    It groups by the code and differences to ready the data for plotting.
    
    Parameters
    ----------
    data: dataframe
        Dataframe with columns userid, code, diff, and the sum of the emotion scores
        for each comment
    Returns
    -------
    Cleaned dataframe that has emotion counts per subtheme and agreement level
    
    """
    # remove the emotionless comments
    data = data[((data['anger']!=0)|(data['fear']!=0)|(data['joy']!=0)|(data['sad']!=0))]
    # obtains the max emition for each comment and adds them to a new column
    data['encode'] = data[["anger", "fear", "sad", "joy"]].idxmax(1).tolist()
    # select columns from orginal data and add to 1 hot encoding of emotions
    df_reduced = data[['USERID', 'code', 'diff']]
    df_one_hot = pd.concat([df_reduced, pd.get_dummies(data['encode'])], axis=1)
    # obtains counts for each sub theme and agreement level
    df_one_hot = df_one_hot.groupby(['code', 'diff'], as_index=False).sum()
    return df_one_hot

    
def filter_subtheme(subtheme, agreement, data):
    """
    Filters the dataframe for to the subtheme and agreement level
    
    Parameters
    ----------
    subtheme: int
        The number of the subtheme 
    agreement: str or int
        Either the agreement number of 0, 1, 2 or "all"
    data: dataframe
        Data with the strength of each comment per the 4 emotions
    
    Returns
    -------
    Dataframe with the counts of each emotion filtered to the subtheme
    
    Example
    -------
    filter_subtheme(12, "all", data)
    filter_subtheme(12, 0, data)
    
    """
    df_counts = one_hot_emotions(data)
    
    if type(agreement) == int:
        if agreement in [0, 1, 2]:
            # filter to the agreement level
            df_plot = df_counts[(df_counts['code'] == subtheme) & (df_counts['diff'] == agreement)]
            return df_plot
            
    if agreement == "all":
        df_plot = df_counts[(df_counts['code'] == subtheme)]
        return df_plot
    
    
    
def create_bar_plot(agreement, data, title):
    """
    Generates bar plots of for a subtheme and agreement level. If agreement="all"
    one plot is generated with all three levels, if a single level is selected only
    that plot will appear. 
    
    Parameters
    ----------
    agreement: str or int
        Either 0, 1, 2 or "all"
    data: dataframe
        Counts are grouped by subtheme and agreement level for each emotion. 
        Dataframe must be in long form where there is a column for each emotion. 
    title: str
        the title including the subtheme and agreement level included
    """
    
    ax = data.plot.bar(rot=0, 
                     x='diff', 
                     y=['anger', 'fear', 'joy', 'sad'], 
                     color=['crimson', 'lightgreen', 'orchid', 'lightblue'])
    plt.xlabel("")
    plt.title(title) 
    plt.legend(bbox_to_anchor=(1.24, 0.85), loc="upper right") 
        
        
    if agreement == "all":
        ind = np.arange(data.shape[0])
        ax.set_xticks(ind)
        ax.set_xticklabels(('Strong', 'Weak', 'None'));
    if agreement == 0:
        ax.set_xticklabels(labels=["Strong"]);
    if agreement == 1:
        ax.set_xticklabels(labels=["Weak"]);
    if agreement == 2:
        ax.set_xticklabels(labels=["None"]);
        

def plot_data(subtheme, agreement, data):
    """
    Parameters
    ----------
    theme: str or integer
        Either input the name of the main theme or the number relating to the subtheme
    agreement: str
        Either input "all" to see all three levels together or input the level of agreement
        "strong", "weak", "none"
    data: dataframe
        Data with the strength of each comment per the 4 emotions
        
    Returns
    -------
    For all it will return 3 plots, for strong, weak and none it will return a single bar plot
        
    """

    possible_subthemes = data['code'].unique()
    if subtheme not in possible_subthemes:
        raise TypeError("Subtheme not present in data")
    
    possible_agreements = ["strong", "weak", "medium", "all"]
    if agreement not in possible_agreements:
        raise TypeError("Entered wrong agreement level")
    
    if agreement == "all":
        title = "Counts of Comments Emotions for Subtheme " + str(subtheme) + " - "+ agreement.capitalize() + " Agreement Levels"
        data_plot = filter_subtheme(subtheme, agreement, data)
        create_bar_plot(agreement, data_plot, title)
        
    elif agreement == "strong":
        title = "Counts of Comments Emotions for Subtheme " + str(subtheme) + " - "+ agreement.capitalize() + " Agreement"
        agreement = int(0)
        data_plot = filter_subtheme(subtheme, agreement, data)
        create_bar_plot(agreement, data_plot, title)
        
    elif agreement == "weak":
        title = "Counts of Comments Emotions for Subtheme " + str(subtheme) + " - "+ agreement.capitalize() + " Agreement"
        agreement = int(1)
        data_plot = filter_subtheme(subtheme, agreement, data)
        create_bar_plot(agreement, data_plot, title)
    elif agreement == "none":
        title = "Counts of Comments Emotions for Subtheme " + str(subtheme) + " - "+ "No Agreement"
        agreement = int(2)
        data_plot = filter_subtheme(subtheme, agreement, data)
        create_bar_plot(agreement, data_plot, title)

        

def examine_emotion_scoring(data, emotion, lexicon):
    """
    Prints comments, emotion values, related words and thier scores. This 
    is used to help understand the specifics 
    
    Parameters
    ----------
    data: dataframe
        Dataframe with the userid, subtheme, level of agreement, comments and
        total emotion score
    emotion: str
        Filters to comments related to the emotion of "anger", "fear",
        "joy", or "sad"
    lexicon: dataframe
        Emotion lexicon with words and score values
        
    Returns
    -------
    Displays the sum of the comment emotions scores, the max score, specific emotion
    words and their score.
    
    Example
    -------
    examine_emotion_scoring(df, "joy",lexicon, anger, fear, joy, sad)
    
    """
    # get the max emotion and one hot-encoding
    data = data[((data['anger']!=0)|(data['fear']!=0)|(data['joy']!=0)|(data['sad']!=0))]
    data['encode'] = data[["anger", "fear", "sad", "joy"]].idxmax(1).tolist()
    df_one_hot = pd.concat([data, pd.get_dummies(data['encode'], prefix="c")], axis=1)
    df_one_hot = df_one_hot[['USERID', 'code', 'diff', 'clean_text', 
                   'anger', 'fear', 'sad', 'joy', 'c_anger', 'c_fear', 'c_sad', 'c_joy']]
    # create dataframes for filter condition
    if emotion == "anger":
        df1 = df_one_hot[df_one_hot['c_anger'] == 1]
        row = random.randint(1, df1.shape[0])
    if emotion == "fear":
        df1 = df_one_hot[df_one_hot['c_fear'] == 1]
        row = random.randint(1, df1.shape[0])
    if emotion == "joy":
        df1 = df_one_hot[df_one_hot['c_joy'] == 1]
        row = random.randint(1, df1.shape[0])
    if emotion == "sad":
        df1 = df_one_hot[df_one_hot['c_sad'] == 1]
        row = random.randint(1, df1.shape[0])
    # print row of dataframe
    display(df1.iloc[[row]])
    print("")
    print("Comment \n",  df1['clean_text'].tolist()[row])
    single_comment = nlp(df1['clean_text'].tolist()[row])
    print("\n")
    # create dataframes for each emotions 
    anger = lexicon[lexicon['AffectDimension']=='anger']
    fear = lexicon[lexicon['AffectDimension']=='fear']
    sad = lexicon[lexicon['AffectDimension']=='sadness']
    joy = lexicon[lexicon['AffectDimension']=='joy']
    # prints related words for each emotion
    matches_anger = create_emotion_matcher(anger)(single_comment)
    print("ANGER")
    print("-----")
    for match_id, start, end in matches_anger:       
        words = []
        span = str(single_comment[start:end])
        value = anger[anger["term"] == span]['score'].tolist()[0]
        print("{0} {1:.3f}".format(span, value))
    print("\n")
    matches_fear = create_emotion_matcher(fear)(single_comment)
    print("FEAR")
    print("----")
    for match_id, start, end in matches_fear:       
        words = []
        span = str(single_comment[start:end])
        value = fear[fear["term"] == span]['score'].tolist()[0]
        print("{0} {1:.3f}".format(span, value))  
    print("\n")
    matches_sad = create_emotion_matcher(sad)(single_comment)
    print("SAD") 
    print("---")
    for match_id, start, end in matches_sad:       
        words = []
        span = str(single_comment[start:end])
        value = sad[sad["term"] == span]['score'].tolist()[0]
        print("{0} {1:.3f}".format(span, value))  
    print("\n")    
    matches_joy = create_emotion_matcher(joy)(single_comment)
    print("JOY")
    print("---")
    for match_id, start, end in matches_joy:       
        words = []
        span = str(single_comment[start:end])
        value = joy[joy["term"] == span]['score'].tolist()[0]
        print("{0} {1:.3f}".format(span, value))
        
def summary_number_comment(data, threshold, include=False):
    """
    Prints summary info about the number of comments and emotionless comments
    
    Parameters
    ----------
    data: dataframe
        Dataframe with the sum of emotion per comment
    
    threshold: float or int
        Value to find the number of comments with a sum of joy less than the threshold
    
    """
    data['encode'] = data[["anger", "fear", "sad", "joy"]].idxmax(1).tolist()
    
    df_no_all_zeros = data[((data['anger']!=0)|(data['fear']!=0)|(data['joy']!=0)|(data['sad']!=0))]
    
    
    df_joy = df_no_all_zeros[((df_no_all_zeros['joy'] != 0) & 
                              (df_no_all_zeros['anger'] == 0) & 
                              (df_no_all_zeros['fear'] == 0) & 
                              (df_no_all_zeros['sad'] == 0))]
    
    number_of_only_joy = df_joy[df_joy['joy'] < threshold].shape[0]
    
    if include == True:
        print("Total Number of Comments", data.shape[0])
        print("Remaining comments when all 4 emotions are zero", df_no_all_zeros.shape[0])
        print("Where joy is the only emotion with a score", df_joy.shape[0])
    print("Number of comments {1} with only joy and a sum score less than {0}".format(threshold, 
                                                                        number_of_only_joy))


