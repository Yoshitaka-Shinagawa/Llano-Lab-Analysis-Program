# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 18:41:03 2019

@author: Yoshi
"""

from PIL import ImageDraw



def cell_drawer(canvas,cell_location,scale,radius,outline,fill,width=5):
    
    # Prepares for drawing on image
    draw = ImageDraw.Draw(canvas)
    
    # Rectangle ROIs
    if cell_location[0] == "rectangle":
        
        # Retrieves coordinates of cell
        top = cell_location[2][0]*scale + 200
        left = cell_location[2][1]*scale
        bottom = cell_location[2][2]*scale + 200
        right = cell_location[2][3]*scale
        
        # Draws rectangle based on coordinates
        draw.rectangle([left,top,right,bottom],outline=outline,fill=fill,width=width)
    
    # Oval ROIs
    if cell_location[0] == "oval":
    
        # Retrieves coordinates of cell
        y_center = cell_location[1][0]
        x_center = cell_location[1][1]
        
        # Creates coordinates for circle
        left = round((x_center-radius)*scale)
        right = round((x_center+radius)*scale)
        top = round((y_center-radius)*scale) + 200
        bottom = round((y_center+radius)*scale) + 200
        
        # Draws circle based on coordinates
        draw.ellipse([left,top,right,bottom],outline=outline,fill=fill,width=width)
    
    # Polygonal ROIs
    if cell_location[0] == "polygon":
        
        # Retrieves coordinates of cell
        y_list = cell_location[2]
        x_list = cell_location[3]
        
        # Converts to list of coordinate tuples
        coord_list = []
        list_len = len(y_list)
        for n in range(list_len):
            coord_list.append((x_list[n]*scale,y_list[n]*scale+200))
        
        # Draws polygon based on coordinates
        draw.polygon(coord_list,outline=outline,fill=fill)
    
    return canvas