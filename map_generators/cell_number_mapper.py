# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 13:53:06 2021

@author: Yoshi
"""

from PIL import Image,ImageDraw,ImageFont



from cell_drawer import *

def cell_number_mapper(path,canvas,width,height,cell_locations,scale,radius,cell_flags,extra_flag):
    
    # Makes a copy of the canvas
    number_map = canvas.copy()
    
    # If there is only one ROI set, draws outline and text for all cells in blue
    cell_total = len(cell_locations)
    if extra_flag == "N/A":
        for cell_number in range(cell_total):
            number_map = cell_drawer(number_map,cell_locations[cell_number],scale,radius,"hsv(180,100%,100%)",None,2)
            draw = ImageDraw.Draw(number_map)
            draw.text((cell_locations[cell_number][1][1]*scale,
                      cell_locations[cell_number][1][0]*scale+200),
                      str(cell_number+1),fill="hsv(180,100%,100%)",
                      anchor="mm",font=ImageFont.truetype("calibri.ttf",20))
    
    # If there are two ROI sets, draws outline and text for flagged cells separately
    if extra_flag != "N/A":
        for cell_number in range(cell_total):
            if cell_flags[cell_number][0] != "N/A":
                number_map = cell_drawer(number_map,cell_locations[cell_number],scale,radius,"hsv(30,100%,100%)",None,2)
                draw = ImageDraw.Draw(number_map)
                draw.text((cell_locations[cell_number][1][1]*scale,
                          cell_locations[cell_number][1][0]*scale+200),
                          str(cell_number+1),fill="hsv(30,100%,100%)",
                          anchor="mm",font=ImageFont.truetype("calibri.ttf",20))
            if cell_flags[cell_number][0] == "N/A":
                number_map = cell_drawer(number_map,cell_locations[cell_number],scale,radius,"hsv(180,100%,100%)",None,2)
                draw = ImageDraw.Draw(number_map)
                draw.text((cell_locations[cell_number][1][1]*scale,
                          cell_locations[cell_number][1][0]*scale+200),
                          str(cell_number+1),fill="hsv(180,100%,100%)",
                          anchor="mm",font=ImageFont.truetype("calibri.ttf",20))
    
    # Preparation for drawing on image
    draw = ImageDraw.Draw(number_map)
    
    # Creates a title on the canvas
    draw.text((width*scale/2,50),"Cell Location and Number",fill="#000000",
              anchor="mm",font=ImageFont.truetype("calibri.ttf",80))
    
    # Creates a key on the canvas
    if extra_flag == "N/A":
        draw.rectangle([0,100,width*scale,200],outline="hsv(180,100%,100%)",fill="hsv(180,100%,100%)")
        draw.text((width*scale/2,150),"Regular Cells",fill="#000000",
                  anchor="mm",font=ImageFont.truetype("calibri.ttf",40))
    if extra_flag != "N/A":
        draw.rectangle([0,100,width*scale,200],outline="hsv(30,100%,100%)",fill="hsv(30,100%,100%)")
        draw.text((width*scale/2,150),extra_flag,fill="#000000",
                  anchor="mm",font=ImageFont.truetype("calibri.ttf",40))
    
    # Saves image
    number_map.save(f"{path}/Output/Tonotopy/Tonotopic Maps/Location Map.png","PNG")
    
    return