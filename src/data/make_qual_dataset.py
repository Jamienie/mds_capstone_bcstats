#!/usr/bin/env python 
# Author: Fan Nie
# Date: May 2019
# This script file includes the "df_combine" function which read in 2015 and 2018 comment files, standardize the column names, select the 12 main themes and 
# combine them into one csv file.

# Dependencies: argparse, pandas, numpy

# Usage with default 2015 and 2018 train datasets: python make_qual_dataset.py 

# Usage with 2015 and 2018 test datasets: python make_qual_dataset.py "../../data/interim/test_2015-qualitative-data.csv" "../../data/interim/test_2018-qualitative-data.csv" "../../data/interim/qual_combined_test.csv"

import pandas as pd

import argparse

parser = argparse.ArgumentParser(description='Write csv file for combined 2015 and 2018 qualitative datasets')
parser.add_argument('--input_2015_csv', '-i2015', type=str, dest="input_2015_qual_interim_filepath", action='store',
                     default='../../data/interim/train_2015-qualitative-data.csv',
                     help='input 2015 qual interim filepath')

parser.add_argument('--input_2018_csv', '-i2018', type=str, dest="input_2018_qual_interim_filepath", action='store',
                     default='../../data/interim/train_2018-qualitative-data.csv',
                     help='input 2018 qual interim filepath')

parser.add_argument('--output_csv', '-o', type=str, dest="output_combined_qual_csv_filepath" ,action='store',
                     default='../../data/interim/qual_combined_train.csv',
                     help="output combined qual csv filepath")
args = parser.parse_args()

def main():
    
    # standardize_columns
   
    # read in 2015 train csv file
    df_2015 = pd.read_csv(args.input_2015_qual_interim_filepath)
    #df_2015 = pd.read_csv(input_2015)

    
    # convert it to a dataframe
    df_2015 = pd.DataFrame(df_2015)
    df_2015['year_of_survey'] = 2015
    
    # rename 2015 column names so they match 2018 columns names
    df_2015.rename(columns={'2015 Comments':'comments',
            'Career_Personal_Development':'CPD','Compensation_Benefits':'CB',
            'Engagement_Workplace_Culture':'EWC','Executives':'Exec',
            'Flexible_Work_Environment':'FWE','Hiring_Promotion':'SP',
            'Recognition_Empowerment':'RE','Supervisors':'Sup',
            'Stress_Workload':'SW','Tools_Equipment_Physical_Environment':'TEPE'
            ,'Vision_Mission_Goals':'VMG','Other':'OTH'}, inplace=True)
    
    # only select the 12 main themes
    selected_columns = ["comments","CPD","CB","EWC","Exec","FWE","SP","RE",
                       "Sup","SW","TEPE","VMG","OTH"]
    df_2015_selected = df_2015[selected_columns]
    #print(df_2015_selected.head())  --- working
   
    # readin 2018 train csv file
    df_2018 = pd.read_csv(args.input_2018_qual_interim_filepath)
    
    # convert it to a dataframe
    df_2018 = pd.DataFrame(df_2018)
    df_2018['year_of_survey'] = 2018
    df_2018.rename(columns={'2018 Comment':'comments'}, inplace=True)
    # only select the 12 main themes
    df_2018_selected = df_2018[selected_columns]
    #print(df_2018_selected.head())  --- working
    
    # combine 2015 and 2018 files
    frames = [df_2015_selected, df_2018_selected]
    df_combined = pd.concat(frames,ignore_index=True)
    #print(df_combined.head())
    # write the joined file to a csv files
    df_combined.to_csv(args.output_combined_qual_csv_filepath)
    


# call main function
if __name__ == "__main__":
    main()