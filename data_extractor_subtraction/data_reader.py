# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:19:44 2019

@author: Yoshi
"""

import numpy as np
from statistics import mean



def data_reader(image_stack,cell_arrays,background_arrays):
    
    # Creates empty array to store data in
    image_total = image_stack.shape[0]
    cell_total = len(cell_arrays)
    folder_data = np.zeros((cell_total,image_total),dtype=np.float64)
    
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
            folder_data[cell_number,image_number] = data_value - 0.4*background_value
    
    return folder_data