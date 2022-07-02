# -*- coding: utf-8 -*-
"""
Created on Thu May 28 11:28:32 2020

@author: Yoshi
"""

import numpy as np
import scipy.stats as stats
import math



def correlation_calculator(data):
    
    # Creates a blank numpy array to store correlation coefficients in
    correlation_coefficients = np.zeros((data.shape[0],data.shape[1],1),dtype=np.float32)
    
    # Creates a list of combinations of trials
    trials = data.shape[2]
    combinations = []
    for x in range(0,trials-1):
        for y in range(x+1,trials):
            combinations.append([x,y])
    
    # Goes through each cell and trial
    cells_total = data.shape[0]
    samples_total = data.shape[1]
    for cell in range(cells_total):
        for sample in range(samples_total):
            
            # Empty list for storing correlation coefficients
            sample_r_values = []
            
            # Goes through each combination
            for combination in combinations:
                trial_a,trial_b = combination
                
                # Calculates correlation coefficient between each combination of trial, and adds them to list
                r,p = stats.pearsonr(data[cell,sample,trial_a],data[cell,sample,trial_b])
                if math.isnan(r):
                    r = 0
                sample_r_values.append(r)
            
            # Calculates the average correlation coefficient and adds it to coefficient array
            average_r = np.mean(sample_r_values)
            correlation_coefficients[cell,sample] = average_r
    
    return correlation_coefficients