# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:19:39 2019

@author: Yoshi
"""

import numpy as np



def cell_noise_flagger(cell_number,info_storage):
    
    """
    This is the function used to determine whether a cell is responsive to the
    noise stimulus or not. The cell is marked as being responsive if the
    average correlation coefficient for the noise stimulus is above the
    specified threshold.
    
    Parameters
    ----------
    cell_number : The number of the cell being analyzed.
    info_storage : The class used to store most of the variables that are used
        in the analysis program.
    
    Returns
    -------
    noise : The response of the cell to noise stimulus
    """
    
    # Extracts variables from the info_storage class
    correlation_coefficients = info_storage.correlation_coefficients
    first_correlation        = info_storage.first_correlation
    threshold                = info_storage.threshold
    
    # Cutoff for determining what"s considered responsive and what"s not
    if threshold == "Default":
        threshold = 0.6
    
    # Default flags
    noise = "N/A"
    adaptive_1st_trial = "N/A"
    responsive = False
    
    # Creates an empty list to store correlation coefficients of the cell
    correlation_coefficient_list = []
    
    # Determines if cell is responsive to noise stimulus or not, and flags for noise
    if correlation_coefficients[cell_number,0] > threshold:
        responsive = True
        noise = "Yes"
        
    if first_correlation[cell_number,0] <= 0.2:
        responsive = True
        adaptive_1st_trial = "Yes"
    
    return noise,adaptive_1st_trial