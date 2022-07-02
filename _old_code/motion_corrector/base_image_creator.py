# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 13:21:02 2021

@author: Yoshi
"""

import os
import shutil
import cv2
import numpy as np
import matplotlib.image as mpimg



def base_image_creator(data_path,output_path,folders_list):
    
    # Creates folder for saving base image
    if os.path.exists(f"{output_path}/Debug/Base Image") == True:
        shutil.rmtree(f"{output_path}/Debug/Base Image")
    if os.path.exists(f"{output_path}/Debug/Base Image") == False:
        os.mkdir(f"{output_path}/Debug/Base Image")
        
    # Empty list to store folder averages
    folder_averages = []
    
    # Goes through each data folder
    for folder in [folders_list[0]]:
        
        # Changes directory to folder
        folder_path = f"{data_path}/{folder}"
        os.chdir(folder_path)
        
        # Generates a list of data images
        files_list = [file for file in os.listdir(folder_path) if file.endswith(".tif")]
        if len(files_list) == 0:
            print("Error! Empty folder detected!")
            return
        
        # Reads each image and adds it to list of all images
        folder_images = [cv2.imread(file,2) for file in files_list]
        folder_images = np.array(folder_images,dtype=np.uint16)
        
        # Create average image for each folder and add to list
        folder_average = np.average(folder_images,axis=0)
        folder_averages.append(folder_average)
    
    # Converts list to numpy array
    
    folder_averages = np.array(folder_averages)
    
    # Creates base image for motion correction
    base_image = np.average(folder_averages,axis=0)
    base_image = base_image*(256/np.amax(base_image))
    base_image = np.around(base_image)
    base_image = base_image.astype(np.uint8)
    
    # Saves image for debugging
    mpimg.imsave(f"{output_path}/Debug/Base Image/Base Image.png",base_image,cmap="gray")
    
    # Removes large arrays to save memory
    del folder_images
    del folder_averages
    
    return base_image