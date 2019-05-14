# tidy_quantitative-data.R 
# Author: Aaron Quinton
# Date: 2019-05-08

# Require pkgs `foreign`, `sjlabelled`, and `tidyverse`
library(tidyverse)


###############################################################################
# Read quantitative data from SPSS file and read in legend to help select and #
# rename columns                                                              #
###############################################################################

# Removes labels from spss file for the multiple choice question data
df_spss <- foreign::read.spss(file = 
                           "./data/WES 2007-2018 LONGITUDINAL DATA_short.sav", 
                               to.data.frame = TRUE, 
                               use.value.labels = FALSE) %>% 
           sjlabelled::remove_all_labels()

# Keeps the labels from spss file for the employee info and demographic data
df_spss_labeled <- foreign::read.spss(file = 
                           "./data/WES 2007-2018 LONGITUDINAL DATA_short.sav", 
                                      to.data.frame = TRUE, 
                                      use.value.labels = TRUE)

# the csv used has been manually built to help make sense of all the columns in
# the spss file
df_legend <- read_csv("./data/survey_mc_legend.csv")


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

df_orgs <- df_info %>% 
  select(USERID, survey_year, ORGANIZATION) %>% 
  mutate(ORGANIZATION = ifelse(str_detect(ORGANIZATION, "."), ORGANIZATION, NA), 
         ORGANIZATION = factor(ORGANIZATION)) %>% 
  left_join(select(filter(df_ORG2018, str_detect(ORGANIZATION, ".")),
                   -survey_year), by = "USERID") %>% 
  filter(!is.na(ORGANIZATION.x), !is.na(ORGANIZATION.y)) %>% 
  rename(ORG2018 = ORGANIZATION.y, ORG = ORGANIZATION.x)

p <- df_orgs %>% 
  filter(ORG2018 == "Advanced Education, Skills and Training") %>% 
  mutate(ORG2 = fct_drop(ORG)) %>% 
  ggplot(aes(x = survey_year, y = ORG2, group = USERID)) +
    geom_path(alpha = 0.1) +
    theme_bw()

p

