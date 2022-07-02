# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 18:35:31 2019

@author: Yoshi
"""

def scale_calculator(width):
    
    # Creates a variable, scale
    scale = 1
    
    # Checks if the image is less than 1500 pixels wide
    if width < 1500:
        
        # Finds the minimum integer multiplier until width is at least 2000 pixels
        while width*scale < 2000:
            scale += 1
    
    # Checks if the image is betwen 1500 and 2000 pixels wide
    elif width < 2000 and width >= 1500:
        scale = 1.5
    
    # Checks if the image is between 3000 and 4000 pixels wide
    elif width <= 4000 and width > 3000:
        scale = 2/3
    
    # Checks if the image is more than 2000 pixels wide
    elif width > 4000:
        
        # Finds the minimum factor of 2 that makes the image barely over 2000 pixels wide
        while width*(scale/2) > 2000:
            scale = scale / 2
    
    return scale
