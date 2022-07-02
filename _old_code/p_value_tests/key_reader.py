# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:32:31 2019

@author: Yoshi
"""

import os
import csv



def key_reader(path):
    
    # Creates a list for frequencies and decibels
    frequencies = []
    decibels = []
    
    # Creates an empty dict for the key
    key = {}
    
    # Opens key
    open_key_file = open(path+'/Data/key.csv')
    key_file = csv.reader(open_key_file)
    
    # Reads content of key
    row_count = 0
    for row in key_file:
        row_length = len(row)
        if row_count == 0:
            for column in range(1,row_length):
                frequencies.append(row[column])
                key[row[column]] = {}
        else:
            for column in range(row_length):
                if column == 0:
                    decibels.append(row[column])
                else:
                    key[frequencies[column-1]][decibels[row_count-1]] = int(row[column])-1
        row_count += 1
    
    # Close file
    open_key_file.close()
    
    return key,frequencies,decibels