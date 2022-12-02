# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 07:29:04 2022

@author: Austin
"""

import os
import shutil 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from string import digits

# Sets a base path and creates paths to each data type excel sheet
base_path = "E:/Llano Lab/SomatoSensory/2022-11-23/101422_RCAMPxgad67_070422_SOMATO_side/Somato_HP/D1/For analysis"
over_path ='f{base_path}/OVER1/Output/Cell Traces/Spreadsheets/Data_by_Trial.xlsx'
so_path ='f{base_path}/SO1/Output/Cell Traces/Spreadsheets/Data_by_Trial.xlsx'
som_path ='f{base_path}/SOM1/Output/Cell Traces/Spreadsheets/Data_by_Trial.xlsx'


def adaptive_response_mapper(over,so,som):
    
    '''
        This function is used for visualizing the adaptive cells based on 
        responsiveness
        
    '''
    # Opens the existing excel sheets
    over_df = pd.read_excel(over)
    so_df = pd.read_excel(so)
    som_df = pd.read_excel(som)
    
    # Slices the dataframes
    over_df = over_df[:,:3]
    so_df = so_df[:,:3]
    som_df = som_df[:,:3]
    
    
    # Shows the plot
    plt.show()
   
    # Saves the figure 
    # plt.savefig(base_path)
    
  
    

    
    
    
    return 