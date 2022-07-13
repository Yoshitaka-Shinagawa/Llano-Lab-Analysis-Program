# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:53:36 2019

@author: Yoshi
"""

import numpy as np
from shapely.geometry import Point,Polygon



def cell_and_background_array(cell_locations,image_shape):
    
    """
    This is the function used to create the masks from the location and size
    of the cells, which are used to extract the 2P signals from the images. 
    
    
    
    
    
    
    This is the function used to extact 2P signals from each cell. It imports
    the ROIs created in ImageJ for the data set using the roi_zip_reader
    function from the read-roi library. This is used to create two masks, one
    that is a replica of the ROIs, and a second mask surrounding the original
    ROIs, roughly four times larger in area. The first mask is applied to the
    data to find the average pixel value within the ROI, while the second mask
    is applied to find the average pixel value of the neuropil (the background
    region surrounding the neuron). Neuropil correction is applied using the
    substraction method, with 0.4 being used as the contamination ratio. The
    corrected value is then converted to dF/F values and reorganized so that
    all segments with the same stimulus frequency and stimulus amplitude are
    grouped together.
    
    Parameters
    ----------
    filtered_images: This is a numpy array containing the filtered images from
        the 2P microscope. This will be passed onto a different function that
        will use this array to extract 2P signals for each cell.
    info_storage: This is the class used to store most of the variables that
        are used in the analysis program.
    
    Returns
    -------
    data: This is a 4D numpy array containing the dF/F values. The first axis
        is the cell number, the second axis is the sample number (unique 
        combination of frequency and amplitude), the third number is the trial
        number (repition of the same frequency and amplitude combination), and
        the fourth axis is the frame number for each segment.
    info_storage: The function returns the info_storage class with the
        cell_locations, extra_flag, cell_flags, framerate_information, key,
        frequencies, frequency_unit, intensities, intensity_unit variables
        added.
    """
    
    # Creates an empty list for storing arrays
    cell_arrays = []
    background_arrays = []
    
    # Creates empty array for tracking all cells
    all_cells = np.zeros(image_shape,dtype=int)
    
    # Goes through each location data for the cell array
    for location in cell_locations:
        
        # Creates empty array
        cell_array = np.zeros(image_shape,dtype=int)
        
        # Rectangular ROIs
        if location[0] == "rectangle":
            
            # Extracts location data
            top = location[2][0]
            left = location[2][1]
            bottom = location[2][2]
            right = location[2][3]
            
            # Creates a list of coordinate points in the rectangle
            coords_list = [(y,x) for y in range(top,bottom+1) for x in range(left,right+1)]
        
        # Oval ROIs
        if location[0] == "oval":
            
            # Extracts location data
            center = location[1]
            y_radius = location[2]
            x_radius = location[3]
            
            # Creates a list of coordinate points in the oval
            coords_list = [(y,x)
                           for y in range(int(center[0]-y_radius),int(center[0]+y_radius+1))
                           for x in range(int(center[1]-x_radius),int(center[1]+x_radius+1))
                           if ((y-center[0])**2)/(y_radius**2) + ((x-center[1])**2)/(x_radius**2) <= 1]
        
        # Polygonal ROIs
        if location[0] == "polygon":
            
            # Extracts location data
            y_list = location[2]
            x_list = location[3]
            y_min = round(min(y_list)+1)
            y_max = round(max(y_list)+1)
            x_min = round(min(x_list)+1)
            x_max = round(max(x_list)+1)
            
            # Creates polygon using shapely library
            polygon_vertices = []
            n_total = len(x_list)
            for n in range(n_total):
                polygon_vertices.append((x_list[n],y_list[n]))
            polygon = Polygon(polygon_vertices)
            
            # Creates a list of coordinate points in the polygon
            coords_list = [(y,x) for y in range(y_min,y_max+1) for x in range(x_min,x_max+1)
                           if polygon.contains(Point(x,y))]
        
        # Attempts to change location in cell array to 1
        for coord in coords_list:
            try:
                cell_array[coord] = 1
            except IndexError:
                pass
        
        # Add array to list of arrays and master array
        cell_arrays.append(cell_array)
        all_cells += cell_array
    
    # Goes through each location data for the background array
    for location in cell_locations:
        
        # Creates empty array
        background_array = np.zeros(image_shape,dtype=int)
        
        # Rectangular ROIs
        if location[0] == "rectangle":
            
            # Extracts location data
            center = location[1]
            top = location[2][0]
            left = location[2][1]
            bottom = location[2][2]
            right = location[2][3]
            half_height = (top-bottom) * 1.125
            half_width = (left-right) * 1.125
            
            # Creates a list of coordinate points in the rectangle
            coords_list = [(y,x) 
                           for y in range(round(center[0]-half_height),round(center[0]+half_height+1))
                           for x in range(round(center[1]-half_width),round(center[1]+half_width+1))]
        
        # Oval ROIs
        if location[0] == "oval":
            
            # Extracts location data
            center = location[1]
            y_radius = location[2] * 2.25
            x_radius = location[3] * 2.25
            
            # Creates a list of coordinate points in the oval
            coords_list = [(y,x)
                           for y in range(int(center[0]-y_radius),int(center[0]+y_radius+1))
                           for x in range(int(center[1]-x_radius),int(center[1]+x_radius+1))
                           if ((y-center[0])**2)/(y_radius**2) + ((x-center[1])**2)/(x_radius**2) <= 1]
        
        # Polygonal ROIs
        if location[0] == "polygon":
            
            # Extracts location data
            center = location[1]
            y_list = location[2]
            x_list = location[3]
            y_min = round(center[0]-(center[0]-min(y_list))*2.25+1)
            y_max = round(center[0]-(center[0]-max(y_list))*2.25+1)
            x_min = round(center[1]-(center[1]-min(y_list))*2.25+1)
            x_max = round(center[1]-(center[1]-max(y_list))*2.25+1)
            
            # Creates polygon using shapely library
            polygon_vertices = []
            n_total = len(x_list)
            for n in range(n_total):
                polygon_vertices.append((center[1]-(center[1]-x_list[n])*2.25,
                                         center[0]-(center[0]-y_list[n])*2.25))
            polygon = Polygon(polygon_vertices)
            
            # Creates a list of coordinate points in the polygon
            coords_list = [(y,x) for y in range(y_min,y_max+1) for x in range(x_min,x_max+1)
                           if polygon.contains(Point(x,y))]
        
        # Attempts to change location in cell array to 1
        for coord in coords_list:
            try:
                background_array[coord] = 1
            except IndexError:
                pass
        
        # Subtracts master cell array to avoid duplicate data
        background_array -= all_cells
        
        # Corrects all instances of -1 to 0
        for row in range(image_shape[0]):
            for column in range(image_shape[1]):
                if background_array[(row,column)] == -1:
                    background_array[(row,column)] = 0
        
        # Adds array to list of arrays
        background_arrays.append(background_array)
    
    return cell_arrays,background_arrays