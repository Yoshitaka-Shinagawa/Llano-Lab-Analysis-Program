# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:42:29 2020

@author: Yoshi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr



def best_angle_calculator(log_frequencies,polar_coordinates):
    
    # Disable Spyder plot window
    plt.ioff()
    
    # Empty list for storing correlation coefficients in
    correlation_coefficients = []
    
    # Goes through each angle from 0 to 90 degrees
    for phi in range(0,91):
        
        # Calculates the distance along the tilted axis from the corner
        distances = []
        for polar_coordinate in polar_coordinates:
            distance = polar_coordinate[1] * np.cos(np.deg2rad(polar_coordinate[0]-phi))
            distances.append(distance)
            
        # Calculates the correlation coefficient and adds it to list
        corr,_ = pearsonr(log_frequencies,distances)
        correlation_coefficients.append(corr)
        
        """
        # Creates a graph of the distances and log frequencies
        plt.scatter(distances,log_frequencies)
        plt.xlabel("Distance")
        plt.ylabel("Log frequency")
        plt.legend(["r = %.2f"%corr],loc="upper right")
        
        # Saves the figure
        plt.savefig(f"Angle {phi}")
        plt.close()
        plt.clf()
        """
    
    # Calculates the best angle based on the highest correlation coefficient
    max_corr = max(correlation_coefficients)
    best_angle = correlation_coefficients.index(max_corr)
    
    return max_corr,best_angle