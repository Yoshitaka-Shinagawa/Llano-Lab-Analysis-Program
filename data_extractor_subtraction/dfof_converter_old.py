# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 23:17:43 2019

@author: Yoshi
"""

import numpy as np



from background_calculator import *

def dfof_converter(raw_data,framerate_information):
    
    # Creates empty numpy array to write data into
    cells = raw_data.shape[1]
    samples = raw_data.shape[0]
    frames = raw_data.shape[2]
    data_duration = round(framerate_information[0]*framerate_information[1])
    cycle_duration = round(framerate_information[0]*framerate_information[2])
    cycles = int(frames/cycle_duration)
    data = np.zeros((cells,samples,cycles-1,cycle_duration),dtype=np.float64)
    
    # Copies data from experiment module to numpy array
    for cell in range(cells):
        for sample in range(samples):
            sample_data = raw_data[sample,cell,:]
            
            # Separates sample into cycles and store data into numpy array
            for cycle in range(1,cycles):
                cycle_start = cycle*cycle_duration
                cycle_end = cycle_start + data_duration
                cycle_data = sample_data[cycle_start:cycle_end]
                background_data = background_calculator(cycle_data,data_duration)
                data[cell,sample,cycle-1] = (cycle_data-background_data) / background_data * 100
    
    return data