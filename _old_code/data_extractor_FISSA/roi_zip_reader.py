# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 12:06:03 2019

@author: Yoshi
"""

from read_roi import read_roi_zip



def roi_zip_reader(flag,roi_zip):
    
    # Reads ROI data from file
    rois = read_roi_zip(roi_zip)
    
    # Empty list to store locations and flags
    locations = []
    flags = []
    
    # Goes through each ROI andadds location and flags to list
    for roi in rois:
        if rois[roi]['type'] == 'oval':
            y_radius = rois[roi]['height']/2
            x_radius = rois[roi]['width']/2
            y_center = rois[roi]['top'] + y_radius
            x_center = rois[roi]['left'] + x_radius
            locations.append([(y_center,x_center),y_radius,x_radius])
            flags.append([flag])
        else:
            print('Error! ROI %s is not oval!' % roi)
    
    return locations,flags