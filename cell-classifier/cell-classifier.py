#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Sep  9 11:07:53 2022

@author: Austin

if peak occurs before 500 ms Excitatory Onset

If peak occurs after 500ms Excitatory Offset 

If negative peak occurs before 500ms Inhibitory Offset

If negative peak occurs after 500ms Inhibitory Offset

If peak is not at least ___ or integral is below ___ no response

Print to Excel sheet 


"""

import os
import shutil
import numpy as np

def cell_classifier(data, info_storage):
    
    """
    This is the function used to plot the 2P signals for each cell for each
    combination of frequency and amplitude, as well as exporting the
    average correlation coefficient, area under the curve, and the peak value
    for each stimulus to an Excel spreadsheet. It creates a subplot grid for
    each stimulus, then plots the individual traces for each signal, as well as
    the average plot for each stimulus. It then colors the subplot in a shade
    of green depending on the average correlation coefficient. It also gathers
    the average correlation coefficient, area under the curve, and the peak
    value for the cells, and creates an Excel spreadsheet to export all of the
    data into.
    
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
    none
    """
    
    
    # Extracts variables from the info_storage class
    path                     = info_storage.path
    cell_flags            = info_storage.cell_flags
    framerate_information = info_storage.framerate_information
    mode                  = info_storage.mode
    
    # Creates output directories
    cell_classification_path = f"{path}/Output/Cell Traces"
    if os.path.exists(f"{path}/Output/Classifications") == True:
        shutil.rmtree(f"{path}/Output/Classifications")
    if os.path.exists(cell_classification_path) == False:
        os.mkdir(f"{cell_classification_path}/Classifcations")
        