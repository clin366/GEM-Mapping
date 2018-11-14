import re 
import pandas as pd 
import argparse

# define function to do reduce mapping
def reduce_mapping(mapping_file, code_frequency_file):
    I9code = []
    I10code = []
    Flag = []
    # read the original I10 to I9 mapping file
    with open(mapping_file, 'r') as fi:
        line = fi.readline()
        
        while line:
            array = re.split(r'\s+',line)
            I10code.append(array[0])
            I9code.append(array[1])
            line = fi.readline()

    I10_pd = pd.DataFrame({'I9code':I9code, 'I10code':I10code})
    I10_rmNoMap = I10_pd[I10_pd['I9code'] != 'NoDx']

    I10_valueCounts = pd.DataFrame(I10_rmNoMap['I10code'].value_counts())
    I10_manyMap = I10_valueCounts[I10_valueCounts['I10code'] > 1]
    I10_index = I10_manyMap.index

    disease_excel = pd.read_excel(code_frequency_file, sheetname='Q1-Q3_ICD-9-CM')

    one_mapping_I10 = []
    one_mapping_I9 = []
    for i in range(0, I10_index.shape[0]):
    #     print(tmp_first)
        print("=====Processing " + str(i) + " I10codes=======")
        tmp_first = I10_index[i]
        
        tmp_I9 = I10_rmNoMap[I10_rmNoMap['I10code'] == tmp_first]['I9code']

        I9_list = []
        I9_count = []
        for i in list(tmp_I9):
        #     print(i)
            tmp_I9_first_code = i[:3] + '.' + i[3:]
            count = disease_excel[disease_excel['ICD9CMCode'] == tmp_I9_first_code]['TotalDiag']

            if (count.shape[0] > 0):
                I9_list.append(i)
                I9_count.append(int(count))
        #         print(int(count)) 
        
        if (len(I9_count) > 0):
            max_value = max(I9_count)
            max_ratio = float(max_value)/sum(I9_count)
            if (max_ratio > 0.5):
                max_ind = I9_count.index(max(I9_count))
                max_I9 = I9_list[max_ind]
                print(max_I9)
                one_mapping_I9.append(max_I9)
                one_mapping_I10.append(tmp_first)

    print("The total one to many mapping I10 codes is:" + str(len(I10_index)))
    print("The number of I10 codes that could be reduced is:" + str(len(one_mapping_I10)))

# use argpares to parse command line options
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mapping_file", type = str, 
                    help="Path to the I10 mapping to I9 file")
parser.add_argument("-c", "--code_frequency_file", type=str,
                    help="Path to the code frequency file")

args = parser.parse_args()

# check if the file path is correct
Flag = True
if args.mapping_file != None: 
    if args.code_frequency_file != None:
        reduce_mapping(args.mapping_file, args.code_frequency_file)
        Flag = False
if Flag:
    print("Missing necessary file path, use --help or -h to see the detail")
