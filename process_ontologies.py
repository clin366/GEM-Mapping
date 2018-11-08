#!/usr/bin/env python
# encoding: utf-8


import argparse
import re
import pandas as pd

def process_gem(path, name):
    I9code = []
    I10code = []
    Flag = []
    with open(path, 'r') as fi:
        line = fi.readline()
        
        while line:
            array = re.split(r'\s+',line)
            I9code.append(array[0])
            I10code.append(array[1])
            line = fi.readline()

    I9_pd = pd.DataFrame({'I9code':I9code, 'I10code':I10code})
    total_count = pd.DataFrame(I9_pd['I9code'].value_counts()).shape[0]
    print("The total number of ontologies in " + name +" is " + str(total_count))

    I9_pdNoDx = I9_pd[I9_pd['I10code'] == 'NoDx']
    no_mapping = pd.DataFrame(I9_pdNoDx['I9code'].value_counts()).shape[0]
    print("The number of no mapping ontologies in " + name +" is " + str(no_mapping))

    I9_rmNoMap = I9_pd[I9_pd['I10code'] != 'NoDx']
    I9_valueCounts = pd.DataFrame(I9_rmNoMap['I9code'].value_counts())
    one_one_map = I9_valueCounts[I9_valueCounts['I9code'] == 1].shape[0]
    print("The number of one to one mapping ontologies in " + name +" is " + str(one_one_map))

    one_many_map = I9_valueCounts[I9_valueCounts['I9code'] > 1].shape[0]
    print("The number of one to many mapping ontologies in " + name +" is " + str(one_many_map))


parser = argparse.ArgumentParser()
parser.add_argument("-I9", "--I9", help="I9 mapping to I10",
                    action="store_true")
parser.add_argument("-I10", "--I10", help="I10 mapping to I9",
                    action="store_true")
parser.add_argument("-path", "--path", type=str,
                    help="Path to the input file")

args = parser.parse_args()
# print args.I9

# print args.path


if not args.path:
    print("Missing command line info '-path', use --help or -h to see the detail")
else:
    if not args.I9:
        if not args.I10:
            name = None
            print("Missing command line info '-I9' or '-I10', use --help or -h to see the detail")
        else:
            name = 'I10'
    else:
        name = 'I9'

    if name:
        path = args.path
        process_gem(path, name)










        
