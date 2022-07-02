# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 00:54:15 2021

@author: Yoshi
"""

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



from modulation_index_mapper import *

def modulation_index_histogram(path,excel_writer,indices_set,intensities,intensity_unit,title,canvas,width,height,cell_locations,scale,radius,color_key,cell_flags,extra_flag):
    
    # Creates output directory for histogram
    histogram_output_path = f"{path}/Histograms"
    if os.path.exists(histogram_output_path) == False:
        os.mkdir(histogram_output_path)
    
    # Creates output directory for map
    map_output_path = f"{path}/Maps"
    if os.path.exists(map_output_path) == False:
        os.mkdir(map_output_path)
    
    # Disable Spyder plot window
    plt.ioff()
    
    # Creates bins so that all graphs are easy to look at.
    x_bins = []
    for i in range(-12,13):
        x_bins.append(i*0.1)
    
    # Goes through each intensity
    for intensity in intensities:
        
        # Creates a histogram
        indices_data = indices_set[intensities.index(intensity)][2]
        plt.hist(indices_data,bins=x_bins)
        indices_mean = round(np.average(indices_data,axis=0),2)
        indices_standard_deviation = round(np.std(indices_data),2)
        
        # Creates a title
        plt.title(f"{title} at {intensity} {intensity_unit}\nMean: {indices_mean}  Standard Deviation: {indices_standard_deviation}")
        
        # Saves the figure and closes it
        plt.savefig(f"{histogram_output_path}/{intensity} {intensity_unit}")
        plt.close()
        plt.clf()
        
        # Exports data to excel
        cell_numbers_list = indices_set[intensities.index(intensity)][0]
        cell_flags_list = indices_set[intensities.index(intensity)][1]
        dataframe = {"Cell Number":cell_numbers_list,
                     "Cell Flag":cell_flags_list,
                     title:indices_data}
        dataframe = pd.DataFrame(dataframe)
        dataframe.to_excel(excel_writer,sheet_name=f"{intensity} {intensity_unit}",index=False)
        
        # Create map for 
        modulation_index_mapper(map_output_path,canvas,width,height,cell_locations,scale,radius,color_key,cell_flags,extra_flag,cell_numbers_list,indices_data,title,intensity,intensity_unit)
    
    return