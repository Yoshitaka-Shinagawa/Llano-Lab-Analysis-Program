# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:19:39 2019

@author: Yoshi
"""

import numpy as np



def cell_noise_flagger(cell_number,correlation_coefficients,threshold):
    
    # Cutoff for determining what"s considered responsive and what"s not
    if threshold == "Default":
        threshold = 0.6
    
    # Default flags
    noise = "N/A"
    responsive = False
    
    # Creates an empty list to store correlation coefficients of the cell
    correlation_coefficient_list = []
    
    # Determines if cell is responsive to noise stimulus or not, and flags for noise
    if correlation_coefficients[cell_number,0] > threshold:
        responsive = True
        noise = "Yes"
    
    return noise