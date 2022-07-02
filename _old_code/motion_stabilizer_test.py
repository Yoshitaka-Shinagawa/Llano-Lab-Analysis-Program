# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:56:13 2019

@author: Yoshi
"""

import numpy as np
import matplotlib
from SSIM_PIL import compare_ssim
from PIL import Image
#from skimage.metrics import structural_similarity as ssim
from scipy.ndimage import shift as array_shift



from xyz_gaussian_filter import *
from image_rounder import *

def motion_stabilizer_test(folder,output_path,base_image,folder_images):
    
    # Filters the folder data
    filtered_images = xyz_gaussian_filter(folder_images,1,1,3)
    
    # Creates an average image of the folder
    folder_average = np.average(filtered_images,axis=0)
    
    # Sets maximum zoom in and zoom out
    start_power = -3
    max_zoom = 3
    
    # Creates dictionary for scaled shifts
    simple_shifts = [(0,0),(0,1),(0,-1),(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1)]
    simple_shifts = np.array(simple_shifts)
    zoom_shifts = {}
    for power in range(start_power,max_zoom+1):
        scaled_shifts = []
        for simple_shift in simple_shifts:
            scaled_shifts.append(simple_shift*2**-power)
        zoom_shifts[power] = scaled_shifts
    
    # Sets constants for calculating base shifts
    power = start_power
    previous_shift = np.array([0,0])
    
    # Converts base_image from array to image
    base_image_converted = Image.fromarray(base_image)
    
    # Loops until power reaches max zoom
    while power <= max_zoom:
        
        # Empty list to store shifts and scores
        shifts = []
        scores = []
        
        # Goes through each shift
        for scaled_shift in zoom_shifts[power]:
            shift = previous_shift + scaled_shift
            shifts.append(shift)
            
            # Shifts image
            shifted_image = array_shift(folder_average,shift,order=5,mode='nearest')
            shifted_image = image_rounder(shifted_image)
            
            # Calculates SSIM score and adds it to list
            score = compare_ssim(base_image_converted,Image.fromarray(shifted_image))
            scores.append(score)
        
        # Caclulates shift with maximum SSIM score
        max_shift = shifts[scores.index(max(scores))]
        
        # Keeps going if power is below max zoom
        if power < max_zoom:
            previous_shift = max_shift
        
        # Otherwise sets base_shift equal to max_shift
        elif power == max_zoom:
            base_shift = max_shift
        
        # Increases power by 1
        power += 1
    
    # Rounds folder average to integers
    folder_average = image_rounder(folder_average)
    
    # Converts folder average from array to image
    folder_average_converted = Image.fromarray(folder_average)
    
    # Empty list to store stabilized images in
    filtered_stabilized_images = []
    
    # Goes through each filtered image
    for filtered_image in filtered_images:
        
        # Constants for loops
        power = start_power
        previous_shift = np.array([0,0])
        
        # Loops until power reaches max zoom
        while power <= max_zoom:
            
            # Empty list to store shifts and scores
            shifts = []
            scores = []
            
            # Goes through each shift
            for scaled_shift in zoom_shifts[power]:
                shift = previous_shift + scaled_shift
                shifts.append(shift)
                
                # Shifts image
                shifted_image = array_shift(filtered_image,shift,order=5,mode='nearest')
                shifted_image = image_rounder(shifted_image)
                
                # Calculates SSIM score and adds it to list
                score = compare_ssim(folder_average_converted,Image.fromarray(shifted_image))
                scores.append(score)
            
            # Caclulates shift with maximum SSIM score
            max_shift = shifts[scores.index(max(scores))]
            
            # Keeps going if power is below max zoom
            if power < max_zoom:
                previous_shift = max_shift
            
            # Otherwise adds stabilized image to list
            elif power == max_zoom:
                final_shift = max_shift + base_shift
                stabilized_image = array_shift(filtered_image,final_shift,order=5,mode='nearest')
                stabilized_image = image_rounder(stabilized_image)
                filtered_stabilized_images.append(stabilized_image)
            
            # Increases power by 1
            power += 1
    
    
    
    ###### DELETE AFTER SWITCHING TO FISSA ######
    #filtered_stabilized_images = np.array(filtered_stabilized_images)
    
    
    
    # Saves stabilized average image for debugging
    stabilized_folder_average = np.average(filtered_stabilized_images,axis=0)
    stabilized_folder_average = stabilized_folder_average * (256/np.amax(stabilized_folder_average))
    stabilized_folder_average = np.around(stabilized_folder_average)
    stabilized_folder_average = stabilized_folder_average.astype(np.uint8)
    #matplotlib.image.imsave(f'{output_path}/Debug/Average Images/{folder}.png',stabilized_folder_average,cmap='gray')
    
    return filtered_stabilized_images