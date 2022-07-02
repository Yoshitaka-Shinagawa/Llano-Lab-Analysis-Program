# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:46:26 2020

@author: Yoshi
"""

import csv
import numpy as np



from background_calculator import *

def data_sorter(path,raw_data,folders_list,framerate_information):
    
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
    movie_total = raw_data.shape[0]
    cycle_total = len(frame_key)
    cycle_duration = framerate_information[1]
    data = np.zeros((cells,cycle_total,movie_total,cycle_duration),dtype=np.float64)
    
    # Goes through each movie
    for movie in range(movie_total):
        
        # Reads the key for each movie
        movie_key = {}
        open_movie_key_file = open(f"{key_path}/Movies/{folders_list[movie]}.csv")
        
        movie_key_file = csv.reader(open_movie_key_file)
        for row in movie_key_file:
            movie_key[row[0]] = row[1]
        open_movie_key_file.close()
        
        # Goes through each cell
        for cell in range(cells):
            
            # Goes through each cycle
            for cycle in range(1,cycle_total+1):
                
                # Reads the data
                cycle_start = int(frame_key[str(cycle)])
                cycle_end = cycle_start + cycle_duration
                cycle_data = raw_data[movie,cell,cycle_start:cycle_end]
                
                # Converts to dF/F
                background_data = background_calculator(cycle_data,cycle_duration)
                dfof_data = (cycle_data-background_data) / background_data * 100
                
                # Sorts data
                sample_number = int(movie_key[str(cycle)])
                data[cell,sample_number-1,movie] = dfof_data
    
    return data