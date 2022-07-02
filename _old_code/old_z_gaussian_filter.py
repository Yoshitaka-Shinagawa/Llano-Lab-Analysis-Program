# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:34:52 2019

@author: Yoshi
"""

import numpy as np
from scipy.stats import norm



def z_gaussian_filter(folder_data,sigma):
    
    # Creates a blank array for storing pixel values in
    filtered_data = np.zeros(folder_data.shape,dtype=np.uint16)
    
    # Calculates the z width
    z_width = round(2*sigma)
    
    # Constants outside of loop
    image_size = folder_data.shape[1:]
    
    # Creates a dictionary of weights
    weights = {}
    for x in range(-z_width,z_width+1):
        weights[x] = norm.pdf(x,0,sigma)
    
    # Goes through each image
    image_total = len(folder_data)
    for image in range(image_total):
        
        # Sets the frame offsets at which blurring begins and ends
        begin = -z_width
        end = z_width
        if image+begin < 0:
            begin = -image
        if image+end > image_total-1:
            end = image_total-1-image
        
        # Calculates the weighted average per array
        weight_sum = 0
        pixel_sums = np.zeros(image_size,dtype=np.float64)
        for x in range(begin,end+1):
            weight = weights[x]
            weight_sum += weight
            pixel_sums += weight*folder_data[image+x]
        pixel_sums = np.around(pixel_sums/weight_sum)
        pixel_sums = pixel_sums.astype(np.uint16)
        filtered_data[image] = pixel_sums
    
    return filtered_data