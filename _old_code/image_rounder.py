# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 20:21:19 2019

@author: Yoshi
"""

import numpy as np



def image_rounder(image):
    
    # Converts float array to int array
    image_rounded = np.around(image)
    image_rounded = image_rounded.astype(np.uint16)
    
    return image_rounded