# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:06:54 2019

@author: Yoshi
"""

def color_key_generator(frequencies):
    
    """
    This function is used to generate a color key for the tonotopic maps. It
    looks at the list of frequencies to determine how many colors are needed in
    total, and generates a shade of green for each frequency.
    
    Parameters
    ----------
    info_storage : The class used to store most of the variables that are used
        in the analysis program.
    
    Returns
    -------
    color_key : A dictionary that has a shade of green for each frequency.
    """
    
    # Finds number of colors needed for key
    steps = len(frequencies)
    
    # Dictionary to store colors
    color_key = {}
    
    # Calculates hue, saturation, and value for each frequency, and adds it to
    # the dictionary
    for step,frequency in enumerate(frequencies):
        hue = 80 + 100 / (steps-1) * step
        saturation = 25 + 75 / (steps-1) * step
        value = 100 - 80 / (steps-1) * step
        color = f"hsv({str(round(hue))},{str(round(saturation))}%,\
                      {str(round(value))}%)"
        color_key[frequency] = color
    
    return color_key