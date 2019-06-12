# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 11:24:21 2019

@author: payla
"""

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
stop_words = stopwords.words('english')
import networkx as nx
import nltk
from sklearn.metrics.pairwise import cosine_similarity

def comment_to_corpus(data, col_name):
    """
    Takes comments from dataframe to a single document

    Parameters
    ----------
    data: dataframe
        Dataframe that contains the text
    col_name: str
        Name of the column that contains the text

    Returns
    -------
    Returns the text combined into a single string
    """
    text = []
    for comment in data[col_name]:
        text.append(comment)
    # combine list to be a single item
    text = ' '.join(text)
    return text

def corpus_prep_sentences(text):
    """
    Takes a string and cleans it so sentence tokenization works better

    Parameters
    ----------
    text: str
        Text to be cleaned
    Returns
    -------
    Returns string that is ready for sentence tokenization
    """

    # change semi-colon (;) to .
    text = re.sub(r';', '.', text)
    # change * to no space
    text = re.sub(r'\*', '', text)
    # if more then 3 spaces add .
    text = re.sub(r'   ', '.', text)
    # change all ... to ' '
    text = re.sub(r'\.{3}', ' ', text)
    # change i.e. to ie
    text = re.sub(r'i\.e\.', 'ie', text)
    # change i.e. to ie
    text = re.sub(r'Ie\.', 'ie', text)
    # change etc. to etc
    text = re.sub(r'etc\.', 'etc', text)
    # change e.g. to eg
    text = re.sub(r'e\.g\.', 'eg', text)
    # change E.g. to eg
    text = re.sub(r'E\.g\.', 'eg', text)
    # change E.g. to eg
    text = re.sub(r'eg\.', 'eg', text)
    # any sentences that have .words change to . words or, words
    text = re.sub(r'([\.,])(\S)', r'\1 \2', text)
    # change - to .
    ## this will cause some poor text but overall it will split up really long sentences
    text = re.sub(r'\s-\s', '. ', text)
    # remove double spaces
    text = re.sub(r'  ', ' ', text)
    # remove all 1) etc
    text = re.sub(r'\d\)', '', text)
    # change any . . to .
    text = re.sub(r'\.\s\.', '. ', text)
    # change any ' '-
    text = re.sub(r'(\s-)', ' ', text)
    # change ADM to adm because it was not splitting on ADM.
    # slightly ugly because adds an extra . but splits it now
    text = re.sub(r'ADM\.', 'ADM. .', text)
    # remove all 1. etc
    text = re.sub(r'\d\.', '', text)

    return text



def sentence_eda(sentences, word_plot=False, character_plot=False):
    """
    Input list of sentences and get the mean, median, max, min number of words per sentence.
    The average mean, median, max and min number of characters per sentence.
    If plot = True, it outputs a histogram of the distribution of sentence length
    """
    # count the number of characters per sentence
    counts_char = []
    for chracters in sentences:
        counts_char.append(len(chracters))
    minimum_char = min(counts_char)
    maximum_char = max(counts_char)
    mean_char = np.mean(counts_char)
    median_char = np.median(counts_char)

    if character_plot == True:
        fig=plt.figure(figsize=(10, 6))
        plt.hist(counts_char, 50)
        plt.title("Number of characters per sentence", fontsize=16)
        plt.xlabel('Number of characters', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.show();

    # count number of words per sentence
    counts_words = []
    for words in sentences:
        counts_words.append(len(words.split()))
    minimum_word = min(counts_words)
    maximum_word = max(counts_words)
    mean_word = np.mean(counts_words)
    median_word = np.median(counts_words)

    if word_plot == True:
         fig=plt.figure(figsize=(10, 6))
         plt.hist(counts_words, 40)
         plt.title("Number of words per sentence", fontsize=16)
         plt.xlabel('Number of words', fontsize=14)
         plt.ylabel('Count', fontsize=14)
         plt.show();

    # create lists for the dataframe
    labels = ["min", "max", "mean", "median"]
    values_char = [minimum_char, maximum_char, mean_char, median_char]
    values_word = [minimum_word, maximum_word, mean_word, median_word]
    # create dataframe
    d = {'stats' : labels,
         'character values': values_char,
         'word values': values_word}
    df = pd.DataFrame(data=d).round(2)

    return df

def pre_processing(text):
    """
    Take tokenized sentences and further preprocessing by removing special characters,
    turning the text lowercase, and removing stopwords

    """
    # Credit to the blog listed below
    #https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
    clean_sentences = pd.Series(text).str.replace("[^a-zA-Z]", " ")

    clean_sentences = [s.lower() for s in clean_sentences]

    def remove_stopwords(sen):
        sen_new = " ".join([i for i in sen if i not in stop_words])
        return sen_new

    processed_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
    return processed_sentences


def summary_textrank(text, clean_sentences, num_summary):
    """
    Summarizes text using TextRank

    Parameters
    ----------
    text: list
        List of sentences that have been cleaned

    num_summary: int
        How many sentences for the summary

    Returns
    -------
    Returns a list of sentences that express the top ranked sentences


    Reference
    ---------
    This implementation is from https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
    credit to Prateek Joshi

    """
    # Credit to the blog listed below
    #https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/


    # read in the word embeddings
    file_path = "./references/pretrained_embeddings.nosync/glove/glove.twitter.27B.100d.txt"

    word_embeddings = {}
    f = open(file_path, encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()

    # create vectors for sentences
    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)

    # similarity matrix
    sim_mat = np.zeros([len(text), len(text)])

    # add cosine similarity scores to the matrix
    for i in range(len(text)):
        for j in range(len(text)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]

    # create graph from cosine matrix
    # nodes represent sentences
    # edges will represent similarity scores between sentences
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
   # sort by score
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(text)), reverse=True)
    # output top n sentences
    top_n = []
    for i in range(num_summary):
        top_n.append(ranked_sentences[i][1])
    return top_n
