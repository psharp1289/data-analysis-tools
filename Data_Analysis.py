###  THIS IS A LIBRARY OF FUNCTIONS FOR PSYCHOLOGICAL DATA ANALYSIS
###  CREATED BY PAUL SHARP ON 7.10.2014
###  Updated 7.26.2018

import csv
import numpy as np
import scipy as sp
import pandas as pd
import os
import sys
import random

#   This function makes sure prgrams know if your data file
#   has columns headers OR not. Used as input for many other
#   functions.

def column_headers(csv_file):
    while True:
            column_headers = raw_input('\nAre there column headers (i.e. a row before the data with column titles) in {}? (y/n) \n'.format(csv_file))
            if column_headers == 'y' or column_headers == 'n':
                break
            print 'Error! Only accept y or n. '
    return column_headers

#   This file outputs the number of subjects in a file
#   which is either the entire length of one column
#   or that length - 1 to account for column headers

def get_subject_nums(csv_file,column_headers):
    subject_nums = 0
    with open(csv_file, 'rU') as f:
        r = csv.reader(f)
        for row in r:
            subject_nums +=1
    if column_headers == 'y':
        return subject_nums-1
    elif column_headers == 'n':
        return subject_nums



#   csv2panda funcction reads in a csv file and converts column
#   headers into the keys in dictionaries, with data as the key_values.
#   Each dictionary is one row (which you can think of as one subject),
#   and the total data is a list of nested dictionaries per the row in the
#   original data. Finally, the function returns a pandas DataFrame of the data.


def csv2pandas(csv_file):
    with open(csv_file, 'rU') as f:
        total_data = []
        r = csv.reader(f)
        lines = [line for line in r]
        row_num = 0
        for row in lines:
            dict_row = {}
            if row_num == 0:
                row_num+=1
            else:
                item_num = 0
                for item in lines[0]:
                    dict_row[item] = int(lines[row_num][item_num])
                    item_num+=1
                total_data.append(dict_row)
                row_num+=1
    return pd.DataFrame(total_data)


#   This is a dictionary that  scripts can reference to score questionnaires. 
#   Each questionnaire (e.g., "TMMS") has the following info:
#   (1) Reverse-score question numbers
#   (2) Reverse-scoring rubric
#   (3) Total number of questions in questionnaire

#   If questionnaire has subscale, see "get_subscales" function below



def get_questionnaire_info():
        info_dict={'TMMS':[[2, 4, 5, 8, 15, 16, 17, 19, 22, 23, 24, 27, 28, 30], {1:5,2:4,4:2,5:1}, 30],
                            'CDI_ANX':[[],{},28],
                            'PSWQ':[[1,3,8,10,11],{1:5,2:4,4:2,5:1},16],
                            'BAI':[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],{1:0,2:1,3:2,4:3},21],
                            'BDI_NO_SUICIDE_Q':[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],{1:0,2:1,3:2,4:3},20],
                            'SOCIAL_ANX':[[],{},18],
                            'FAM_ID':[[4],{1:5,2:4,4:2,5:1},8],
                            'FAM_COHESION':[[3,4,8,9],{1:5,2:4,4:2,5:1},10],
                            'SFMQ':[[],{},13],
                            'FAM_CONFLICT':[[],{},10],
                            'FFMQ':[[2,3,4,6,7,8,9,10,11,12,15,16,19],{1:5,2:4,4:2,5:1},21],
                            'MASQ':[[2, 4, 5, 7, 11, 14, 19, 23, 26, 28, 32, 34, 36, 37],{1:5,2:4,4:2,5:1},39],
                            'MASQ_SCAND_TELZER':[[5,11],{1:5,2:4,4:2,5:1},26],
                            'GTS':[[28, 35, 43, 51],{'true':0,'false':1},55],
                            'RRQ':[[6, 9, 10, 13, 14, 17, 20, 24],{1:5,2:4,4:2,5:1},24],
                            'RRQ-RUMINATION':[[6,9,10],{1:5,2:4,4:2,5:1},12],
                            'NEO-FFI':[[1, 6, 7, 12, 13, 18, 19, 24],{1:5,2:4,4:2,5:1},24],
                            'PANAS_TRAIT':[[],{},20],
                            'PANAS_TRAIT_26':[[],{},26], 
                            'PANAS_TRAIT_31':[[],{},31], 
                            'PANAS_STATE_31':[[],{},31], 
                            'PANAS_CHILD':[[],{},10],Y
                            'YSQ':[[],{},25], 
                            'RELATIONS_1':[[],{},1], 
                            'RELATIONS_2':[[],{},4],
                            'TAT_18':[[],{},18], 
                            'TAT_SET':[[],{},1],
                            'TAT_7':[[],{},7], 
                            'TAT_CODER':[[],{},1], 
                            'TIPI_10':[[2,4,6,8,10],{1:7,2:6,3:5,5:3,6:2,7:1},10],
                            'ERQ':[[],{},10],
                            'GBI_DEPRESSION':[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],{1:0,2:1,3:2,4:3},19],
                            'PSS':[[4,5,7,8],{1:5,2:4,4:2,5:1},10]
                            }
        print '\nBelow is a list of the available questionnaires:'
        print info_dict.keys()
        questionnaire = raw_input('Choose one to extract: \n')
        questionnaire = questionnaire.upper()

        while True:
            try:
                return questionnaire,info_dict[questionnaire][0], info_dict[questionnaire][1], info_dict[questionnaire][2]
                break
            except:
                print '\nError. Questionnaire not in dictionary. Below are the available questionnaire names. (TYPE EXACTLY HOW YOU SEE IT!)\n'
                print info_dict.keys()
                questionnaire = raw_input('Valid questionnaire name: \n')
                questionnaire = questionnaire.upper()


#   This retrieves the subscale for each questionnaire. The data structure is a nested dictionary.
#   The first key is the questionnaire, and the second key (which is the nested dictionary) is the subscales.
#   The function returns the questions that belong to that subscale.

def get_subscales(questionnaire):
    questionnaire = questionnaire.upper()
    subscales_dict = {'MASQ':{'AA':[1, 3, 6, 8, 10, 12, 15, 16, 18, 20, 22, 24, 25, 27, 31, 33, 39],
                              'AD14_LowPositiveAffect':[2, 4, 5, 7, 11, 14, 19, 23, 26, 28, 32, 34, 36, 37],
                              'AD8_DepressedMood':[9, 13, 17, 21, 29, 30, 35, 38]},
                       'MASQ_SCAND_TELZER': {'AnxiousArousal':[4,6,8,10,14,16,18,22,24,26],
                                             'Depression':[1,5,9,11,15,19,23,25],
                                             'General_Distress':[2,3,7,12,13,17,20,21]},
                       'TAT_18':{'AFF':[1,4,7,10,13,16],
                                   'AGG':[2,5,8,11,14,17],
                                   'SE':[3,6,9,12,15,18]},
                       'SOCIAL_ANX':{},
                       'TAT_SET':{},
                       'FAM_ID':{},
                       'CDI_ANX':{},
                       'SFMQ':{},
                       'FAM_CONFLICT':{},
                       'TMMS':{'clarity':[4,5,6,9,12,17,21,22,25,28,29],
                               'attention':[1,2,3,8,11,13,15,18,19,24,26,27,30],
                               'repair':[7,10,14,16,20,23]},
                        'ERQ':{'reappraisal':[1,3,5,7,8,10],
                               'suppression':[2,4,6,9]},
                        'TIPI_10':{'Extraversion':[1,6],
                                   'Agreeableness':[2,7],
                                   'Conscientiousness':[3,8],
                                   'Emotional_Stability':[4,9],
                                   'Openness':[5,10]},
                        'PANAS_CHILD':{'PA':[1,4,5,7,10],
                               'NA':[2,3,6,8,9]},
                        'PANAS_TRAIT_26':{'NA_LOW_AROUSAL':[21,22,23,24,25,26],
                                          'NA_HIGH_AROUSAL':[1,2,3,5,6,7,10,18,19,20],
                                          'PA_HIGH_AROUSAL':[4,8,9,11,12,13,14,15,16,17]},
                        'PANAS_TRAIT_31':{'NA_LOW_AROUSAL':[26,27,28,29,30,31],
                                          'NA_HIGH_AROUSAL':[1,2,3,6,7,8,12,22,23,24],
                                          'PA_HIGH_AROUSAL':[4,9,11,13,14,16,17,18,19,21],
                                          'REJECTION':[5,10,15,20,25]},
                        'PANAS_STATE_31':{'NA_LOW_AROUSAL':[26,27,28,29,30,31],
                                          'NA_HIGH_AROUSAL':[1,2,3,6,7,8,12,22,23,24],
                                          'PA_HIGH_AROUSAL':[4,9,11,13,14,16,17,18,19,21],
                                          'REJECTION':[5,10,15,20,25]},
                        'YSQ':{'ED':[1, 6, 11, 16, 21],
                               'AB':[2, 7, 12, 17, 22],
                               'MA':[3, 8, 13, 18, 23],
                               'SI':[4, 9, 14, 19, 24],
                               'DS':[5, 10, 15, 20, 25]},
                        'GTS':{'NT':[3,5,6,7,9,10,14,15,17,19,21,22,24,26,29,31,33,35,37,38,41,42,43,44,47,49,51,52],
                               'PT':[1,2,4,8,11,12,13,16,18,20,23,25,27,28,30,32,34,36,39,40,45,46,48,50,53,54,55]},
                        'RRQ':{'rumination':[1,2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                               'reflection':[13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]},
                        'PANAS_TRAIT':{'PA':[4, 8, 9, 11, 12, 13, 14, 15, 16, 17],
                                 'NA':[1, 2, 3, 5, 6, 7, 10, 18, 19, 20]},
                        'NEO-FFI':{'neuroticism':[1,3,5,7,9,11,13,15,17,19,21,23],
                                   'extraversion':[2,4,6,8,10,12,14,16,18,20,22,24]},
                        'FFMQ':{'Describing':[1,7,10,15,18],
                               'Acting_Awareness':[3,4,8,12,16,19],
                               'Nonjudgment':[2,6,9,11,20],
                               'Nonreactivity':[5,13,14,17,20,21]}
                        }
    try:
        subscales_dict[questionnaire]
    except:
        print 'There are no subscales for this measure'
        sys.exit(0)
    while True:
        how_many = raw_input('Would you like specific subscales, or all subscales (type all or specific)?  ')
        if how_many == 'all' or how_many == 'specific':
            break
        print 'Error. Need to type ''all'' or ''specific'' '
    available_subscales = list(subscales_dict[questionnaire].keys())
    if how_many == 'specific':
        print 'These are the available subscales to choose from: {}\n'.format(available_subscales)
        while True:
            try:
                num_subscales = int(raw_input('How many subscales from this list would you like? \n'))
                break
            except:
                print 'Only accepts an INTEGER. Try again\n'
        subscales = []
        current_subscales_dict = {}
        for current_num in range(1,num_subscales+1):
            while True:
                subscale = raw_input('These are the available subscales to choose from: {}. Please input subscale number {}: '.format(available_subscales, current_num))
                try:
                    current_subscales_dict[subscale] = subscales_dict[questionnaire][subscale]
                    subscales.append(subscale)
                    break
                except:
                    print 'INVALID subscale! Choose again\n.'
        return subscales, current_subscales_dict

    else:
        subscales = []
        for key in subscales_dict[questionnaire]:
            subscales.append(key)
        return subscales, subscales_dict[questionnaire] #returns dictionary of all subscales for questionnaire of interest

#this function update the textfile that has a list of data files, the corresponding
#questionnaire of interest, and which subject numbers in that data file are corrupted
#by invalid input
def update_invalid_subjects_text(invalid_list, questionnaire, original_data_set):
    with open('Invalid_SubjectIDs_For_Data_Files.csv', 'a') as f:
        lines = [[],[original_data_set] + [questionnaire] + invalid_list]
        writer = csv.writer(f)
        writer.writerows(lines)


#this function converts SPSS .sav files to .CSV files,
#and writes them to a new .CSV file with new file name input.
def spss_to_csv(filename):
    fn = raw_input('\nName for new csv file: \n')
    import pandas.rpy.common as com
    w = com.robj.r('foreign::read.spss("%s", to.data.frame=TRUE)' % filename)
    df = com.convert_robj(w)
    df.to_csv('{}.csv'.format(fn))

# this function outputs the number corresponding to an alphabetical column in excel
# for example, column A = 1, column B = 2, etc. 

def column_key(column):
    column = column.upper()
    column_dict = {}
    import string
    letters = string.ascii_uppercase
    alphabet = list(letters)
    num = 0
    for i in alphabet:
        column_dict[i] = num
        num+=1
    num=26
    for let1 in alphabet:
        for let2 in alphabet:
            column_dict[let1+let2] = num
            num+=1
    num=702
    for let1 in alphabet:
        for let2 in alphabet:
            for let3 in alphabet:
                column_dict[let1+let2+let3] = num
                num+=1
    return column_dict[column]


#variable must have same name with appended number attached
#sees if subject number
def if_both(subject,number,ivs_dict,variable,have_both_list):
    if number == 0:
        have_both_list.append(subject)
    elif subject in ivs_dict[variable]:
        number-=1
        variable = 'x{}'.format(number)
        if_both(subject,number,ivs_dict,variable,have_both_list)
    else:
        print 'invalid subject number: {}'.format(subject)

# deidentifies a file 
# creates a file with pariticpant names and the new random ID# this function replaces ID names with
def deidentifier(filename,colheaders):
    subjects = get_subject_nums(filename,colheaders)
    print 'subjects = {}'.format(subjects)
    with open(filename, 'rU') as f:
        r = csv.reader(f)
        lines = [line for line in r]
        col_name_index = int(raw_input('What is the column index (i.e. column-1) that includes participant names?'))
        name = filename[:-4]
        deidentified_record_file = '{}_deifentified_record.csv'.format(name)
        deidentified_file = '{}_DEIDENTIFIED.csv'.format(name)
        record = []
        randlist = random.sample(range(1000000),subjects)
        if colheaders == 'y':
            for subject in range(1,subjects+1):
                record.append([lines[subject][col_name_index]])
                lines[subject][col_name_index] = randlist[subject-1]
                record[subject-1].append(lines[subject][col_name_index])
        elif colheaders == 'n':
            for subject in range(subjects):
                print 'subject number = {}'.format(subject)
                record.append([lines[subject][col_name_index]])
                lines[subject][col_name_index] = randlist[subject]
                record[subject].append(lines[subject][col_name_index])
                print record

    with open(deidentified_record_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(record)

    with open(deidentified_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(lines)

## This function allows one to control for a variable by giving a cutoff score
## At the mean usually

def cutoff_group(filename, cutoff_score, cutoff_variable_index, full_path_to_data):
    os.chdir(full_path_to_data)
    print '\nThis file assumes your subject ID is in the first column!!!!\n'
    while True:
        answer = raw_input('\nWould you like to proceed knowing the above is necessary for this to work?  Answer only (y/n)\n')
        if answer == 'y':
            break
    cols = column_headers(filename)
    if cols == 'y':
        start_row = 1
    else:
        start_row = 0
    subjects = get_subject_nums(filename,cols)
    zero_mat = np.zeros((subjects+1,variables+1), dtype=int)
    invalid_cutoffs = []
    variables = raw_input('\nHow many variables are in your dataset? (only accepts integers) \n')
    with open(filename, 'rU') as f:
        r = csv.reader(f)
        lines = [line for line in r]
        row_index=1 #row number for new matrix
        for row in range(start_row,subjects+1): #places subject IDs in first column of new matrix
            zero_mat[row,0] = lines[row][0]
        for row in range(start_row,subjects+1): #places data in
            for variable in range(1,variables-1):
                zero_mat[row,variable] = lines[row][variable]
        direction = raw_input('Do you want to eliminate scores greater than (g) or less than (l) the cutoff score? (g/l) \n')
        if direction == 'g':
            print 'in greater than section'
            row_index = 1
            for row_data in range(start_row,subjects+1):
                if int(lines[row_data][cutoff_variable_index]) > cutoff_score:
                    print 'Deleting subject number: {} from analysis.'.format(lines[row_data][0])
                    invalid_cutoffs.append('Row:{} Col:{}'.format(row_data+1,cutoff_index+1))
                    zero_mat = np.delete(zero_mat,row_index,0) #deletes this row from new matrix. invalid data b/c of missing value.
                else:
                    zero_mat[row_index,cutoff_variable_index] = lines[row_data][cutoff_variable_index]
                    row_index+=1
        elif direction == 'l':
            print 'in less than section'
            row_index = 1
            for row_data in range(1,subjects+1):
                if int(lines[row_data][cutoff_index]) < cutoff_score:
                    print 'Deleting subject number: {} from analysis.'.format(lines[row_data][0])
                    invalid_cutoffs.append('Row:{} Col:{}'.format(row_data+1,cutoff_variable_index+1))
                    zero_mat = np.delete(zero_mat,row_index,0) #deletes this row from new matrix. invalid data b/c of missing value.
                else:
                    zero_mat[row_index,cutoff_index] = lines[row_data][cutoff_index]
                    row_index+=1

    cutoff_csv = raw_input('\nPlease name the new file with excised cutoff scores: \n')
    cutoff_csv = cutoff_csv + '.csv'
    np.savetxt(cutoff_csv, zero_mat, delimiter=',')
    with open(cutoff_csv, 'rU') as f:
        r = csv.reader(f)
        newlines = [line for line in r]
        for col in range(0,3):
            newlines[0][col] = lines[0][col]
        rows = get_subject_nums(cutoff_csv, 'y')
        for row in range(1,rows+1):
            for col in range(0,3):
                newlines[row][col] = float(newlines[row][col])
                newlines[row][col] = int(newlines[row][col])
    with open(cutoff_csv, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(newlines)
