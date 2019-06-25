#! /usr/bin/env Rscript 
# quantitative_other.R 
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: Pull out the demographic information from the qualitative data.
#           Code to help with re-org mapping. 
#
#






input_quant <- "./data/raw/WES 2007-2018 LONGITUDINAL DATA_short.sav"


# Keeps the labels from spss file for the employee info and demographic data
df_spss_labeled <- foreign::read.spss(file = input_quant, 
                                      to.data.frame = TRUE, 
                                      use.value.labels = TRUE)



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


filepath_reorg = paste0("./references/data-dictionaries/", 
                        "Current Position with BU and Org Hierarchy - WES 2018.csv")


###############################################################################
# Map correct Organization labels by Position number over time                #
###############################################################################

# Data dictionary to help with organization mapping
df_reorg_legend <- read_csv(filepath_reorg)

# Relevant columns to select for reorganization
col_reorg <- df_legend %>% 
  filter(category %in% c('BC Stats Background', 'Sensitive Info')) %>% 
  filter(str_detect(original_column_name, "LEVEL") |
           str_detect(original_column_name, "CURPOS") |
           str_detect(original_column_name, "ORGANIZATION") |
           str_detect(original_column_name, "DEPTID") |
           original_column_name == 'USERID') %>% 
  pull(original_column_name)

# Tidy the Dataframe, Correct/Fill In missing Position Numbers, and Cross
# Reference the reogranization legend based on Position number
df_reorg <- df_spss_labeled %>% 
  select(col_reorg) %>% 
  gather(-USERID, key = "original_column_name", value = "temp_val") %>% 
  left_join(df_legend, by = "original_column_name") %>% 
  select(USERID, new_column_name, survey_year, temp_val) %>% 
  spread(key = new_column_name, value = temp_val) %>% 
  ## NEED TO JOIN 2007-2009 POSITION NUMBERS HERE
  mutate_at(vars(CURPOSDESC:ORGANIZATION), str_squish) %>% 
  mutate(CURPOSNUM = str_pad(CURPOSNUM, width = 8, side = "left",
                             pad = "0")) %>% 
  group_by(USERID, CURPOSDESC) %>% 
  mutate(CURPOSNUM = na.locf(CURPOSNUM, fromLast = TRUE, na.rm = FALSE)) %>% 
  left_join(df_reorg_legend, by = c("CURPOSNUM" = "POSITION NBR")) %>% 
  ungroup()

# Based off the data dictionary, map the correct organization name
df_reorg <- df_reorg %>%
  mutate(New_Org = case_when(
    Level1 == "Public Guardian & Trustee"                   ~ "Public Guardian and Trustee",
    Level1 == "Emergency Management BC"                     ~ "Emergency Management BC",
    Level1 == "Liquor Control & Licensing"                  ~ "Attorney General",
    Level1 == "Corporate Management Services"               ~ "Public Safety and Solicitor General",
    Organization == "Natural Gas Development"               ~ "Energy, Mines and Petroleum Resources",
    Organization == "Housing"                               ~ "Municipal Affairs and Housing",
    DEPTID.x == "125-8002"                                  ~ "Municipal Affairs and Housing",
    DEPTID.x == "125-8004"                                  ~ "Municipal Affairs and Housing",
    DEPTID.x == "125-8006"                                  ~ "Municipal Affairs and Housing",
    DEPTID.x == "125-8007"                                  ~ "Municipal Affairs and Housing",
    DEPTID.x == "125-8009"                                  ~ "Municipal Affairs and Housing",
    `Business Unit Description` == "Ministry of Justice AG" ~ "Attorney General",
    `Business Unit Description` == "Ministry of Justice SG" ~ "Public Safety and Solicitor General",
    `Business Unit Description` == "Env Assessment Office"  ~ "Environmental Assessment Office",
    Organization == "Job, Trade and Technology"             ~ "Jobs, Trade and Technology",
    Organization == "Citizens Services"                     ~ "Citizens' Services",
    is.na(CURPOSNUM)                                        ~ "",
    TRUE                                                    ~ as.character(Organization))) %>%
  select(USERID, survey_year, CURPOSNUM, DEPTID.x, ORGANIZATION, New_Org)

# Fill in Missing Oraganization Names
df_reorg$New_Org[df_reorg$New_Org == ""] <- NA
df_reorg <- df_reorg %>% 
  group_by(USERID, ORGANIZATION) %>% 
  mutate(New_Org = na.locf(New_Org, fromLast = TRUE, na.rm = FALSE)) 