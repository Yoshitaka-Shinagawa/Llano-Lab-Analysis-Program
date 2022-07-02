# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 16:58:13 2021

@author: Yoshi
"""

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
from PIL import ImageColor



def correlation_matrix(path,data,cell_flags,framerate_information,extra_flag,mode=0):
    
    # Creates output directory
    matrix_output_path = path + "/Output/Correlation Matrix"
    if os.path.exists(matrix_output_path) == True:
        shutil.rmtree(matrix_output_path)
    if os.path.exists(matrix_output_path) == False:
        os.mkdir(matrix_output_path)
    
    # Only creates matrix if analyzing noise data
    if mode == 1:
        
        # Declares start of creation of correlation matrix
        print("Creating correlation matrix")
        
        # Disable Spyder plot window
        plt.ioff()
        
        # Calculates x-axis labels
        cycle_frames = framerate_information[1]
        cycle_duration = framerate_information[2]*1000
        times = []
        step = cycle_duration / cycle_frames
        for frame in range(cycle_frames):
            times.append(step*frame)
        
        # Makes list of cells
        cell_total = data.shape[0]
        regular_cells = []
        for cell_number in range(cell_total):
            if cell_flags[cell_number][0] == "N/A" and cell_flags[cell_number][3] != "N/A":
                regular_cells.append(cell_number)
        flagged_cells = []
        for cell_number in range(cell_total):
            if cell_flags[cell_number][0] != "N/A" and cell_flags[cell_number][3] != "N/A":
                flagged_cells.append(cell_number)
        combined_cells = []
        for cell_number in range(cell_total):
            if extra_flag != "N/A" and cell_flags[cell_number][3] != "N/A":
                combined_cells.append(cell_number)
        
        # Creates empty array to store cell averages in
        trial_length = data.shape[3]
        cell_averages = np.zeros((cell_total,trial_length),dtype=np.float32)
        
        # Goes through each cell list
        for list_number in range(3):
            cell_list = [regular_cells,flagged_cells,combined_cells][list_number]
            cell_list_total = len(cell_list)
            
            # Calculates cell averages for each responsive cell
            if cell_list_total != 0 and list_number != 2:
                for cell_number in cell_list:
                    cell_averages[cell_number] = np.mean(data[cell_number,0],axis=0)
            
            # Makes sure cell list is not empty
            if cell_list_total != 0:
            
                # Creates empty subplots for the detailed correlation matrix
                figure,axes = plt.subplots(cell_list_total,cell_list_total,
                                           sharex=True,sharey=True,squeeze=False,
                                           gridspec_kw={"hspace":0,"wspace":0},
                                           figsize=(cell_list_total*2,cell_list_total*2))
                
                # Goes through each row
                for cell_number_1 in range(cell_list_total):
                    
                    # Reads the average trace for cell 1
                    sample_average_1 = cell_averages[cell_list[cell_number_1]]
                    
                    # Determines the name of the cell to use
                    cell_name_1 = "Cell "+str(cell_list[cell_number_1]+1)
                    
                    # Goes through each column
                    for cell_number_2 in range(cell_list_total):
                    
                        # Reads the average trace for cell 2
                        sample_average_2 = cell_averages[cell_list[cell_number_2]]
                        
                        # Determines the name of the cell to use
                        cell_name_2 = "Cell "+str(cell_list[cell_number_2]+1)
                        
                        # Plots averages of trials onto each square
                        axes[cell_number_1,cell_number_2].plot(times,sample_average_1,color="#000000",linestyle="solid")
                        axes[cell_number_1,cell_number_2].plot(times,sample_average_2,color="#000000",linestyle="solid")
                        
                        # Calculates correlation coefficient between each cell average
                        correlation_coefficient,p = stats.pearsonr(sample_average_1,sample_average_2)
                        if math.isnan(correlation_coefficient):
                            correlation_coefficient = 0
                        axes[cell_number_1,cell_number_2].legend(["r = %.2f"%correlation_coefficient],loc="upper right")
                        
                        # Colors in the background based on the correlation coefficient
                        if correlation_coefficient > 0.50:
                            hue = 120
                            saturation= int(25+(correlation_coefficient-0.75)*100)
                            value = 80
                            hsv = f"hsv({hue},{saturation}%,{value}%)"
                            rgb = "#%02x%02x%02x" % ImageColor.getrgb(hsv)
                            axes[cell_number_1,cell_number_2].set_facecolor(rgb)
                        
                        # Axes labels
                        if cell_number_1 == 0:
                            axes[cell_number_1,cell_number_2].set_title(cell_name_2,fontsize=16)
                        if cell_number_2 == 0:
                            axes[cell_number_1,cell_number_2].set_ylabel(cell_name_1,fontsize=16)
                
                # Creates title for correlation matrix
                if list_number == 0:
                    figure.suptitle("Correlation Matrix for Regular Cells",fontsize=16)
                if list_number == 1:
                    figure.suptitle(f"Correlation Matrix for {extra_flag} Cells",fontsize=16)
                if list_number == 2:
                    figure.suptitle(f"Correlation Matrix for All Cells",fontsize=16)
                
                # Saves the figure
                if list_number == 0:
                    plt.savefig(f"{matrix_output_path}/Correlation Matrix for Regular Cells")
                if list_number == 1:
                    plt.savefig(f"{matrix_output_path}/Correlation Matrix for {extra_flag} Cells")
                if list_number == 2:
                    plt.savefig(f"{matrix_output_path}/Correlation Matrix for All Cells")
                plt.close()
                plt.clf()
        
        # Declares end of cell graphing
        print("Finished correlation matrix")
    
    return