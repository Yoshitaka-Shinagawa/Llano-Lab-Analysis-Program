# -*- coding: utf-8 -*-
"""
Created on Thu May 28 11:28:32 2020

@author: Yoshi
"""

import numpy as np
import scipy.stats as stats
import math



def correlation_calculator(data):
    
    """
    This is the function used to calculate the average correlation coefficient
    for each stimuli. Since a correlation coefficient can only be calculated
    between two timeseries, the correlation coefficient for every possible
    combination of pairs of repetition is calculated, then averaged.
    
    Parameters
    ----------
    data : The 4D numpy array containing the dF/F values. The first axis is the
        cell number, the second axis is the sample number (unique combination
        of frequency and amplitude), the third number is the trial number
        (repetition of the same frequency and amplitude combination), and the
        fourth axis is the frame number for each segment.
    
    Returns
    -------
    correlation_coefficients : A 2D numpy array containing the average
        correlation coefficient for each stimulus. The first axis is the cell
        number and the second axis is the sample number (unique combination
        of frequency and amplitude).
    """
    
    # Creates a blank numpy array to store correlation coefficients in
    correlation_coefficients = np.zeros((data.shape[0],data.shape[1],1),dtype=np.float32)
    first_correlation = np.zeros((data.shape[0],data.shape[1],1),dtype=np.float32)
    
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
            sample_r_values_of_first = []
            
            # Goes through each combination
            for combination in combinations:
                trial_a,trial_b = combination
                
                # Calculates correlation coefficient between each combination of trial, and adds them to list
                r,p = stats.pearsonr(data[cell,sample,trial_a],data[cell,sample,trial_b])
                if math.isnan(r):
                    r = 0
                sample_r_values.append(r)
                
                if trial_a == 0:
                
                    sample_r_values_of_first.append(r)
            
            # Calculates the average correlation coefficient and adds it to coefficient array
            average_r = np.mean(sample_r_values)
            average_first_trial_r = np.mean(sample_r_values_of_first)
            correlation_coefficients[cell,sample] = average_r
            first_correlation[cell,sample] = average_first_trial_r 
    
    return correlation_coefficients,first_correlation