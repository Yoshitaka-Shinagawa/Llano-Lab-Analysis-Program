# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 11:31:12 2022

@author: Austin
"""

import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns


def test_pair_plot():
    
    #Opens the CSV file
    df2 = pd.read_csv('E:/Llano Lab/Pair Plot/cannon_waves.csv')
  
    #Creates correlation matrix
    matrix = df2.corr().round(2)
    
    #Creates the pairplot and heatmap correlation matrix
    sns.heatmap(matrix, annot=True)
    sns.pairplot(matrix, kind = 'reg' )

    #Shows the heatmap and the pairplot 
    plt.show()
        
    return

#Runs the code
test_pair_plot()
