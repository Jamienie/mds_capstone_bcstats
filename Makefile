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

all: test_predictions.pickle

###########################################################################
# Run the two scripts step by step to prepare datasets for modelling
###########################################################################

DESEN_FILE = data/interim/desensitized_qualitative-data2018.csv
RAW = data/raw/2018\ WES\ Qual\ Coded\ -\ Final\ Comments\ and\ Codes.xlsx
QUAL = data/interim/test_2018-qualitative-data.csv data/interim/train_2018-qualitative-data.csv


# 1. Desensitization text - identify sensitive text (people's names) and remove the comments entirely
# usage: make data/interim/desensitized_qualitative-data2018.csv
$(DESEN_FILE) : $(RAW) references/data-dictionaries/NationalNames.csv src/data/sensitive_text.py
		python src/data/sensitive_text.py -i data/raw/2018\ WES\ Qual\ Coded\ -\ Final\ Comments\ and\ Codes.xlsx -o data/interim/desensitized_qualitative-data2018.csv -s 1
		@echo $(RAW) references/data-dictionaries/NationalNames.csv $(DESEN_FILE)


# 2. Read 2018 desensitized qualitative data. Split for test/train
# usage: make data/interim/test_2018-qualitative-data.csv data/interim/train_2018-qualitative-data.csv
$(QUAL) : $(DESEN_FILE) src/data/split_qual_data.py
		python src/data/split_qual_data.py $(DESEN_FILE) $(QUAL)

###########################################################################
# Run the these scripts step by step to build baseline model
# for text classification -- Bag of Words with LinearSVC
###########################################################################

# 1. Preprocess text and fit Bag of Words Vectorizer
# usage: make src/models/bow_vectorizer.pickle
bow_vectorizer.pickle : data/interim/train_2018-qualitative-data.csv src/features/bow_vectorizer.py
		python src/features/bow_vectorizer.py -i data/interim/train_2018-qualitative-data.csv
		@echo data/interim/train_2018-qualitative-data.csv src/models/bow_vectorizer.pickle

# 2. Transform comments to a matrix of token counts for training data
# usage: make data/processed/X_train_bow.npz
data/processed/X_train_bow.npz : data/interim/train_2018-qualitative-data.csv src/data/preprocessing_text.py src/features/vectorize_comments.py
		python src/features/vectorize_comments.py -i data/interim/train_2018-qualitative-data.csv -o data/processed/X_train_bow.npz
		@echo data/interim/train_2018-qualitative-data.csv data/processed/X_train_bow.npz

# 3. Transform comments to a matrix of token counts for test data
# usage: make data/processed/X_test_bow.npz
data/processed/X_test_bow.npz : data/interim/test_2018-qualitative-data.csv src/data/preprocessing_text.py src/features/vectorize_comments.py
		python src/features/vectorize_comments.py -i data/interim/test_2018-qualitative-data.csv -o data/processed/X_test_bow.npz
		@echo data/interim/test_2018-qualitative-data.csv data/processed/X_test_bow.npz

# 4. Train Lienar Classifer
# usage: make src/models/linearsvc_model.pickle

INPUT_TRAIN_LINEAR = data/interim/train_2018-qualitative-data.csv data/processed/X_train_bow.npz

src/models/linearsvc_model.pickle : $(INPUT_TRAIN_LINEAR) src/models/linearsvc.py
		python src/models/linearsvc.py $(INPUT_TRAIN_LINEAR) src/models/linearsvc_model.pickle


###########################################################################
# Run the these scripts step by step to build deep learning model with
# pre-trained embeddings for text classification -- ensamble method
###########################################################################

EMBED_PICKLES = src/models/embed_tokenizers.pickle src/models/embed_matrices.pickle

# 1. Preprocess text, fit tokenizers, and build embedding matrices
# usage: make src/models/embed_tokenizers.pickle src/models/embed_matrices.pickle
$(EMBED_PICKLES) : data/interim/train_2018-qualitative-data.csv src/features/keras_embeddings.py
		python src/features/keras_embeddings.py -i data/interim/train_2018-qualitative-data.csv
		@echo data/interim/train_2018-qualitative-data.csv
		@echo $(EMBED_PICKLES)

# 2. Transform comments into coded numbers for training data
# usage: make data/processed/X_train_encoded.pickle
data/processed/X_train_encoded.pickle : data/interim/train_2018-qualitative-data.csv  src/features/encode_comments.py
		python src/features/encode_comments.py -i data/interim/train_2018-qualitative-data.csv -o data/processed/X_train_encoded.pickle
		@echo data/interim/train_2018-qualitative-data.csv data/processed/X_train_encoded.pickle

# 3. Transform comments into coded numbers for test data
# usage: make data/processed/X_test_encoded.pickle
data/processed/X_test_encoded.pickle : data/interim/test_2018-qualitative-data.csv  src/features/encode_comments.py
		python src/features/encode_comments.py -i data/interim/test_2018-qualitative-data.csv -o data/processed/X_test_encoded.pickle
		@echo data/interim/test_2018-qualitative-data.csv data/processed/X_test_encoded.pickle

# 4. Train Bidirectonal GRU
# usage: make src/models/biGRU_models.pickle
src/models/biGRU_models.pickle : data/interim/train_2018-qualitative-data.csv src/models/embed_matrices.pickle data/processed/X_train_encoded.pickle src/models/biGRU.py
		python src/models/biGRU.py
		@echo data/interim/train_2018-qualitative-data.csv src/models/embed_matrices.pickle data/processed/X_train_encoded.pickle
		@echo src/models/biGRU_models.pickle

# 5. Train convulutional neural net
# usage: make src/models/conv1d_models.pickle
src/models/conv1d_models.pickle : data/interim/train_2018-qualitative-data.csv src/models/embed_matrices.pickle data/processed/X_train_encoded.pickle src/models/conv1d.py
		python src/models/conv1d.py
		@echo data/interim/train_2018-qualitative-data.csv src/models/embed_matrices.pickle data/processed/X_train_encoded.pickle
		@echo src/models/conv1d_models.pickle

###########################################################################
# Generate themem predictions for test data
###########################################################################

# 1. Predict themems for test data
# usage: make data/output/test_predictions.pickle
data/output/test_predictions.pickle : data/interim/train_2018-qualitative-data.csv src/models/linearsvc_model.pickle data/processed/X_test_encoded.pickle src/models/conv1d_models.pickle src/models/biGRU_models.pickle src/models/theme_classification.py
		python src/models/theme_classification.py
		@echo data/interim/train_2018-qualitative-data.csv src/models/linearsvc_model.pickle data/processed/X_test_encoded.pickle src/models/conv1d_models.pickle
		@echo data/output/test_predictions.pickle





###########################################################################
# Remove all files
###########################################################################

clean:
	rm -f data/interim/desensitized_qualitative-data2018.csv
	rm -f data/interim/test_2018-qualitative-data.csv
	rm -f data/interim/train_2018-qualitative-data.csv
	rm -f src/models/bow_vectorizer.pickle
	rm -f data/processed/X_train_bow.npz
	rm -f data/processed/X_test_bow.npz
	rm -f src/models/linearsvc_model.pickle
	rm -f src/models/embed_tokenizers.pickle
	rm -f src/models/embed_matrices.pickle
	rm -f data/processed/X_train_encoded.pickle
	rm -f data/processed/X_test_encoded.pickle
	rm -f src/models/biGRU_models.pickle
	rm -f src/models/conv1d_models.pickle
	rm -f data/output/test_predictions.pickle
