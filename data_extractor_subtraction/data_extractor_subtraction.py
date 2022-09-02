# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 19:33:28 2019

@author: Yoshi
"""

import os
import numpy as np
import tifffile as tiff
import csv
import pandas



from roi_zip_reader import *
from key_reader import *
from cell_and_background_array import *
from data_sorter import *
from data_reader import *
from dfof_converter import *

def data_extractor_subtraction(filtered_images,info_storage):
    
    """
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
    filtered_images : The numpy array containing the filtered images from the
        2P microscope.
    info_storage : The class used to store most of the variables that are used
        in the analysis program.
    
    Returns
    -------
    data : A 4D numpy array containing the dF/F values. The first axis is the
        cell number, the second axis is the sample number (unique combination
        of frequency and amplitude), the third number is the trial number
        (repetition of the same frequency and amplitude combination), and the
        fourth axis is the frame number for each segment.
    info_storage : The function returns the info_storage class with the
        cell_locations, extra_flag, cell_flags, framerate_information, key,
        frequencies, frequency_unit, intensities, intensity_unit variables
        added.
    """
    
    # Extracts variables from the info_storage class
    path         = info_storage.path
    folders_list = info_storage.folders_list
    mode         = info_storage.mode
    
    # Declares start of data extraction
    print("Starting data extraction")
    
    # Location of the data path
    data_path = f"{path}/Data"
    
    # If combined ROI set for FISSA exists, deletes it
    if os.path.exists(f"{data_path}/RoiSet_FISSA.zip"):
        os.remove(f"{data_path}/RoiSet_FISSA.zip")
    
    # Import ROIs with two different ways of reading depending on whether there
    # are one or two sets of ROIs
    roi_zip_list = [f"{data_path}/{file}" for file in os.listdir(data_path)
                    if file.endswith(".zip")]
    extra_flag = "N/A"
    if len(roi_zip_list) == 2:
        for roi_zip in roi_zip_list:
            if "non" not in roi_zip:
                extra_flag = roi_zip[len(data_path)+8:-4]
                locations_1,flags_1 = roi_zip_reader(extra_flag,roi_zip)
            elif "non" in roi_zip:
                locations_2,flags_2 = roi_zip_reader("N/A",roi_zip)
            else:
                print("Error! ROIs are not named properly!")
                return
        cell_locations = locations_1 + locations_2
        cell_flags = flags_1 + flags_2
    elif len(roi_zip_list) == 1:
        cell_locations,cell_flags = roi_zip_reader("N/A",roi_zip_list[0])
    elif len(roi_zip_list) != 0:
        print("Error! Too many ROI zip files found!")
        return
    else:
        print("Error! No ROI zip file found!")
        return
    
    # Reading data from new data set
    if 1:#len(image_list) == 10 or len(image_list) == 9:
        
        # Read framerate info from the csv file
        if os.path.exists(f"{data_path}/Key/framerates.csv") == True:
            open_framerate_file = open(f"{data_path}/Key/framerates.csv")
            framerate_file = csv.reader(open_framerate_file)
            framerate_information = []
            for row in framerate_file:
                for info in row:
                    framerate_information.append(float(info))
            framerate_information[0] = int(framerate_information[0])
            framerate_information[1] = int(framerate_information[1])
            framerate_information = tuple(framerate_information)
        else:
            print("Error! Framerate data not found!")
            return
        
        # Converts ROIs to coordinates
        image_shape = filtered_images.shape[2:4]
        cell_arrays,background_arrays = cell_and_background_array(
            cell_locations,image_shape)
        
        # Empty array to store raw data in
        raw_data = np.zeros((filtered_images.shape[0],len(cell_arrays),
                             filtered_images.shape[1]),dtype=np.float64)
        
        # Goes through each folder image in the filtered data array
        for folder_number in range(len(filtered_images)):
            
            # Reads the data from images and appends to list
            folder_data = data_reader(filtered_images[folder_number],
                                      cell_arrays,background_arrays,info_storage)
            raw_data[folder_number] = folder_data
        
        # Converts raw data to numpy array
        raw_data = np.array(raw_data)
        
        # New tonotopy analysis
        if mode == 0:
            
            # Sorts data for new tonotopy analysis
            data = data_sorter(path,raw_data,folders_list,
                               framerate_information)
            
            # Reads key from file
            if os.path.exists(f"{data_path}/Key/key.csv"):
                key,frequencies,frequency_unit,intensities,intensity_unit = \
                key_reader(f"{data_path}/Key/key.csv")
            else:
                print("Error! Key not found!")
                return
            
            # Frequencies list override for PCB data
            # frequencies = ["5","7.1","10","14.1","20","28.3","40"]
        
        # Noise analysis
        if mode == 1:
            
            # Converts to dF/F values for noise analysis
            data = dfof_converter(path,raw_data,framerate_information)
            
            # Other information to make the other functions run
            frequencies = ["Noise"]
            frequency_unit = "kHz"
            intensities = ["Noise"]
            intensity_unit = "dB"
            key = {"Noise":{"Noise":0}}
    
    # Reading data from single photon data set
    elif len(image_list) == 1:
        
        # Go through each tiff stack in folder
        for image in image_list:
            
            # Read tiff stack using scikit-image
            image_stack = tiff.imread(image)
            
            # Converts ROIs to coordinates if image is first one
            if image == image_list[0]:
                image_shape = image_stack.shape[1:3]
                cell_arrays,background_arrays = \
                    cell_and_background_array(cell_locations,image_shape)
            
            # Reads the data from images
            folder_data = data_reader(image_stack,cell_arrays,
                                      background_arrays,info_storage)
            raw_data = folder_data
        
        # Exports data to Excel spreadsheet
        data = np.swapaxes(raw_data,0,1)
        print(data.shape)
        dataframe = pandas.DataFrame(data)
        dataframe.to_excel(f"{path}/Data.xlsx",header=False,index=False)
        
        # Prematurely ends the code because no further analysis is needed
        print("Finished data extraction")
        return
    
    # Reading data from old data set
    else:
        
        # Read framerate info
        if os.path.exists(f"{data_path}/framerates.csv") == True:
            open_framerate_file = open(f"{data_path}/framerates.csv")
            framerate_file = csv.reader(open_framerate_file)
            framerate_information = []
            for row in framerate_file:
                for info in row:
                    framerate_information.append(float(info))
            framerate_information[0] = int(framerate_information[0])
        else:
            print("Error! Framerate data not found!")
            return
        
        # Goes through each tiff stack in the folder
        for image in image_list:
            
            # Read tiff stack using scikit-image
            image_stack = tiff.imread(image)
            
            # Converts ROIs to coordinates if image is first one
            if image == image_list[0]:
                image_shape = image_stack.shape[1:3]
                cell_arrays,background_arrays = \
                    cell_and_background_array(cell_locations,image_shape)
            
            # Reads the data from images
            folder_data = data_reader(image_stack,cell_arrays,
                                      background_arrays,info_storage)
            raw_data.append(folder_data)
        
        # Converts raw data to dF/F values
        raw_data = np.array(raw_data)
        data = dfof_converter(raw_data,framerate_information)
        
        # Reads key from file
        if os.path.exists(f"{data_path}/key.csv"):
            key,frequencies,decibels = key_reader(f"{data_path}/key.csv")
        else:
            print("Error! Key not found!")
            return
    
    # Deletes filtered_images to save space in memory
    del filtered_images
    
    # Adds new information to the info_storage class
    info_storage.cell_locations        = cell_locations
    info_storage.extra_flag            = extra_flag
    info_storage.cell_flags            = cell_flags
    info_storage.framerate_information = framerate_information
    info_storage.key                   = key
    info_storage.frequencies           = frequencies
    info_storage.frequency_unit        = frequency_unit
    info_storage.intensities           = intensities
    info_storage.intensity_unit        = intensity_unit
    
    # Declares end of data extraction
    print("Finished data extraction")
    
    return data,info_storage
