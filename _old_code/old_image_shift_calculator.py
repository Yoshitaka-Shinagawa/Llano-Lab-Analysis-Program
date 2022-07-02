# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:18:54 2019

@author: Yoshi
"""

import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim



from image_rounder import *

def image_shift_calculator(folder_average,filtered_images,min_power,max_power):
    
    # Creates a list of shifts
    shifts = [(0,0),(0,1),(0,-1),(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1)]
    shifts = np.array(shifts)
    
    # Finds the shape of the image
    height = folder_average.shape[0]
    width = folder_average.shape[1]
    
    # Finds the width of borders to crop out
    y_border = round(height/16)
    x_border = round(width/16)
    borders = {}
    for power in range(min_power,max_power+1):
        scale = 2 ** power
        border = (round(y_border*scale),round(x_border*scale))
        borders[power] = border
    
    # Creates a dictionary of resized averages
    resized_averages = {}
    for power in range(min_power,max_power+1):
        scale = 2 ** power
        resized_average = cv2.resize(folder_average,None,fx=scale,fy=scale,interpolation=cv2.INTER_CUBIC)
        resized_average = image_rounder(resized_average)
        cropped_resized_average = resized_average[borders[power][0]:-borders[power][0],borders[power][1]:-borders[power][1]]
        resized_averages[power] = cropped_resized_average
    
    # An empty list to keep track of the shifts
    image_shifts = []
    
    # Goes through each image
    for image in filtered_images:
        
        # Variables to keep track of
        power = 0
        start_power = 0
        current_shift = np.array([0,0])
        
        # Goes through each power of 2
        while power <= max_power:
            
            # Resizes the image
            scale = 2 ** power
            resized_image = cv2.resize(image,None,fx=scale,fy=scale,interpolation=cv2.INTER_CUBIC)
            resized_image = image_rounder(resized_image)
            
            # Uses the previous shifts to calculate the offset
            previous_shift = current_shift * 2
            y_shift_0 = previous_shift[0]
            x_shift_0 = previous_shift[1]
            
            # An empty list to keep track of the SSIM scores
            scores = []
            
            # Goes through each of the 9 shifts
            for shift in shifts:
                
                # Calculates shifts
                y_shift = y_shift_0 + shift[0]
                x_shift = x_shift_0 + shift[1]
                
                # Crops the image based on its shift
                height,width = resized_image.shape
                cropped_resized_image = resized_image[borders[power][0]+y_shift:height-borders[power][0]+y_shift,borders[power][1]+x_shift:width-borders[power][1]+x_shift]
                
                # Calculates the SSIM score and adds it to the list
                score = ssim(resized_averages[power],cropped_resized_image)
                scores.append(score)
            
            # Finds the maximum score
            max_index = scores.index(max(scores))
            max_shift = shifts[max_index]
            
            # If the starting shift wasn't [0,0], backs up one step unless it reaches the minimum power
            if power == start_power and max_shift.tolist() != [0,0] and start_power > min_power:
                power -= 1
                start_power -= 1
            
            # If it's the final shift, it calculates how much the image has moved overall
            elif power == max_power:
                final_shift = (previous_shift+max_shift) / 2**power
                power += 1
            
            # Otherwise it adds the pixel shift to the original shift and moves onto the next power
            else:
                power += 1
                current_shift = previous_shift + max_shift
        
        # Adds the final calculated shift to the list
        image_shifts.append(final_shift)
        
    return image_shifts