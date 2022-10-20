# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:23:13 2022

@author: Austin
"""

import os
import shutil
import numpy as np
import pandas as pd

from operator import add

def sample_averages(data,info_storage):
    
    # Extracts variables from the info_storage class
    # path                     = info_storage.path
    framerate_information    = info_storage.framerate_information
    key                      = info_storage.key
    frequencies              = info_storage.frequencies
    intensities              = info_storage.intensities
    frequency_unit           = info_storage.frequency_unit
    intensity_unit           = info_storage.intensity_unit
    correlation_coefficients = info_storage.correlation_coefficients
    threshold                = info_storage.threshold



    # Declares start of cell graphing
    print("Starting Sample Averaging ")
    
    # Creates output directories
    # cell_trace_output_path = f"{path}/Output/Cell Traces"
    # if os.path.exists(f"{path}/Output/Graphs") == True:
    #     shutil.rmtree(f"{path}/Output/Graphs")
    # if os.path.exists(cell_trace_output_path) == True:
    #     shutil.rmtree(cell_trace_output_path)
    # if os.path.exists(cell_trace_output_path) == False:
    #     os.mkdir(cell_trace_output_path)
    #     os.mkdir(f"{cell_trace_output_path}/Spreadsheets")
    #     os.mkdir(f"{cell_trace_output_path}/Graphs")
    
    #Reverse intensity list
    intensities_reversed = intensities.copy()
    intensities_reversed.reverse()
    
    #Calculates x-axis labels
    cycle_frames = framerate_information[1]
    cycle_duration = framerate_information[2]*1000
    times = []
    step = cycle_duration / cycle_frames
    for frame in range(cycle_frames):
        times.append(step*frame)
    
    #Constants for loops
    cell_total = data.shape[0]
    trial_length = data.shape[3]
    
    #Creates empty hashmap to store data
    sample_hash = {}
    
    #Creates empty list to store values
    current_cell = []
    current_frequency_intensity = []
    current_array = []
    current_coefficient = []
    averages = {'cell_number': current_cell,
                'frequency(kHz),intensity(dB)':current_frequency_intensity,
                'correlation_coefficient':current_coefficient,
                'averages':current_array
                }

    #Goes through each cell
    for cell_number in range(cell_total):

        #Goes through each frequency
        for column_number,frequency in enumerate(frequencies):
            
            #Goes through each intensity
            for row_number,intensity in enumerate(intensities_reversed):
                
                #Obtains sample number from key
                sample_number = key[frequency][intensity]
                
                #Empty array for storing trial total data
                trial_sums = np.zeros(trial_length,dtype=np.float32)
                
                #Sets a value to correlation_coefficient
                correlation_coefficient = correlation_coefficients[
                    cell_number,sample_number][0]
                
                
                for trial in data[cell_number,sample_number]:
                    
                    trial_sums += trial
                
                    #Obtains sample average
                    sample_average = np.mean(data[cell_number,sample_number],
                                             axis=0)
                    
                    #Adds to hashmap 
                    sample_hash[f'{cell_number},{frequency}{frequency_unit},{intensity}{intensity_unit},{correlation_coefficient}']=\
                        [sample_average]
                    
                    # Creates data to put into dataframe
                    current_cell.append(cell_number)
                    current_frequency_intensity.append([frequency,intensity])
                    current_coefficient.append(correlation_coefficient)
                    current_array.append([sample_average])
                    
    #Stores data into dataframe
    df = pd.DataFrame(averages)    
    
    #Stores data into info_storage 
    # info_storage.df = df
    info_storage.sample_hash = sample_hash
    
    # Exports dataframe to csv 
    df.to_csv('E:/Llano Lab/Pair Plot/cell_averages.csv')
    
    #Notifies stage of process
    print('Finishing Sample Averaging')


    return sample_hash,df,info_storage 
    