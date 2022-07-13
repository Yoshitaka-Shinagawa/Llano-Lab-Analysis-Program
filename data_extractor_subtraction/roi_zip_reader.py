# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 12:06:03 2019

@author: Yoshi
"""

import numpy as np
from read_roi import read_roi_zip



def roi_zip_reader(flag,roi_zip):
    
    """
    This is the function used to import the ROI zip file. It uses the
    read_roi_zip function from the read-roi library to read the ImageJ ROI zip
    file and exports a list containing the shape, location, and size of each of
    the cells, along with a list of flags to differentiate between two types of
    cells, if applicable. The feature was originally designed to differentiate
    between GABAergic and non-GABAergic cells, but can be used to for other
    cell types as well.
    
    Parameters
    ----------
    flag: The name of the flag for the ROI zip, which should be a string. If 
        there is only one type of cell, enter "N/A".
    roi_zip: The location of the ROI zip file, which should be a string.
    
    Returns
    -------
    locations: A list containing the shape, location, and size information of
        the cells.
    flags: A list containing the flag of each cell.
    """
    
    # Reads ROI data from file
    rois = read_roi_zip(roi_zip)
    
    # Empty list to store locations and flags
    locations = []
    flags = []
    
    # Goes through each ROI and adds location information and flags to list
    for roi in rois:
        
        # Rectangular ROIs
        if rois[roi]["type"] == "rectangle":
            top = rois[roi]["top"]
            left = rois[roi]["left"]
            bottom = top + rois[roi]["height"]
            right = left + rois[roi]["width"]
            y_center = round(top+rois[roi]["height"]/2)
            x_center = round(left+rois[roi]["width"]/2)
            locations.append(["rectangle",(y_center,x_center),
                              [top,left,bottom,right]])
            flags.append([flag])
        
        # Oval ROIs
        elif rois[roi]["type"] == "oval":
            y_radius = rois[roi]["height"]/2
            x_radius = rois[roi]["width"]/2
            y_center = rois[roi]["top"] + y_radius
            x_center = rois[roi]["left"] + x_radius
            locations.append(["oval",(y_center,x_center),y_radius,x_radius])
            flags.append([flag])
        
        # Polygonal ROIs
        elif rois[roi]["type"] == "polygon":
            y_list = rois[roi]["y"]
            x_list = rois[roi]["x"]
            y_center = round(np.mean([max(y_list),min(y_list)]))
            x_center = round(np.mean([max(x_list),min(x_list)]))
            locations.append(["polygon",(y_center,x_center),y_list,x_list])
            flags.append([flag])
        
        # Anything else
        else:
            print("ROI %s does not have a recognized shape" % roi)
    
    return locations,flags