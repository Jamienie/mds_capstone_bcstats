# preprocessing_text.py
# Authors: Aaron Quinton
# Date: 2019-05-15

# Many functions and the overall workflow have been built from a KDnuggets Blog
# written by Matthew Mayo:
# https://www.kdnuggets.com/2018/03/text-data-preprocessing-walkthrough-python.html


# Import modules
import re
import unicodedata
import contractions
import inflect
from pattern.en import suggest
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer


###############################################################################
# Define specific preprocessing tasks as individual funtions to be combined   #
###############################################################################

def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)


def to_lowercase(text):
    """Convert all characters in a string to lowercase"""
    return text.lower()


def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word)
        new_word = new_word.encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words


def reduce_lengthening(words):
    """Reduce greater than 2 repeating characters in a word"""
    new_words = []
    for word in words:
        pattern = re.compile(r"(.)\1{2,}")
        new_word = pattern.sub(r"\1\1", word)
        new_words.append(new_word)
    return new_words


def correct_spelling(words):
    """Correct all misspelled tokenized words in a list"""
    new_words = []
    for word in words:
        suggested_word = suggest(word)
        if suggested_word[0][1] > 0.75:
            new_word = suggested_word[0][0]
        else:
            new_word = word
        new_words.append(new_word)
    return new_words


def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual
    representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words


def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems


def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas


###############################################################################
# Combine preprocessing functions for overall
###############################################################################

def preprocess_text(text):
    text = replace_contractions(text)
    text = to_lowercase(text)
    words = word_tokenize(text)
    words = remove_non_ascii(words)
    words = reduce_lengthening(words)
    words = correct_spelling(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    words = stem_words(words)
    words = lemmatize_verbs(words)
    text = ' '.join(words)
    return text
