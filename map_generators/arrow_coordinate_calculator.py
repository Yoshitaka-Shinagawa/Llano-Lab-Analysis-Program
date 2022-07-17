# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:35:49 2020

@author: Yoshi
"""

import os
import shutil
import numpy as np



from polar_coords_calc import *
from best_angle_calc import *

def arrow_coordinate_calculator(info_storage,map_type,mode):
    
    """
    This is the function used to calculate the coordinates for the arrow that
    depicts the best angle (the axes along which there is a correlation
    between the log of the response of the cells vs their location along the
    axis). It first goes through the specified cells to gather a list of the
    responsive frequencies and their log (base 10) frequencies, then calculates
    the correlation coefficient for the log frequency and the location of the
    cell along an axes, once for each degree (360) of a circle. The angle of
    axis along which the correlation coefficient is the highest is set as the
    best angle, and the coordinates for the arrow is calculated.
    
    Parameters
    ----------
    info_storage : The class used to store most of the variables that are used
        in the analysis program.
    map_type : The integer used to determine whether the best frequency,
        characteristic frequency, or noise will be plotted on the map. 1 is for
        best frequency, 2 is for characteristic frequency, and 3 is for noise.
    mode : The string is used to determine whether one or both types of cells
        will be plotted on the same map, if there are two types of cells
        present. "combined" is for combined maps, "flags" is for special flags
        (GABAergic for us) only, and "no flag" is for normal cells only.
    
    Returns
    -------
    max_corr : The highest correlation coefficient.
    converted_best_angle : The best angle.
    arrow_coordinates : A list containing the coordinates for the corners of
        the arrow.
    """
    
    # Extracts variables from the info_storage class
    path           = info_storage.path
    width          = info_storage.width
    height         = info_storage.height
    scale          = info_storage.scale
    cell_locations = info_storage.cell_locations
    cell_flags     = info_storage.cell_flags
    
    # Creates folders to output graphs to
    if map_type == 1:
        map_type_name = "Best Frequency"
    if map_type == 2:
        map_type_name = "Characteristic Frequency"
    tonotopic_graph_output_path = f"{path}/Output/Debug/Tonotopic Graphs (\
                                    {map_type_name})"
    if os.path.exists(tonotopic_graph_output_path) == True:
        shutil.rmtree(tonotopic_graph_output_path)
    # if os.path.exists(tonotopic_graph_output_path) == False:
    #     os.mkdir(tonotopic_graph_output_path)
    #     os.mkdir(f"{tonotopic_graph_output_path}/Upper Left")
    #     os.mkdir(f"{tonotopic_graph_output_path}/Upper Right")
    #     os.mkdir(f"{tonotopic_graph_output_path}/Lower Left")
    #     os.mkdir(f"{tonotopic_graph_output_path}/Lower Right")
    
    # Lists for storing frequencies, log (base 10) of frequencies, and
    # locations of responive cells
    responsive_frequencies = []
    log_frequencies = []
    responsive_locations = []
    
    # Goes through each cell"s frequency and adds to above lists if responsive
    cell_total = len(cell_locations)
    if mode == "combined":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][map_type] != "N/A":
                responsive_frequency = float(cell_flags[cell_number][map_type])
                responsive_frequencies.append(responsive_frequency)
                if responsive_frequency != 0:
                    log_frequencies.append(np.log10(responsive_frequency))
                else:
                    log_frequencies.append(0)
                responsive_locations.append(cell_locations[cell_number])
    elif mode == "flag":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][map_type] != "N/A" and \
                cell_flags[cell_number][0] != "N/A":
                responsive_frequency = float(cell_flags[cell_number][map_type])
                responsive_frequencies.append(responsive_frequency)
                if responsive_frequency != 0:
                    log_frequencies.append(np.log10(responsive_frequency))
                else:
                    log_frequencies.append(0)
                responsive_locations.append(cell_locations[cell_number])
    elif mode == "no flag":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][map_type] != "N/A" and \
                cell_flags[cell_number][0] == "N/A":
                responsive_frequency = float(cell_flags[cell_number][map_type])
                responsive_frequencies.append(responsive_frequency)
                if responsive_frequency != 0:
                    log_frequencies.append(np.log10(responsive_frequency))
                else:
                    log_frequencies.append(0)
                responsive_locations.append(cell_locations[cell_number])
    
    # Checks to make sure that the list of log frequencies is not empty
    if len(log_frequencies) != 0 and len(log_frequencies) != 1:
        
        # List for storing best angles and correlation coefficients for later
        best_angles = []
        converted_best_angles = []
        max_correlation_coefficients = []
        
        # Upper left corner
        # os.chdir(f"{tonotopic_graph_output_path}/Upper Left")
        polar_coords = polar_coords_calc(responsive_locations,(0,0))
        max_corr,best_angle = best_angle_calc(log_frequencies,polar_coords)
        best_angles.append(best_angle)
        converted_best_angle = -best_angle
        converted_best_angles.append(converted_best_angle)
        max_correlation_coefficients.append(max_corr)
        
        # Upper right corner
        # os.chdir(f"{tonotopic_graph_output_path}/Upper Right")
        polar_coords = polar_coords_calc(responsive_locations,(width,0))
        max_corr,best_angle = best_angle_calc(log_frequencies,polar_coords)
        best_angles.append(best_angle)
        converted_best_angle = -(180-best_angle)
        converted_best_angles.append(converted_best_angle)
        max_correlation_coefficients.append(max_corr)
        
        # Lower left corner
        # os.chdir(f"{tonotopic_graph_output_path}/Lower Left")
        polar_coords = polar_coords_calc(responsive_locations,(0,height))
        max_corr,best_angle = best_angle_calc(log_frequencies,polar_coords)
        best_angles.append(best_angle)
        converted_best_angle = best_angle
        converted_best_angles.append(converted_best_angle)
        max_correlation_coefficients.append(max_corr)
        
        # Lower right corner
        # os.chdir(f"{tonotopic_graph_output_path}/Lower Right")
        polar_coords = polar_coords_calc(responsive_locations,(width,height))
        max_corr,best_angle = best_angle_calc(log_frequencies,polar_coords)
        best_angles.append(best_angle)
        converted_best_angle = 180-best_angle
        converted_best_angles.append(converted_best_angle)
        max_correlation_coefficients.append(max_corr)
        
        # Finds which angle has the highest correlation coefficient
        max_corr = max(max_correlation_coefficients)
        best_angle = best_angles[max_correlation_coefficients.index(max_corr)]
        converted_best_angle = converted_best_angles[
            max_correlation_coefficients.index(max_corr)]
        
        # Calculates the coordinates of the arrow to display
        arrow_coordinates=[]
        arrow_length = np.hypot(width/8*scale,width/8*scale)
        tip_angle = np.arctan((1/16*arrow_length)/(7/8*arrow_length))
        tip_length = 7/8*arrow_length / np.cos(tip_angle)
        
        # Upper left corner
        if max_correlation_coefficients.index(max_corr) == 0:
            arrow_coordinates.append((0,200))
            arrow_coordinates.append((
                round(arrow_length*np.cos(np.deg2rad(best_angle))),
                round(arrow_length*np.sin(np.deg2rad(best_angle))+200)))
            arrow_coordinates.append((
                round(tip_length*np.cos(np.deg2rad(best_angle)+tip_angle)),
                round(tip_length*np.sin(np.deg2rad(
                    best_angle)+tip_angle)+200)))
            arrow_coordinates.append((
                round(arrow_length*np.cos(np.deg2rad(best_angle))),
                round(arrow_length*np.sin(np.deg2rad(best_angle))+200)))
            arrow_coordinates.append((
                round(tip_length*np.cos(np.deg2rad(best_angle)-tip_angle)),
                round(tip_length*np.sin(np.deg2rad(
                    best_angle)-tip_angle)+200)))
        
        # Upper right corner
        elif max_correlation_coefficients.index(max_corr) == 1:
            arrow_coordinates.append((width*scale,200))
            arrow_coordinates.append((
                round(width*scale-arrow_length*np.cos(np.deg2rad(best_angle))),
                round(arrow_length*np.sin(np.deg2rad(best_angle))+200)))
            arrow_coordinates.append((
                round(width*scale-tip_length*np.cos(np.deg2rad(
                    best_angle)+tip_angle)),
                round(tip_length*np.sin(np.deg2rad(
                    best_angle)+tip_angle)+200)))
            arrow_coordinates.append((
                round(width*scale-arrow_length*np.cos(np.deg2rad(
                    best_angle))),
                round(arrow_length*np.sin(np.deg2rad(
                    best_angle))+200)))
            arrow_coordinates.append((
                round(width*scale-tip_length*np.cos(np.deg2rad(
                    best_angle)-tip_angle)),
                round(tip_length*np.sin(np.deg2rad(
                    best_angle)-tip_angle)+200)))
        
        # Lower left corner
        elif max_correlation_coefficients.index(max_corr) == 2:
            arrow_coordinates.append((0,height*scale+200))
            arrow_coordinates.append((
               round(arrow_length*np.cos(np.deg2rad(best_angle))),
               round(height*scale-arrow_length*np.sin(np.deg2rad(
                   best_angle))+200)))
            arrow_coordinates.append((
               round(tip_length*np.cos(np.deg2rad(best_angle)+tip_angle)),
               round(height*scale-tip_length*np.sin(np.deg2rad(
                   best_angle)+tip_angle)+200)))
            arrow_coordinates.append((
               round(arrow_length*np.cos(np.deg2rad(best_angle))),
               round(height*scale-arrow_length*np.sin(np.deg2rad(
                   best_angle))+200)))
            arrow_coordinates.append((
               round(tip_length*np.cos(np.deg2rad(best_angle)-tip_angle)),
               round(height*scale-tip_length*np.sin(np.deg2rad(
                   best_angle)-tip_angle)+200)))
        
        # Lower right corner
        elif max_correlation_coefficients.index(max_corr) == 3:
            arrow_coordinates.append((width*scale,height*scale+200))
            arrow_coordinates.append((
                round(width*scale-arrow_length*np.cos(np.deg2rad(best_angle))),
                round(height*scale-arrow_length*np.sin(np.deg2rad(
                    best_angle))+200)))
            arrow_coordinates.append((
                round(width*scale-tip_length*np.cos(np.deg2rad(
                    best_angle)+tip_angle)),
                round(height*scale-tip_length*np.sin(np.deg2rad(
                    best_angle)+tip_angle)+200)))
            arrow_coordinates.append((
                round(width*scale-arrow_length*np.cos(np.deg2rad(best_angle))),
                round(height*scale-arrow_length*np.sin(np.deg2rad(
                    best_angle))+200)))
            arrow_coordinates.append((
                round(width*scale-tip_length*np.cos(np.deg2rad(
                    best_angle)-tip_angle)),
                round(height*scale-tip_length*np.sin(np.deg2rad(
                    best_angle)-tip_angle)+200)))
        
        # Error
        else:
            print("Error with choosing best angle")
    
    # Otherwise returns N/A as the correlation and best angle
    else:
        max_corr = "N/A"
        converted_best_angle = "N/A"
        arrow_coordinates = []
    
    return max_corr,converted_best_angle,arrow_coordinates