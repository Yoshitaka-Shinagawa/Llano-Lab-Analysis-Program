# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 13:17:31 2021

@author: Yoshi
"""

import cv2
import numpy as np
import matplotlib.image as mpimg
from scipy.ndimage import gaussian_filter
from scipy.ndimage import shift as array_shift

import matplotlib.pyplot as plt

from xyz_gaussian_filter import *

def motion_stabilizer(folder,output_path,base_image,folder_images,gauss_filter):
    
    # Constants for image size
    image_height = base_image.shape[1]
    image_crop_start = round(image_height*(1/8))
    image_crop_end = round(image_height*(7/8))
    
    # Crops base image
    base_image_cropped = base_image#gaussian_filter(base_image,sigma=(2,2),mode="nearest")
    base_image_cropped = base_image_cropped[image_crop_start:image_crop_end,image_crop_start:image_crop_end]
    
    # Creates folder average for base motion correction
    folder_average = np.average(folder_images,axis=0)
    # folder_average = gaussian_filter(folder_average,sigma=(2,2),mode="nearest")
    folder_average = folder_average*(256/np.amax(folder_average))
    folder_average = np.around(folder_average)
    folder_average = folder_average.astype(np.uint8)
    folder_average_cropped = folder_average[image_crop_start:image_crop_end,image_crop_start:image_crop_end]
    
    # Calculates optical flow of image
    win_size = int(round(base_image.shape[1]/64))
    flow = cv2.calcOpticalFlowFarneback(base_image_cropped,folder_average_cropped,None,0.9,30,win_size,10,1,1.0,0)
    x_shift = np.average(flow[:,:,0])
    y_shift = np.average(flow[:,:,1])
    base_shift = np.array([x_shift,y_shift])
    print("base shift: ",base_shift)
    
    # Sees if Gaussian filter values are specified, and if not, assigns default values
    if gauss_filter == "Default":
        x_value = 2
        y_value = 2
        image_height = base_image.shape[1]
        z_value = 512/image_height
    else:
        x_value = gauss_filter[0]
        y_value = gauss_filter[1]
        z_value = gauss_filter[2]
    
    # Filters folder images
    filtered_images = xyz_gaussian_filter(folder_images,x_value,y_value,z_value)
    filtered_images = filtered_images*(256/np.amax(filtered_images))
    filtered_images = np.around(filtered_images)
    filtered_images = filtered_images.astype(np.uint8)
    filtered_images_cropped = filtered_images[:,image_crop_start:image_crop_end,image_crop_start:image_crop_end]
    
    # Recreates folder average for filtered motion correction
    folder_average = np.average(filtered_images,axis=0)
    folder_average = np.around(folder_average)
    folder_average = folder_average.astype(np.uint8)
    folder_average_cropped = folder_average[image_crop_start:image_crop_end,image_crop_start:image_crop_end]
    
    # Empty list to store stabilized images in
    stabilized_images = []
    
    # Fallback in case shift cannot be calculated
    
    # Goes through each filtered image
    image_total = filtered_images_cropped.shape[0]
    for image_number in range(image_total):
        
        # Specifies filtered image
        filtered_image_cropped = filtered_images_cropped[image_number]
        
        # Calculates optical flow of image
        win_size = int(round(base_image.shape[1]/64))
        flow = cv2.calcOpticalFlowFarneback(folder_average_cropped,filtered_image_cropped,None,0.8,10,win_size,5,1,1.0,0)
        x_shift = np.average(flow[:,:,0])
        y_shift = np.average(flow[:,:,1])
        shift = np.array([x_shift,y_shift])
        
        # Shifts the original image and adds to list of stabilized images
        final_shift = shift + base_shift
        stabilized_image = array_shift(folder_images[image_number],final_shift,order=5,mode="nearest")
        stabilized_image = np.around(stabilized_image)
        stabilized_image = stabilized_image.astype(np.uint16)
        stabilized_images.append(stabilized_image)
        
    # Converts to numpy array
    stabilized_images = np.array(stabilized_images,dtype=np.uint16)
    
    # Creates and saves folder average image for debugging
    folder_average = np.average(stabilized_images,axis=0)
    folder_average = folder_average*(256/np.amax(folder_average))
    folder_average = np.around(folder_average)
    folder_average = folder_average.astype(np.uint8)
    mpimg.imsave(f"{output_path}/Debug/Average Images/{folder}.png",folder_average,cmap="gray")
    
    # Filters stabilized images for analysis
    filtered_stabilized_images = xyz_gaussian_filter(stabilized_images,x_value,y_value,z_value)
    
    return filtered_stabilized_images