# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 16:03:47 2021

@author: Yoshi
"""

import os
import shutil
import cv2
import matplotlib.image as mpimg
import numpy as np
from scipy.ndimage import gaussian_filter



def base_image_creator(data_path,output_path,folders_list):
    
    # Empty list to store folder averages
    folder_averages = []
    
    # Goes through each data folder
    for folder in folders_list:
        
        # Empty list to store folder images
        folder_images = []
        
        # Changes directory to folder
        folder_path = f'{data_path}/{folder}'
        os.chdir(folder_path)
        
        # Generates a list of data images
        files_list = [file for file in os.listdir(folder_path) if file.endswith('.tif') and 'Ch1' in file]
        if len(files_list) == 0:
            print('Error! Empty folder detected!')
            return
        
        # Reads each image and adds it to list of all images
        for file in files_list:
            folder_images.append(cv2.imread(file,2))
        folder_images = np.array(folder_images,dtype=np.float32)
        
        # Create average image for each folder and add to list
        folder_average = np.average(folder_images,axis=0)
        folder_average = np.around(folder_average)
        folder_average = folder_average.astype(np.uint16)
        folder_averages.append(folder_average)
    
    # Converts list to numpy array
    folder_averages = np.array(folder_averages,dtype=np.float32)
    
    # Creates average image without filter for debugging
    base_image_no_filter = np.average(folder_averages,axis=0)
    base_image_no_filter = np.around(base_image_no_filter)
    base_image_no_filter = base_image_no_filter.astype(np.uint16)
    
    # Creates folder for saving base image
    if os.path.exists(f'{output_path}/Debug/Base Image') == True:
        shutil.rmtree(f'{output_path}/Debug/Base Image')
    if os.path.exists(f'{output_path}/Debug/Base Image') == False:
        os.mkdir(f'{output_path}/Debug/Base Image')
    
    # Saves base image without filter for debugging
    save_base_image = base_image_no_filter * (256/np.amax(base_image_no_filter))
    save_base_image = np.around(save_base_image)
    save_base_image = save_base_image.astype(np.uint8)
    mpimg.imsave(f'{output_path}/Debug/Base Image/Base Image No Filter.png',save_base_image,cmap='gray')
    
    # Filters base image to make it closer to what filtered images look like
    base_image = gaussian_filter(base_image_no_filter,sigma=(2,2),mode='nearest')
    base_image = np.around(base_image)
    base_image = base_image.astype(np.uint16)
    
    # Saves base image for debugging
    save_base_image = base_image * (256/np.amax(base_image))
    save_base_image = np.around(save_base_image)
    save_base_image = save_base_image.astype(np.uint8)
    mpimg.imsave(f'{output_path}/Debug/Base Image/Base Image.png',save_base_image,cmap='gray')
    
    return base_image