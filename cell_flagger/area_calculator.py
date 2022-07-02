# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 18:05:21 2021

@author: Yoshi
"""

import numpy as np
from scipy import integrate



def area_calculator(data,framerate_information):
    
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