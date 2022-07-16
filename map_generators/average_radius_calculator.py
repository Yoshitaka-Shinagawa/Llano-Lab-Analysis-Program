# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 18:37:32 2019

@author: Yoshi
"""

import numpy as np



def average_radius_calculator(cell_locations):
    
    """
    This is the function used to calculate the average radius of the oval ROIs.
    It creates a list of all of the radii in the x and y axes, then finds the
    average.
    
    Parameters
    ----------
    cell_locations : The list containing the shape, location, and size 
        information of the cells.
    
    Returns : The average radius of the cells.
    """
    
    # Radius is set to "N/A" if it contains no oval ROIs
    radius = "N/A"
    
    # Empty list to store radii information
    radii = []
    
    # Goes through each cell and adds radii to list of radii
    for cell_location in cell_locations:
        if cell_location[0] == "oval":
            radii.append(cell_location[2])
            radii.append(cell_location[3])
    
    # Averages radii to find average radius
    if len(radii) != 0:
        radius = round(np.mean(radii))
    
    return radius