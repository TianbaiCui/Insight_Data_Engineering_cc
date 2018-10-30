#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 00:18:33 2018

@author: tianbai
"""

import sys
import re
import csv

def extract(input):
    """
    This function extracts the relevant information from the input dataset.
    In this project, the relevant information is:
    1) the case status;
    2) the occupation name;
    3) the state where the work will take place.
    Only store state and occupation names if status is 'CERTIFIED'.

    Argument: input -- the path to the dataset needs to be analyzed
    Return:   states -- the list of state names (string) with 'CERTIFIED' case status
              occupations -- the list of occupation names (string) with 'CERTIFIED' case status
    """
    states = []      # Store the working state.
    occupations = [] # Store the occupational name.
    with open(input) as csvfile:
        data = csv.DictReader(csvfile, delimiter=';')
        # Semicolon separated (";") format is used.
        # Otherwise, change the delimiter correspondingly.
        header = data.fieldnames
        # Locate the header with the keywords:
        # 1) "status" for the case status,
        # 2) "state & (work or 1)" for the working state,
        # 3) "(SOC or occupation) & (name or title)" for the occupational name.
        for i in range(len(header)):
            if re.search('STATUS', header[i], re.IGNORECASE):
                status = header[i]
            if re.search('STATE', header[i], re.IGNORECASE) and (re.search('WORK', header[i], re.IGNORECASE) and not re.search('2', header[i])):
                place = header[i]
            if (re.search('SOC', header[i], re.IGNORECASE) or re.search('OCCUPATION', header[i], re.IGNORECASE)) and (re.search('NAME', header[i], re.IGNORECASE) or re.search('TITLE', header[i], re.IGNORECASE)):
                soc = header[i]

        for row in data:
            # Only store the relevant data for Step 2.
            #if re.search('CERTIFIED', row[status]): # if want to include the case 'CERTIFIED-WITHDRAW'
            if row[status] == 'CERTIFIED':
                states.append(row[place])
                occupations.append(row[soc])
    return states, occupations

def stat(states, occupations):
    """
    This function picks the top 10 states and top 10 occupations get the CERTIFIED H1B visa.
    1) count: count the number of certified applications.
    2) sort: sort by the number of certified applications.
    3) pick: pick the top 10 occupations and states.

    Arguments: states -- the list of state names (a list of strings)
               occupations -- the list of occupation names (a list of strings)
    Return:    state_count[0:9] -- the top 10 states with certified applications (a list of tuples)
               occupation_count[0:9] -- the top 10 occupations with certified applications (a list of tuples)
               total -- the total number of certified applications (an integer)
    """
    state_dict = {}  # use dictionary to count
    occupation_dict ={}  # use dictionary to count
    total = len(states) # total number of the certified applications
    for i in range(total):
        if states[i] not in state_dict:
            state_dict[states[i]] = 1
        else:
            state_dict[states[i]] += 1

        if occupations[i] not in occupation_dict:
            occupation_dict[occupations[i]] = 1
        else:
            occupation_dict[occupations[i]] += 1

    # put the dictionary in a list of tuple pairs, which is convient for sorting
    state_count = state_dict.items()
    occupation_count = occupation_dict.items()
    # sort the list reversely by the count, then alphabetically by its name
    state_count.sort(key=lambda x: (-x[1], x[0]))
    occupation_count.sort(key=lambda x: (-x[1], x[0]))
    # return the top 10 results and the total number of certified applications
    return state_count[0:9], occupation_count[0:9], total

def add_percent(feature_count, total):
    """
    This function adds an "percentage" column to the "feature_count" list.
    The count of each feature is stored in the second column of "feature_count".
    The percentage is equal to the count divided by "total" times 100%.

    Arguments: feature_count -- a list of tuples, each tuple has two elements
               total -- the total number of certified applications (an integer)
    Return: with_percent -- a list of tuples, each tuple has three elements
    """
    with_percent = []
    for row in feature_count:
        with_percent.append(row + tuple(("{0:.1f}%".format(row[1]*100.0 / total),)))
        # The percentage is rounded off to 1 decimal place.
    return with_percent

def output(header, list_of_tuples, path):
    """
    This function generate the output file with the given 'path'.
    'header' is a string of the name of each field of the 'list_of_tuples'.
    Different field names shoule be separated by semicolon (;).

    Arguments: header -- the field names of the list_of_tuples
               list_of_tuples -- the data will be saved as a semicolon-separated txt file
               path -- path to the output file
    """
    if header.count(';') != len(list_of_tuples[0]) - 1:
        print 'ERROR output file: %s \n Number of field names does not match with the number of fields!' % path
    else:
        outfile = open(path, "w")
        outfile.write('%s\n' % header) # Write the header as the first row.
        for row in list_of_tuples:
            # Write each row of 'list_of_tuples' in a semicolon separated format.
            outfile.write('%s;%d;%s\n' % row)
        outfile.close
        print 'Finish output file: %s' % path

if __name__=="__main__":
    # Read the input/output file names from the arguments.
    if len(sys.argv[1:]) != 3:
        print "ERROR: Check the number of arguments!"
    else:
        for i in [1, 2, 3]:
            if re.search('/input/', sys.argv[i], re.IGNORECASE):
                input = sys.argv[i]
            if re.search('state', sys.argv[i], re.IGNORECASE):
                output_state = sys.argv[i]
            if re.search('occupation', sys.argv[i], re.IGNORECASE) or re.search('SOC', sys.argv[i], re.IGNORECASE):
                output_occupation = sys.argv[i]
    # Step 1: Extract the relevant information
    states, occupations = extract(input)
    # Step 2: Data analysis
    state_stat, occupation_stat, total = stat(states, occupations)
    state_stat = add_percent(state_stat, total)
    occupation_stat = add_percent(occupation_stat, total)
    # Step 3: Output Results
    header_state = 'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'
    header_occupation = 'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'
    output(header_state, state_stat, output_state)
    output(header_occupation, occupation_stat, output_occupation)
