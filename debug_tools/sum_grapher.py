# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 21:12:47 2019

@author: Yoshi
"""

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt



def sum_grapher(path,data,framerate,key,frequencies,decibels):
    
    # Creates and changes to output directory
    graph_output_path = path + "/Output/Debug/Summed Graph"
    if os.path.exists(graph_output_path) == True:
        shutil.rmtree(graph_output_path)
    if os.path.exists(graph_output_path) == False:
        os.mkdir(graph_output_path)
    os.chdir(graph_output_path)
    
    # Constants for loops
    cell_total = data.shape[0]
    sample_length = data.shape[2]
    
    # Calculates x-axis labels
    times = []
    for frame in range(sample_length):
        step = 1 / framerate
        times.append(step*frame)
    
    # Creates empty subplots for each set of data
    figure,axes = plt.subplots(len(decibels),len(frequencies),sharex=True,sharey=True,gridspec_kw={"hspace": 0,"wspace":0},figsize=(20,15))
    
    # Goes through each frequency and decibel
    for column_number,frequency in enumerate(frequencies):
        for row_number,decibel in enumerate(reversed(decibels)):
            
            # Obtains sample number from key
            sample_number = key[frequency][decibel]
            
            # Sums up all of the values in each set of data
            sample_sum = np.zeros(sample_length,dtype=np.float32)
            for cell_number in range(cell_total):
                cell_data = data[sample_number,cell_number,:]
                sample_sum += cell_data
            
            # Plots it in the subplot
            axes[row_number,column_number].plot(times,sample_sum)
            
            # Axes labels
            if row_number == 0:
                axes[row_number,column_number].set_title(frequency+" kHz",fontsize=16)
            if frequency == frequencies[-1]:
                decibel_axis = axes[row_number,column_number].twinx()
                decibel_axis.set_ylabel(decibel+" dB",fontsize=16)
                decibel_axis.set_yticklabels([])
                decibel_axis.tick_params(axis="both",which="both",length=0)
            if column_number == 0:
                axes[row_number,column_number].set_ylabel("Raw pixel values (No units)",fontsize=12)
            if row_number == 0:
                axes[row_number,column_number].set_xlabel("Time (s)")
    
    # Creates title for graph
    figure.suptitle("Summed Data",fontsize=16)
    
    # Saves the figure
    plt.savefig("Summed Data")
    plt.close()
    
    return