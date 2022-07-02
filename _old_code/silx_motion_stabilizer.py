# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:56:13 2019

@author: Yoshi
"""

import os
import numpy as np
import matplotlib
from silx.image import sift



from xyz_gaussian_filter import *

def motion_stabilizer(folder,output_path,folder_images):
    
    # Filters the folder data
    filtered_images = xyz_gaussian_filter(folder_images,1,1,3)
    
    
    
    ###### CHANGE ABOVE TO (1,1,1) AFTER SWITCHING TO FISSA ######
    
    
    
    # Creates an average image of the folder
    folder_average = np.average(filtered_images,axis=0)
    
    # Uses silx to stabilize motion of images
    filtered_stabilized_images = []
    os.environ["PYOPENCL_COMPILER_OUTPUT"] = "0"
    alignment = sift.LinearAlign(folder_average,devicetype='GPU')
    for image in filtered_images:
        stabilized_image = alignment.align(image,shift_only=False)
        if type(stabilized_image) == np.ndarray:
            filtered_stabilized_images.append(stabilized_image)
        else:
            filtered_stabilized_images.append(image)
    
    
    
    ###### DELETE AFTER SWITCHING TO FISSA ######
    filtered_stabilized_images = np.array(filtered_stabilized_images)
    
    
    
    # Saves stabilized average image for debugging
    stabilized_folder_average = np.average(filtered_stabilized_images,axis=0)
    stabilized_folder_average = stabilized_folder_average * (256/np.amax(stabilized_folder_average))
    stabilized_folder_average = np.around(stabilized_folder_average)
    stabilized_folder_average = stabilized_folder_average.astype(np.uint8)
    matplotlib.image.imsave(f'{output_path}/Debug/Average Images/{folder}.png',stabilized_folder_average,cmap='gray')
    
    return filtered_stabilized_images