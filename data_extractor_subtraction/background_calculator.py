# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 23:32:10 2019

@author: Yoshi
"""

import numpy as np

def background_calculator(cycle_data,cycle_duration):
    
    """
    This is the function used to calculate the background value for each
    analysis segment that also takes in bleaching into consideration. It does
    so by calculating the slope between the first and last values of the
    analysis segment and considers that to be the background value. While this
    method is far from perfect and possibly flawed, it is easy to implement and
    has been reliable thus far.
    
    Parameters
    ----------
    cycle_data: The array containing the corrected data values for the analysis
        segment.
    cycle_duration: The integer representing the duration of the analysis
        segment in terms of the number of frames.
    
    Returns
    -------
    background_data: The array containing the estimated background for the
        analysis segment.
    """
    
    # Make empty list for background
    background_data = []
    
    # Finds the start and end values for the background and finds the slope
    slope = (cycle_data[-1]-cycle_data[0]) / cycle_duration
    
    # Creates a line for the background
    for i in range(cycle_duration):
        background_data.append(cycle_data[0]+slope*i)
    
    # Converts to array
    background_data = np.array(background_data,dtype=np.float64)
    
    return background_data