
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 21:14:11 2019

@author: Yoshi
"""

import numpy as np
from PIL import Image,ImageDraw,ImageFont



from cell_drawer import *
from arrow_coordinate_calculator import *

def cell_response_mapper(path,canvas,width,height,map_type,cell_locations,scale,radius,color_key,frequency_unit,cell_flags,extra_flag,mode="combined"):
    
    # Makes a copy of the canvas
    response_map = canvas.copy()
    
    # Goes through each cell and colors them in with the unresponsive color
    cell_total = len(cell_locations)
    if mode == "combined":
        for cell_number in range(cell_total):
            response_map = cell_drawer(response_map,cell_locations[cell_number],scale,radius,"#FF0000","#FF0000")
    elif mode == "flag":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][0] != "N/A":
                response_map = cell_drawer(response_map,cell_locations[cell_number],scale,radius,"#FF0000","#FF0000")
    elif mode == "no flag":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][0] == "N/A":
                response_map = cell_drawer(response_map,cell_locations[cell_number],scale,radius,"#FF0000","#FF0000")
    
    # Goes through each cell and colors them in based on frequency
    if mode == "combined":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][map_type] != "N/A":
                color = color_key[cell_flags[cell_number][map_type]]
                response_map = cell_drawer(response_map,cell_locations[cell_number],scale,radius,color,color)
    elif mode == "flag":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][map_type] != "N/A" and cell_flags[cell_number][0] != "N/A":
                color = color_key[cell_flags[cell_number][map_type]]
                response_map = cell_drawer(response_map,cell_locations[cell_number],scale,radius,color,color)
    elif mode == "no flag":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][map_type] != "N/A" and cell_flags[cell_number][0] == "N/A":
                color = color_key[cell_flags[cell_number][map_type]]
                response_map = cell_drawer(response_map,cell_locations[cell_number],scale,radius,color,color)
    
    # If in combined mode, creates an outline for cells with extra flag
    if mode == "combined":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][0] != "N/A":
                response_map = cell_drawer(response_map,cell_locations[cell_number],scale,radius,"hsv(30,100%,100%)",None)
    
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
    draw.text((width*scale/2,50),title,fill="#000000",
              anchor="mm",font=ImageFont.truetype("calibri.ttf",80))
    
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
        draw.rectangle([key_boundaries[i],100,key_boundaries[i+1],200],outline=color,fill=color)
        if map_type == 1 or map_type == 2:
            draw.text((np.mean([key_boundaries[i],key_boundaries[i+1]]),150),f"{key} {frequency_unit}",
                      fill="#000000",anchor="mm",font=ImageFont.truetype("calibri.ttf",40))
        elif map_type == 3:
            draw.text((np.mean([key_boundaries[i],key_boundaries[i+1]]),150),"Responsive",
                      fill="#000000",anchor="mm",font=ImageFont.truetype("calibri.ttf",40))   
        i += 1
    if mode == "combined" and extra_flag != "N/A":
        color = "hsv(30,100%,100%)"
        draw.rectangle([key_boundaries[-2],100,key_boundaries[-1],200],outline=color,fill=color)
        draw.text((np.mean([key_boundaries[-2],key_boundaries[-1]]),150),extra_flag,
                  fill="#000000",anchor="mm",font=ImageFont.truetype("calibri.ttf",40))
    
    # Saves image
    response_map.save(f"{path}/Output/Tonotopy/Tonotopic Maps/{title}.png","PNG")
    
    # Tonotopic arrow calculations
    if map_type == 1 or map_type == 2:
    
        # Calculates the best angle and max correlation coefficient for tonotopy
        max_corr,best_angle,arrow_coordinates = arrow_coordinate_calculator(path,cell_flags,cell_locations,map_type,mode,width,height,scale)
        
        # Checks if there is tonotopy
        if best_angle != "N/A":
            
            # Creates copy with extra space on bottom
            response_map_arrow = Image.new("RGBA",(width*scale,height*scale+250),(0,0,0,0))
            response_map_arrow.paste(response_map,(0,0))
            draw = ImageDraw.Draw(response_map_arrow)
            
            # Displays the max correlation coefficient and best angle at the bottom of the canvas
            draw.rectangle([0,height*scale+200,width*scale,height*scale+250],outline="#FFFFFF",fill="#FFFFFF")
            draw.text((0,height*scale+210),f"Tonotopic Angle: {best_angle}"+u"\u00b0"+", Correlation coefficient: %.2f"%max_corr,fill="#000000",font=ImageFont.truetype("calibri.ttf",40))
            
            # Draws arrow on the tonotopic map
            draw.line(arrow_coordinates,fill="#FFFFFF",width=int(round(scale/2)))
            
            # Adds circle at each point to make it look nice
            for point in arrow_coordinates:
                draw.ellipse((
                    point[0]-int(round(scale/4)),
                    point[1]-int(round(scale/4)),
                    point[0]+int(round(scale/4)),
                    point[1]+int(round(scale/4))),
                    fill="#FFFFFF")
            
            # Saves image
            response_map_arrow.save(f"{path}/Output/Tonotopy/Tonotopic Maps/{title} + Arrow.png","PNG")
    
    return