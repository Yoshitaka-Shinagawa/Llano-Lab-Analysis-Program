# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 14:59:35 2022

@author: Austin
"""

import numpy as np

def first_2_trials_extractor(data):
    

    
    # Constants for loops
    cells_total = data.shape[0]
    samples_total = data.shape[1]
    two_trials = 2
    frames_total = data.shape[3]
    half_of_frames = frames_total/2
    half_of_frames = int(half_of_frames)
    
    # Empty arrays to store the new data into 
    data_first_two = np.zeros((cells_total,samples_total,two_trials,frames_total))
    
    
    # Copies the onset data into the new 4d Array 
    for cell in range(cells_total):
        for sample in range(samples_total):
            for trial in range(two_trials):
                    np.copyto(data_first_two[cell,sample,trial],data[cell,sample,trial])
    
   
    return data_first_two