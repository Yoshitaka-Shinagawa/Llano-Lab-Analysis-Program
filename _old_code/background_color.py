# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:17:35 2019

@author: Yoshi
"""

def background_color(sample_dfof,max_dfof,threshold_dfof):
    
    # Default color
    color = "#FFFFFF"
    
    # Calculates gradient of red and blue and adds it to pure green
    if sample_dfof > threshold_dfof:
        
        # Red and blue calculation
        red_blue = int(255*(1-(sample_dfof-threshold_dfof)/max_dfof))
        
        # Converts the green value to hex
        if len(hex(red_blue)) == 4:
            red_blue_hex = hex(red_blue)[-2:].upper()
        if len(hex(red_blue)) == 3:
            red_blue_hex = '0' + hex(red_blue)[-1:].upper()
        
        # Concatenates values for hex color
        color = "#" + red_blue_hex + "FF" + red_blue_hex
    
    return color