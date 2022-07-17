# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 13:53:06 2021

@author: Yoshi
"""

from PIL import Image,ImageDraw,ImageFont



from cell_drawer import *

def cell_number_mapper(info_storage):
    
    """
    This is the function used to generate the map showing which cell has which
    cell number. It draws each cell on the map with its number inside and is
    capable of using different colors for special cells (GABAergic in our
    case).
    
    Parameters
    ----------
    info_storage : The class used to store most of the variables that are used
        in the analysis program.
    
    Returns
    -------
    none
    
    """
    
    # Extracts variables from the info_storage class
    path           = info_storage.path
    canvas         = info_storage.canvas
    width          = info_storage.width
    height         = info_storage.height
    cell_locations = info_storage.cell_locations
    scale          = info_storage.scale
    radius         = info_storage.radius
    cell_flags     = info_storage.cell_flags
    extra_flag     = info_storage.extra_flag
    
    # Makes a copy of the canvas
    number_map = canvas.copy()
    
    # If there is only one ROI set, draws outline and text for cells in blue
    cell_total = len(cell_locations)
    if extra_flag == "N/A":
        for cell_number in range(cell_total):
            number_map = cell_drawer(number_map,cell_locations[cell_number],
                                     scale,radius,"hsv(180,100%,100%)",None,2)
            draw = ImageDraw.Draw(number_map)
            draw.text((cell_locations[cell_number][1][1]*scale,
                      cell_locations[cell_number][1][0]*scale+200),
                      str(cell_number+1),fill="hsv(180,100%,100%)",
                      anchor="mm",font=ImageFont.truetype("calibri.ttf",20))
    
    # If there are two ROI sets, draws outline and text for flagged cells
    if extra_flag != "N/A":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][0] != "N/A":
                number_map = cell_drawer(number_map,cell_locations[
                    cell_number],scale,radius,"hsv(30,100%,100%)",None,2)
                draw = ImageDraw.Draw(number_map)
                draw.text((cell_locations[cell_number][1][1]*scale,
                          cell_locations[cell_number][1][0]*scale+200),
                          str(cell_number+1),fill="hsv(30,100%,100%)",anchor=
                          "mm",font=ImageFont.truetype("calibri.ttf",20))
            if cell_flags[cell_number][0] == "N/A":
                number_map = cell_drawer(number_map,cell_locations[
                    cell_number],scale,radius,"hsv(180,100%,100%)",None,2)
                draw = ImageDraw.Draw(number_map)
                draw.text((cell_locations[cell_number][1][1]*scale,
                          cell_locations[cell_number][1][0]*scale+200),
                          str(cell_number+1),fill="hsv(180,100%,100%)",anchor=
                          "mm",font=ImageFont.truetype("calibri.ttf",20))
    
    # Preparation for drawing on image
    draw = ImageDraw.Draw(number_map)
    
    # Creates a title on the canvas
    draw.text((width*scale/2,50),"Cell Location and Number",fill="#000000",
              anchor="mm",font=ImageFont.truetype("calibri.ttf",80))
    
    # Creates a key on the canvas
    if extra_flag == "N/A":
        draw.rectangle([0,100,width*scale,200],outline="hsv(180,100%,100%)",
                       fill="hsv(180,100%,100%)")
        draw.text((width*scale/2,150),"Regular Cells",fill="#000000",
                  anchor="mm",font=ImageFont.truetype("calibri.ttf",40))
    if extra_flag != "N/A":
        draw.rectangle([0,100,width*scale,200],outline="hsv(30,100%,100%)",
                       fill="hsv(30,100%,100%)")
        draw.text((width*scale/2,150),extra_flag,fill="#000000",
                  anchor="mm",font=ImageFont.truetype("calibri.ttf",40))
    
    # Saves image
    number_map.save(f"{path}/Output/Tonotopy/Tonotopic Maps/Location Map.png")
    
    return