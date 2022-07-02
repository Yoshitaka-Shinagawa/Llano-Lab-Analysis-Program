# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 20:10:12 2019

@author: Yoshi
"""

import numpy as np



def image_normalizer(image,bit_depth=16):
    
    # Finds the max value in the image
    max_value = np.amax(image)
    
    # Creates a blank array for storing pixel values in
    normalized_image = np.zeros((len(image),len(image[0])),dtype=np.uint16)
    
    # Calculates the scale
    scale = 2**bit_depth / max_value
    
    # Normalizes the image
    normalized_image = np.around(image*scale)
    normalized_image = normalized_image.astype(np.uint16)
    
    return normalized_image