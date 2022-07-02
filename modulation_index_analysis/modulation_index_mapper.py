# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 15:33:01 2022

@author: Yoshi
"""

import os
import numpy as np
from PIL import Image,ImageDraw,ImageFont



os.chdir("../map_generators")
from cell_drawer import *

def modulation_index_mapper(map_output_path,canvas,width,height,cell_locations,scale,radius,color_key,cell_flags,extra_flag,cell_numbers_list,indices_data,title,intensity,intensity_unit):
    
    # Makes a copy of the canvas
    modulation_index_map = canvas.copy()
    
    # Makes a dictionary for looking up modulation index values
    modulation_index_dict = dict(zip(cell_numbers_list,indices_data))
    
    # Goes through each cell and colors them in with the unresponsive color
    cell_total = len(cell_locations)
    for cell_number in range(cell_total):
        modulation_index_map = cell_drawer(modulation_index_map,cell_locations[cell_number],scale,radius,"#FF0000","#FF0000")
    
    # Goes through each cell
    for cell_number in range(cell_total):
        
        # Checks to see if RFS value has been calculated
        if cell_number+1 in cell_numbers_list:
            
            # Look up RFS value from dictionary
            modulation_index = modulation_index_dict[cell_number+1]
            
            # Default color tag
            color = "N/A"
            
            # Calculates the color to use
            if modulation_index == 0:
                color = "hsv(60,100%,100%)"
            if modulation_index >= -1 and modulation_index < 0:
                hue = 160 - 80 * modulation_index
                saturation = 25 - 75 * modulation_index
                value = 100 - 80 * modulation_index
                color = f"hsv({str(round(hue))},{str(round(saturation))}%,{str(round(value))}%)"
            if modulation_index <= 1 and modulation_index > 0:
                hue = 100 + 80 * modulation_index
                saturation = 25 + 75 * modulation_index
                value = 100 - 80 * modulation_index
                color = f"hsv({str(round(hue))},{str(round(saturation))}%,{str(round(value))}%)"
            
            # Colors cell in based on modulation index value
            if color != "N/A":
                modulation_index_map = cell_drawer(modulation_index_map,cell_locations[cell_number],scale,radius,color,color)
    
    # Creates an outline for cells with extra flag if applicable
    for cell_number in range(cell_total):
        if cell_flags[cell_number][0] != "N/A":
            modulation_index_map = cell_drawer(modulation_index_map,cell_locations[cell_number],scale,radius,"hsv(30,100%,100%)",None)
    
    # Preparation for drawing on image
    draw = ImageDraw.Draw(modulation_index_map)
    
    # Creates a title on the canvas
    draw.rectangle([0,0,width*scale,200],outline="#FFFFFF",fill="#FFFFFF")
    draw.text((width*scale/2,50),f"{title} of Cells",fill="#000000",
              anchor="mm",font=ImageFont.truetype("calibri.ttf",80))
    
    # Determines y coordinates for key boxes
    key_boundaries = []
    if extra_flag != "N/A":
        columns = len(color_key)+1
    else:
        columns = len(color_key)
    for i in range(columns+1):
        x_value = round(width*scale/columns*i)
        key_boundaries.append(x_value)
    
    # Creates a key on the canvas
    i = 0
    for key in color_key:
        color = color_key[key]
        draw.rectangle([key_boundaries[i],100,key_boundaries[i+1],200],outline=color,fill=color)
        draw.text((np.mean([key_boundaries[i],key_boundaries[i+1]]),150),f"{key}",
                   fill="#000000",anchor="mm",font=ImageFont.truetype("calibri.ttf",40))  
        i += 1
    if extra_flag != "N/A":
        color = "hsv(30,100%,100%)"
        draw.rectangle([key_boundaries[-2],100,key_boundaries[-1],200],outline=color,fill=color)
        draw.text((np.mean([key_boundaries[-2],key_boundaries[-1]]),150),extra_flag,
                  fill="#000000",anchor="mm",font=ImageFont.truetype("calibri.ttf",40))
    
    # Saves image
    modulation_index_map.save(f"{map_output_path}/{intensity} {intensity_unit}.png","PNG")
    
    return