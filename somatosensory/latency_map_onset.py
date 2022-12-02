# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 13:14:53 2022

@author: Austin
"""

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import ImageColor
from scipy import integrate



def latency_map_onset(data,info_storage,latency_mode):
    
    """
    This is the function used to plot the 2P signals for each cell for each
    combination of frequency and amplitude, as well as exporting the
    average correlation coefficient, area under the curve, and the peak value
    for each stimulus to an Excel spreadsheet. It creates a subplot grid for
    each stimulus, then plots the individual traces for each signal, as well as
    the average plot for each stimulus. It then colors the subplot in a shade
    of green depending on the average correlation coefficient. It also gathers
    the average correlation coefficient, area under the curve, and the peak
    value for the cells, and creates an Excel spreadsheet to export all of the
    data into.
    
    Parameters
    ----------
    data : The 4D numpy array containing the dF/F values. The first axis is the
        cell number, the second axis is the sample number (unique combination
        of frequency and amplitude), the third number is the trial number
        (repetition of the same frequency and amplitude combination), and the
        fourth axis is the frame number for each segment.
    info_storage : The class used to store most of the variables that are used
        in the analysis program.
    
    Returns
    -------
    none
    """
    
    # Extracts variables from the info_storage class
    path                     = info_storage.path
    cell_flags               = info_storage.cell_flags
    cell_flags_first_trial   = info_storage.cell_flags_first_trial
    correlation_coefficients = info_storage.correlation_coefficients
    areas_under_curves       = info_storage.areas_under_curves
    framerate_information    = info_storage.framerate_information
    key                      = info_storage.key
    frequencies              = info_storage.frequencies
    frequency_unit           = info_storage.frequency_unit
    intensities              = info_storage.intensities
    intensity_unit           = info_storage.intensity_unit
    mode                     = info_storage.mode
    threshold                = info_storage.threshold
    first_correlation        = info_storage.first_correlation
    
    # Declares start of cell graphing
    print("Starting Onset graphing")
    
    # Disable Spyder plot window
    plt.ioff()
    
    # Creates output directories
    if latency_mode == 1: 
        latency_output_path = f"{path}/Output/Latency/Onset"
        if os.path.exists(f"{latency_output_path}") == True:
            shutil.rmtree(f"{latency_output_path}")
        if os.path.exists(f"{path}/Output/Latency") == True:
            shutil.rmtree(f"{path}/Output/Latency")
        if os.path.exists(latency_output_path) == True:
            shutil.rmtree(latency_output_path)
        if os.path.exists(latency_output_path) == False:
            os.mkdir(f"{path}/Output/Latency")
            os.mkdir(latency_output_path)
            os.mkdir(f"{latency_output_path}/Graphs")
            os.mkdir(f"{latency_output_path}/Spreadsheets")
    elif latency_mode == 2:
        latency_output_path = f"{path}/Output/Latency/Onset/First Two"
        if os.path.exists(f"{latency_output_path}") == True:
            shutil.rmtree(f"{latency_output_path}")
        if os.path.exists(latency_output_path) == False:
            os.mkdir(latency_output_path)
            os.mkdir(f"{latency_output_path}/Graphs")
            os.mkdir(f"{latency_output_path}/Spreadsheets")
    
    # Reverse intensity list
    intensities_reversed = intensities.copy()
    intensities_reversed.reverse()
    
    # Calculates x-axis labels
    cycle_frames = int(framerate_information[1]/2)
    cycle_duration = framerate_information[2]*1000
    times = []
    step = cycle_duration / cycle_frames
    for frame in range(cycle_frames):
        times.append(step*frame/2)
    
    # Constants for loops
    cell_total = data.shape[0]
    sample_total = data.shape[1]
    trial_length = int(data.shape[3]/2)
    intensities_total = len(intensities)
    frequencies_total = len(frequencies)
    
    # Lists and numpy array to store dataframe data in
    cell_numbers = []
    cell_flag_list = []
    cell_flag_first_trial_list = []
    array_cc = np.zeros((sample_total,cell_total))
    array_aoc = np.zeros((sample_total,cell_total))
    array_peak = np.zeros((sample_total,cell_total))
    
    # Goes through each cell
    for cell_number in range(cell_total):
        
        # Creates an if statement to check cell responsiveness
        if correlation_coefficients[cell_number,0] > threshold:
            noise = "Yes"
        else:
            noise = "N/A"
        
        # Adds data to list to export to Excel
        cell_numbers.append(cell_number+1)
        cell_flag_list.append(noise)
        cell_flag_first_trial_list.append(cell_flags_first_trial[cell_number][3])
        
        # Determines size of graph based on number of frequencies and 
        # intensities
        if mode == 0:
            graph_size = (frequencies_total*2,intensities_total*3)
        elif mode == 1:
            graph_size = (10,8)
        
        # Creates empty subplots for each set of data
        fig,axes = plt.subplots(intensities_total,frequencies_total,
                                   sharex=True,sharey=True,squeeze=False,
                                   gridspec_kw={"hspace":0,"wspace":0},
                                   figsize=graph_size)    
        
        # Goes through each frequency
        for column_number,frequency in enumerate(frequencies):
            
            # Goes through each intensity
            for row_number,intensity in enumerate(intensities_reversed):
            
                # Obtains sample number from key
                sample_number = key[frequency][intensity]
                
                # Empty array for storing trial total data
                # trial_sums = np.zeros(trial_length,dtype=np.float32)
                
                # Plots trial data in light gray
                for trial in data[cell_number,sample_number]:
                    axes[row_number,column_number].plot(
                        times,trial,color="#888888",linestyle="dotted")
                    # trial_sums += trial
                
                # Plots avearge of trials
                sample_average = np.mean(data[cell_number,sample_number],
                                         axis=0)
                axes[row_number,column_number].plot(
                    times,sample_average,color="#000000",linestyle="solid")
                
                # Adds correlation coefficient and area under curve to upper 
                # right corner
                correlation_coefficient = correlation_coefficients[
                    cell_number,sample_number][0]
                area_under_curve = areas_under_curves[
                    cell_number,sample_number][0]
                axes[row_number,column_number].legend(["r = %.2f"
                    %correlation_coefficient,"a = %.2f"%area_under_curve],
                    loc="upper right")
                
                # Adds data to list
                array_cc[sample_number,cell_number] = round(
                    correlation_coefficient,2)
                array_aoc[sample_number,cell_number] = round(
                    area_under_curve,2)
                array_peak[sample_number,cell_number] = round(
                    max(sample_average),2)
                
                # Colors in the background based on the correlation coefficient
                if correlation_coefficient > threshold:
                    hue = 120
                    saturation = int(25+(correlation_coefficient-0.75)*100)
                    value = 80
                    hsv = f"hsv({hue},{saturation}%,{value}%)"
                    rgb = "#%02x%02x%02x" % ImageColor.getrgb(hsv)
                    axes[row_number,column_number].set_facecolor(rgb)
                
                # Axes labels
                if mode == 0:
                    if row_number == 0:
                        axes[row_number,column_number].set_title(
                            f"{frequency} {frequency_unit}",fontsize=16)
                    if frequency == frequencies[-1]:
                        intensity_axis = axes[row_number,column_number].twinx()
                        intensity_axis.set_ylabel(
                            f"{intensity} {intensity_unit}",fontsize=16)
                        intensity_axis.set_yticklabels([])
                        intensity_axis.tick_params(
                            axis="both",which="both",length=0)
                if column_number == 0:
                    axes[row_number,column_number].set_ylabel(
                        "dF/F (%)",fontsize=12)
                if row_number == intensities_total-1:
                    axes[row_number,column_number].set_xlabel("Time (ms)")
        
        
        # Creates title for noise graph
        if mode == 1:
            fig.suptitle(f"Noise Responses for Cell {cell_number+1}\n\n"+
                         f"Responsive to Touch: {cell_flag_list[cell_number]}",
                         fontsize=16)
        
        # Saves the graph
        plt.savefig(f"{latency_output_path}/Graphs/Cell {cell_number+1}")
        plt.close()
        plt.clf()
        
    # Exports dataframes to excel spreadsheet
    writer_cc = pd.ExcelWriter(f"{latency_output_path}/Spreadsheets/"+
                               "Correlation Coefficients.xlsx")
    writer_aoc = pd.ExcelWriter(f"{latency_output_path}/Spreadsheets/"+
                                "Areas under curve.xlsx")
    writer_peak = pd.ExcelWriter(f"{latency_output_path}/Spreadsheets/"+
                                 "Peak values.xlsx")
    for frequency in frequencies:
        dataframe_cc = {"Cell Number":cell_numbers,
                        "Cell Flag":cell_flag_list}
        dataframe_aoc = {"Cell Number":cell_numbers,
                         "Cell Flag":cell_flag_list}
        dataframe_peak = {"Cell Number":cell_numbers,
                          "Cell Flag":cell_flag_list}
        for intensity in intensities:
            sample_number = key[frequency][intensity]
            dataframe_cc[f"{intensity} {intensity_unit}"] = \
                array_cc[sample_number]
            dataframe_aoc[f"{intensity} {intensity_unit}"] = \
                array_aoc[sample_number]
            dataframe_peak[f"{intensity} {intensity_unit}"] = \
                array_peak[sample_number]
    
    dataframe_cc = pd.DataFrame(dataframe_cc)
    dataframe_aoc = pd.DataFrame(dataframe_aoc)
    dataframe_peak = pd.DataFrame(dataframe_peak)
    dataframe_peak['first_onset_response'] = 'N/A'
    dataframe_peak['first_integral'] = 'N/A'
        
    for cell_number in range(cell_total):
        for sample_number in range(sample_total):
            for trial in range(1):
                #Creates a variable for the current trial 
                first_trial = data[cell_number,sample_number,trial]
                dataframe_peak['first_integral'].iloc[cell_number] = integrate.simpson(first_trial, dx=step) 
    
        if cell_flag_first_trial_list[cell_number] == 'Yes' and\
        first_correlation[cell_number,sample_number] >= dataframe_cc['Noise dB'].iloc[cell_number]:
            dataframe_peak['first_onset_response'].iloc[cell_number] = 'Yes'
                        
          
        dataframe_cc.to_excel(writer_cc,sheet_name=f"{frequency} "+
                                      f"{frequency_unit}",index=False)
        dataframe_aoc.to_excel(writer_aoc,sheet_name=f"{frequency} "+
                                       f"{frequency_unit}",index=False)
        dataframe_peak.to_excel(writer_peak,sheet_name=f"{frequency} "+
                                        f"{frequency_unit}",index=False)
        
   
    writer_cc.close()
    writer_aoc.save()
    writer_aoc.close()
    writer_peak.save()
    writer_peak.close()
    
    # Declares end of cell graphing
    print("Finished Onset cell graphing")
    
    return