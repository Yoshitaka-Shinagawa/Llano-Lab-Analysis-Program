# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:12:11 2019

@author: Yoshi
"""

import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image



from average_radius_calculator import *
from color_key_generator import *
from scale_calculator import *
from cell_number_mapper import *
from cell_response_mapper import *

def tonotopic_map_generator(path,cell_locations,frequencies,frequency_unit,cell_flags,extra_flag,mode=0):
    
    # Declares start of tonotopic map generation
    print("Starting tonotopic map generation")
    # Creates and changes to output directory
    output_folder_path = f"{path}/Output"
    if os.path.exists(output_folder_path) == False:
        os.mkdir(output_folder_path)
    tonotopic_map_output_path = f"{path}/Output/Tonotopy"
    if os.path.exists(tonotopic_map_output_path) == True:
        shutil.rmtree(tonotopic_map_output_path)
    if os.path.exists(f"{path}/Output/Tonotopic Map") == True:
        shutil.rmtree(f"{path}/Output/Tonotopic Map")
    if os.path.exists(tonotopic_map_output_path) == False:
        os.mkdir(tonotopic_map_output_path)
        os.mkdir(f"{tonotopic_map_output_path}/Tonotopic Maps")
        os.mkdir(f"{tonotopic_map_output_path}/Spreadsheets")
    
    # Calculates average radius of cells
    radius = average_radius_calculator(cell_locations)
    
    # Generates color key if doing tonotopic analysis
    if mode == 0:
        color_key = color_key_generator(frequencies)
    
    # Generates another color key for noise analysis
    elif mode == 1:
        color_key = {"Yes":"hsv(140,100%,100%)"}
    
    # Finds the size of the images from the base image
    average_images_folder = f"{path}/Output/Debug/Average Images"
    average_images = [file for file in os.listdir(average_images_folder) if file.endswith(".png")]
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
    
    # Generates map of location of cells
    cell_number_mapper(tonotopic_map_output_path,canvas,width,height,cell_locations,scale,radius,cell_flags,extra_flag)
    
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
    
    # Exports best frequency and characteristic frequency of cells
    cell_numbers = []
    cell_flag_list = []
    best_frequencies = []
    characterstic_frequencies = []
    cell_total = len(cell_flags)
    for cell_number in range(cell_total):
        cell_numbers.append(cell_number+1)
        cell_flag_list.append(cell_flags[cell_number][0])
        best_frequencies.append(cell_flags[cell_number][1])
        characterstic_frequencies.append(cell_flags[cell_number][2])
    dataframe = {"Cell Number":cell_numbers,"Cell Flag":cell_flag_list,"Best Frequency":best_frequencies,"Characteristic Frequency":characterstic_frequencies}
    dataframe = pd.DataFrame(dataframe)
    dataframe.to_excel(f"{tonotopic_map_output_path}/Spreadsheets/Frequencies.xlsx",index=False)
    
    # Exports statistics for the data
    [total_cells,responsive_cells,unresponsive_cells] = [0,0,0]
    [flagged_total,flagged_responsive,flagged_unresponsive] = [0,0,0]
    [unflagged_total,unflagged_responsive,unflagged_unresponsive] = [0,0,0]
    for cell_flag in cell_flags:
        total_cells += 1
        if cell_flag[1] != "N/A":
            responsive = True
            responsive_cells += 1
        else:
            responsive = False
            unresponsive_cells += 1
        if cell_flag[0] != "N/A":
            flagged_total += 1
            if responsive == True:
                flagged_responsive += 1
            else:
                flagged_unresponsive += 1
        if cell_flag[0] == "N/A":
            unflagged_total += 1
            if responsive == True:
                unflagged_responsive += 1
            else:
                unflagged_unresponsive += 1
    if extra_flag != "N/A":
        statistics = {"Responsive Cells": [responsive_cells,flagged_responsive,unflagged_responsive],
                      "Unresponsive Cells": [unresponsive_cells,flagged_unresponsive,unflagged_unresponsive],
                      "Total Cells": [total_cells,flagged_total,unflagged_total]}
        statistics = pd.DataFrame(statistics,index=["Combined","Flagged","Unflagged"])
    else:
        statistics = {"Responsive Cells": [responsive_cells],
                      "Unresponsive Cells": [unresponsive_cells],
                      "Total Cells": [total_cells]}
        statistics = pd.DataFrame(statistics,index=["Combined"])
    statistics.to_excel(f"{tonotopic_map_output_path}/Spreadsheets/Statistics.xlsx")
    
    # Declares end of tonotopic map generation
    print("Finished tonotopic map generation")
    
    return canvas,width,height,scale,radius