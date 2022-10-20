# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 11:29:32 2022

@author: Austin
"""
import os
import shutil
import numpy as np
import pandas as pd
import matplotlib as plt 
import seaborn as sns


def pair_plot(df2):
    
     # Extracts variables from the info_storage class
     # path                     = info_storage.path
     # framerate_information    = info_storage.framerate_information
     # key                      = info_storage.key
     # frequencies              = info_storage.frequencies
     # intensities              = info_storage.intensities
     # frequency_unit           = info_storage.frequency_unit
     # intensity_unit           = info_storage.intensity_unit
     # correlation_coefficients = info_storage.correlation_coefficients
     # threshold                = info_storage.threshold
     # df2                      = info_storage.df2 
     
     #Creates correlation matrix
     matrix = df2.corr().round(2)
     
     #Creates the pairplot and heatmap correlation matrix
     sns.heatmap(matrix, annot=True)
     sns.pairplot(matrix, kind = 'reg' )

     #Shows the heatmap and the pairplot 
     plt.show()
        
     return 