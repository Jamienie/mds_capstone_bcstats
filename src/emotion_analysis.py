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

#

def create_emotion_matcher(emotion_lexicon):
    """
    Adds all the rules for the emotion from a lexicon to the SpaCy Matcher. The rule adds
    the words to the matcher all in lower case. 
    
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
    Gets the strength of the emotion for each comment. Strength is calculated
    by summing the scores for each word. 
    
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


def one_hot_emotions(data, groupby):
    """
    Removes all the emotionless comments, labels the emotion of the comment based on the
    maximum emotion score and then converts the data to be one-hot encoding for the labels.
    It groups by the code and differences to ready the data for plotting.
    
    Parameters
    ----------
    data: dataframe
        Dataframe with columns userid, code, diff, and the sum of the emotion scores
        for each comment
    groupby: str
        Variable the data needs to be grouped by, works for theme and subtheme levels
    
    Returns
    -------
    Cleaned dataframe that has emotion counts per subtheme and agreement level
    
    """
    # remove the emotionless comments
    data = data[((data['anger']!=0)|(data['fear']!=0)|(data['joy']!=0)|(data['sad']!=0))].copy()
    # obtains the max emition for each comment and adds them to a new column
    data['encode'] = data[["anger", "fear", "sad", "joy"]].idxmax(1).tolist()
    # select columns from orginal data and add to 1 hot encoding of emotions    
    df_reduced = data[['USERID', groupby, 'diff']]
    df_one_hot = pd.concat([df_reduced, pd.get_dummies(data['encode'])], axis=1)
    # obtains counts for each sub theme and agreement level
    df_one_hot = df_one_hot.groupby([groupby, 'diff'], as_index=False).sum()
    return df_one_hot

    
def filter_depth(name, col_name, agreement, data):
    """
    Filters the dataframe for to the subtheme and agreement level
    
    Parameters
    ----------
    name: str or integer
        Either input the name of the main theme or the number relating to the subtheme
    col_name: str
        Name of the column where the subtheme numbers or theme names are located
    agreement: str or int
        Either the agreement number of 0, 1, 2 or "all"
    data: dataframe
        Data with one-hot encoding with the counts of themes or subthemes by agreement level
    
    Returns
    -------
    Dataframe with the counts of each emotion filtered to the subtheme
    
    Example
    -------
    filter_depth(12, "all", data)
    filter_depth(12, 0, data)
    
    """
    
    if type(agreement) == int:
        if agreement not in [0, 1, 2]:
            raise TypeError("Agreement out of range")
            # filter to the agreement level
        df_plot = data[(data[col_name] == name) & (data['diff'] == agreement)]
        return df_plot
    if agreement == "all":
        df_plot = data[(data[col_name] == name)]
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
        
    Returns
    -------
    Bar plot with custom settings
        
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
        

def plot_data(depth, name, agreement, data):
    """
    Parameters
    ----------
    depth: str
        Either "theme" or "subtheme"
    name: str or integer
        Either input the name of the main theme (ex:"Executive", "Staffing Practices") 
        or the number relating to the subtheme (ex: 12, 43, 102)
    agreement: str
        Either input "all" to see all three levels together or input the level of agreement
        "strong", "weak", "none"
    data: dataframe
        Data with the strength of each comment per the 4 emotions
        
    Returns
    -------
    For all it will return 3 plots, for strong, weak and none it will return a single bar plot
        
    """
    
    if depth == "theme":
        depth = "main_theme"
        if depth not in data.columns:
            raise TypeError("name of column containing themes must be called 'main_theme'")
        if name not in data['main_theme'].unique():
            raise TypeError("theme not present in data")
        title_intro = "Counts of Comments Emotions by "
            
    if depth == "subtheme":
        depth = "code"
        if depth not in data.columns:
            raise TypeError("name of column containing subthemes must be called 'code'")
        if name not in data['code'].unique():
            raise TypeError("subtheme not present in data")
        title_intro = "Counts of Comments Emotions for Subtheme "
   
    possible_agreements = ["strong", "weak", "none", "all"]
    if agreement not in possible_agreements:
        raise TypeError("Entered wrong agreement level")
    
    if agreement == "all":
        title = title_intro + str(name) + " - "+ agreement.capitalize() + " Agreement Levels"
        df_counts = one_hot_emotions(data, depth)
        data_plot = filter_depth(name, depth, agreement, df_counts)
        create_bar_plot(agreement, data_plot, title)
        
    elif agreement == "strong":
        title = title_intro + str(name) + " - "+ agreement.capitalize() + " Agreement"
        agreement = int(0)
        df_counts = one_hot_emotions(data, depth)
        data_plot = filter_depth(name, depth, agreement, df_counts)
        create_bar_plot(agreement, data_plot, title)
        
    elif agreement == "weak":
        title = title_intro + str(name) + " - "+ agreement.capitalize() + " Agreement"
        agreement = int(1)
        df_counts = one_hot_emotions(data, depth)
        data_plot = filter_depth(name, depth, agreement, df_counts)
        create_bar_plot(agreement, data_plot, title)
        
    elif agreement == "none":
        title = title_intro + str(name) + " - "+ "No Agreement"
        agreement = int(2)
        df_counts = one_hot_emotions(data, depth)
        data_plot = filter_depth(name, depth, agreement, df_counts)
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
    examine_emotion_scoring(df, "joy", lexicon, anger, fear, joy, sad)
    
    """
    # create a copy to not overwrite orginal dataframe
    df = data.copy()
    # get the max emotion and one hot-encoding
    df = df[((df['anger']!=0)|(df['fear']!=0)|(df['joy']!=0)|(df['sad']!=0))].copy()
    df['encode'] = df[["anger", "fear", "sad", "joy"]].idxmax(1).tolist()
    df_one_hot = pd.concat([df, pd.get_dummies(df['encode'], prefix="c")], axis=1)    
    df_one_hot = df_one_hot[['USERID', 'code', 'diff', 'text', 'anger',
                             'fear', 'sad', 'joy', 'c_anger', 'c_fear', 'c_sad', 'c_joy']]
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
    print("Comment \n",  df1['text'].tolist()[row])
    single_comment = nlp(df1['text'].tolist()[row])
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
    inlcude: bool
        Default is false which only prints the threshold and number of joy comments below
        the threshold. If True is selected it prints the total number of comments, 
        number of comments after all emotionless comments are removed, and the count 
        of how many comments whre joy is the only score
    
    Returns
    -------
    Prints the total comments, the number of comments after all emotionless comments are 
    removed, count of how many comments only have joy as a score and the threshold with 
    the number of joy comments below the threshold
    
    Example
    -------
    summary_number_comment(df, 0.3, include=True)
    summary_number_comment(df, 0.3)
    
    """
    # make a copy so it doesn't overwrite original dataframe
    df = data.copy()
    # add new column with max value
    df['encode'] = df[["anger", "fear", "sad", "joy"]].idxmax(1).tolist()
    # filter out comments that are emotionless ie all emotions are zero
    df_no_all_zeros = df[((df['anger']!=0)|(df['fear']!=0)|(df['joy']!=0)|(df['sad']!=0))]
    # find comments that joy is only emotion
    df_joy = df_no_all_zeros[((df_no_all_zeros['joy'] != 0) & 
                              (df_no_all_zeros['anger'] == 0) & 
                              (df_no_all_zeros['fear'] == 0) & 
                              (df_no_all_zeros['sad'] == 0))]
    # set threshold to look into joy comments
    number_of_only_joy = df_joy[df_joy['joy'] < threshold].shape[0]
    if include == True:
        print("Total Number of Comments", data.shape[0])
        print("Remaining comments when all 4 emotions are zero", df_no_all_zeros.shape[0])
        print("Where joy is the only emotion with a score", df_joy.shape[0])
    print("Number of comments {1} with only joy and a sum score less than {0}".format(threshold, 
                                                                        number_of_only_joy))

    
def get_main_theme_codes(data, new_col_name):
    """
    Obtains the main theme numbers
    
    Parameters
    ----------
    data: dataframe
        Dataframe that has the subtheme codes present in a column named 'code'
    new_col_name: str
        Name of the new column with the main theme number
    
    Returns
    -------
    Returns a dataframe with a new column that has the main theme number
    
    Example
    -------
    get_main_theme_codes(df, "main_theme")
    
    """
    # create copy so original is not overwritten
    df = data.copy()
    # pull out first number or first two depending on the length of the subtheme code
    df[new_col_name] = pd.np.where(df['code'].astype(str).str.len()==2,
                                          df['code'].astype(str).str[0:1], 
                                          df['code'].astype(str).str[0:2])    
    return df


theme_dict = {
     "1": "Career & Personal Development",
     "2": "Compensation & Benefits",
     "3": "Engagement & Workplace Culture",
     "4": "Executives",
     "5": "Flexible Work Environment",
     "6": "Staffing Practices",
     "7": "Recognition & Empowerment",
     "8": "Supervisors",
     "9": "Stress & Workload",
     "10":"Tools, Equipment & Physical Environment",
     "11": "Vision, Mission & Goals",
     "12": "Other"}

def get_main_theme_label(theme_number, dictonary=theme_dict):
    """
    Converts the main theme number to the theme name
    
    Parameters
    ----------
    theme_number: str
        Number of the main theme
    dictonary: dict
        Mapping between theme numbers and theme names.
        
    Returns
    -------
    The name of the theme as per the matching in the dictonary
        
    Examples
    --------
    df["main_theme"].apply(get_main_theme_label)

    """
    return theme_dict[theme_number]
    
    
   
    

