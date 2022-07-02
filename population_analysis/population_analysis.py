# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 14:10:45 2021

@author: Yoshi
"""

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import integrate
from PIL import ImageColor



def population_analysis(path,data,cell_flags,framerate_information,key,frequencies,frequency_unit,intensities,intensity_unit,extra_flag,mode=0):
    
    # Declares start of population analysis
    print("Starting population analysis")
    
    # Creates output directory
    population_analysis_output_path = path + "/Output/Population Analysis"
    if os.path.exists(population_analysis_output_path) == True:
        shutil.rmtree(population_analysis_output_path)
    if os.path.exists(population_analysis_output_path) == False:
        os.mkdir(population_analysis_output_path)
        os.mkdir(f"{population_analysis_output_path}/Spreadsheets")
        os.mkdir(f"{population_analysis_output_path}/Graphs")
    
    # Excel spreadsheet writers
    regular_writer = pd.ExcelWriter(f"{population_analysis_output_path}/Spreadsheets/Regular cells.xlsx")
    if extra_flag != "N/A":
        flagged_writer = pd.ExcelWriter(f"{population_analysis_output_path}/Spreadsheets/Flagged Cells.xlsx")
        difference_writer = pd.ExcelWriter(f"{population_analysis_output_path}/Spreadsheets/Difference.xlsx")
    
    # Reverse intensity list
    intensities_reversed = intensities.copy()
    intensities_reversed.reverse()
    
    # Disable Spyder plot window
    plt.ioff()
    
    # Calculates x-axis labels
    cycle_frames = framerate_information[1]
    cycle_duration = framerate_information[2]*1000
    times = []
    step = cycle_duration / cycle_frames
    for frame in range(cycle_frames):
        times.append(step*frame)
    
    # Calculates x interval in seconds
    x_interval = cycle_duration / cycle_frames
    
    # Constants for loops
    cell_total = data.shape[0]
    sample_total = data.shape[1]
    trial_length = data.shape[3]
    intensities_total = len(intensities)
    frequencies_total = len(frequencies)
    
    # Goes through cell flags to segragate cells
    regular_cells = []
    flagged_cells = []
    for cell_number in range(cell_total):
        responsive = False
        if mode == 0:
            if cell_flags[cell_number][1] != "N/A" or cell_flags[cell_number][2] != "N/A":
                responsive = True
        if mode == 1:
            if cell_flags[cell_number][3] != "N/A":
                responsive = True
        if responsive == True:
            if cell_flags[cell_number][0] == "N/A":
                regular_cells.append(cell_number)
            if cell_flags[cell_number][0] != "N/A":
                flagged_cells.append(cell_number)
    
    # Goes through each cell population and averages responses
    sample_total = data.shape[1]
    trial_length = data.shape[3]
    population_averages = np.zeros((2,sample_total,1,trial_length),dtype=np.float32)
    cell_lists = [regular_cells,flagged_cells]
    for list_number in range(2):
        for cell_number in cell_lists[list_number]:
            for sample_number in range(sample_total):
                population_averages[list_number,sample_number,0] += np.mean(data[cell_number,sample_number],axis=0)
        if len(cell_lists[list_number]) != 0:
             population_averages[list_number] = population_averages[list_number] / len(cell_lists[list_number])
    
    # Determines size of graph based on number of frequencies and intensities
    if mode == 0:
        graph_size = (frequencies_total*2,intensities_total*3)
    elif mode == 1:
        graph_size = (10,8)
    
    # Creates empty subplots for each set of data
    figure,axes = plt.subplots(intensities_total,frequencies_total,
                               sharex=True,sharey=True,squeeze=False,
                               gridspec_kw={"hspace":0,"wspace":0},figsize=graph_size)
    
    # Calculates rgb values for blue and orange
    hue,saturation,value = 210,50,100
    hsv = f"hsv({hue},{saturation}%,{value}%)"
    blue_rgb = "#%02x%02x%02x" % ImageColor.getrgb(hsv)
    hue,saturation,value = 30,50,100
    hsv = f"hsv({hue},{saturation}%,{value}%)"
    orange_rgb = "#%02x%02x%02x" % ImageColor.getrgb(hsv)
    
    # Empty dictionary for aoc dataframe
    regular_aoc_dataframe = {}
    flagged_aoc_dataframe = {}
    difference_aoc_dataframe = {}
    
    # Empty dictionary for peak dataframe
    regular_peak_dataframe = {}
    flagged_peak_dataframe = {}
    difference_peak_dataframe = {}
    
    # Goes through each frequency
    for column_number,frequency in enumerate(frequencies):
        
        # Empty lists to store aocs into
        regular_frequency_aocs = []
        flagged_frequency_aocs = []
        difference_frequency_aocs = []
        
        # Empty lists to store peak values into
        regular_frequency_peaks = []
        flagged_frequency_peaks = []
        difference_frequency_peaks = []
        
        # Goes through each intensity
        for row_number,intensity in enumerate(reversed(intensities)):
        
            # Obtains sample number from key
            sample_number = key[frequency][intensity]
            
            # Plots avearge of cell population
            regular_cell_average = population_averages[0,sample_number,0]
            axes[row_number,column_number].plot(times,regular_cell_average,color=blue_rgb,linestyle="solid")
            if extra_flag != "N/A":
                flagged_cell_average = population_averages[1,sample_number,0]
                axes[row_number,column_number].plot(times,flagged_cell_average,color=orange_rgb,linestyle="solid")
                difference_cell_average = regular_cell_average - flagged_cell_average
                axes[row_number,column_number].plot(times,difference_cell_average,color="#000000",linestyle="solid")
            
            # Adds areas under curve to list
            regular_area = integrate.simpson(regular_cell_average,dx=x_interval)
            regular_frequency_aocs.append(round(regular_area,2))
            if extra_flag != "N/A":
                flagged_area = integrate.simpson(flagged_cell_average,dx=x_interval)
                flagged_frequency_aocs.append(round(flagged_area,2))
                difference_area = integrate.simpson(difference_cell_average,dx=x_interval)
                difference_frequency_aocs.append(round(difference_area,2))
            
            # Adds peak values to list
            regular_frequency_peaks.append(round(max(regular_cell_average),2))
            if extra_flag != "N/A":
                flagged_frequency_peaks.append(round(max(flagged_cell_average),2))
                difference_frequency_peaks.append(round(max(difference_cell_average),2))
            
            # Adds legend to upper right corner
            if extra_flag != "N/A" and column_number == frequencies_total-1 and row_number == 0:
                axes[row_number,column_number].legend(["Regular",f"{extra_flag}"],loc="upper right")
            
            # Axes labels
            if mode == 0:
                if row_number == 0:
                    axes[row_number,column_number].set_title(f"{frequency} {frequency_unit}",fontsize=16)
                if frequency == frequencies[-1]:
                    intensity_axis = axes[row_number,column_number].twinx()
                    intensity_axis.set_ylabel(f"{intensity} {intensity_unit}",fontsize=16)
                    intensity_axis.set_yticklabels([])
                    intensity_axis.tick_params(axis="both",which="both",length=0)
            if column_number == 0:
                axes[row_number,column_number].set_ylabel("dF/F (%)",fontsize=12)
            if row_number == intensities_total-1:
                axes[row_number,column_number].set_xlabel("Time (ms)")
    
        # Adds aoc list to dataframe
        regular_aoc_dataframe[frequency] = regular_frequency_aocs
        if extra_flag != "N/A":
            flagged_aoc_dataframe[frequency] = flagged_frequency_aocs
            difference_aoc_dataframe[frequency] = difference_frequency_aocs
        
        # Adds peak list to dataframe
        regular_peak_dataframe[frequency] = regular_frequency_peaks
        if extra_flag != "N/A":
            flagged_peak_dataframe[frequency] = flagged_frequency_peaks
            difference_peak_dataframe[frequency] = difference_frequency_peaks
    
    # Creates title for tonotopic graph
    figure.suptitle("Population analysis",fontsize=16)
    
    # Saves the figure
    plt.savefig(f"{population_analysis_output_path}/Graphs/Population Analysis")
    plt.close()
    plt.clf()
    
    # Exports aoc dataframe to excel spreadsheet
    regular_aoc_dataframe = pd.DataFrame(regular_aoc_dataframe,index=intensities_reversed)
    regular_aoc_dataframe.to_excel(regular_writer,sheet_name="Area under curve")
    if extra_flag != "N/A":
        flagged_aoc_dataframe = pd.DataFrame(flagged_aoc_dataframe,index=intensities_reversed)
        flagged_aoc_dataframe.to_excel(flagged_writer,sheet_name="Area under curve")
        difference_aoc_dataframe = pd.DataFrame(difference_aoc_dataframe,index=intensities_reversed)
        difference_aoc_dataframe.to_excel(difference_writer,sheet_name="Area under curve")
    
    # Exports peak dataframe to excel spreadsheet
    regular_peak_dataframe = pd.DataFrame(regular_peak_dataframe,index=intensities_reversed)
    regular_peak_dataframe.to_excel(regular_writer,sheet_name="Peak values")
    if extra_flag != "N/A":
        flagged_peak_dataframe = pd.DataFrame(flagged_peak_dataframe,index=intensities_reversed)
        flagged_peak_dataframe.to_excel(flagged_writer,sheet_name="Peak values")
        difference_peak_dataframe = pd.DataFrame(difference_peak_dataframe,index=intensities_reversed)
        difference_peak_dataframe.to_excel(difference_writer,sheet_name="Peak values")
        
    # Close pandas writers
    regular_writer.save()
    regular_writer.close()
    if extra_flag != "N/A":
        flagged_writer.save()
        flagged_writer.close()
        difference_writer.save()
        difference_writer.close()
    
    # Declares end of population analysis
    print("Finished population alaysis")

    return