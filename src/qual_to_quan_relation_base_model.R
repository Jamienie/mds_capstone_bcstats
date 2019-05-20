# Base Model - Relating qualitative to quantitative data
# Author: Ayla Pearson
# Date: 2019-05-10

# Require pkgs `tidyverse`, `readxl` and `testthat`
library(tidyverse)
library(readxl)
library(testthat)


###############################################################################
# Load the quantitative and qualitative data                                  #
###############################################################################

## remove all when tidy quant reads in correctly
# this will need to be updated to the full spss format, currently reading in
# csv sub set
# load quantitive data
#quan_data <- "./data/raw/old/WES 2007-2018 LONGITUDINAL DATA_sample.csv"
#quant <- read_csv(quan_data)
#quant <- quant %>% 
#  filter(USERID != "Policy") %>% 
#  filter(!grepl("^EP", USERID))
######

path_quant <- "./data/processed/tidy_quant_questions.csv"
#path_quant <- "./data/raw/old/WES 2007-2018 LONGITUDINAL DATA_sample.csv"

quant <- read_csv(path_quant)



# load qualitative data
path_qual <- "./data/raw/2018 WES Qual Coded - Final Comments and Codes.xlsx"
qual <- read_excel(path_qual, sheet = "Comments", skip = 1)



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
  select(USERID, main_theme, qual_value)

# confirm filtering is working as expected
# if not working code will stop here 
person1 = "172541-914038"  # 4 separate codes, all should appear = 4
person2 = "173108-219388"  # only has code 122, should NOT appear = 0
person3 = "173924-784228"  # has code 122 and 93, only code 93 should appear =1
person4 = "190199-111388"  # only has comment 99, should NOT appear =0
person5 = "180129-727518"  # has 4 codes, one being 123, so only 3 should appear =3

test1 <- qual %>% 
  filter(USERID %in% c(person1, person2, person3, person4, person5)) %>% 
  arrange(USERID)

test_that("test that test1 has 8 rows", {
  expect_equal(nrow(test1), 8)
})


# remove duplications from converting from sub-theme to main theme 
qual_data <- qual %>% 
  unique()


test2 <- qual_data %>% 
  filter(USERID %in% c(person1, person2, person3, person4, person5)) %>% 
  arrange(USERID)

test_that("test that test2 has 5 rows", {
  expect_equal(nrow(test2), 5)
})


###############################################################################
# Clean and wrangle quantitative data                                         #
###############################################################################


# turn the quantitative data into a tidy form for comparison 
# converts the 100 value average scores to neg(-1), neutral(0) and pos(+1)
quant_data <- quant %>% 
  filter(survey_year==2018) %>% 
  select(USERID, quan_col_names ) %>% 
  gather(key = "theme", value="score", quan_col_names) %>% 
  mutate(
    quan_value = case_when(
      score < 40              ~ -1,
      score > 40 & score < 60 ~  0,
      score > 60              ~  1,
      TRUE                    ~ NA_real_
    )
  ) %>% 
  select(USERID, theme, quan_value) %>% 
  drop_na(quan_value) %>% 
  mutate(theme = factor(theme))


test3 <- quant_data %>% 
  filter(USERID %in% c(person1, person3)) %>% 
  arrange(USERID)

test_that("conversion from 100 point scale to pos, neg, neutral", {
  expect_equal(test3[[3]][[1]],   1)
  expect_equal(test3[[3]][[18]],  0)
  expect_equal(test3[[3]][[26]], -1)
  expect_equal(nrow(test3), 32)
  })

###############################################################################
# Compare qual and quant                                                      #
###############################################################################


# change factor level names in the qual data to match quant data
new_vect    = c( "Professional_Development",     #1
                 "Pay_Benefits",                 #2
                 "Engagement",                   #3
                 "Executive_Level",              #4
                 "Job_Suitability",              #5
                 "Staffing_Practices",           #6
                 "Recognition",                  #7
                 "Supervisory_Level",            #8
                 "Stress_Workload",              #9
                 "Tools_Workspace",              #10
                 "Vision_Mission_Goals")         #11

new_qual <- qual_data %>% 
  mutate(theme = factor(main_theme, labels = new_vect)) %>% 
  select(USERID, theme, qual_value)


# left join on the qual data (since we are matching qual to quant)
joined_data <- left_join(new_qual, quant_data, by=c("USERID", "theme")) %>% 
  drop_na(quan_value) %>% 
  mutate(diff = quan_value - qual_value) 


test4 <- joined_data %>% 
  filter(USERID %in% c(person1, person2, person3, person4, person5))  

test_that("number of rows should match unique qual data", {
  expect_equal(nrow(test4), nrow(test2))
})



# counts overall 
joined_data %>%
  group_by(diff) %>% 
  summarize(count = n())

# counts by theme 
joined_data %>% 
  group_by(theme, diff) %>% 
  summarize(n = n()) %>% 
  arrange(diff, desc(n))









