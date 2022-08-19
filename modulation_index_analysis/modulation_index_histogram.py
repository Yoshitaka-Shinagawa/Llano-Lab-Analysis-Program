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

def modulation_index_histogram(path,excel_writer,indices_set,
                               title,color_key,tonotopy_info):
    
    """
    This is the function used to create histograms for the modulation indices
    at each intensity level, as well as exporting the data to Excel and
    creating maps for the modulation indices. 
    
    
    
    
    """
    
    # Extracts variables from the info_storage class
    intensities    = tonotopy_info.intensities
    intensity_unit = tonotopy_info.intensity_unit
    
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
        plt.title(f"{title} at {intensity} {intensity_unit}\nMean: "+
                  f"{indices_mean}  Standard Deviation: "+
                  f"{indices_standard_deviation}")
        
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
        dataframe.to_excel(excel_writer,sheet_name=f"{intensity} "+
                           f"{intensity_unit}",index=False)
        
        # Create map for modulation indices
        modulation_index_mapper(map_output_path,cell_numbers_list,indices_data,
                                title,color_key,intensity,tonotopy_info)
    
    return