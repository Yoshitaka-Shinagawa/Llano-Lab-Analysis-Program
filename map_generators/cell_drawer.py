# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 18:41:03 2019

@author: Yoshi
"""

from PIL import ImageDraw



def cell_drawer(canvas,cell_location,scale,radius,outline,fill,width=5):
    
    """
    This is the function used to draw cells on the map. It takes the coordinate
    information of the cell, scales it up, and draws it on the map.
    
    Parameters
    ----------
    canvas : The map that the cells are drawn on. It is a PIL image that is 
    cell_location : The list containing the shape, location, and size 
        information of the cell being drawn.
    scale : The scale used to increase the size of the cell to fit the map.
    radius : The average radius that oval cells will be drawn at.
    outline : The color of the outline of the cell.
    fill : The color of the fill of the cell.
    width : The width of the outline of the cell.
    
    Returns
    -------
    canvas : The original input map with the cell drawn in.
    """
    
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
        draw.rectangle([left,top,right,bottom],outline=outline,
                       fill=fill,width=width)
    
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
        draw.ellipse([left,top,right,bottom],outline=outline,
                     fill=fill,width=width)
    
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