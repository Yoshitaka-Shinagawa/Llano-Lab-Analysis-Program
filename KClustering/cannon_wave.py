# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:29:52 2022

@author: Austin
"""

import os
import shutil
import numpy as np
import pandas as pd


def cannon_wave(data,info_storage):
    
    # Extracts variables from the info_storage class
    # path                     = info_storage.path
    framerate_information      = info_storage.framerate_information
    df                         = info_storage.df
    correlation_coefficients   = info_storage.correlation_coefficients
    # key                      = info_storage.key
    # frequencies              = info_storage.frequencies
    # intensities              = info_storage.intensities
    threshold                  = info_storage.threshold
    
    #Empty Dataframe to store data inside
    df2 = pd.DataFrame()

    #Divides by every 5th row because I coded the last part bad
    df = df.iloc[::5, :]
    
    #Drops all rows that have less than the desired correlation coefficient
    df.drop(df[df['correlation_coefficient'] < 0.6].index, inplace = True)
    
    #Empty lists to store values
    avg=[]
    col_averages=[]
    
    #Creates variables to make new dataframe
    current_cell = df2['cell_number'].iloc[0]
    temp_df = df2.iloc[1:]

    for cell in temp_df: 
        for c in range(len(df['averages'][0])):
            for d in df['averages']:
                if current_cell == cell:
                    col_averages.append(d[c])
                    current_cell = cell
                if current_cell != cell:
                    avg.append(sum(col_averages)/len(col_averages))
                    df2['cell_number'] = current_cell
                    df2['final_wave'] = avg
                    avg.clear()
                    col_averages.clear()
                    current_cell = cell
            
    info_storage.df2 = df2
          
    return df2,info_storage