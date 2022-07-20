# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:21:44 2020

@author: Yoshi
"""

import numpy as np



def polar_coords_calc(responsive_locations,corner):
    
    """
    This is the function used to calculate the polar coordinates for each cell
    from each corner. This makes it much easier to calculate the distance along
    each axis for calculating the best angle.
    
    Parameters
    ----------
    responsive_locations : The list containing the locations of the cells that
        were considered responsive.
    corner : The coordinates of the corner from which the polar coordinates are
        being calculated from. It is a tuple of two positive integers, (y,x),
        where y is the y coordinate of the corner from which the polar
        coordinates are being calculated and x is the x coordinate of the
        corner.
    
    Returns
    -------
    polar_coords : A list containing the polar coordinates for each cell. Each
        polar coordinate contains a tuple of two positive floats, (theta,
        hypotenuse), where theta is the arctangent angle from the corner and
        hypotenuse is the distance from the corner.
    """
    
    # Converts cartesian coordinates to polar coordinates
    polar_coords = []
    for cell_location in responsive_locations:
        x_corner = corner[0]
        y_corner = corner[1]
        x_center = abs(cell_location[1][1]-x_corner)
        y_center = abs(cell_location[1][0]-y_corner)
        theta = np.arctan(y_center/x_center)
        theta = np.rad2deg(theta)
        hypotenuse = np.hypot(x_center,y_center)
        polar_coords.append((theta,hypotenuse))
        
    return polar_coords