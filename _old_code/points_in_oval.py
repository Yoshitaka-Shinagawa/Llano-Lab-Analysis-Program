# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:53:36 2019

@author: Yoshi
"""

import numpy as np



def cell_and_background_array(cell_locations,image_shape):
    
    # Creates an empty list for storing coordinate lists
    cell_coordinate_array = []
    
    # Goes through each location data
    for location in cell_locations:
        
        # Extracts location data
        center = location[0]
        y_radius = location[1]
        x_radius = location[2]
        
        # Creates empty array
        
        
        
        
        
        # Creates an empty list for storing coordinates
        coordinates = []
        
        # Goes through each point in the rectangle around center
        for y in range(int(center[0]-y_radius),int(center[0]+y_radius+1)):
            for x in range(int(center[1]-x_radius),int(center[1]+x_radius+1)):
                if ((y-center[0])**2)/(y_radius**2) + ((x-center[1])**2)/(x_radius**2) <= 1:
                    coordinates.append((y,x))
        
        # Add list of coordinates to master list
        cell_coordinates.append(coordinates)
    
    return cell_coordinates