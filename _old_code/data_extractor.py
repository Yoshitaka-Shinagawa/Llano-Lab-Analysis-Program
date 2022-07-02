# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 19:33:28 2019

@author: Yoshi
"""

import os
import numpy as np
import csv
from skimage import io



from roi_zip_reader import *
from cell_and_background_array import *
from data_reader import *
from dfof_converter import *

def data_extractor(path):
    
    # Location of the data path
    data_path = f'{path}/Data'
    os.chdir(data_path)
    
    # Import ROIs with two different ways of reading depending on whether there are one or two sets of ROIs
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
    
    # Empty list to store data later
    data = []
    dfof_data = []
    
    # Declares start of data extraction
    print('Starting data extraction')
    
    # Makes a list of tiff image stacks to read data from
    images_path = f'{path}/Stabilized Images'
    os.chdir(images_path)
    image_list = [file for file in os.listdir(images_path) if file.endswith('.tiff')]
    
    # Checks if the key is there so it stops the program early if it doesn't exist
    if os.path.exists(f'{data_path}/key.csv') == False and len(image_list) != 10:
        print('Error! Key file could not be found!')
        return
    
    # Read framerate data
    if os.path.exists(f'{data_path}/framerates.csv') == True:
        open_framerate_file = open(f'{data_path}/framerates.csv')
        framerate_file = csv.reader(open_framerate_file)
        for row in framerate_file:
            framerate = row
        framerate_information = [int(framerate[0]),1000,0]
    elif os.path.exists(f'{data_path}/framerate.csv') == False and len(image_list) != 10:
        print('Error! Framerate data not found!')
        return
    # else:
        # framerate = 
    
    # Goes through each tiff stack in the folder
    for image in image_list[0:3]:
        
        # Read tiff stack using scikit-image
        image_stack = io.imread(image)
        
        # Converts ROIs to coordinates if image is first one
        if image == image_list[0]:
            image_shape = image_stack.shape[1:3]
            cell_arrays,background_arrays = cell_and_background_array(cell_locations,image_shape)
        
        # Reads the data from images
        folder_data = data_reader(image_stack,cell_arrays)
        data.append(folder_data)
        
        # Calculates the dF/F values from images
        folder_dfof_data = dfof_converter(image_stack,cell_arrays,background_arrays,framerate_information[0])
        dfof_data.append(folder_dfof_data)
        
        
        
        
        
    '''
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
        folder_images = [cv2.imread(file,2) for file in files_list]
        folder_images = np.array(folder_images,dtype=np.float32)
        
        # Creates base image for tonotopic map
        if folder == folders_list[0]:
            filtered_images = xyz_gaussian_filter(folder_images,1,1,1)
            base_image = np.average(filtered_images,axis=0)
            base_image = np.around(base_image)
            base_image = base_image.astype(np.uint16)
        
        # Stabilizes motion of images
        filtered_stabilized_images = motion_stabilizer(folder,output_path,base_image,folder_images)
        
        # Reads the data from the images
        folder_data = data_reader(filtered_stabilized_images,cell_coordinates)
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
    '''
    
    
    # Converts data to array for easier parsing
    data = np.array(data,dtype=np.float32)
    dfof_data = np.array(dfof_data,dtype=np.float32)
    
    # Declares end of data extraction
    print('Finished data extraction')
    
    return data,dfof_data#extra_flag,cell_locations,cell_flags,data,dfof_data,base_image,framerate

data,dfof_data = data_extractor('D:/Llano Lab/Tonotopic Analysis/Old Data Set/2019-07-18/2019-07-18 Anesthetized IC Area 1')