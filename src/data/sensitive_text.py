# sensitive_text.py
# Author: Aaron Quinton
# Date: 2019-05-16

# USAGE: This script defines a function to identify comments that contain
# senstive information. To use you need to have the NationalNames.csv on your
# local computer. The csv can be downloaded on kaggle at the following link:
# https://www.kaggle.com/kaggle/us-baby-names#NationalNames.csv

import pandas as pd
import spacy

# File Paths to read in datadictionary
filepath_names = "./references/data-dictionaries/NationalNames.csv"


###############################################################################
# Create name_check list based on US Census data to be used in the function   #
###############################################################################

# Read in data dictionary
df_names = pd.read_csv(filepath_names)
name_check = df_names.Name.unique().tolist()

# Names that are in the names list and NER labels as Person, but are not
# actually sensitive. ie. they are false positives
false_names = ['Sheriff', 'Law', 'Child', 'Warden', 'Care', 'Cloud', 'Honesty',
               'Maple', 'Marijuana', 'Parks', 'Ranger', 'Travel', 'Young',
               'Branch', 'Field', 'Langford', 'Surrey', 'Cap', 'Lean', 'Van',
               'Case', 'Min', 'Merit', 'Job', 'Win', 'Forest', 'Victoria']

# Drop the false_names from the names list
name_check = list(set(name_check).difference(set(false_names)))

# Names that are not in the names list, but should be! ie. false negatives
missing_names = ['Kristofferson']

# Add missing names
for missing_name in missing_names:
    name_check.append(missing_name)


###############################################################################
# Define function to check if text is sensitive and needs to be removed       #
###############################################################################

def sensitive_index(comments):
    """Return a list of indices identifying comments with sensitive information
    given a list of comments"""

    # Apply Named entity recognition on list of comments
    nlp = spacy.load("en_core_web_sm")
    docs = [nlp(comment) for comment in comments]

    # Create a list of the words tagged as PERSON and the original index
    person_index = []
    person_list = []
    for index, doc in enumerate(docs):
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                person_index.append(index)
                person_list.append(ent.text)

    # Cross check a name dictionary to confirm names
    sensitive_person = []
    sensitive_person_index = []
    for index, person in enumerate(person_list):
        for name in person.split():
            if name in name_check:
                sensitive_person.append(person)
                sensitive_person_index.append(person_index[index])
                break

    return sensitive_person_index
