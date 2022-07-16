# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:19:39 2019

@author: Yoshi
"""

import numpy as np



def cell_excitatory_flagger(cell_number,data,info_storage):
    
    """
    This is the function used to find the best frequency (the frequency that
    cells are most responsive to across all frequencies) and characteristic
    frequency (the frequency that cells are most responsive to at the lowest
    responsive amplitude). It first sees if any of the average correlation
    coefficients are above the threshold to see whether the cell is responsive
    in general or not. It then calculates the best frequency by finding the
    frequency at which the total area under the curve is the highest. Next, it
    calculates the characteristic frequency by finding the lowest amplitude at
    which any of the responses have an average correlation coefficient above
    the threshold, and finding the frequency with the highest area under the
    curve at that frequency.
    
    Parameters
    ----------
    cell_number : The number of the cell being analyzed.
    data : The 4D numpy array containing the dF/F values. The first axis is the
        cell number, the second axis is the sample number (unique combination
        of frequency and amplitude), the third number is the trial number
        (repetition of the same frequency and amplitude combination), and the
        fourth axis is the frame number for each segment.
    info_storage : The class used to store most of the variables that are used
        in the analysis program.

    Returns
    -------
    best_frequency : The best frequency of the cell.
    characteristic_frequency : The characteristic frequency of the cell.
    """
    
    # Extracts variables from the info_storage class
    key                      = info_storage.key
    frequencies              = info_storage.frequencies
    intensities              = info_storage.intensities
    correlation_coefficients = info_storage.correlation_coefficients
    areas_under_curves       = info_storage.areas_under_curves
    threshold                = info_storage.threshold
    
    # Default flags
    best_frequency,characteristic_frequency = "N/A","N/A"
    responsive = False
    
    # Creates an empty list to store correlation coefficients of the cell
    correlation_coefficient_list = []
    
    # Goes through each sample and adds correlation coefficient to list
    sample_total = correlation_coefficients.shape[1]
    for sample_number in range(sample_total):
        correlation_coefficient_list.append(correlation_coefficients[
            cell_number,sample_number])
    
    # Sees if the highest correlation coefficient is higher than the threshold,
    # and if so, marks the cell as being responsive
    if max(correlation_coefficient_list) > threshold:
        responsive = True
    
    # Calculates the best frequency
    if responsive == True:
        
        #Creates empty list to store total areas under curves
        area_frequency_totals = []
        
        # Goes through each sample by frequency to calculate total areas under
        # curves, and adds it to list
        for frequency in frequencies:
            area_frequency_total = 0.0
            for intensity in intensities:
                sample_number = key[frequency][intensity]
                area_frequency_total += areas_under_curves[
                    cell_number,sample_number]
            area_frequency_totals.append(area_frequency_total)
        
        # Finds frequency with highest area under curve and sets it equal to 
        # best frequency
        max_index = area_frequency_totals.index(max(area_frequency_totals))
        best_frequency = frequencies[max_index]
        
        # # Creates empty list to store frequency averages
        # dfof_frequency_maxes = []
        
        # # Goes through each sample by frequency to calculate the highest
        # # summed peak, and adds it to list
        # for frequency in frequencies:
        #     dfof_frequency_max = 0.0
        #     for intensity in intensities:
        #         sample_number = key[frequency][intensity]
        #         trial_summed = np.zeros(data.shape[3])
        #         for trial_data in data[cell_number,sample_number]:
        #             trial_summed += trial_data
        #         dfof_frequency_max += max(trial_summed)
        #     dfof_frequency_maxes.append(dfof_frequency_max)
        
        # # Finds frequency with highest summed peak and sets it equal to best 
        # # frequency
        # max_index = dfof_frequency_maxes.index(max(dfof_frequency_maxes))
        # best_frequency = frequencies[max_index]
    
    # Calculates the characteristic frequency
    if responsive == True:
        
        # Goes through each intensity
        for intensity in intensities:
            area_frequency_totals = []
            intensity_r_list = []
            for frequency in frequencies:
                sample_number = key[frequency][intensity]
                intensity_r_list.append(correlation_coefficients[
                    cell_number,sample_number])
                area_frequency_totals.append(areas_under_curves[
                    cell_number,sample_number])
            
            # If highest correlation coefficient is above threshold, then sets
            # it as the characteristic frequency
            if max(intensity_r_list) > threshold:
                max_index = area_frequency_totals.index(max(
                    area_frequency_totals))
                characteristic_frequency = frequencies[max_index]
                break
        
        # # Goes through each intensity
        # for intensity in intensities:
        #     dfof_frequency_maxes = []
        #     intensity_r_list = []
        #     for frequency in frequencies:
        #         sample_number = key[frequency][intensity]
        #         intensity_r_list.append(correlation_coefficients[
        #             cell_number,sample_number])
        #         trial_summed = np.zeros(data.shape[3])
        #         for trial_data in data[cell_number,sample_number]:
        #             trial_summed += trial_data
        #         dfof_frequency_maxes.append(max(trial_summed))
        #     
        #     # If highest correlation coefficient is above threshold, then sets 
        #     if max(intensity_r_list) > threshold:
        #         max_index = dfof_frequency_maxes.index(max(
        #             dfof_frequency_maxes))
        #         characteristic_frequency = frequencies[max_index]
        #         break
    
    return best_frequency,characteristic_frequency