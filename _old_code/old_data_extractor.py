# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 19:33:28 2019

@author: Yoshi
"""

import os
import cv2
import numpy as np
from xml.dom import minidom



from roi_zip_reader import *
from points_in_oval import *
from xyz_gaussian_filter import *
from image_rounder import *
from motion_stabilizer import *
from data_reader import *
from dfof_converter import *

def data_extractor(path):
    
    # Creates debug folder for storing averaged images
    output_path = path + '/Output'
    if os.path.exists(output_path) == False:
        os.mkdir(output_path)
    if os.path.exists(output_path+'/Debug') == False:
        os.mkdir(output_path+'/Debug')
    if os.path.exists(output_path+'/Debug/Average Images') == False:
        os.mkdir(output_path+'/Debug/Average Images')
    
    # Location of the data path
    data_path = path + '/Data'
    
    # Creates a list of folders in the data directory
    os.chdir(data_path)
    folders_list = [folder for folder in os.listdir(data_path) if os.path.isdir(folder)]
    if len(folders_list) == 0:
        print('Error! Folders could not be found!')
        return
    
    # Checks if the key is there so it stops the program early if it doesn't exist
    if os.path.exists('key.csv') == False:
        print('Error! Key file could not be found!')
        return
    
    # Import ROIs with two different ways of reading depending on whether tehre are 
    roi_zip_list = [file for file in os.listdir(data_path) if file.endswith('.zip')]
    extra_flag = 'N/A'
    if len(roi_zip_list) == 2:
        for roi_zip in roi_zip_list:
            if 'non' not in roi_zip:
                extra_flag = roi_zip[7:-4]
                locations_1,flags_1 = roi_zip_reader(extra_flag,roi_zip)
            else:
                locations_2,flags_2 = roi_zip_reader('N/A',roi_zip)
        cell_locations = locations_1 + locations_2
        cell_flags = flags_1 + flags_2
    elif len(roi_zip_list) == 1:
        cell_locations,cell_flags = roi_zip_reader('N/A',roi_zip_list[0])
    elif len(roi_zip_list) != 0:
        print('Error! Too many ROI zip files found!')
    else:
        print('Error! No ROI zip file found!')
        return
    
    # Finds the coordinates for each ROI
    cell_coordinates = points_in_oval(cell_locations)
    
    # Empty list to store data later
    data = []
    dfof_data = []
    
    # Declares start of data extraction
    print('Starting data extraction')
    
    # Goes through each data folder
    for folder in folders_list:
        
        # Changes directory to folder
        folder_path = data_path + '/' + folder
        os.chdir(folder_path)
        
        # Generates a list of data images
        files_list = [file for file in os.listdir(folder_path) if file.endswith('.tif') and 'Ch1' in file]
        if len(files_list) == 0:
            print('Error! Empty folder detected!')
            return
        
        # Goes through each data image and reads the data
        folder_images = []
        for file in files_list:
            folder_images.append(cv2.imread(file,2))
        folder_images = np.array(folder_images,dtype=np.float32)
        
        # Creates base image to match all stabilizations against
        if folder == folders_list[0]:
            filtered_images = xyz_gaussian_filter(folder_images,1,1,1)
            base_image = np.average(filtered_images,axis=0)
            base_image = image_rounder(base_image)
        
        # Finds the shifts of the images
        max_zoom = 3
        filtered_images,image_shifts = motion_stabilizer(folder,output_path,base_image,folder_images,max_zoom)
        
        # Reads the data from the images
        folder_data = data_reader(filtered_images,image_shifts,cell_coordinates,max_zoom)
        data.append(folder_data)
        
        # Reads XML file find framerate
        if folder == folders_list[0]:
            xml_file = [file for file in os.listdir(folder_path) if file.endswith('.xml')]
            metadata = minidom.parse(xml_file[0])
            frame_period = float(metadata.getElementsByTagName('PVStateValue')[5].attributes['value'].value)
            framerate = 1 / frame_period
            framerate = int(framerate)
        
        # Converts the data to df/f values
        folder_dfof_data = dfof_converter(folder_data,framerate)
        dfof_data.append(folder_dfof_data)
        
        # Prints folder number for tracking
        print(f'Folder {folder}')
    
    # Converts data to array for easier parsing
    data = np.array(data,dtype=np.float32)
    dfof_data = np.array(dfof_data,dtype=np.float32)
    
    # Declares end of data extraction
    print('Finished data extraction')
    
    return extra_flag,cell_locations,cell_flags,data,dfof_data,base_image,framerate