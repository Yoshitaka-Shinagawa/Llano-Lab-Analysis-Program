# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 23:32:10 2019

@author: Yoshi
"""

import numpy as np

def background_calculator(segment,data_duration):
    
    # Make empty list for background
    background_data = []
    
    # Finds the start and end values for the background and finds the slope
    slope = (segment[-1]-segment[0]) / data_duration
    
    # Creates a line for the background
    for i in range(data_duration):
        background_data.append(segment[0]+slope*i)
    
    # Converts to array
    background_data = np.array(background_data,dtype=np.float64)
    
    return background_data