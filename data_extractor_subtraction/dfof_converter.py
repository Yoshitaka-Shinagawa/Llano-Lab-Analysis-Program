# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 23:17:43 2019

@author: Yoshi
"""

import csv
import numpy as np



from background_calculator import *

def dfof_converter(path,raw_data,framerate_information):
    
    # Defines path to key folder
    key_path = f"{path}/Data/Key"
    
    # Reads frame key
    frame_key = {}
    open_frame_key_file = open(f"{key_path}/Frame Key.csv")
    frame_key_file = csv.reader(open_frame_key_file)
    for row in frame_key_file:
        frame_key[row[0]] = row[1]
    open_frame_key_file.close()
    
    # Creates empty array to store data in
    cells = raw_data.shape[1]
    samples = raw_data.shape[0]
    cycle_total = len(frame_key)
    cycle_duration = framerate_information[1]
    data = np.zeros((cells,samples,cycle_total,cycle_duration),dtype=np.float64)
    
    # Goes through each cell, sample, and movie
    for cell in range(cells):
        for sample in range(samples):
            for cycle in range(1,cycle_total+1):
                
                # Reads the data
                cycle_start = int(frame_key[str(cycle)])
                cycle_end = cycle_start + cycle_duration
                cycle_data = raw_data[sample,cell,cycle_start:cycle_end]
                
                # Converts to dF/F
                background_data = background_calculator(cycle_data,cycle_duration)
                dfof_data = (cycle_data-background_data) / background_data * 100
                
                # Sorts data
                data[cell,sample,cycle-1] = dfof_data
    
    return data