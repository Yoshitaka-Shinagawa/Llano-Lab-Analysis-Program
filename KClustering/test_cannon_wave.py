# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 10:41:00 2022

@author: Austin
"""


import os
import shutil
import numpy as np
import pandas as pd


         
         

def test_cannon_wave():
    
    
    #Sets cell_total for test example
    cell_total = 139
    
    #Reads the dataframe
    df = pd.read_csv('E:/Llano Lab/Pair Plot/cell_averages.csv')
    
    #Divides by every 5th row because I coded the last part bad
    df2 = df.iloc[::5, :]
        
    # Calculates x-axis labels
    # cycle_frames = 32
    # cycle_duration = 1100
    # times = []
    # step = cycle_duration / cycle_frames
    # for frame in range(cycle_frames):
    #     times.append(step*frame)
    
    #Sets x equal to a numpy array that equals time
    # times_array= np.array(times)
    
    #Creates a new column with just times 
    # df2['times(ms)'] = times_array
    
    #Creates a new column that links the times to average trial flouresence
    
    #Drops all rows that have less than the desired correlation coefficient
    df2.drop(df2[df2['correlation_coefficient'] < 0.6].index, inplace = True)
    
    #Creates Empty Dataframe To Store What will be pairplotted 
    df3 = pd.DataFrame()
    
    #Empty lists to store values
    avg=[]
    col_averages=[]
    

    
    # df2['averages'] = np.fromstring(temp_df['averages'], dtype=int, sep=',')

    for c in range(len(df2['averages'][0])):
        for d in df2['averages']:
            col_averages.append(d[c])
        avg.append(sum(col_averages)/len(col_averages))
        col_averages.clear()
    
    df3['final_wave'] = avg
            
    
    #Creates variables to make new dataframe
    current_cell = df2['cell_number'].iloc[0]
    temp_df = df2.iloc[1:]
    # list_cannon = []
        
    #Creates the cannonical waveform from previous data frame
    for cell in temp_df: 
        
        #Checks to see if the current cell has the same value of the next
        if current_cell == cell and current_cell <= 137:
            
            #Adds the current_array into a list
            # list_cannon.append([df2['averages'][current_cell]])
            
            #Reinitializes cell
            # current_cell = cell
            
        # When the next_cell does not equal the current cell
        # if current_cell != cell:
            
            #Adds it to list again
            # list_cannon.append([df2['averages'][current_cell]])
            
            #Adds the current cell number to the other column
            # df3['cell_number'] = current_cell
            
            #Reinitializes cell
            # current_cell = cell
    
    
    
    #Exports to CSV file        
    df2.to_csv('E:/Llano Lab/Pair Plot/cannon_waves.csv')
    
    #Data for pairplot
    df3.to_csv('E:/Llano Lab/Pair Plot/ready_for_pair_plot.csv')

    
    
    return df2,df3 

test_cannon_wave()

        
    
        
    