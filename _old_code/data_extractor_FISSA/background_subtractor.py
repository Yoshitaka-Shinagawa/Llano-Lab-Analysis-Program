# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 23:32:10 2019

@author: Yoshi
"""

import numpy as np



def background_subtractor(segment):
    
    # Constants for loops
    segment_length = len(segment)
    
    # Make empty list for background
    background_data = []
    
    # Finds the start and end values for the background and finds the slope
    slope = (segment[-1]-segment[0]) / segment_length
    
    # Creates a line for the background
    for i in range(segment_length):
        background_data.append(segment[0]+slope*i)
    
    # Converts to array
    background_data = np.array(background_data,dtype=np.float32)
    
    # Subtracts background from actual data
    subtracted_data = segment - background_data
    
    return subtracted_data