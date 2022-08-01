# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:19:44 2019

@author: Yoshi
"""

import numpy as np
from statistics import mean



def data_reader(image_stack,cell_arrays,background_arrays):
    
    """
    This is the function that reads the 2P signals from the images and applies
    neuropil correction. It first obtains the data value for each cell for each
    frame by averaging the pixel value within each cell's ROI, then finding the
    background value for each cell for each frame by averaging the pixel value
    in the region surrounding the cell's ROI. The corrected data value is found
    using the formula corrected_value = data_value - r * neuropil_value, where
    r is the contamination ratio.
    
    Parameters
    ----------
    image_stack : The numpy array containing the raw images.
    cell_arrays : The list of numpy arrays containing the masks for each of the
        cells.
    background_arrays : The list of numpy arrays containing the masks for the
        regions surrounding the cells.
    
    Returns
    -------
    folder_data : A 2D numpy array containing the corrected data values for
        each cell. The first axis is the cell number and the second axis is the
        frame number.
    """
    
    # Creates empty array to store data in
    image_total = image_stack.shape[0]
    cell_total = len(cell_arrays)
    folder_data = np.zeros((cell_total,image_total),dtype=np.float64)
    contamination_ratio = 0.4
    # Goes through each image
    for image_number,image in enumerate(image_stack):
        
        # Goes through each cell, gathers data from the image, and adds it to the array
        for cell_number in range(cell_total):
            
            # Finds average value of data and adds it to array
            if np.count_nonzero(cell_arrays[cell_number]) == 0:
                data_value = 0
            else:
                data_value = np.sum(image*cell_arrays[cell_number]) / np.count_nonzero(cell_arrays[cell_number])
            if np.count_nonzero(background_arrays[cell_number])!= 0:
                background_value = np.sum(image*background_arrays[cell_number]) / np.count_nonzero(background_arrays[cell_number])
            else:
                background_value = 0
            folder_data[cell_number,image_number] = data_value 
            - contamination_ratio*background_value
    
    return folder_data