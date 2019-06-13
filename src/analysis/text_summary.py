# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 11:24:21 2019

@author: payla
"""

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import nltk


from src.data.preprocessing_text import clean_text
from src.data.preprocessing_text import replace_typical_misspell

# from nltk.corpus import stopwords
# stop_words = stopwords.words('english')

from gensim.models import KeyedVectors
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

from summa import summarizer
from gensim.summarization.summarizer import summarize as gensim_summarize



def generate_corpus_from_comments(data, depth=None, name=None, agreement=None, sentences=True):
    """
    Filters the data frame down to a specific subtopic or topic and agreement 
    level. If all the defaults are used it will generate a corpus for all the comments
    present. 
    
    Parameters
    ----------
    data: dataframe
        Dataframe with the columns USERID, theme, code, text and diff present if you are
        looking at agreement levels. 
    depth: str
        Either "theme" or "subtheme" or None. The default is none
        which will give counts for all comments. To use name or agreement
        this can not be set to None.
    name: str or integer
        Either input the name of the main theme (ex: "Executive", "Staffing Practices")
        or the number relating to the subtheme (ex: 12, 43, 102). The default is None
        which means it will do all the
    agreement: strr'
        Either input "all" to see all three levels together or input the level of agreement
        "strong", "weak", "no". Default is set to None which is for comments that have not
        be related to the multiple choice questions
    sentences: bool
        This either leaves the corpus as a single string or breaks it into sentences. The 
        default is true which breaks it into sentences
     
    Returns
    -------
    
    
        
    """

    data = data.copy()
    # filter to either theme or subtheme level
    if depth == "theme":
        if name not in data['theme'].unique():
            raise TypeError("theme not present in data")
        data = data[data["theme"] == name]
    if depth == "subtheme":
        if name not in data['code'].unique():
            raise TypeError("subtheme not present in data")       
        data = data[data["code"] == name]
    
    possible_agreements = ["strong", "weak", "no", "all", None]
    if agreement not in possible_agreements:
        raise TypeError("Entered wrong agreement level must be 'strong', 'weak' 'no', 'all', None")

    # filter when agreement level is present
    if agreement != None:
        agreement_dict = {"strong":0, "weak":1, "no":0}
        agreement_level = agreement_dict[agreement]
        data = data[data["diff"] == agreement_level]    

    # remove duplicate comments 
    data = data.drop_duplicates(subset=['USERID'])
    # add each comment to a list
    text = []
    for comment in data["text"]:
        text.append(comment)
    # combine list to be a single item
    text = ' '.join(text)
    
    
    if sentences == True:
        text = corpus_clean_sentences(text)
        sentences = nltk.sent_tokenize(text)
        return sentences
    
    if sentences == False:
        text = corpus_clean_sentences(text)
        return text


def corpus_clean_sentences(text):
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


    
def preprocess_corpus(text, stop_words=""):
    """
    Preprocesses the text for the fastText crawl pretrained embeddings.
    It removes all puncuation, fixes spelling to match vocab and removes
    stop words.
    
    Parameters
    ----------
    text: list
        List containing each sentence as an item
    stop_words: list or default
        If default selected a stop word list is supplied otherwise you
        can pass it your own
    
    Returns
    -------
    Returns preprocessed sentences in a list
    
    """
    
    if stop_words == "":
        stop_words = ["a", "to", "of", "and", "it"]

    preprocessed = []
    for sentence in text:
        # removes all puncuation
        x = clean_text(sentence)
        # fix spelling
        x = replace_typical_misspell(x)
        # remove stop words
        sentence_no_stopwords = []
        for word in x.split():
            if word not in stop_words:
                sentence_no_stopwords.append(word)
        processed_sentences = " ".join(sentence_no_stopwords)        
        preprocessed.append(processed_sentences)

    return preprocessed
    


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



def load_word_embeddings(file_path):
    """
    
    
    Parameters:
    file_path: str
        The file path to the downloaded embeddings 
    
    
    """
    
    embedd = KeyedVectors.load_word2vec_format(file_path)
    return embedd



def generate_summary_pagerank_pretrained_embedding(text, embedding, embedding_size=300, size_summary=5):
    """
    Uses pre-trained word embeddings to get the average sentence embedding. The similarity
    between each sentence is calculated and stored in a graph. PageRank is then used to 
    determine the most relavent sentences.
    
    # Reference https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
    # some changes to the code from the blog
    
    Parameters
    ----------
    text: list
        Orginal form of the sentences which is used in the output of the summary so it is readable
        text compared to preprocessed text
    embedding: gensim.models.keyedvectors.Word2VecKeyedVectors
        Embeddings
    embedding_size: int
        The size of the word vectors. The default is 300.
    size_summary: int
        The number of sentences to be included in the summary. 
    
    Returns
    -------
    Returns a list with the top ranked sentences
    
    """
    # pre-process the text into sentences ready to be compared
    clean_sentences = preprocess_corpus(text)
    # get the average embedding for each sentence
    sentence_vectors = []
    for sentence in clean_sentences:
        # check if there is a sentence and make sure its not "" or " "
        if len(sentence) != 0:

            single_sentence_vect =[]
            for word in sentence.split():
                # need excpetion handling incase word not in the embedding 
                # generates a np.array with all zeros
                try:
                    w = embedding[word]
                except:
                    w = np.zeros((embedding_size,))
                # create vector of all words in a sentence
                single_sentence_vect.append(w)
            # get the average embedding for the sentence
            v = sum(single_sentence_vect)/(len(sentence.split()))        
        # if the sentence is blank just give it all zeros
        else:
            v = np.zeros((embedding_size,))

        sentence_vectors.append(v)  
        
        
           # similarity matrix
    sim_mat = np.zeros([len(text), len(text)])

    # add cosine similarity scores to the matrix
    for i in range(len(text)):
        for j in range(len(text)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,embedding_size), sentence_vectors[j].reshape(1,embedding_size))[0,0]

    # create graph from cosine matrix: nodes represent sentences
    # edges represent similarity scores between sentences
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
   # sort by score
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(text)), reverse=True)
    # output top n sentences
    
    top_n = []
    for i in range(size_summary):
        top_n.append(ranked_sentences[i][1])
    
    return top_n 
        
        
def generate_summary_summa(text, size_summary=200):
    """
    Performs text summary from summa summarizer
    
    Parameters
    ----------
    text: list
        A list of sentences
    
   
    """
    
    # still need to cross references it back to pre-preproccess so it has better grammar
    # but good enough for now
    
    text = preprocess_corpus(text)
    text = ". ".join(text)
    
    return summarizer.summarize(text, words=size_summary, split=True)
    
    
    
    
    
def generate_summary_gensim(text, size_summary=200):
    """
    Performs text summary from gensim summarizer 
    
    
    Parameters
    ----------
    text: list
        A list of sentences
    
    """
    
    text = preprocess_corpus(text)
    text = ". ".join(text)
    
    return gensim_summarize(text, word_count=size_summary, split=True)
    
    
    
    
    
    
    