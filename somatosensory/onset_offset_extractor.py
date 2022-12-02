# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 13:51:03 2022

@author: Austin
"""

import numpy as np

def onset_offset_extractor(data):
    
    
    # Prints a notifier
    print("Starting onset and offset data extraction")
    
    # Constants for loops
    cells_total = data.shape[0]
    samples_total = data.shape[1]
    trials_total = data.shape[2]
    frames_total = data.shape[3]
    half_of_frames = frames_total/2
    half_of_frames = int(half_of_frames)
    
    # Empty arrays to store the new data into 
    data_onset = np.zeros((cells_total,samples_total,trials_total,half_of_frames))
    data_offset = np.zeros((cells_total,samples_total,trials_total,half_of_frames)) 
    
    # Reverses the array
    reversed_data = data[:,:,:,::-1]
    
    
    # Copies the onset data into the new 4d Array 
    for cell in range(cells_total):
        for sample in range(samples_total):
            for trial in range(trials_total):
                for frame in range(half_of_frames):
                    data_onset[cell,sample,trial,frame] = data[cell,sample,trial,frame]
    
    # Copies the offset data into the new 4d Arra 
    for cell in range(cells_total):
        for sample in range(samples_total):
            for trial in range(trials_total):
                for frame in range(half_of_frames):
                    data_offset[cell,sample,trial,frame]=reversed_data[cell,sample,trial,frame]
    
    #Reverses the data again so that it shows up in the right way
    data_offset = data_offset[:,:,:,::-1]
    
    
    # Prints another notifier
    print("Finished onset and offset data extraction")
    
    return data_onset,data_offset
    
    