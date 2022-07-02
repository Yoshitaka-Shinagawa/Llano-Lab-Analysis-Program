# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:21:44 2020

@author: Yoshi
"""

import numpy as np



def polar_coordinates_calculator(responsive_locations,corner):
    
    # Converts cartesian coordinates to polar coordinates
    polar_coordinates = []
    for cell_location in responsive_locations:
        x_corner = corner[0]
        y_corner = corner[1]
        x_center = abs(cell_location[1][1]-x_corner)
        y_center = abs(cell_location[1][0]-y_corner)
        # print("Center: ",x_center,y_center)
        theta = np.arctan(y_center/x_center)
        theta = np.rad2deg(theta)
        hypotenuse = np.hypot(x_center,y_center)
        # print("Polar Coordinates: ",theta,hypotenuse)
        polar_coordinates.append([theta,hypotenuse])
        
    return polar_coordinates