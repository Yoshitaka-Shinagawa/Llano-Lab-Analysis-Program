# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 13:17:30 2021

@author: Yoshi
"""

import warnings
warnings.simplefilter(action="ignore",category=FutureWarning)

import os
import shutil
import cv2
import numpy as np
import matplotlib.image as mpimg
import imageio
import caiman
from caiman.motion_correction import MotionCorrect



from xyz_gaussian_filter import *

def motion_corrector(info_storage):
    
    """
    This is the function used for motion correction and filtering. It uses the
    NoCorreRM algorithm embedded within the CaImAn library to stabilize the
    images, then uses a 3D Gaussian filter to apply a low-pass filter.
    
    Parameters
    ----------
    info_storage : The class used to store most of the variables that are used
        in the analysis program.
    
    Returns
    -------
    raw_images : A 3D numpy array containing the raw images from the 2P
        microscope. This will be empty in most cases, except when noise data is
        being analyzed.
    filtered_images : A 3D numpy array containing the filtered images from the
        2P microscope. The first axis is the temporal axis, while the second
        and third axes are the y ans x axes of the individual images,
        respectively. This will be passed onto a different function that will
        use this array to extract 2P signals for each cell.
    info_storage : The function returns the info_storage class with the
        folders_list variable added.
    """
    
    # Extracts variables from the info_storage class
    path         = info_storage.path
    gauss_filter = info_storage.gauss_filter
    mode         = info_storage.mode
    
    # Removes old Stabilized Images folder if it exists to save space
    old_folder_path = f"{path}/Stabilized Images"
    if os.path.exists(old_folder_path) == True:
        shutil.rmtree(old_folder_path)
    
    # Creates temporary output folder for stabilized images
    images_output_path = f"{path}/CaImAn Files"
    if os.path.exists(images_output_path) == True:
        try:
            shutil.rmtree(images_output_path)
        except PermissionError:
            pass
    if os.path.exists(images_output_path) == False:
        os.mkdir(images_output_path)
    
    # Creates debug folder for storing averaged images
    output_path = f"{path}/Output"
    if os.path.exists(output_path) == False:
        os.mkdir(output_path)
    debug_output_path = f"{output_path}/Debug"
    if os.path.exists(debug_output_path) == False:
        os.mkdir(debug_output_path)
    if os.path.exists(f"{debug_output_path}/Base Image") == True:
        shutil.rmtree(f"{debug_output_path}/Base Image")
    if os.path.exists(f"{debug_output_path}/Average Images") == True:
        shutil.rmtree(f"{debug_output_path}/Average Images")
    if os.path.exists(f"{debug_output_path}/Average Images") == False:
        os.mkdir(f"{debug_output_path}/Average Images")
    
    # Creates a list of folders in the data directory
    data_path = f"{path}/Data"
    os.chdir(data_path)
    folders_list = [folder for folder in os.listdir(data_path)
                    if os.path.isdir(folder)]
    if "Key" in folders_list:
        folders_list.remove("Key")
    if len(folders_list) == 0:
        print("Error! Folders could not be found!")
        return
    
    # Declares start of motion stabilization
    print("Starting motion stabilization")
    
    # Goes through each data folder
    folder_total = len(folders_list)
    for folder_number in range(folder_total):
        
        # Grabs name of folder
        folder = folders_list[folder_number]
        
        # Generates a list of data images
        files_list = [file for file in os.listdir(f"{data_path}/{folder}")
                      if file.endswith(".tif")]
        if len(files_list) == 0:
            print("Error! Empty folder detected!")
            return
        
        # Goes through each data image and reads the data
        folder_images = [cv2.imread(f"{data_path}/{folder}/{file}",2)
                         for file in files_list]
        folder_images = np.array(folder_images,dtype=np.uint16)
        
        # Gets information about folder shape
        if folder == folders_list[0]:
            images,height,width = folder_images.shape
        
        # Saves as temporary TIFF stack for CaImAn to read
        imageio.mimwrite(f"{images_output_path}/{folder}.tiff",folder_images)
    
    # Sets up variables for CaImAn
    os.chdir(images_output_path)
    fnames = [f"{folder}.tiff" for folder in folders_list]
    max_shifts = (16,16)
    strides = (32,32)
    overlaps = (16,16)
    num_frames_split = 100
    max_deviation_rigid = 3
    pw_rigid = True
    shifts_opencv = False
    border_nan = "copy"
    
    # Performs motion correction using NoRMCorre inside CaImAn
    mc = MotionCorrect(fnames,max_shifts=max_shifts,strides=strides,
                       overlaps=overlaps,max_deviation_rigid=\
                       max_deviation_rigid,shifts_opencv=shifts_opencv,
                       nonneg_movie=True,border_nan=border_nan)
    mc.motion_correct(save_movie=True)
    
    # Assign default values to Gaussian Filter if unspecified
    if gauss_filter == "Default":
        x_value = 2
        y_value = 2
        z_value = 512/height
    else:
        x_value = gauss_filter[0]
        y_value = gauss_filter[1]
        z_value = gauss_filter[2]
    
    # Creates empty list for storing filtered data
    filtered_images = np.zeros((len(folders_list),images,height,width),
                               dtype=np.uint16)
    if mode == 1:
        raw_images = np.zeros((len(folders_list),images,height,width),
                              dtype=np.uint16)
    else:
        raw_images = "N/A"
    
    # Goes through each folder's data
    folder_total = len(folders_list)
    for folder_number in range(folder_total):
        
        # Reads each output file and converts it
        data_location = mc.mmap_file[folder_number]
        folder_images = caiman.load(data_location)
        folder_images = folder_images - np.amin(folder_images)
        folder_images = np.around(folder_images)
        folder_images = folder_images.astype(np.uint16)
        
        # Option to save motion corrected images
        imageio.mimwrite(f"{images_output_path}/{folders_list[folder_number]}\
                         _mc.tiff",folder_images)
        
        # Filters the raw data and writes them into array
        if mode == 1:
            raw_images[folder_number] = folder_images
        filtered_folder_images = xyz_gaussian_filter(folder_images,
                                                     x_value,y_value,z_value)
        filtered_images[folder_number] = filtered_folder_images
        
        # Saves folder average image for debugging
        folder_average = np.average(folder_images,axis=0)
        folder_average = folder_average*(256/np.amax(folder_average))
        folder_average = np.around(folder_average)
        folder_average = folder_average.astype(np.uint8)
        mpimg.imsave(f"{debug_output_path}/Average Images/\
                     {folders_list[folder_number]}.png",
                     folder_average,cmap="gray")
    
    # Deletes TIFF folder to save space but most times it doesn't work
    os.chdir(path)
    try:
        shutil.rmtree(images_output_path)
    except PermissionError:
        pass
    
    # Adds folders_list to the info_storage class
    info_storage.folders_list = folders_list
    
    # Declares end of data extraction
    print("Finished motion stabilization")
    
    return raw_images,filtered_images,info_storage