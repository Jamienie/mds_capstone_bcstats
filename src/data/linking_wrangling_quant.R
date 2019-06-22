
#! /usr/bin/env Rscript 
# linking_qual_to_quant.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This script reads in the raw quantitative data and outputs
#           the data ready to be related to the qualitative data
#
# Inputs: 
#   This script takes 2 arguments
#     - raw quantitative data
#     - survey legend that contains sub-theme codes and 
#          multiple-choice questions
#
# Outputs:
#   This script has 1 output
#     - clean and wrangled quantitative data
#
# Usage: Run from the project root
# General example:
# Rscript src/analysis/linking_wrangling_quant.R input_file_quant input_data_legend output_file
# Real example:
# Rscript src/data/linking_wrangling_quant.R "./data/processed/tidy_quant_questions.csv" "./references/data-dictionaries/survey_mc_legend.csv" "./data/interim/relating_quant_subtheme_mc.csv"


# load packages 
suppressWarnings(suppressPackageStartupMessages(library(tidyverse)))
suppressPackageStartupMessages(library(testthat))

# read in command line arguments
args <- commandArgs(trailingOnly = TRUE)
input_file_quant <- args[1]
input_file_labels <- args[2]
output_file <- args[3]


# define main function
main <- function(){
  # load quantitative data
  options(readr.num_columns = 0)
  data_quant <- read_csv(input_file_quant)  
    
  # select the 2018 questions 
  quant <- data_quant %>% 
    filter(survey_year == 2018) %>% 
    select(USERID, dplyr::matches("Q.."))  %>% 
    gather(key = "question", value="score", dplyr::matches("Q..")) %>% 
    drop_na() %>% 
    mutate(
      question = factor(question),
      quan_value = case_when(
        score < 50     ~ -1,
        score == 50    ~  0,
        score > 50     ~  1,
        TRUE           ~ 99
      )
    ) %>% 
    select(USERID, question, quan_value)  %>% 
    mutate(question = as.character(question))
  
  # load sub-theme labels matched to multiple-choice questions
  data_label <- read_csv(input_file_labels)
  
  # create df with sub-theme label and mc question
  labels <- data_label %>% 
    filter(survey_year == "2018") %>% 
    filter(category == "Raw Survey Question") %>% 
    select(new_column_name, subtheme_code) %>% 
    mutate(sub_theme = (na_if(subtheme_code, 0))) %>% 
    separate(sub_theme, 
             sep=", ", 
             into = c("theme1", "theme2"), 
             fill="right") %>%   
    gather(key="theme_name", value="theme", theme1, theme2) %>% 
    select(theme, question = new_column_name) %>% 
    drop_na(theme) %>% 
    arrange(question)
  
  # join the labels with thequantitative data 
  quant_theme_mc <- left_join(labels, quant, by=c("question")) %>% 
    select(USERID, theme,  quan_value, question) %>% 
    mutate(theme = as.numeric(theme))
  
  # Unit tests to ensure filtering is occurring correctly
  # Code will not write output file if tests don't pass
  person1 = "172541-914038"  # 4 separate codes, all should appear = 4
  person2 = "173108-219388"  # only has code 122, should NOT appear = 0
  person3 = "173924-784228"  # code 122 and 93, only 93 should appear = 1
  person4 = "190199-111388"  # only comment 99, should NOT appear = 0 
  person5 = "180129-727518"  # has 4 codes, one is 123, = 3 
  
  test2 <- quant %>% 
    filter(USERID %in% c(person1, person2, person3, person4, person5))
  
  test_that("quantitative gather and filtering correctly", {
    expect_equal(nrow(test2), 393)
  })
  
  test3 <- labels %>% 
    filter(question == "Q39")
  
  test_that("Ensure labels have been parsed in correctly", {
    expect_equal(test3$theme, c("102",  "104"))
    expect_equal(nrow(labels), 53)
  })
  
  test4 <- quant_theme_mc %>% 
    filter(USERID %in% c(person1, person2, person3, person4, person5)) %>% 
    arrange(USERID)
  
  test5 <- quant_theme_mc %>% 
    filter(USERID == person1 & question == "Q01")
  
  test6 <- quant_theme_mc %>% 
    filter(USERID == person1 & question == "Q17")
  
  test7 <- quant_theme_mc %>% 
    filter(USERID == person1 & question == "Q41")
  
  test_that("Ensure correct joining of subtheme codes to quant data", {
    expect_equal(nrow(test4), 258)
    expect_equal(test5$theme, 34)  
    expect_equal(nrow(test6), 0)
    expect_equal(test7$theme, c(105, 106))
  })
  
  write_csv(quant_theme_mc, output_file)
  
}

# call main function
main()