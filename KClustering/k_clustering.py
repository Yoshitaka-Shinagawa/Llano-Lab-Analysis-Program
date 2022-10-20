# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:23:34 2022

potentially use hashmap to index per frame?? 

@author: Austin
"""


import os
import shutil
import numpy as np
import pandas as pd
# import seaborn as sns 

# from sklearn.preprocessing import MinMaxScalar
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.model_selection import train_test_split 
# from sklearn.linear_model import LinearRegression as LR
# from sklearn.metrics import mean_absolute_error as mae 

def k_clustering(data,info_storage):
    
    # Extracts variables from the info_storage class
    # path                     = info_storage.path
    framerate_information      = info_storage.framerate_information
    df2                        = info_storage.df2
    correlation_coefficients   = info_storage.correlation_coefficients
    # key                      = info_storage.key
    # frequencies              = info_storage.frequencies
    # intensities              = info_storage.intensities
    threshold                  = info_storage.threshold

    
    #Drops the column we are trying to predict
    x = df.drop(['classification'], axis=1)
    y = data['classification']
    
    #Creates variables that are used to train the ML model
    # train_x,test_x,train_y,test_y = train_test_split(x,y, random_state = 56)
    
    # Declares start of cell graphing
    print("Starting Cell Classification with Machine Learning")
     
 
    return 

                
    
    
    