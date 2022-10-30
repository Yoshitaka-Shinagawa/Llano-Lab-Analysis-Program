# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 21:11:16 2022

@author: Austin
"""

import os 
import shutil 

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def labeled_waveform_graphs(df,df2):
    
    
    #Sets the path value
    path = 'E:/Llano Lab/Sex Difference/2022-08-24/RCAMP CBA 032722 F (+287,-006,-094)/Tonotopy'
    
    # Creates output directories
    cell_trace_output_path = f"{path}/Output/Cell Traces"
    if os.path.exists(f"{path}/Output/Graphs") == True:
        shutil.rmtree(f"{path}/Output/Graphs")
    if os.path.exists(cell_trace_output_path) == True:
        shutil.rmtree(cell_trace_output_path)
    if os.path.exists(cell_trace_output_path) == False:
        os.mkdir(cell_trace_output_path)
        os.mkdir(f"{cell_trace_output_path}/Spreadsheets")
        os.mkdir(f"{cell_trace_output_path}/Graphs")
    
    # Calculates x-axis labels
    cycle_frames = 32
    cycle_duration = 1100
    times = []
    step = cycle_duration / cycle_frames
    for frame in range(cycle_frames):
        times.append(step*frame)
    # Creates empty subplots for each set of data
    fig,ax = plt.subplots(5,figsize=(4,8))   
    
    #Groups the data
    # labels_sorted = df['label']
    
    #Sets title for entire graph
    fig.suptitle('Change in Fluorescence Across 1100ms for Each Cell \n Grouped by Machine Learning Classification')
    
    
    sns.set_theme()
    #adds a column to df
    # df['trial_average'] = df2['trial_average']
    
    # print(df)
    
    #Creates empty list
    
    col_names = []
    for i in range(32):
        col_names.append(f'trial_{i}')
    col_names.append('mean_flouresence')
    col_names.append('label')
    col_names.append('combined')
    col_names.append('trial_average')
    df.columns = col_names
    temp_list = []
    for i in range(df['label'].max() + 1):
        temp = df[df['label'] == i].reset_index(drop=True)
        for x in range(temp.shape[0]):
            for t in temp['trial_average'][x][0]:
                temp_list.append(t)
                ax[i].tick_params(
                    axis='x',          
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    labelbottom=False) # labels along the bottom edge are off
                ax[i].set_ylabel("dF/F")
            ax[i].plot(times, temp_list, label = f'line{x}')
            temp_list = []
        ax[i].title.set_text(f'label {i}')
            
          
    
    
#        for i in range(df.shape[0]):
#            axes[1,g].plot(times,g['trial_average'][i])
                
                
    #Shows the Graph
    plt.show()
    
    return
                
            
            
            #Goes through each cell
#            for cell in range(df_by_label[i]):  
                
                #Creates empty subplots for each set of data
#                fig,axes = plt.subplots(sharex=True,sharey=True,squeeze=False, 
#                                        gridspec_kw={"hspace":0,"wspace":0}, figsize=graph_size)  
                
                   
                
                   
                    
                    
                   
            

    
    
