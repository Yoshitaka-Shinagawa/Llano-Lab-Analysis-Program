# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:23:34 2022

potentially use hashmap to index per frame?? 

@author: Austin
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans 
from sklearn.preprocessing import StandardScaler


def k_clustering(df):
    
        
    
    
    # Declares start of cell graphing
    print("Starting Cell Classification with Machine Learning")
    
    
    #Creats instance of Standard Scaler
    # ss = StandardScaler()
    
    #Scales the dataframe
    # df_scaled = pd.Dataframe(ss.fit_transform(df), columns = df.columns)
    
    #Chooses the features to be used
    col_list = []
    for i in range(32):
        col_list.append(f'trial_{i}')
        
    trial_list = []
    for x in df['trial_average']:
        trial_list.append(x[0])
    # df[col_list] = pd.DataFrame(df.trial_average.tolist())
    # x = df['trial_average']
    
    df2 = pd.DataFrame(trial_list, columns = [col_list])
    print(df2)
    features = col_list
    x = df2[features]
    #Creates instance of kmeans
    kmeans = KMeans(n_clusters=5)
    
    #Fits the data
    kmeans.fit(x)
    
    
    #Creates labels for plotting
    df2['mean_flouresence'] = df2.mean(axis=1)
    df2['label'] = kmeans.labels_
    
    
    
    return df2

                
    
    
    