# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 19:33:28 2019

@author: Yoshi
"""

import os
import numpy as np
import tifffile as tiff
import csv



from roi_zip_reader import *
from cell_and_background_array import *
from data_reader import *
from dfof_converter import *

def data_extractor_noise(path):
    
    # Location of the data path
    data_path = f'{path}/Data'
    os.chdir(data_path)
    
    # If combined ROI set for FISSA exists, deletes it
    if os.path.exists('RoiSet_FISSA.zip'):
        os.remove('RoiSet_FISSA.zip')
    
    # Import ROIs with two different ways of reading depending on whether there are one or two sets of ROIs
    roi_zip_list = [file for file in os.listdir(data_path) if file.endswith('.zip')]
    extra_flag = 'N/A'
    if len(roi_zip_list) == 2:
        for roi_zip in roi_zip_list:
            if 'non' not in roi_zip:
                extra_flag = roi_zip[7:-4]
                locations_1,flags_1 = roi_zip_reader(extra_flag,roi_zip)
            elif 'non' in roi_zip:
                locations_2,flags_2 = roi_zip_reader('N/A',roi_zip)
            else:
                print('Error! ROIs are not named properly!')
                return
        cell_locations = locations_1 + locations_2
        cell_flags = flags_1 + flags_2
    elif len(roi_zip_list) == 1:
        cell_locations,cell_flags = roi_zip_reader('N/A',roi_zip_list[0])
    elif len(roi_zip_list) != 0:
        print('Error! Too many ROI zip files found!')
        return
    else:
        print('Error! No ROI zip file found!')
        return
    
    # Declares start of data extraction
    print('Starting data extraction')
    
    # Empty list to store data
    raw_data = []
    
    # Makes a list of tiff image stacks to read data from
    images_path = f'{path}/Stabilized Images'
    os.chdir(images_path)
    image_list = [file for file in os.listdir(images_path) if file.endswith('.tiff')]
    
    # Read framerate info
    if os.path.exists(f'{data_path}/Key/framerates.csv') == True:
        open_framerate_file = open(f'{data_path}/Key/framerates.csv')
        framerate_file = csv.reader(open_framerate_file)
        framerate_information = []
        for row in framerate_file:
            for info in row:
                framerate_information.append(float(info))
        framerate_information[0] = int(framerate_information[0])
        framerate_information[1] = int(framerate_information[1])
    else:
        print('Error! Framerate data not found!')
        return
    
    # Goes through each tiff stack in the folder
    for image in image_list:
        
        # Read tiff stack using scikit-image
        image_stack = tiff.imread(image)
        
        # Converts ROIs to coordinates if image is first one
        if image == image_list[0]:
            image_shape = image_stack.shape[1:3]
            cell_arrays,background_arrays = cell_and_background_array(cell_locations,image_shape)
        
        # Reads the data from images
        folder_data = data_reader(image_stack,cell_arrays,background_arrays)
        raw_data.append(folder_data)
    
    # Sorts out the data and converts to dF/F values
    raw_data = np.array(raw_data)
    data = dfof_converter(path,raw_data,framerate_information)
    
    # Other information to make the other functions run
    frequencies = ['Noise']
    decibels = ['Noise']
    key = {'Noise':{'Noise':1}}
    
    # Declares end of data extraction
    print('Finished data extraction')
    
    return extra_flag,cell_locations,cell_flags,data,framerate_information,key,frequencies,decibels

