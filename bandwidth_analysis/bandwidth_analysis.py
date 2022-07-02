# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 15:48:15 2021

@author: Yoshi
"""

import os
import shutil
import math
import statistics
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numpy.polynomial import Polynomial



def bandwidth_analysis(path,key,cell_flags,correlation_coefficients,areas_under_curves,frequencies,frequency_unit,intensities,intensity_unit,threshold):
    
    # Declares start of bandwidth analysis
    print("Starting bandwidth analysis")
    
    # Disable Spyder plot window
    plt.ioff()
    
    # Creates and changes to output directory
    bandwidth_output_path = f"{path}/Output/Bandwidth Analysis"
    if os.path.exists(bandwidth_output_path) == True:
        shutil.rmtree(bandwidth_output_path)
    if os.path.exists(bandwidth_output_path) == False:
        os.mkdir(bandwidth_output_path)
        os.mkdir(f"{bandwidth_output_path}/Tuning Curves")
        os.mkdir(f"{bandwidth_output_path}/Spreadsheets")
    
    # Goes through each intensity
    for intensity in intensities:
        
        # Make a folder for each intensity
        os.mkdir(f"{bandwidth_output_path}/Tuning Curves/{intensity} {intensity_unit}")
        
        # Empty lists to store data in
        cell_numbers = []
        cell_flags_list = []
        full_widths = []
        half_maximums = []
        
        # Goes through each cell
        cell_total = correlation_coefficients.shape[0]
        for cell_number in range(cell_total):
            
            # Checks to make sure cell is responsive to puretone
            responsive = False
            for frequency in frequencies:
                sample_number = key[frequency][intensity]
                if correlation_coefficients[cell_number][sample_number] > threshold:
                    responsive = True
                    break
            if responsive == True:
                
                # Creates points for the tuning curve
                tuning_x_values = []
                tuning_y_values = []
                for frequency in frequencies:
                    octave = math.log2(float(frequency)/float(frequencies[0]))
                    tuning_x_values.append(octave)
                    sample_number = key[frequency][intensity]
                    tuning_y_values.append(areas_under_curves[cell_number][sample_number][0])
                
                # Fit an nth degree polynomial to the tuning curve
                n = 4
                polynomial = Polynomial.fit(tuning_x_values,tuning_y_values,n)
                polynomial_coefficients = polynomial.convert().coef
                polynomial_coefficients = polynomial_coefficients.tolist()
                polynomial_coefficients.reverse()
                derivative_coefficients = polynomial.deriv().convert().coef
                derivative_coefficients = derivative_coefficients.tolist()
                derivative_coefficients.reverse()
                
                # Calculate x and y values for approximation
                approx_x_values = np.linspace(0,max(tuning_x_values),int(max(tuning_x_values)*100+1))
                approx_y_values = []
                polynomial_function = np.poly1d(polynomial_coefficients)
                for x in approx_x_values:
                    approx_y_values.append(polynomial_function(x))
                
                # Calculates half maximum
                half_maximum = 0#statistics.mean([max(approx_y_values),min(approx_y_values)])
                
                # Finds roots of original function minus half maximum
                roots_function = polynomial_function - half_maximum
                roots = roots_function.r.tolist()
                
                # Find real roots
                real_roots = []
                for root in roots:
                    if isinstance(root,float):
                        real_roots.append(root)
                    elif isinstance(root,complex):
                        if root.imag == 0:
                            real_roots.append(root.real)
                
                # Check roots to see if they are within bounds
                good_roots = []
                for root in real_roots:
                    if root > 0 and root < max(tuning_x_values):
                        good_roots.append(root)
                
                # If there are more than two roots or no roots, break loop
                # if len(good_roots) > 2 or len(good_roots) == 0:
                    # break
                
                # If there is only one root, add a fake root at the side depending on which one is more appropriate
                if len(good_roots) == 1:
                    derivative_function = np.poly1d(derivative_coefficients)
                    derivative = derivative_function(good_roots[0])
                    if derivative < 0:
                        good_roots.append(0.0)
                    elif derivative > 0:
                        good_roots.append(max(tuning_x_values))
                    else:
                        break
                
                # Calculate the full width at half maximum
                full_width = 0#abs(good_roots[0]-good_roots[1])
                
                # Adds data to list
                cell_numbers.append(cell_number+1)
                cell_flags_list.append(cell_flags[cell_number][0])
                full_widths.append(full_width)
                half_maximums.append(half_maximum)
                
                # Creates points to graph
                fullwidth_x_values = good_roots.copy()
                fullwidth_y_values = []
                for x in fullwidth_x_values:
                    if x == 0.0 or x == max(tuning_x_values):
                        fullwidth_y_values.append(half_maximum)
                    else:
                        fullwidth_y_values.append(polynomial_function(x))
                
                # Adjust figure size
                plot = plt.figure()
                plot.set_figheight(8)
                plot.set_figwidth(12)
                
                # Plot the tuning curve and polynomial approximation
                plt.plot(tuning_x_values,tuning_y_values,label="Tuning Curve")
                plt.plot(approx_x_values,approx_y_values,label="Approximation")
                plt.plot(fullwidth_x_values,fullwidth_y_values,label="Full Width at Half Maximum")
                
                # Creates titles and legends
                plt.xlabel(f"Octaves above {frequencies[0]} {frequency_unit}")
                plt.ylabel("Area under the curve (Arbitrary units)")
                plt.title(f"Tuning Curve for Cell {cell_number+1}\n\n"+
                          "Half Maximum: %.2f\n"%half_maximum+
                          "Full Width: %.2f Octaves"%full_width)
                plt.legend()
                
                # Saves the figure
                plt.savefig(f"{bandwidth_output_path}/Tuning Curves/{intensity} {intensity_unit}/Cell {cell_number+1}")
                plt.close()
                plt.clf()
        
        # Exports dataframe to excel spreadsheet
        dataframe = {"Cell Number":cell_numbers,"Cell Flag":cell_flags_list,"Full Width":full_widths,"Half Maximum":half_maximums}
        dataframe = pd.DataFrame(dataframe)
        dataframe.to_excel(f"{bandwidth_output_path}/Spreadsheets/{intensity} {intensity_unit}.xlsx",index=False)
    
    # Declares end of bandwidth analysis
    print("Finished bandwidth analysis")
    
    return