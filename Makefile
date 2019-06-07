# Makefile
# Authors: Fan Nie
# Date: June 2019
#
# Purpose: This script is use to automate our data analysis project pipline
# Useage:
# 		- make <specific script name>
#		- make all
#		- make clean


############################################################################
# Run all scripts at once
############################################################################

all: reports/final_report.md

###########################################################################
# Run the three scripts step by step to prepare datasets for analysis
###########################################################################

DESEN_FILES = data/interim/desensitized_qualitative-data2015.csv data/interim/desensitized_qualitative-data2018.csv
RAW = data/raw/WES2015_Final_Qual_Results.xlsx data/raw/2018 WES Qual Coded - Final Comments and Codes.xlsx
QUAL_TEST = data/interim/test_2015-qualitative-data.csv data/interim/test_2018-qualitative-data.csv
QUAL_TRAIN = data/interim/train_2015-qualitative-data.csv data/interim/train_2018-qualitative-data.csv
QUAL = data/interim/test_2015-qualitative-data.csv data/interim/test_2018-qualitative-data.csv data/interim/train_2015-qualitative-data.csv data/interim/train_2018-qualitative-data.csv

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
# Run the these scripts step by step to qualitative data classification
###########################################################################



#####################################
# Generate report
#####################################

doc/vancouver_bike_report.md : doc/vancouver_bike_report.Rmd results/figures/viz_exploratory.png results/figures/bike_boxplot.png results/analysis_summary.csv
	Rscript -e "rmarkdown::render('doc/vancouver_bike_report.Rmd')"

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
