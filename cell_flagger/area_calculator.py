# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 18:05:21 2021

@author: Yoshi
"""

import numpy as np
from scipy import integrate



def area_calculator(data,framerate_information):
    
    """
    This is the function used to calculate the area under the curve for each
    combination of frequency and amplitude. It first calculates the average
    signal trace for each stimulus, then approximates the area under the curve
    with Simpson's method using the integrate.simpson function from the scipy
    library. 
    
    Parameters
    ----------
    data : The 4D numpy array containing the dF/F values. The first axis is the
        cell number, the second axis is the sample number (unique combination
        of frequency and amplitude), the third number is the trial number
        (repetition of the same frequency and amplitude combination), and the
        fourth axis is the frame number for each segment.
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
    areas_under_curves : A 2D numpy array containing the area under the curve
        for each stimulus. The first axis is the cell number and the second
        axis is the sample number (unique combination of frequency and
        amplitude).
    """
    
    # Calculates x interval in seconds
    cycle_frames = framerate_information[1]
    cycle_duration = framerate_information[2]*1000
    x_interval = cycle_duration / cycle_frames
    
    # Creates a blank numpy array to store area under curves in
    areas_under_curves = np.zeros((data.shape[0],data.shape[1],1),dtype=np.float32)
    
    # Goes through each cell and trial
    cells_total = data.shape[0]
    samples_total = data.shape[1]
    for cell in range(cells_total):
        for sample in range(samples_total):
            
            # Calculates area under curve of average trace and adds it to area array
            average_trace = np.mean(data[cell,sample],axis=0)
            areas_under_curves[cell,sample] = integrate.simpson(average_trace,dx=x_interval)
    
    return areas_under_curves