# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:40:05 2022

@author: Yoshi
"""

import os
import shutil
# import matplotlib.pyplot as plt
# from PIL import Image



from average_radius_calculator import *
# from scale_calculator import *
# from cell_number_mapper import *
# from cell_response_mapper import *

def modulation_index_map_generator(path,modulation_path,cell_locations,frequencies,frequency_unit,cell_flags,extra_flag,mode=0):
    
    # Declares start of tonotopic map generation
    print("Starting modulation index map generation")
    
    # Creates and changes to output directory
    modulation_index_map_output_path = f"{path}/Modulation Index Map"
    if os.path.exists(modulation_index_map_output_path) == True:
        shutil.rmtree(modulation_index_map_output_path)
    if os.path.exists(modulation_index_map_output_path) == False:
        os.mkdir(modulation_index_map_output_path)    
    
    # Calculates average radius of cells
    radius = average_radius_calculator(cell_locations)
    
    # Generates color key
    steps_list = 
    color_key = {}
    
    
    
    
    
    
    
    
    # Finds the size of the images from the base image
    average_images_folder = f"{modulation_path}/Output/Debug/Average Images"
    average_images = [file for file in os.listdir(average_images_folder) if file.endswith(".png")]
    base_image_path = f"{average_images_folder}/{average_images[0]}"
    base_image = plt.imread(base_image_path)
    base_image = base_image[:,:,0]
    base_image = base_image * (256/np.amax(base_image))
    base_image = base_image.astype(np.uint8)
    height,width = base_image.shape
    
    # Reads the background image, if it exists
    if os.path.exists(f"{modulation_path}/Data/background_image.tif"):
        background_image = plt.imread(f"{modulation_path}/Data/background_image.tif")
        image = Image.fromarray(background_image,"RGB")
    
    # Otherwise, reads the base image to use as the background image
    else:
        image = Image.fromarray(base_image,"L")
    
    # Calculates appropriate scale for image
    scale = scale_calculator(width)
    
    # Resizes image
    image = image.resize((width*scale,height*scale),resample=3)
    
    # Creates canvas for output image
    canvas = Image.new("RGB",(width*scale,height*scale+200),color="#FFFFFF")
    canvas.paste(image,(0,200))
    
    # Generates map of location of cells
    cell_number_mapper(path,canvas,width,height,cell_locations,scale,radius,cell_flags,extra_flag)
    
    # Generates tonotopic maps for for best frequency and characteristic frequency
    if mode == 0:
        if extra_flag != "N/A":
            cell_response_mapper(path,canvas,width,height,1,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"combined")
            cell_response_mapper(path,canvas,width,height,2,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"combined")
            cell_response_mapper(path,canvas,width,height,1,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"flag")
            cell_response_mapper(path,canvas,width,height,2,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"flag")
            cell_response_mapper(path,canvas,width,height,1,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"no flag")
            cell_response_mapper(path,canvas,width,height,2,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"no flag")
        else:
            cell_response_mapper(path,canvas,width,height,1,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"combined")
            cell_response_mapper(path,canvas,width,height,2,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"combined")
    
    # Generate noise response maps
    elif mode == 1:
        if extra_flag != "N/A":
            cell_response_mapper(path,canvas,width,height,3,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"combined")
            cell_response_mapper(path,canvas,width,height,3,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"flag")
            cell_response_mapper(path,canvas,width,height,3,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"no flag")
        else:
            cell_response_mapper(path,canvas,width,height,3,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,"combined")
    
    # Declares end of tonotopic map generation
    print("Finished tonotopic map generation")
    
    return