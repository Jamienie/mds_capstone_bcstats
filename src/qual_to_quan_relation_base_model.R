# Base Model - Relating qualitative to quantitative data
# Author: Ayla Pearson
# Date: 2019-05-10

# Require pkgs `tidyverse` and `readxl`
library(tidyverse)
library(readxl)


###############################################################################
# Load the quantitative and qualitative data                                  #
###############################################################################

# this will need to be updated to the full spss format, currently reading in
# csv sub set

# load quantitive data
quan_data <- "../data/raw/WES 2007-2018 LONGITUDINAL DATA_sample.csv"
quant <- read_csv(quan_data)

# remove 18 weird rows that appeared when it was converted to csv
# this may not need to be done on real data set
quant <- quant %>% 
  filter(USERID != "Policy") %>% 
  filter(!grepl("^EP", USERID))


# load qualitative data
qual_data <- "../data/raw/2018 WES Qual Coded - Final Comments and Codes for Martin Capstone_sample.xlsx"
qual <- read_excel(qual_data, sheet = "Comments", skip = 1)



###############################################################################
# Clean and wrangle qualitative data                                          #
###############################################################################


# subset required columns, rename and filter out people who only had positive 
#comments
qual <- qual %>% 
  select(USERID = `_telkey`,
         code1 = `Code 1`,
         code2 = `Code 2`,
         code3 = `Code 3`,
         code4 = `Code 4`,
         code5 = `Code 5`) %>% 
  filter(!(code1 == 122 & is.na(code2))) 


# re-organize data into tidy form
qual <- gather(qual, key= "code_num", value="code", code1, code2, code3, code4, code5)


# main theme labels
theme_levels = c("Career & Personal Development",   #1
                 "Compensation & Benefits",         #2
                 "Engagement & Workplace Culture",  #3
                 "Executives",                      #4
                 "Flexible Work Environment",       #5
                 "Staffing Practices",              #6
                 "Recognition & Empowerment",       #7
                 "Supervisor",                      #8
                 "Stress & Workload",               #9
                 "Tools, Equipt & Physical Envir",  #10
                 "Vision, Mission & Goals")         #11


# remove other theme and unrelated comments, create negative rating, and
# add main themes label from subtheme code
qual <- qual %>% 
  drop_na(code) %>% 
  filter(!code %in% c(99, 121, 123, 122)) %>% 
  mutate(qual_value = -1) %>% 
  mutate(main_theme = str_sub(code, start = 1, end = str_length(code)-1)) %>% 
  mutate(main_theme = factor(as.double(main_theme), labels = theme_levels)) %>% 
  select(USERID, code_num, code, main_theme, qual_value)


# need to look into creating some kind of unit test file
# filter condition to double check process is working correctly
person1 = "172541-914038"  # 4 separate codes, all should appear = 4
person2 = "173108-219388"  # only has code 122, should NOT appear = 0
person3 = "173924-784228"  # has code 122 and 93, only code 93 should appear =1
person4 = "190199-111388"  # only has comment 99, should NOT appear =0
person5 = "180129-727518"  # has 4 codes, one being 123, so only 3 should appear =3
# there should only be 8 codes present in the output

# needs to be evaluated before doing unique (see code below)
qual %>% 
  filter(USERID %in% c(person1, person2, person3, person4, person5)) %>% 
  arrange(USERID)

# remove duplications from converting from sub-theme to main theme 
qual_data <- qual %>% 
  select(USERID, main_theme, qual_value) %>% 
  unique()


###############################################################################
# Clean and wrangle quantitative data                                         #
###############################################################################


# manual list of names of key drivers for 2018
quan_col_names = c(
  "Engagement_18",
  "Commitment_18",
  "Job_Satisfaction_18",
  "Org_Satisfaction_18",
  "Empowerment_18",
  "Stress_Workload_18",
  "Vision_Mission_Goals_18",
  "Teamwork_18",
  "Recognition_18",
  "Professional_Development_18",
  "Pay_Benefits_18",
  "Staffing_Practices_18",
  "Respectful_Environment_18",
  "Executive_Level_18",
  "Supervisory_Level_18",
  "Job_Suitability_18",
  "Tools_Workspace_18")

# select the 2018 questions and key drivers
quant_summary <- quant %>% 
  select(USERID, quan_col_names )

# turn the quantitative data into a tidy form for comparison 
# converts the 100 value average scores to neg(-1), neutral(0) and pos(+1)
quant_data <- quant_summary %>% 
  select(USERID, quan_col_names) %>% 
  gather(key = "theme", value="score", quan_col_names) %>% 
  mutate(
    quan_value = case_when(
      score < 40              ~ -1,
      score > 40 & score < 60 ~  0,
      score > 60              ~  1,
      TRUE                    ~ 99
    )
  ) %>% 
  select(USERID, theme, quan_value) %>% 
  drop_na(quan_value) %>% 
  mutate(theme = factor(theme))



###############################################################################
# Compare qual and quant                                                      #
###############################################################################


# change factor level names in the qual data to match quant data
new_vect    = c( "Professional_Development_18",     #1
                 "Pay_Benefits_18",                 #2
                 "Engagement_18",                   #3
                 "Executive_Level_18",              #4
                 "Job_Suitability_18",              #5
                 "Staffing_Practices_18",           #6
                 "Recognition_18",                  #7
                 "Supervisory_Level_18",            #8
                 "Stress_Workload_18",              #9
                 "Tools_Workspace_18",              #10
                 "Vision_Mission_Goals_18")         #11

new_qual <- qual_data %>% 
  mutate(theme = factor(main_theme, labels = new_vect)) %>% 
  select(USERID, theme, qual_value)

# left join on the qual data (since we are matching qual to quant)
joined_data <- left_join(new_qual, quant_data, by=c("USERID", "theme")) %>% 
  drop_na(quan_value) %>% 
  mutate(diff = quan_value - qual_value) 


# this needs to be moved to a test file 
# check that left join did what was expected
# looks like everything joined corrected
joined_data %>% 
  filter(USERID == person1)  
# look at qual and quan separetly for person 1
# this confirms that join did what was expected
new_qual %>% 
  filter(USERID == person1)
quant_data %>% 
  filter(USERID == person1)


# diff of 0 means they match
# diff of 2 means they are most different 

# counts overall 
joined_data %>%
  group_by(diff) %>% 
  summarize(count = n())

# counts by theme 
joined_data %>% 
  group_by(theme, diff) %>% 
  summarize(n = n()) %>% 
  arrange(diff, desc(n))









