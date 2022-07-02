# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 15:58:31 2022

@author: Yoshi
"""

def modulation_color_key_generator():
    
    # Dictionary to store colors
    color_key = {}
    
    # Calculates HSV values for negative values
    negative_list = [-1.0,-0.8,-0.6,-0.4,-0.2]
    for index in negative_list:
        hue = 160 - 80 * index
        saturation = 25 - 75 * index
        value = 100 + 80 * index
        color = f"hsv({str(round(hue))},{str(round(saturation))}%,{str(round(value))}%)"
        color_key[index] = color
    
    # Adds HSV value for 0
    color_key[0] = "hsv(60,100%,100%)"
    
    # Calculates hue, saturation, and value for each frequency, and adds it to the dictionary
    positive_list = [0.2,0.4,0.6,0.8,1.0]
    for index in positive_list:
        hue = 100 + 80 * index
        saturation = 25 + 75 * index
        value = 100 - 80 * index
        color = f"hsv({str(round(hue))},{str(round(saturation))}%,{str(round(value))}%)"
        color_key[index] = color
    
    return color_key