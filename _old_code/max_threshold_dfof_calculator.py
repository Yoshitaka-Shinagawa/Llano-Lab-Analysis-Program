# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:11:38 2019

@author: Yoshi
"""

import numpy as np



def max_threshold_dfof_calculator(data):
    
    # Adds average df/f values of each sample into list
    dfof_averages = []
    for cell in data:
        for sample in cell:
            for trial in sample:
                dfof_averages.append(np.mean(trial))
    
    # Calculates max value
    max_dfof = max(dfof_averages)
    
    # Calculates threshold value
    threshold_dfof = np.mean(dfof_averages) + np.std(dfof_averages)
    
    return max_dfof,threshold_dfof