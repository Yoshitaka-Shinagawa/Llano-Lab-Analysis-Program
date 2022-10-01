#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 11:28:31 2022

@author: austincoder
"""

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
import pandas as pd
from PIL import ImageColor


#Path
path = ""

def correlation_of_averages_grapher():
    
    # Extracts variables from the info_storage class
    # path                     = info_storage.path
    
    # Creates output directory
    matrix_output_path = "f{path}/Output/Correlation Frequencies"
    if os.path.exists(matrix_output_path) == True:
        shutil.rmtree(matrix_output_path)
    if os.path.exists(matrix_output_path) == False:
        os.mkdir(matrix_output_path)
    
    #Converts .excel sheets to CSV files
    excel_converter = pd.read_excel("f{path}/Output/Cell Traces/Spreadsheets/Area under curves.xlsx")
    excel_converter.to_csv("f{path}/Output/Cell Traces/Spreadsheets")
    
    #Reads the newly created CSV file
    # integral_reader = pd.read_csv("f{path}/Output/Cell Traces/Spreadsheets/Area under curves.csv")
    
    
    return 
    

#Runs the function to convert file to CSV file 
correlation_of_averages_grapher() 

#Reads the newly created CSV file
integral_reader = pd.read_csv("f{path}/Output/Cell Traces/Spreadsheets/Area under curves.csv")
 
#Prints the entire dataframe to console 
print(integral_reader.to_string())