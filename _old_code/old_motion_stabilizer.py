# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:56:13 2019

@author: Yoshi
"""

import numpy as np
import matplotlib



from xyz_gaussian_filter import *
from image_shift_calculator import *

def motion_stabilizer(folder,output_path,base_image,folder_images,max_zoom):
    
    # Filters the folder data
    filtered_images = xyz_gaussian_filter(folder_images,1,1,3)
    
    # Creates an average image of the folder
    folder_average = np.average(filtered_images,axis=0)
    matplotlib.image.imsave(output_path+'/Debug/Average Images/'+folder+'.png',folder_average,cmap='gray')
    
    # Calculates the shifts of the images in the folder
    image_shifts = image_shift_calculator(folder_average,filtered_images,-3,max_zoom)
    
    # Calculates the base shift between the base image and the folder average
    base_image_array = np.zeros((1,folder_images.shape[1],folder_images.shape[2]),dtype=np.float32)
    base_image_array[0] = base_image
    base_shift = image_shift_calculator(folder_average,base_image_array,-3,max_zoom)
    
    # Shifts all of the shifts by the base shift
    for shift in image_shifts:
        shift += base_shift[0]
    
    return filtered_images,image_shifts