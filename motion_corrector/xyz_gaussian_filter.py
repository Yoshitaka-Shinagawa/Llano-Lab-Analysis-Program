# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:32:30 2019

@author: Yoshi
"""

import numpy as np
from joblib import Parallel, delayed
from scipy.ndimage import gaussian_filter,gaussian_filter1d

def xyz_gaussian_filter(folder_images,x_sigma,y_sigma,z_sigma):
    
    """
    This is the function used to apply a 3D Gaussian filter on a stack of numpy
    arrays of images. It first applies a 2D Gaussian blur to all images using
    the gaussian_filter function from the scipy.ndimage library, then applies a
    1D Gaussian blur along the temporal axis using the gaussian_filter1d
    function from the same library.
    
    Parameters
    ----------
    folder_images: A 3D numpy array containing the images that need to be
        filtered.
    x_sigma: The sigma value for the up-down axis.
    y_sigma: The sigma value for the left-right axis.
    z_sigma: The sigma value for the temporal axis.
    
    Returns
    -------
    filtered_images: A 3D numpy array containing the filtered images.
    """
    
    # Goes through each image and applies a 2D Gaussian blur
    filtered_images = Parallel(n_jobs=12)(delayed(gaussian_filter)(image,sigma=(x_sigma,y_sigma),mode="nearest") for image in folder_images)
    filtered_images = np.array(filtered_images)
    
    # Loop constants
    rows = folder_images.shape[1]
    columns = folder_images.shape[2]
    
    # Goes through each pixel in z direction
    for row in range(rows):
        columns_data = Parallel(n_jobs=12)(delayed(gaussian_filter1d)(filtered_images[:,row,column],sigma=z_sigma,mode="nearest") for column in range(columns))
        for column in range(columns):
            filtered_images[:,row,column] = columns_data[column]
            gaussian_filter1d(filtered_images[:,row,column],sigma=z_sigma,mode="nearest")
    
    return filtered_images