# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:06:54 2019

@author: Yoshi
"""

def color_key_generator(frequencies):
    
    # Finds number of colors needed for key
    steps = len(frequencies)
    
    # Dictionary to store colors
    color_key = {}
    
    # Calculates hue, saturation, and value for each frequency, and adds it to the dictionary
    for step,frequency in enumerate(frequencies):
        hue = 80 + 100 / (steps-1) * step
        saturation = 25 + 75 / (steps-1) * step
        value = 100 - 80 / (steps-1) * step
        color = f"hsv({str(round(hue))},{str(round(saturation))}%,{str(round(value))}%)"
        color_key[frequency] = color
    
    return color_key