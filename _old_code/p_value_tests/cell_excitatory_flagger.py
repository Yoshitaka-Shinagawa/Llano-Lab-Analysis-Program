# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:19:39 2019

@author: Yoshi
"""

import numpy as np
import scipy.stats as stats



def cell_excitatory_flagger(cell_number,dfof_data,key,frequencies,decibels,pvalue_threshold):
    
    # Default flags
    best_frequency,characteristic_frequency = 'N/A','N/A'
    
    # Creates averages for each cell's data
    dfof_sample_averages = []
    sample_total = dfof_data.shape[0]
    for sample_number in range(sample_total):
        
        # Creates averages for each trial
        dfof_trial_averages = []
        for trial_data in dfof_data[sample_number,cell_number]:
            dfof_trial_averages.append(np.mean(trial_data))
        dfof_sample_averages.append(dfof_trial_averages)
    
    # Determines if the neuron has a statistically significatnt difference in response among different frequencies
    _,pvalue = stats.f_oneway(*dfof_sample_averages)
    
    # Calculates the best frequency
    if pvalue < pvalue_threshold:
        
        # Creates empty list to store frequency averages
        dfof_frequency_averages = []
        
        # Goes through each sample by frequency to create an average and add it to the list
        for frequency in frequencies:
            dfof_frequency_average = []
            for decibel in decibels:
                sample_number = key[frequency][decibel]
                dfof_frequency_average.append(np.mean(dfof_sample_averages[sample_number]))
            dfof_frequency_averages.append(np.mean(dfof_frequency_average))
        
        # Finds the larges average df/f value and sets it equal to the best frequency
        max_index = dfof_frequency_averages.index(max(dfof_frequency_averages))
        best_frequency = frequencies[max_index]
    
    # Calculates the characteristic frequency
    if pvalue < pvalue_threshold:
        
        cell_threshold_dfof = []
        
        for decibel in decibels:
            dfof_decibel_averages = []
            for frequency in frequencies:
                sample_number = key[frequency][decibel]
                dfof_decibel_averages.append(dfof_sample_averages[sample_number])
            
            
            if stats.f_oneway(*dfof_decibel_averages)[1] < pvalue_threshold*10:
                for dfof_decibel_average in dfof_decibel_averages:
                    cell_threshold_dfof.append(np.mean(dfof_decibel_average))
                break
        
        if len(cell_threshold_dfof) != 0:
            max_at_threshold = cell_threshold_dfof.index(max(cell_threshold_dfof))
            characteristic_frequency = frequencies[max_at_threshold]
        
    
    return best_frequency,characteristic_frequency