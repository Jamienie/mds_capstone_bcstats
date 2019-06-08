# Makefile
# Authors: Fan Nie
# Date: June 2019
#
# Purpose: This script is use to automate our data analysis project pipline
# Useage:
# 		- make <specific file name>
#		- make all
#		- make clean


############################################################################
# Run all scripts at once
############################################################################

all: reports/final_report.md

###########################################################################
# Run the three scripts step by step to prepare datasets for
# (exploratory data) analysis 
###########################################################################

DESEN_FILES = data/interim/desensitized_qualitative-data2015.csv data/interim/desensitized_qualitative-data2018.csv
RAW = data/raw/WES2015_Final_Qual_Results.xlsx data/raw/2018\ WES\ Qual\ Coded\ -\ Final\ Comments\ and\ Codes.xlsx
QUAL_TEST = data/interim/test_2015-qualitative-data.csv data/interim/test_2018-qualitative-data.csv
QUAL_TRAIN = data/interim/train_2015-qualitative-data.csv data/interim/train_2018-qualitative-data.csv
QUAL = data/interim/test_2015-qualitative-data.csv data/interim/test_2018-qualitative-data.csv data/interim/train_2015-qualitative-data.csv data/interim/train_2018-qualitative-data.csv
TIDY_FILES = data/raw/WES\ 2007-2018\ LONGITUDINAL\ DATA.sav references/data-dictionaries/survey_mc_legend.csv references/data-dictionaries/Current\ Position\ with\ BU\ and\ Org\ Hierarchy\ -\ WES\ 2018.csv

# 1. Desensitization text - identify sensitive text (people's names) and remove the comments entirely
# usage: make data/interim/desensitized_qualitative-data2015.csv data/interim/desensitized_qualitative-data2018.csv
$(DESEN_FILES) : src/data/sensitive_text.py
		python src/data/remove_sensitive_data.py $(RAW) $(DESEN_FILES)

# 2. Read in 2015 and 2018 desensitized qualitative data. Split for test/train
# usage: make data/interim/test_2015-qualitative-data.csv data/interim/test_2018-qualitative-data.csv data/interim/train_2015-qualitative-data.csv data/interim/train_2018-qualitative-data.csv
$(QUAL) : $(DESEN_FILES) src/data/split_qual_data.py 
		python src/data/split_qual_data.py $(DESEN_FILES) $(QUAL)

# 3. combine 2015 and 2018 datasets into one csv file
# usage: make data/interim/qual_combined_train.csv
data/interim/qual_combined_train.csv : src/data/make_qual_dataset.py 
		python src/data/make_qual_dataset.py $(QUAL_TRAIN) data/interim/qual_combined_train.csv
        
###########################################################################
# Run the these scripts step by step to build baseline model 
# for text classification -- Bag of Words with LinearSVC
###########################################################################

SPLIT_FILES = data/interim/X_train_2018-qualitative-data.csv data/interim/X_valid_2018-qualitative-data.csv data/interim/Y_train_2018-qualitative-data.csv data/interim/Y_valid_2018-qualitative-data.csv
X_FIles = data/interim/X_train_2018-qualitative-data.csv data/interim/X_valid_2018-qualitative-data.csv
BOW_FILES = data/interim/X_train_bow.npz data/interim/X_valid_bow.npz 

# 1. Preprocessing and Data Preperation 2018 comment data
# usage: make data/interim/X_train_2018-qualitative-data.csv data/interim/X_valid_2018-qualitative-data.csv data/interim/Y_train_2018-qualitative-data.csv data/interim/Y_valid_2018-qualitative-data.csv
$(SPLIT_FILES) : data/interim/train_2018-qualitative-data.csv src/models/preprocessing_data_preperation.py 
		python src/models/preprocessing_data_preperation.py data/interim/train_2018-qualitative-data.csv $(SPLIT_FILES)

# 2. Build Bag of Words
# usage: make data/interim/X_train_bow.npz data/interim/X_valid_bow.npz
$(BOW_FILES) : $(X_FILES) src/data/preprocessing_text.py src/models/bow.py
		python src/models/bow.py $(X_FILES) $(BOW_FILES)        

# 3. Build LinearSVC model
# usage: make data/interim/Y_pred_bow.csv
data/interim/Y_pred_bow.csv: $(BOW_FILES) data/interim/Y_train_2018-qualitative-data.csv src/models/linearsvc.py
		python src/models/linearsvc.py $(BOW_FILES) data/interim/Y_train_2018-qualitative-data.csv data/interim/Y_pred_bow.csv


###########################################################################
# Run the these scripts step by step to build deep learning model with 
# pre-trained embeddings for text classification -- Keras model
###########################################################################




#####################################
# Generate report
#####################################



#####################################
# Remove all files
#####################################

clean:
	rm -f data/interim/desensitized_qualitative-data2015.csv
	rm -f data/interim/desensitized_qualitative-data2018.csv
	rm -f data/interim/test_2015-qualitative-data.csv 
	rm -f data/interim/test_2018-qualitative-data.csv
	rm -f data/interim/train_2015-qualitative-data.csv
	rm -f data/interim/train_2018-qualitative-data.csv
