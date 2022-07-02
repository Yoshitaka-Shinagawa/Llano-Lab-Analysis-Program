# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:56:13 2019

@author: Yoshi
"""

import numpy as np
import matplotlib.image as mpimg
from joblib import Parallel, delayed
from skimage.metrics import structural_similarity
#from SSIM_PIL import compare_ssim
from PIL import Image
from scipy.ndimage import shift as array_shift



from xyz_gaussian_filter import *
from image_rounder import *

# Stupid function needed for parallelization

def motion_stabilizer(folder,output_path,base_image,folder_images,min_zoom,max_zoom):
    
    # Constants for image size
    image_height = base_image.shape[1]
    image_crop_start = round(image_height*(1/4))
    image_crop_end = round(image_height*(3/4))
    
    # Decides value for filtering in z axis based on image 
    z_value = 512/image_height
    
    # Filters the folder data
    filtered_images = xyz_gaussian_filter(folder_images,2,2,z_value)
    
    # Creates an average image of the folder
    folder_average = np.average(filtered_images,axis=0)
    
    # Rounds folder average to integers
    folder_average = image_rounder(folder_average)
    
    # Converts array to image format
    folder_average_converted =folder_average[image_crop_start:image_crop_end,image_crop_start:image_crop_end]
    base_image_converted = base_image[image_crop_start:image_crop_end,image_crop_start:image_crop_end]
    
    # Calculate maximum number of steps to take
    max_steps = 2**(max_zoom-min_zoom)
    
    # Creates dictionary for scaled shifts
    step_shifts = {}
    step_shifts[0] = [np.array([0,0])]
    simple_shifts = [(x,y) for x in range(-1,2) for y in range(-1,2)]
    simple_shifts.remove((0,0))
    simple_shifts = np.array(simple_shifts)
    step_size = 2**min_zoom
    for step in range(1,2**(max_zoom-min_zoom)+1):
        step_shifts[step] = [simple_shift*step*step_size for simple_shift in simple_shifts]   
        
    # Blank list to add shifts and scores to for base adjustment
    all_shifts = []
    all_scores = []
    
    # Goes through each step
    for step in range(0,2**(max_zoom-min_zoom)+1):
        
        # Calculates shifts and adds it to comprehensive list of shifts
        shifts = [step_shift for step_shift in step_shifts[step]]
        all_shifts += shifts
        
        # Shifts images
        shifted_images = Parallel(n_jobs=8)(delayed(array_shift)(folder_average,shift,order=5,mode='nearest') for shift in shifts)
        
        # Rounds and converts images
        shifted_rounded_images = [image_rounder(shifted_image) for shifted_image in shifted_images]
        shifted_rounded_converted_images = [shifted_rounded_image[image_crop_start:image_crop_end,image_crop_start:image_crop_end] for shifted_rounded_image in shifted_rounded_images]
        
        # Calculates scores of images and adds it to comprehensive list of scores
        scores = Parallel(n_jobs=8)(delayed(structural_similarity)(base_image_converted,shifted_rounded_converted_image) for shifted_rounded_converted_image in shifted_rounded_converted_images)
        all_scores += scores
        
        # Checks if the max score is above the threshold
        if max(scores) >= 0.90:
            
            # Sets the maximum shift and previous shift, calculates the final shift, and adds image to list of stabilized images
            base_shift = shifts[scores.index(max(scores))]
            print('Base shift: ',base_shift,max(scores))
            print(all_shifts[0:10],all_scores[0:10])
            break
        
        # Otherwise calculates the max score from the comprehensive list of scores
        elif step == 2**(max_zoom-min_zoom):
            
            # Sets the maximum shift and previous shift, calculates the final shift, and adds image to list of stabilized images                
            base_shift = all_shifts[all_scores.index(max(all_scores))]
            print('Base shift: ',base_shift,max(all_scores))
            print(all_shifts[0:10],all_scores[0:10])
            break
    
    # Sets previous_shift for first image
    previous_shift = np.array([0,0])
    
    # Empty list to store stabilized images in
    filtered_stabilized_images = []
    
    # Calculate the shift for each filtered image
    for filtered_image in filtered_images:
        
        # Blank list to add shifts and scores to
        all_shifts = []
        all_scores = []
        
        # Goes through each step
        for step in range(0,max_steps+1):
            
            # Calculates shifts and adds it to comprehensive list of shifts
            shifts = [previous_shift+step_shift for step_shift in step_shifts[step]]
            all_shifts += shifts
            
            # Shifts images
            shifted_images = Parallel(n_jobs=8)(delayed(array_shift)(filtered_image,shift,order=5,mode='nearest') for shift in shifts)
            
            # Rounds and converts images
            shifted_rounded_images = [image_rounder(shifted_image) for shifted_image in shifted_images]
            shifted_rounded_converted_images = [shifted_rounded_image[image_crop_start:image_crop_end,image_crop_start:image_crop_end] for shifted_rounded_image in shifted_rounded_images]
            
            # Calculates scores of images and adds it to comprehensive list of scores
            scores = Parallel(n_jobs=8)(delayed(structural_similarity)(folder_average_converted,shifted_rounded_converted_image) for shifted_rounded_converted_image in shifted_rounded_converted_images)
            all_scores += scores
            
            # Checks if the max score is above the threshold
            if max(scores) >= 0.90:
                
                # Sets the maximum shift and previous shift, calculates the final shift, and adds image to list of stabilized images
                max_shift = shifts[scores.index(max(scores))]
                previous_shift = max_shift
                final_shift = max_shift + base_shift
                # print(max_shift,max(scores))
                stabilized_image = array_shift(filtered_image,final_shift,order=5,mode='nearest')
                stabilized_image = image_rounder(stabilized_image)
                filtered_stabilized_images.append(stabilized_image)
                break
            
            # Otherwise calculates the max score from the comprehensive list of scores
            elif step == max_steps:
                
                # Sets the maximum shift and previous shift, calculates the final shift, and adds image to list of stabilized images                
                max_shift = all_shifts[all_scores.index(max(all_scores))]
                previous_shift = max_shift
                final_shift = max_shift + base_shift
                print(max_shift,max(all_scores))
                stabilized_image = array_shift(filtered_image,final_shift,order=5,mode='nearest')
                stabilized_image = image_rounder(stabilized_image)
                filtered_stabilized_images.append(stabilized_image)
                break
    
    # Converts to numpy array to save as tiff stack
    filtered_stabilized_images = np.array(filtered_stabilized_images)
    
    # Saves stabilized average image for debugging
    stabilized_folder_average = np.average(filtered_stabilized_images,axis=0)
    stabilized_folder_average = stabilized_folder_average * (256/np.amax(stabilized_folder_average))
    stabilized_folder_average = np.around(stabilized_folder_average)
    stabilized_folder_average = stabilized_folder_average.astype(np.uint8)
    mpimg.imsave(f'{output_path}/Debug/Average Images/{folder}.png',stabilized_folder_average,cmap='gray')
    
    return filtered_stabilized_images