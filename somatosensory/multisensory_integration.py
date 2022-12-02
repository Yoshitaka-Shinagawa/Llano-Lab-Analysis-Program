# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 09:45:40 2022

@author: Austin
"""

import numpy as np
import pandas as pd
from scipy import integrate

def multisensory_integration(data,info_storage):
    
    #Extracts info_storage information
    path                     = info_storage.path
    framerate_information    = info_storage.framerate_information
    cell_flags               = info_storage.cell_flags
    standard_deviations      = info_storage.standard_deviations
    cell_flags_first_trial   = info_storage.cell_flags_first_trial

    
    
    #Creates a directiory to save the excel sheets to
    cell_traces_path = f'{path}/Output/Cell Traces/Spreadsheets'
    
    # Calculates x interval in seconds
    cycle_frames = framerate_information[1]
    cycle_duration = framerate_information[2]*1000
    x_interval = cycle_duration / cycle_frames
    
    # Creates a blank numpy array to store area under curves and peak values in
    areas_under_curves = np.zeros((data.shape[0],data.shape[1],data.shape[2]),dtype=np.float32)
    peak_values = np.zeros((data.shape[0],data.shape[1],data.shape[2]),dtype=np.float32)
    
    # Goes through each cell and trial
    cells_total = data.shape[0]
    samples_total = data.shape[1]
    trials_total = data.shape[2]
    frames_total = data.shape[3]
    
    #Creates empty lists to store values into
    cell_numbers = []
    cell_flag_list = []
    cell_adaptive_list = []
    df = pd.DataFrame()
    
    #Makes a column for cell number
    for cell in range(cells_total):
        cell_numbers.append(cell+1)
        cell_flag_list.append(cell_flags[cell][3])
        cell_adaptive_list.append(cell_flags_first_trial[cell][3])

    #Adds a cell_number and cell flag column
    df['cell_number'] = cell_numbers
    df['cell_flag'] = cell_flag_list
    df['adaptive_1_trial'] = cell_adaptive_list
    df['first_response'] = "N/A"
    
    # Creates columns that will be replaced 
    for i in range(1,6):
        df[f'peak_{i}'] = cell_numbers
    
    for i in range(1,6):
        df[f'auc_{i}'] = cell_numbers
                    
    #Adds the data into a 3d Array 
    for cell in range(cells_total):
        
        #Creates counter to be used for later
        n=1
        
        for sample in range(samples_total):
            for trial in range(trials_total):
                    
                    #Creates a variable for the current trial 
                    current_trial = data[cell,sample,trial]
                    
                    # Calculates area under curve for each trial
                    areas_under_curves[cell,sample,trial] = integrate.simpson(current_trial,dx=x_interval)
                    
                    
                    #Finds the peak values per trial
                    peak_values[cell,sample,trial] = round(max(current_trial),2)
        
                    #Adds data to dataframe
                    df.loc[[cell],[f'peak_{n}']] = peak_values[cell,sample,trial]
                    df.loc[[cell],[f'auc_{n}']] = areas_under_curves[cell,sample,trial]
                    
                    #Adds to Counter  
                    n+=1
    

    # Checks the first trial and checks if it is responsive
    # for cell in range(cells_total):
    #     for sample in range(samples_total):
    #         for trial in range(1):
    #             for frame in range(frames_total):
                    
    #                 i = 0
                
                    # Creates variables for current standard deviation and frame
                    # current_frame = data[cell,sample,trial,frame]
                    # current_cell_flag = cell_flag_list[cell]
                    # sample_average = np.mean(data[cell,sample],\
                                             # axis=0)
                    # if current_cell_flag == 'Yes' and current_frame >= sample_average[frame]:
                        
                        # i+= 1
                        # df.loc[[cell],['first_response']] = "Yes"
                        # i = 0 
                    
                    # i = 1
                    # cell += 1
                    
                    
    # print(df)
    # print(i)

    #Creates excel sheets
    writer_trial = pd.ExcelWriter(f"{cell_traces_path}/Data_by_Trial.xlsx")
    
    #Puts the dataframes into Excel
    df.to_excel(writer_trial, index =False)

    #Saves and closes the excel sheets
    writer_trial.save()
    writer_trial.close()

    return df
    
    
   