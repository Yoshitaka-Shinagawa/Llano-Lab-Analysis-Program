
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 21:14:11 2019

@author: Yoshi
"""

import numpy as np
from PIL import Image,ImageDraw,ImageFont



from cell_drawer import *
from arrow_coordinate_calculator import *

def cell_response_mapper(info_storage,color_key,map_type,mode="combined"):
    
    """
    This is the function used to generate the tonotopic maps. It draws the
    cells onto a map and colors them in with their best or characteristic
    frequency, then creates an outline to distinguish special cells
    (GABAergic in our case) from normal cells.
    
    Parameters
    ----------
    info_storage : The class used to store most of the variables that are used
        in the analysis program.
    color_key : The dictionary that has a shade of green for each frequency.
    map_type : The integer used to determine whether the best frequency,
        characteristic frequency, or noise will be plotted on the map. 1 is for
        best frequency, 2 is for characteristic frequency, and 3 is for noise.
    mode : The string is used to determine whether one or both types of cells
        will be plotted on the same map, if there are two types of cells
        present. "combined" is for combined maps, "flags" is for special flags
        (GABAergic for us) only, and "no flag" is for normal cells only.
    
    Returns
    -------
    none
    """
    
    # Extracts variables from the info_storage class
    path           = info_storage.path
    canvas         = info_storage.canvas
    width          = info_storage.width
    height         = info_storage.height
    scale          = info_storage.scale
    radius         = info_storage.radius
    cell_locations = info_storage.cell_locations
    cell_flags     = info_storage.cell_flags
    extra_flag     = info_storage.extra_flag
    frequency_unit = info_storage.frequency_unit
    
    # Makes a copy of the canvas
    response_map = canvas.copy()
    
    # Goes through each cell and colors them in with the unresponsive color
    cell_total = len(cell_locations)
    if mode == "combined":
        for cell_number in range(cell_total):
            response_map = cell_drawer(response_map,cell_locations[
                                       cell_number],scale,radius,
                                       "#FF0000","#FF0000")
    elif mode == "flag":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][0] != "N/A":
                response_map = cell_drawer(response_map,cell_locations[
                                           cell_number],scale,radius,
                                           "#FF0000","#FF0000")
    elif mode == "no flag":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][0] == "N/A":
                response_map = cell_drawer(response_map,cell_locations[
                                           cell_number],scale,radius,
                                           "#FF0000","#FF0000")
    
    # Goes through each cell and colors them in based on frequency
    if mode == "combined":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][map_type] != "N/A":
                color = color_key[cell_flags[cell_number][map_type]]
                response_map = cell_drawer(response_map,cell_locations[
                                           cell_number],scale,radius,
                                           color,color)
    elif mode == "flag":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][map_type] != "N/A" and \
                cell_flags[cell_number][0] != "N/A":
                color = color_key[cell_flags[cell_number][map_type]]
                response_map = cell_drawer(response_map,cell_locations[
                                           cell_number],scale,radius,
                                           color,color)
    elif mode == "no flag":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][map_type] != "N/A" and \
                cell_flags[cell_number][0] == "N/A":
                color = color_key[cell_flags[cell_number][map_type]]
                response_map = cell_drawer(response_map,cell_locations[
                                           cell_number],scale,radius,
                                           color,color)
    
    # If in combined mode, creates an outline for cells with extra flag
    if mode == "combined":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][0] != "N/A":
                response_map = cell_drawer(response_map,cell_locations[
                                           cell_number],scale,radius,
                                           "hsv(30,100%,100%)",None)
    
    # Preparation for drawing on image
    draw = ImageDraw.Draw(response_map)
    
    # Finds name of map type
    if map_type == 1:
        map_type_name = "Best Frequency"
    elif map_type == 2:
        map_type_name = "Characteristic Frequency"
    elif map_type == 3:
        map_type_name = "Noise Response"
    
    # Creates title based on mode and map type
    if mode == "combined":
        title = f"{map_type_name} of Cells"
    elif mode == "flag":
        title = f"{map_type_name} of {extra_flag} Cells"
    elif mode == "no flag":
        title = f"{map_type_name} of non-{extra_flag} Cells"
    else:
        title = "Error: Unrecognized Mode"
    
    # Creates a title on the canvas
    draw.rectangle([0,0,width*scale,200],outline="#FFFFFF",fill="#FFFFFF")
    try:
        font = ImageFont.truetype("calibri.ttf",80)
    except OSError:
        font = ImageFont.load_default()
    draw.text((width*scale/2,50),title,fill="#000000",
              anchor="mm",font=font)
    
    # Determines y coordinates for key boxes
    key_boundaries = []
    if mode == "combined" and extra_flag != "N/A":
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
        if map_type == 1 or map_type == 2:
            try:
                font = ImageFont.truetype("calibri.ttf",40)
            except OSError:
                font = ImageFont.load_default()
            draw.text((np.mean([key_boundaries[i],key_boundaries[i+1]]),150),
                      f"{key} {frequency_unit}",fill="#000000",anchor="mm",
                      font=font)
        elif map_type == 3:
            try:
                font = ImageFont.truetype("calibri.ttf",40)
            except OSError:
                font = ImageFont.load_default()
            draw.text((np.mean([key_boundaries[i],key_boundaries[i+1]]),150),
                      "Responsive",fill="#000000",anchor="mm",font=font)   
        i += 1
    if mode == "combined" and extra_flag != "N/A":
        color = "hsv(30,100%,100%)"
        draw.rectangle([key_boundaries[-2],100,key_boundaries[-1],200],
                       outline=color,fill=color)
        try:
            font = ImageFont.truetype("calibri.ttf",40)
        except OSError:
            font = ImageFont.load_default()
        draw.text((np.mean([key_boundaries[-2],key_boundaries[-1]]),150),
                  extra_flag,fill="#000000",anchor="mm",font=font)
    
    # Saves image
    response_map.save(f"{path}/Output/Tonotopy/Tonotopic Maps/{title}.png")
    
    # Tonotopic arrow calculations
    if map_type == 1 or map_type == 2:
    
        # Calculates best angle and max correlation coefficient for tonotopy
        max_corr,best_angle,arrow_coordinates = arrow_coordinate_calculator(
            info_storage,map_type,mode)
        
        # Checks if there is tonotopy
        if best_angle != "N/A":
            
            # Creates copy with extra space on bottom
            response_map_arrow = Image.new("RGBA",(width*scale,height*scale
                                                   +250),(0,0,0,0))
            response_map_arrow.paste(response_map,(0,0))
            draw = ImageDraw.Draw(response_map_arrow)
            
            # Displays the max correlation coefficient and best angle at the
            # bottom of the canvas
            draw.rectangle([0,height*scale+200,width*scale,height*scale+250],
                           outline="#FFFFFF",fill="#FFFFFF")
            try:
                font = ImageFont.truetype("calibri.ttf",40)
            except OSError:
                font = ImageFont.load_default()
            draw.text((0,height*scale+210),f"Tonotopic Angle: {best_angle}"+
                      u"\u00b0"+", Correlation coefficient: %.2f"%max_corr,
                      fill="#000000",font=font)
            
            # Draws arrow on the tonotopic map
            draw.line(arrow_coordinates,fill="#FFFFFF",
                      width=int(round(scale/2)))
            
            # Adds circle at each point to make it look nice
            for point in arrow_coordinates:
                draw.ellipse((
                    point[0]-int(round(scale/4)),
                    point[1]-int(round(scale/4)),
                    point[0]+int(round(scale/4)),
                    point[1]+int(round(scale/4))),
                    fill="#FFFFFF")
            
            # Saves image
            response_map_arrow.save(f"{path}/Output/Tonotopy/Tonotopic Maps/"+
                                    f"{title} + Arrow.png","PNG")
    
    return