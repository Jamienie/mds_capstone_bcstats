# tidy_quantitative_data.R 
# Author: Aaron Quinton
# Date: 2019-05-08

# Tidy's the raw quanititative data into two csv files, one with the scores
# on the multiple choice questions and engagement model, the second details
# the demographic and other employee info

# Require pkgs `foreign`, `sjlabelled`, and `tidyverse`
library(tidyverse)

# File input paths
filepath_spss = "./data/raw/WES 2007-2018 LONGITUDINAL DATA_short.sav"
filepath_legend = "./references/data-dictionaries/survey_mc_legend.csv"

# File output paths
filepath_out_questions = "./data/processed/tidy_quant_questions.csv"
filepath_out_info = "./data/processed/tidy_quant_demographics.csv"

  
###############################################################################
# Read quantitative data from SPSS file and read in legend to help select and #
# rename columns                                                              #
###############################################################################

# Removes labels from spss file for the multiple choice question data
df_spss <- foreign::read.spss(file = filepath_spss, 
                              to.data.frame = TRUE, 
                              use.value.labels = FALSE) %>% 
           sjlabelled::remove_all_labels()

# Keeps the labels from spss file for the employee info and demographic data
df_spss_labeled <- foreign::read.spss(file = filepath_spss, 
                                      to.data.frame = TRUE, 
                                      use.value.labels = TRUE)

# the csv used has been manually built to help make sense of all the columns in
# the spss file
df_legend <- read_csv(filepath_legend)


###############################################################################
# Build tidy dataframe with m.c. questions and engagement model: df_questions #
###############################################################################

# specify columns to select 
col_questions <- df_legend %>%
  filter(category == "Raw Survey Question" | 
         sub_category == "Engagement Model" |
         original_column_name == "USERID") %>% 
  pull(original_column_name)

# Rename columns, fix data types, and reorganize data frame. Rows used to be 
# unqiuely identified by USERID, it is now by USERID and survey_year
df_questions <- df_spss %>% 
  select(col_questions) %>% 
  gather(-USERID, key = "original_column_name", value = "temp_val") %>% 
  left_join(df_legend, by = "original_column_name") %>% 
  select(USERID, new_column_name, survey_year, temp_val) %>% 
  spread(key = new_column_name, value = temp_val) %>% 
  mutate_at(vars(-USERID), as.double)%>% 
  select(-contains("Q"), Q01:Q80) 



###############################################################################
# Build tidy dataframe of employee info variables: df_info                    #
###############################################################################

# specify columns to select
col_info <- df_legend %>% 
  filter(sub_category == "Employee Info" |
         sub_category == "Survey Info" |
         sub_category == "Demographic", 
         category != "Exclude",
         category != "Sensitive Info") %>% 
  pull(original_column_name)

# Rename columns, fix data types, and reorganize data frame
df_info <- df_spss_labeled %>% 
  select(col_info) %>% 
  gather(-USERID, key = "original_column_name", value = "temp_val") %>% 
  left_join(df_legend, by = "original_column_name") %>% 
  select(USERID, new_column_name, survey_year, temp_val) %>%
  spread(key = new_column_name, value = temp_val) %>% 
  mutate_if(is.character, str_squish) %>% 
  mutate_at(c("survey_year", "HIREYRS", "REGHOURS", "SRVCYRS", "SUPERVISEES"),
            as.double)

# Clean character columns to have consistent labels and convert to factors  
df_info <- df_info %>% 
  mutate_at(c("CITYGRP", "FRINGE_FLAG", "LOCATIONGRP", 
              "PSAREGION", "UNIONSTATUS"), as.factor) %>% 
  mutate(AGEGRP = case_when(
            AGEGRP == "< 35" | AGEGRP == "Less than 35"           ~ "<35",
            AGEGRP == "35-44.99" | AGEGRP == "35 to 44 years old" ~ "35-44",
            AGEGRP == "45-54.99" | AGEGRP == "45 to 54 years old" ~ "45-54",
            AGEGRP == "55 years or more"                          ~ "55+",
            TRUE                                                  ~ AGEGRP),
         AGEGRP = factor(AGEGRP, levels = c("<35", "35-44", "45-54", "55+")), 
         GENDER = case_when(
            GENDER == "Male"   ~ "M",
            GENDER == "Female" ~ "F",
            TRUE               ~ GENDER),
         GENDER = factor(GENDER, levels = c("F", "M")),
         HIREYRS_GRP = factor(HIREYRS_GRP, 
                              levels = c("Less than 3 years", 
                                         "3 to 9.99 years", 
                                         "10 to 19.99 years",
                                         "20 years or more"),
                              labels = c("<3", "3-9", "10-19", "20+")),
         SRVCYRSGRP = case_when(
           SRVCYRSGRP == "0-2.99"                                 ~ "<3",
           SRVCYRSGRP == "3-9.99" | SRVCYRSGRP == "3.00-9.99"     ~ "3-9",
           SRVCYRSGRP == "10-19.99" | SRVCYRSGRP == "10.00-19.99" ~ "10-19",
           SRVCYRSGRP == "20.00+"                                 ~ "20+",
           TRUE                                                  ~ SRVCYRSGRP),
         SRVCYRSGRP = factor(SRVCYRSGRP, 
                             levels = c("<3", "3-9", "10-19", "20+")))


# Work needs to be done to clean Organization inconsistencies, LEVEL1_NAME,
# LEVEL2_NAME, WESJOBCLASGRP etc.


###############################################################################
# Write quantitative data files to csv                                        #
###############################################################################

write.csv(df_questions, filepath_out_questions)
write.csv(df_info, filepath_out_info)
