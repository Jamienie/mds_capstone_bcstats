# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 11:24:21 2019

@author: payla
"""


import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS)
import matplotlib.pyplot as plt


def word_frequency(text, max_features=200, min_df=10, ngram_range=(1, 1)):
    """
    Counts the word frequency in the given text
    
    Parameters
    ----------
    text: list
        The text to determine the word frequenies from
    max_features: int
        The max number of features for count vectorizer
    min_df: int
        The minimum frequency for a word to be added
    
    Returns
    -------
    Returns a data frame with the most frequent words and their counts
    
    """

    vect = CountVectorizer(min_df=min_df, 
                           max_features=max_features, 
                           stop_words="english",
                           ngram_range=ngram_range)
    term_doc_matrix = vect.fit_transform(text)
    words = vect.get_feature_names()

    word_counts = term_doc_matrix.sum(axis=0)
    word_count = []
    for i in word_counts.tolist():
        for j in i:
            word_count.append(j) 

    d = {"words":words, "counts":word_count}
    word_freq = pd.DataFrame(d)

    word_freq=word_freq.sort_values(by=["counts"], ascending=False)
    return word_freq


def generate_WordCloud(text, background_color="white", min_font_size=10, max_words=50, collocations=False):
    """
    Creates a word cloud from the given text
    
    Parameters
    ----------
    text: str
        Input to the wordcloud
        
        
    Returns
    -------
    Returns the wordcloud as a matplotlib plot
    
    """
    
    
    wordcloud = WordCloud(width = 800, 
                      height = 800, 
                      background_color = background_color, 
                      stopwords = stopwords, 
                      min_font_size =  min_font_size, 
                      max_words=max_words,
                      collocations=collocations
                     ).generate(text) 

    plt.figure(figsize = (10, 10)) 
    plt.imshow(wordcloud) 
    plt.axis("off") 

    return plt.show() 

    
    
    
    