# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:29:52 2022

@author: Austin
"""

import os
import shutil
import numpy as np
import pandas as pd


def cannon_wave(info_storage):
    
    # Extracts variables from the info_storage class
    # path                     = info_storage.path
    # framerate_information      = info_storage.fra1merate_information
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
    #current_cell = df2['cell_number'].iloc[0]
    #temp_df = df2.iloc[1:]
    df2 = df
    temp_df = df
    next_cell = temp_df['cell_number'].shift(-1).replace(np.nan, -1)
    df2['next_cell'] = next_cell
    df2['streak_ending'] = df2['next_cell'] != df2['cell_number']
    i = 0
    
    for c in range(len(df['averages'][0])):
        while i < df2.shape[0]:
            col_averages.append(df2['averages'].iloc[i][c])
            if df2['streak_ending'].iloc[i]:
                avg.append(sum(col_averages)/len(col_averages))
                col_averages.clear()
            i += 1
        i = 0
    #        if current_cell == cell:
    #            col_averages.append(d[c])
    #            current_cell = cell
    #        if current_cell != cell:
    #            avg.append(sum(col_averages)/len(col_averages))
    #            df2['cell_number'] = current_cell
    #            avg.clear()
    #            col_averages.clear()
    #            current_cell = cell
    n = len(df2['cell_number'].unique())
    cell_numbers = df2['cell_number'].unique()
    avg_downwards = []
    for i in range(n):
        avg_downwards.append(avg[i::n])
    cell_uni_list = cell_numbers.tolist()
    df3 = pd.DataFrame({'cell_number': cell_uni_list, 'trial_average':avg_downwards})
    # print(df3)
    
    info_storage.df2 = df2
    info_storage.df3 = df3
    
    return df3,df2,info_storage