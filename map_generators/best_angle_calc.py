# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:42:29 2020

@author: Yoshi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr



def best_angle_calc(log_frequencies,polar_coords):
    
    """
    This is the function used to calculate the best angle for each corner. It
    first tilts the axis at each angle from 0 to 90 to calculate the parallel
    distance from the origin of the axis, then calculates the correlation
    coefficient between the distance and the log of the frequencies for the
    cells. The axis with the highest correlation coefficient is chosen as the
    best angle for the corner.
    
    Parameters
    ----------
    log_frequencies : The list containing the log (base 10) of the frequencies
        of the responsive cells.
    polar_coords : The list containing the polar coordinates for each cell.
        Each polar coordinate contains a tuple of two positive floats, (theta,
        hypotenuse), where theta is the arctangent angle from the corner and
        hypotenuse is the distance from the corner.
    
    Returns
    -------
    max_corr : The highest correlation coefficient of the best angles.
    best_angle : The best angle.
    """
    
    # Disable Spyder plot window
    plt.ioff()
    
    # Empty list for storing correlation coefficients in
    correlation_coefficients = []
    
    # Goes through each angle from 0 to 90 degrees
    for phi in range(0,91):
        
        # Calculates the distance along the tilted axis from the corner
        distances = []
        for polar_coord in polar_coords:
            distance = polar_coord[1] * np.cos(np.deg2rad(polar_coord[0]-phi))
            distances.append(distance)
            
        # Calculates the correlation coefficient and adds it to list
        corr,_ = pearsonr(log_frequencies,distances)
        correlation_coefficients.append(corr)
        
        # # Creates a graph of the distances and log frequencies
        # plt.scatter(distances,log_frequencies)
        # plt.xlabel("Distance")
        # plt.ylabel("Log frequency")
        # plt.legend(["r = %.2f"%corr],loc="upper right")
        
        # # Saves the figure
        # plt.savefig(f"Angle {phi}")
        # plt.close()
        # plt.clf()
    
    # Calculates the best angle based on the highest correlation coefficient
    max_corr = max(correlation_coefficients)
    best_angle = correlation_coefficients.index(max_corr)
    
    return max_corr,best_angle