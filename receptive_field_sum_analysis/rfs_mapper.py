# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:56:40 2022

@author: Yoshi
"""

import os
import numpy as np
from PIL import Image,ImageDraw,ImageFont



os.chdir("../map_generators")
from cell_drawer import *

def rfs_mapper(info_storage,map_output_path,color_key,cell_numbers,
               receptive_field_sums,title,rfs_max):
    
    """
    This is the function used to create the maps of the RFS values. It draws 
    the cells onto a map and colors them in with their corresponding RFS value,
    then creates an outline to distinguish special cells (GABAergic in our
    case) from normal cells.
    
    Parameters
    ----------
    info_storage : The class used to store most of the variables that are used
        in the analysis program.
    map_output_path : The path to the folder in which the maps will be saved
        in.
    color_key : The dictionary that has a shade of green for each major step of
        the RFS value.
    cell_numbers : The list containing the cell numbers of the cells that had
        an RFS value above 0.
    receptive_field_sums : The list containing the RFS values of the cells that
         had an RFS value above 0.
    title : The file name that the map will be saved as.
    rfs_max : The highest possible RFS value.
    
    Returns
    -------
    none
    """
    
    # Extracts variables from the info_storage class
    canvas                   = info_storage.canvas
    width                    = info_storage.width
    height                   = info_storage.height
    cell_locations           = info_storage.cell_locations
    scale                    = info_storage.scale
    radius                   = info_storage.radius
    cell_flags               = info_storage.cell_flags
    extra_flag               = info_storage.extra_flag
    
    # Makes a copy of the canvas
    rfs_map = canvas.copy()
    
    # Makes a dictionary for looking up RFS values
    rfs_dict = dict(zip(cell_numbers,receptive_field_sums))
    
    # Goes through each cell and colors them in with the unresponsive color
    cell_total = len(cell_locations)
    for cell_number in range(cell_total):
        rfs_map = cell_drawer(rfs_map,cell_locations[cell_number],scale,radius,
                              "#FF0000","#FF0000")
    
    # Goes through each cell
    for cell_number in range(cell_total):
        
        # Checks to see if RFS value has been calculated
        if cell_number+1 in cell_numbers:
            
            # Look up RFS value from dictionary
            rfs_value = rfs_dict[cell_number+1]
            
            # Make sure RFS value is above zero
            if rfs_value > 0:
                
                # Calculate the color to use
                hue = 80 + 100 / (rfs_max-1) * rfs_value
                saturation = 25 + 75 / (rfs_max-1) * rfs_value
                value = 100 - 80 / (rfs_max-1) * rfs_value
                color = f"hsv({str(round(hue))},{str(round(saturation))}%,"+\
                    f"{str(round(value))}%)"
                
                # Colors cell in based on RFS value
                rfs_map = cell_drawer(rfs_map,cell_locations[cell_number],
                                      scale,radius,color,color)
    
    # Creates an outline for cells with extra flag if applicable
    for cell_number in range(cell_total):
        if cell_flags[cell_number][0] != "N/A":
            rfs_map = cell_drawer(rfs_map,cell_locations[cell_number],scale,
                                  radius,"hsv(30,100%,100%)",None)
    
    # Preparation for drawing on image
    draw = ImageDraw.Draw(rfs_map)
    
    # Creates a title on the canvas
    draw.rectangle([0,0,width*scale,200],outline="#FFFFFF",fill="#FFFFFF")
    draw.text((width*scale/2,50),"Receptive Field Sums of Cells",
              fill="#000000",anchor="mm",
              font=ImageFont.truetype("calibri.ttf",80))
    
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
        draw.rectangle([key_boundaries[i],100,key_boundaries[i+1],200],
                       outline=color,fill=color)
        draw.text((np.mean([key_boundaries[i],key_boundaries[i+1]]),150),
                  f"{key}",
                   fill="#000000",anchor="mm",font=ImageFont.truetype(
                       "calibri.ttf",40))  
        i += 1
    if extra_flag != "N/A":
        color = "hsv(30,100%,100%)"
        draw.rectangle([key_boundaries[-2],100,key_boundaries[-1],200],
                       outline=color,fill=color)
        draw.text((np.mean([key_boundaries[-2],key_boundaries[-1]]),150),
                  extra_flag,
                  fill="#000000",anchor="mm",font=ImageFont.truetype(
                      "calibri.ttf",40))
    
    # Saves image
    rfs_map.save(f"{map_output_path}/{title}.png","PNG")
    
    return