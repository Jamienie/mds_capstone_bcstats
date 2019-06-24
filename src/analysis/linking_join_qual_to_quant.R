#! /usr/bin/env Rscript 
# linking_join_qual_to_quant.R
# Aaron Quinton, Ayla Pearson, Fan Nie
# June 2019
#
# Purpose: This script takes in the cleaned qualitative data and 
#           cleaned quantititaive data and joins them and outputs
#           the joined data
#
# Inputs: 
#   This script takes 2 arguments
#     - cleaned qualitative data
#     - cleaned quantitative data
#
# Outputs:
#   This script has 1 output
#     - csv of joined qualitative and quanitative data
#
# Usage: 
# Run from the project root
#
# General example:
# Rscript src/analysis/linking_join_qual_to_quant.R input_qual input_quant output_joined
#
# Real example:
# Rscript src/analysis/linking_join_qual_to_quant.R "./data/interim/linking_cleaned_qual.csv" "./data/interim/linking_cleaned_quant.csv" "./data/interim/linking_joined_qual_qaunt.csv"
#


# load packages 
suppressWarnings(suppressPackageStartupMessages(library(tidyverse)))
suppressPackageStartupMessages(library(testthat))

# read in command line arguments
args <- commandArgs(trailingOnly = TRUE)
input_qual <- args[1]
input_quant <- args[2]
output_file <- args[3]


# define main function
main <- function(){
  # read in cleaned data
  options(readr.num_columns = 0)
  qual <- read_csv(input_qual)
  quant <- read_csv(input_quant)
  
  # combine qualitative and quanitative dfs
  joined_data <- left_join(qual, quant, by=c("USERID", "code"="theme")) %>% 
    drop_na(quan_value) %>% 
    mutate(diff = quan_value - qual_value)
  
  # Unit Test to confirm filtering is working correctly
  person1 = "172541-914038"  # code 92 = 1
  person3 = "173924-784228"  # code 93 appear twice = 2
  person5 = "180129-727518"  # code 105 & 93 (but only once) = 2
  
  test1 <- joined_data %>% 
    filter(USERID %in% c(person1, person3, person5)) %>% 
    arrange(USERID)
  
  test_that("qual ad quant data have been properly joined", {
    expect_equal(nrow(test1), 5)
  })
  # if all tests pass, write cleaned data to file
  write_csv(joined_data, output_file)
  
}

# call main function
main()
