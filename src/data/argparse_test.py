# argpare_test.py
# Authors: Varada Kholkater
# Date: 2019-05-16

# USAGE: This script defines a function to get arguments using argparse. It is
# meant to be used as an example/test

import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description='Write csv files for crowd'
                                                 'annotation')

    parser.add_argument('--input_csv', '-i', type=str, dest='input_csv',
                        action='store', default='../data/processed/input.csv',
                        help='the input csv file')

    parser.add_argument('--output_csv', '-o', type=str, dest='output_csv',
                        action='store', default='../data/intermediate/'
                        'input.csv', help='the output csv file')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_arguments()
    print(args)
