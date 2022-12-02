# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 11:04:50 2022

@author: Austin
"""

import os
import shutil 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image



from average_radius_calculator import *
from color_key_generator import *
from scale_calculator import *
from cell_number_mapper import *
from cell_response_mapper import *

# Sets a base path and creates paths to each data type excel sheet
# path = "E:/Llano Lab/SomatoSensory/2022-11-23/101422_RCAMPxgad67_070422_SOMATO_side/Somato_HP/D1/For analysis"


def latency_response_mapper(info_storage):
    
    '''
        This function is used for visualizing the responsive cells based on 
        a their latency 
        
    '''
    
    # Extracts variables from the info_storage class
    path           = info_storage.path
    cell_locations = info_storage.cell_locations
    cell_flags     = info_storage.cell_flags
    extra_flag     = info_storage.extra_flag
    frequencies    = info_storage.frequencies
    mode           = info_storage.mode

    
    
    # Declares start of tonotopic map generation
    print("Starting latency map generation")
    
    # Creates output directories 
    latency_map_output_path = f"{path}/Output/Latency"
    if os.path.exists(f"{path}/Latency Maps") == True:
        shutil.rmtree(f"{path}/Latency Maps")
    if os.path.exists(f"{path}/Output/Adaptive Maps") == True:
        shutil.rmtree(f"{path}/Output/Adaptive Maps")
    if os.path.exists(f'{latency_map_output_path}/Latency Maps') == False:
        os.mkdir(f"{latency_map_output_path}/Latency Maps")
    if os.path.exists(f'{path}/Output/Adaptive Maps') == False:
        os.mkdir(f"{path}/Output/Adaptive Maps")
        # excel_output_path = f"{latency_map_output_path}/Spreadsheets"
        # os.mkdir(excel_output_path)
        
    # Calculates average radius of cells
    radius = average_radius_calculator(cell_locations)
   
    # Generates another color key for noise analysis
    if mode == 1:
        color_key = {"Yes":"hsv(120,100%,100%)"}
    
    # Finds the size of the images from the base image
    average_images_folder = f"{path}/Output/Debug/Average Images"
    average_images = [file for file in os.listdir(average_images_folder) if 
                      file.endswith(".png")]
    base_image_path = f"{average_images_folder}/{average_images[0]}"
    base_image = plt.imread(base_image_path)
    base_image = base_image[:,:,0]
    base_image = base_image * (256/np.amax(base_image))
    base_image = base_image.astype(np.uint8)
    height,width = base_image.shape
    
    # Reads the background image, if it exists
    if os.path.exists(f"{path}/Data/background_image.tif"):
        background_image = plt.imread(f"{path}/Data/background_image.tif")
        image = Image.fromarray(background_image,"RGB")
    
    # Otherwise, reads the base image to use as the background image
    else:
        image = Image.fromarray(base_image,"L")
    
    # Calculates appropriate scale for image
    scale = scale_calculator(width)
    
    # Resizes image
    image = image.resize((width*scale,height*scale),resample=3)
    
    # Creates canvas for output image
    canvas = Image.new("RGBA",(width*scale,height*scale+200),(0,0,0,0))
    # canvas.paste(image,(0,200))
    
    # Adds new information to the info_storage class
    info_storage.canvas = canvas
    info_storage.width  = width
    info_storage.height = height
    info_storage.scale  = scale
    info_storage.radius = radius
    
    # Generates map of location of cells
    cell_number_mapper(info_storage)
    
    # Generate noise response maps
    if mode == 1:
        if extra_flag != "N/A":
            cell_response_mapper(info_storage,color_key,4,"combined")
            cell_response_mapper(info_storage,color_key,4,"flag")
            cell_response_mapper(info_storage,color_key,4,"no flag")
        else:
            cell_response_mapper(info_storage,color_key,4,"somatosensory")
            cell_response_mapper(info_storage,color_key,5,"somatosensory")
            cell_response_mapper(info_storage,color_key,6,"adaptive")
            cell_response_mapper(info_storage,color_key,7,"adaptive")

    
    # Shows the plot
    plt.show()
   
    # Saves the figure 
    # plt.savefig(base_path)
    
  


    
    
    
    return info_storage