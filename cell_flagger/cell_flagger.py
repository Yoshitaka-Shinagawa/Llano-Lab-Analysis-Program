# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:09:08 2019

@author: Yoshi
"""

from correlation_calculator import *
from area_calculator import *
from cell_excitatory_flagger import *
from cell_noise_flagger import *
from std_calculator import *

def cell_flagger(data,info_storage):
    
    """
    This is the function used to determine which combination of frequency and
    amplitude the cells are responsive to. It does so by calculating the
    average correlation coefficient of all of the repetitions for each
    combination of frequency and amplitdue, and if it is above the threshold,
    then the cell is flagged as being responsive to that particular stimulus.
    
    Parameters
    ----------
    data : The 4D numpy array containing the dF/F values. The first axis is the
        cell number, the second axis is the sample number (unique combination
        of frequency and amplitude), the third number is the trial number
        (repetition of the same frequency and amplitude combination), and the
        fourth axis is the frame number for each segment.
    info_storage : The class used to store most of the variables that are used
        in the analysis program.
    
    Returns
    -------
    info_storage : The function returns the info_storage class with the
        cell_flags, correlation_coefficients, areas_under_curves variables
        added.
    """
    
    # Extracts variables from the info_storage class
    cell_flags            = info_storage.cell_flags
    framerate_information = info_storage.framerate_information
    mode                  = info_storage.mode
    
    # Copies cell_flags
    cell_flags_first_trial = cell_flags.copy()
    
    # Declares start of cell flagging
    print("Starting cell flagging")
    
    # Calculates the standard deviation of each trial at every frame
    standard_deviations = std_calculator(data,framerate_information)
    
    # Calculates average correlation coefficients for each sample
    correlation_coefficients,first_correlation = correlation_calculator(data)
    
    # Calculates area under ccurve for each sample
    areas_under_curves = area_calculator(data,framerate_information)
    
    # Adds new information to the info_storage class
    info_storage.correlation_coefficients = correlation_coefficients
    info_storage.first_correlation        = first_correlation
    info_storage.areas_under_curves       = areas_under_curves
    
    # Excitatory cell flagging
    if mode == 0:
        
        # Goes through each cell
        cell_total = data.shape[0]
        for cell_number in range(cell_total):
            
            # Finds best frequency and characteristic frequency of each cell
            best_frequency,characteristic_frequency = cell_excitatory_flagger(
                cell_number,data,info_storage)
            cell_flags[cell_number].append(best_frequency)
            cell_flags[cell_number].append(characteristic_frequency)
    
    # Noise cell flagging
    if mode == 1:
        
        # Goes through each cell
        cell_total = data.shape[0]
        for cell_number in range(cell_total):
            
            # Determines if the cell is responsive to noise
            noise,adaptive = cell_noise_flagger(cell_number,info_storage)
            cell_flags[cell_number].append("N/A")
            cell_flags[cell_number].append("N/A")
            cell_flags[cell_number].append(noise)
            
            noise,adaptive = cell_noise_flagger(cell_number,info_storage)
            cell_flags_first_trial[cell_number].append("N/A")
            cell_flags_first_trial[cell_number].append("N/A")
            cell_flags_first_trial[cell_number].append(adaptive)
        
    
    # Adds new information to the info_storage class
    info_storage.cell_flags = cell_flags
    info_storage.cell_flags_first_trial = cell_flags_first_trial
    info_storage.standard_deviations = standard_deviations 
    
    # Declares end of cell flagging
    print("Finished cell flagging")
    
    return info_storage