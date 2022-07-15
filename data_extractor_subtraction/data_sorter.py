# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:46:26 2020

@author: Yoshi
"""

import csv
import numpy as np



from background_calculator import *

def data_sorter(path,raw_data,folders_list,framerate_information):
    
    """
    This is the function used to reorganize the data and convert to dF/F
    values. It first imports the frame key, which is used to determine the
    movie frame that each analysis segment starts at. It then goes through each
    movie and imports the movie key, which is used to determine which order the
    stimuli were given in. Finally, it goes through each analysis segment and
    subtracts the sloping background, which is used to estimate the background
    fluorescence and takes in bleaching into account, and converts the data
    value into dF/F values.
    
    Parameters
    ----------
    path : The path to the parent folder of the data folder.
    raw_data : The numpy array containing the corrected data values for each
        cell for all movies.
    folders_list : The list containing the names of the folders that contain
        the image files from the 2P microscope. This is used to match the movie
        with its key.
    framerate_information : The information regarding framerates for the
        movies. It is a tuple of three numbers, (framerate,total_frames,
        seconds), where framerate is a float/integer representing the number of
        frames per second that was used to acquire the images, total_frames is
        an integer representing the number of frames in each analysis segment,
        and seconds is a float representing the number of seconds that each
        analysis segment takes. Of these numbers, the first and last are used
        purely for labeling the graph later in the analysis, and is not as
        critical to the analysis as the middle number.
    
    Returns
    -------
    data : A 4D numpy array containing the dF/F values. The first axis is the
        cell number, the second axis is the sample number (unique combination
        of frequency and amplitude), the third number is the trial number
        (repetition of the same frequency and amplitude combination), and the
        fourth axis is the frame number for each segment.
    """
    
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